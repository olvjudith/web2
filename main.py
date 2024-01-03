from tools import sum

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    c = sum(1,2)


    return f"<p style='color:blue'>Hello, World!</p>"


@app.route("/web_sum")
def web_sum():
    c = sum(1,2)
    nums = list(range(100))

    return f"<p>c= {c}</p>"



