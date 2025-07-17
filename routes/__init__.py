from .post import post_bp
from .tactile_paving import tactile_paving_bp

def register_routes(app):
    app.register_blueprint(post_bp)
    app.register_blueprint(tactile_paving_bp)