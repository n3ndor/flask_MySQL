from flask_app.controllers import authors_route, books_route
from flask_app import app


if __name__ == "__main__":
    app.run(debug=True)