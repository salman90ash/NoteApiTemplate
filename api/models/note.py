from api import db
from api.models.user import UserModel
from api.models.tag import TagModel
from api.models.mixins import ModelDBExt
from sqlalchemy.sql import expression

# COR
tags = db.Table('tags_to_notes',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                db.Column('note_model_id', db.Integer, db.ForeignKey('note_model.id'), primary_key=True)
                )


class NoteModel(db.Model, ModelDBExt):  # ORM
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(UserModel.id))
    text = db.Column(db.String(255), unique=False, nullable=False)
    private = db.Column(db.Boolean(), default=True, nullable=False)
    tags = db.relationship(TagModel, secondary=tags, lazy='subquery', backref=db.backref('notes', lazy=True))
    is_archive = db.Column(db.Boolean(), server_default=expression.false(), default=False, nullable=False)

    def delete(self):
        self.is_archive = True
        db.session.commit()

    def restore(self):
        self.is_archive = False
        db.session.commit()
