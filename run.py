from flask import g
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app, db

app = create_app('development')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@app.before_request
def before_request():
    from app.auth.forms import LoginForm
    g.loginform=LoginForm()
    from app.auth.forms import RegistrationForm
    g.registrationform = RegistrationForm()

@app.context_processor
def inject_loginform():
    return dict(loginform=g.loginform)

@app.context_processor
def inject_registrationform():
    return dict(registrationform=g.registrationform)

if __name__ == '__main__':
    app.run()


