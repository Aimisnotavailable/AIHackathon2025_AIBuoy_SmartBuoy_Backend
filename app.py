import pkgutil
import importlib
from api.routes import __path__ as routes_path
from flask import Flask
from flask_migrate import Migrate
from api.scripts.config import Config   

def register_blueprints(app):
    for finder, module_name, ispkg in pkgutil.iter_modules(routes_path):
        module = importlib.import_module(f'api.routes.{module_name}')
        # expect each module to expose a blueprint named "<module>_bp"
        bp = getattr(module, f"{module_name}_bp", None)
        if bp:
            app.register_blueprint(bp)
            # print(bp)
            
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    migrate = Migrate(app)

    # Register blueprints
    register_blueprints(app)
    
    # for url in app.url_map.iter_rules():
    #     print(url)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)



