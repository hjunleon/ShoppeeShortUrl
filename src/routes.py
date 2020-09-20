def add_short_url_routes(app, view):
    app.add_url_rule('/urls', view_func=view.create_short_url, methods=['POST'])
    app.add_url_rule('/<short_key>', view_func=view.get_short_url, methods=['GET'])
