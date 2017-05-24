# ~*~ encoding: utf-8 ~*~
import os
from app import create_app, db
from app.models import User
from flask_script import Manager, Shell


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell():
    return dict(app=app, db=db, User=User)
manager.add_command("shell", Shell(make_context=make_shell))


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
