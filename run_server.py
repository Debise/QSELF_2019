import os

os.environ["FLASK_APP"] = "viewer/server.py"

os.system("pipenv run flask run")  # To run the server locally
# os.system("pipenv run flask run --host=0.0.0.0")  # To expose the server publicly
