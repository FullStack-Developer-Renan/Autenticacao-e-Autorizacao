from flask import Flask

def init_app(app: Flask):
    from app.views.users_views import bp as bp_users_views
    from app.views.users_views import bp_admin as bp_admin_views
    app.register_blueprint(bp_users_views)
    app.register_blueprint(bp_admin_views)