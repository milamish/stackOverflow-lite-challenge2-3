from API import app, Api
from API import models
from API.models import table, RegisterUser, Questions


if __name__ == "__main__":
    table()
    app.run(debug=True)