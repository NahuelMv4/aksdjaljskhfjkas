from flask import Flask, jsonify
from flask import render_template
from flask_session import Session
from web.handlers import errores
from web.config import config
from src.core import database, seeds
from src.web.helpers import auth
from src.core.errores.custom_errors import AppError

# -- Importacion de Blueprints --
from src.web.controllers.personal_controller import personal_bp
from src.web.controllers.private_personal_controller import priv_personal_bp
from src.web.helpers import auth
from src.web.controllers.auth import auth_bp
from src.web.controllers.cupos_api import cupos_api_bp
from src.web.controllers.usuario_controller import bp as usuarios_bp
from src.web.controllers.private_personal_controller import priv_personal_bp
from src.web.helpers.auth import is_authenticated, check_permission
from src.web.controllers.sector_controller import bp_sector
from src.web.helpers import auth
from src.web.controllers.private_sector_controller import priv_sector_bp

def create_app(env= "development", static_folder="../../static"):
  app = Flask(__name__, static_folder=static_folder)
  app.config.from_object(config[env])
  database.init_app(app)
  app.jinja_env.globals.update(is_authenticated=is_authenticated)
  app.jinja_env.globals.update(check_permission=check_permission)

  app.config['SESSION_TYPE'] = 'filesystem'
  Session(app)

  @app.route("/")
  def home():
    return render_template ('home.html')
  
  # --       Blueprints       --
  app.register_blueprint(personal_bp)  
  app.register_blueprint(usuarios_bp)
  app.register_blueprint(priv_personal_bp)
  app.register_blueprint(auth_bp)
  app.register_blueprint(bp_sector)
  app.register_blueprint(cupos_api_bp)
  app.register_blueprint(priv_sector_bp)

  #--   Manejador de errores REST   --
  @app.errorhandler(AppError)
  def handle_app_error(error):
    return jsonify({"error": error.message}), error.status_code
  
  #--       Errores HTML       --
  app.register_error_handler(401, errores.unauthorized)  
  app.register_error_handler(403, errores.forbidden)
  app.register_error_handler(404, errores.not_found)  
  app.register_error_handler(500, errores.internal_server_error)

  #--       Comandos       --
  @app.cli.command("reset-db")
  def reset_db():
    database.reset_db()

  @app.cli.command("seed-db")
  def seed_db():
    seeds.run()

  return app