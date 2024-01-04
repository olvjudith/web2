from tools import sum

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    c = sum(1,2)


    return f"<p style='color:red'>Hello, World!</p>"


@app.route("/web_sum")
def web_sum():
    c = sum(1,2)
    nums = list(range(100))

    return f"<p>c= {c}</p>"


@app.route('/post/<int:post_id>')
def show_post(post_id):
    
    with open("data.txt", "a") as file:
        file.write(f"{post_id}\n")

        return f'Saved {post_id}!!'


@app.route('/read')
def read_post():
    
    with open("data.txt", "r") as file:
        data = file.readlines()

        return f'data: {data}!!'