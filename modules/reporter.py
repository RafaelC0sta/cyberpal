from flask import Flask
from db import exportSelect

app = Flask(__name__)

def dbTableSelect():
    return (exportSelect())

@app.route("/")
def main():
    return "Pagina inicial"

@app.get('/dados')
def showReport():
    return dbTableSelect()


if __name__ == "__main__":
    app.run(debug=True)