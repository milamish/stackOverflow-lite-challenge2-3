from __init__ import app, Api
from models import table, RegisterUser, Questions


if __name__ == "__main__":
    table()
    app.run(debug=True)