from flask.ext.script import Manager, Shell, Server
from app import app

manager = Manager(app)
manager.add_command("runserver", Server())
manager.add_command("shell", Shell())


@manager.command
def createdb():
    from app.models import db
    db.create_all()

manager.run()
