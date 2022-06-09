from api import Resource, abort, reqparse, auth, docs
from api.models.note import NoteModel
from api.schemas.note import NoteSchema
from api.models.tag import TagModel
from api.schemas.tag import TagSchema, TagRequestSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc


@doc(tags=["Tags"])
class TagsResource(MethodResource):
    @doc(description='Full: Get Tag by id')
    @doc(summary='Get Tag by id')
    @marshal_with(TagSchema(), code=200)
    def get(self, tag_id):
        tag = TagModel.query.get(tag_id)
        if tag is None:
            abort(404, error=f"Note with id={tag_id} not found")
        return tag, 200


@doc(tags=["Tags"])
class TagsListResource(MethodResource):
    @doc(summary='Get all tags')
    @marshal_with(TagSchema(many=True), code=200)
    def get(self):
        tags = TagModel.query.all()
        return tags, 200

    @doc(summary='Create new tag')
    @marshal_with(TagSchema, code=201)
    @use_kwargs(TagRequestSchema, location='json')
    def post(self, **kwargs):
        tag = TagModel(**kwargs)
        tag.save()
        return tag, 201

