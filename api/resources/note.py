from api import auth, abort, g, Resource, reqparse
from api.models.note import NoteModel
from api.schemas.note import note_schema, notes_schema, NoteSchema, NoteRequistSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields
from api.models.tag import TagModel
from helpers.shortcuts import get_object_or_404


@doc(tags=['Notes'])
class NoteResource(MethodResource):
    # @auth.login_required
    # @doc(security=[{"basicAuth": []}])
    @doc(summary="Get Note by id")
    @marshal_with(NoteSchema, 200)
    def get(self, note_id):
        """
        Пользователь может получить ТОЛЬКО свою заметку
        """
        # author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")
        return note, 200

    @auth.login_required
    def put(self, note_id):
        """
        Пользователь может редактировать ТОЛЬКО свои заметки
        """
        author = g.user
        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True)
        parser.add_argument("private", type=bool)
        note_data = parser.parse_args()
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        note.text = note_data["text"]

        note.private = note_data.get("private") or note.private

        note.save()
        return note_schema.dump(note), 200

    @doc(summary="Delete note")
    def delete(self, note_id):
        note = get_object_or_404(NoteModel, note_id)
        note.delete()
        return {"message": f"Note with id={note}"}, 200


@doc(tags=['Notes'])
class NotesListResource(MethodResource):
    @doc(summary="Get all notes")
    @marshal_with(NoteSchema(many=True), 200)
    def get(self):
        notes = NoteModel.query.all()
        return notes_schema.dump(notes), 200

    @auth.login_required
    @doc(security=[{"basicAuth": []}])
    @doc(summary="Create new note")
    @marshal_with(NoteSchema, 201)
    @use_kwargs(NoteRequistSchema, location="json")
    def post(self, **kwargs):
        author = g.user
        note = NoteModel(author_id=author.id, **kwargs)
        note.save()
        return note, 201


@doc(tags=['Notes'])
class NoteSetTagsResource(MethodResource):
    @doc(summary="Set tags to Note")
    @use_kwargs({"tags": fields.List(fields.Int())}, location=('json'))
    @marshal_with(NoteSchema)
    def put(self, note_id, **kwargs):
        note = NoteModel.query.get(note_id)
        if not note:
            return {"error": f"note {note_id} not found"}
        for tag_id in kwargs["tags"]:
            tag = TagModel.query.get(tag_id)
            note.tags.append(tag)
        note.save()
        return note, 200


@doc(tags=['Notes'])
class NotesListByUserResource(MethodResource):
    @marshal_with(NoteSchema(many=True), code=200)
    @doc(description='Get all notes by user_id')
    @doc(summary='Get all notes by user_id')
    def get(self, user_id):
        notes = NoteModel.query.filter_by(author_id=user_id).all()
        return notes_schema.dump(notes), 200


@doc(tags=['Notes'])
# PUT /notes/<note_id>/restore
class NoteRestoreResource(MethodResource):
    @doc(summary="Restore Note")
    @marshal_with(NoteSchema, code=200)
    def put(self, note_id):
        note = get_object_or_404(NoteModel, note_id)
        note.is_archive = False
        note.save()
        return note, 200
