import json
import os
from api import db
from api.schemas.user import UserRequestSchema
from api.schemas.note import NoteRequistSchema
from config import BASE_DIR, base_dir
from sqlalchemy.exc import IntegrityError
from api.models.note import NoteModel
from api.models.user import UserModel
from api.models.tag import TagModel
import click


@click.command
@click.option('--fixture', help='fixture name .json')
def load_fixture(fixture):
    path_to_fixture = BASE_DIR / "fixtures" / fixture
    models = {
        "NoteModel": NoteModel,
        "UserModel": UserModel,
        "TagModel": TagModel
    }
    with open(path_to_fixture, "r", encoding="UTF-8") as f:
        data = json.load(f)
        model_name = data["model"]
        model = models[model_name]
        for record in data["records"]:
            obj = model(**record)
            obj.save()
        print("ready")


if __name__ == "__main__":
    load_fixture()
