# ~*~ encoding: utf-8 ~*~
import os
from app import create_app
from flask_script import Manager, Shell


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app.run(host='0.0.0.0'))


def make_shell():
    return dict(app=app)
manager.add_command("shell", Shell(make_context=make_shell))

if __name__ == '__main__':
    manager.run()