from flask import Flask, render_template


def app_creation(data_to_render, path_to_template='to_render.html'):
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def render():
        return render_template(path_to_template, data=data_to_render)

    app.run(host='0.0.0.0', port=8080, debug=True)
