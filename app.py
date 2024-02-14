from flask import Flask
from crud import LivreRepository

app = Flask(__name__)
repo_livre = LivreRepository()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
