# from flask import Flask
# from models import db
# from routes import configure_routes
# from auth import configure_jwt

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object('config.Config')

#     db.init_app(app)
#     configure_routes(app)
#     configure_jwt(app)

#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)
from flask import Flask
from src.models import db
from src.routes import configure_routes
from .config import Config
from src.config import Config



def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    configure_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
