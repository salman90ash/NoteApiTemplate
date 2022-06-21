from api import app
from api.models.user import UserModel
import click
from api import db


@app.cli.command('users')
@click.argument('do')  # create, delete, show
@click.option("--all", is_flag=True, default=False)
def user_operation(do, all):
    """
    Operation for users
    """
    if do == "delete":
        if all:
            UserModel.query.delete()
            db.session.commit()
            print("All users deleted")
            return
        username = input("username: ")
        user = UserModel.query.filter_by(username=username).first()
        if user:
            user.delete()
            print("User deleted")
        else:
            print(f"User with {username} not found")
    elif do == "show-all":
        users = UserModel.query.all()
        for user in users:
            print(f"{user.username}")


@app.cli.command('createsuperuser')
def create_superuser():
    """
    Creates a user with the admin role
    """
    username = input("Username[default 'admin']:") or "admin"
    password = input("Password[default 'admin']:") or "admin"
    user = UserModel(username, password, role="admin", is_staff=True)
    user.save()
    if user.id:
        print(f"Superuser create successful! id={user.id}")
    else:
        print(f"User with {user.surname} already exists")


@app.cli.command('all_users')
def all_users():
    """
    Get list of users
    """
    users = UserModel.query.all()
    for user in users:
        print(f"User id: {user.id} {user.username}")
