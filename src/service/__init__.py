from src import app


def start_service():
    app.run(debug=True,host="0.0.0.0",use_reloader=False)
