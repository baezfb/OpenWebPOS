import os

from flask import Flask, send_from_directory

from openwebpos.blueprints import blueprints
from openwebpos.extensions import db
from openwebpos.utils import create_folder, create_file


def open_web_pos(instance_dir=None):
    template_dir = 'ui/templates'
    static_dir = 'ui/static'
    base_path = os.path.abspath(os.path.dirname(__file__))

    if instance_dir is None:
        instance_dir = os.path.join(os.getcwd(), 'instance')

    if os.path.isdir(instance_dir):
        if not os.listdir(instance_dir):
            create_file(file_path=os.getcwd(), file_name='instance/__init__.py')
            create_file(file_path=os.getcwd(),
                        file_name='instance/settings.py',
                        file_mode='w',
                        file_content="DB_DIALECT = 'sqlite'\n")

    create_folder(folder_path=os.getcwd(), folder_name='instance')
    create_folder(folder_path=os.getcwd(), folder_name='uploads')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir, instance_relative_config=True,
                instance_path=instance_dir)

    app.config.from_pyfile(os.path.join(base_path, 'config/settings.py'))
    app.config.from_pyfile(os.path.join('settings.py'), silent=True)

    extensions(app)

    @app.before_first_request
    def before_first_request():
        from openwebpos.extensions import db
        from openwebpos.blueprints.user.models import User
        db.create_all()
        if not User.query.first():
            User.insert_user()

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app


def extensions(app):
    from openwebpos.extensions import db, login_manager
    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from openwebpos.blueprints.user.models import User
        return User.query.get(user_id)

    login_manager.login_view = 'user.login'

    return app
