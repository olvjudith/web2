import base64
from tools import sum

from flask import Flask, jsonify, render_template, send_file
import numpy as np
import matplotlib.pyplot as plt
import io

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


@app.route('/post/<float:post_id>')
def show_post(post_id):
    
    with open("data.txt", "a") as file:
        file.write(f"{post_id}\n")

        return f'Saved {post_id}!!'


@app.route('/read')
def read_post():
    
    with open("data.txt", "r") as file:
        data = file.readlines()

        return f'data: {data}!!'
    

@app.route('/plot2')
def plot_data2():

    # Read data from a file and assign it to a numpy array
    data = np.loadtxt('data.txt')

    # Create a simple plot
    plt.figure()
    plt.plot(data)
    plt.title('Your Plot Title')
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')

    # Save the plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    return send_file(buf, mimetype='image/png')

def generate_plot():
    # Read data from a file and assign it to a numpy array
    data = np.loadtxt('data.txt')

    # Create a simple plot
    plt.figure()
    plt.plot(data)
    plt.title('Your Plot Title')
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')
     

    # Save the plot to a BytesIO object
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Convert the BytesIO object to base64 for embedding in HTML
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')

    # Close the plot to free up resources
    plt.close()

    return image_base64

@app.route('/plot', methods=['GET'])
def plot_data():
    # Generate the plot and return it as JSON
    plot_image = generate_plot()
    return jsonify({'plot': plot_image})

@app.route('/plot_page', methods=['GET'])
def plot_page():
    # Generate the plot and render an HTML page
    plot_image = generate_plot()
    explanation_text = "This is a simple sine wave plot from 0 to 3."

    return render_template('plot_page.html', plot_image=plot_image, explanation_text=explanation_text)


if __name__ == '__main__':
    app.run(debug=True)