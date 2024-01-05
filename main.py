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
    
@app.route('/voltage/<float:post_id>')
def show_voltage(post_id):
    
    with open("voltage_data.txt", "a") as file:
        file.write(f"{post_id}\n")

        return f'Saved {post_id}!!'
    
@app.route('/current/<float:post_id>')
def show_current(post_id):
    
    with open("current_data.txt", "a") as file:
        file.write(f"{post_id}\n")

        return f'Saved {post_id}!!'
    
@app.route('/power/<float:post_id>')
def show_power(post_id):
    
    with open("power_data.txt", "a") as file:
        file.write(f"{post_id}\n")

        return f'Saved {post_id}!!'


@app.route('/read')
def read_post():
    
    with open("data.txt", "r") as file:
        data = file.readlines()

        return f'data: {data}!!'
    
def generate_plot(data, variable, title, xlabel, ylabel):
    # Create a simple plot
    plt.figure()
    plt.plot(data, label=variable)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # plt.legend()

    # Save the plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Convert the buffer to base64 for embedding in HTML
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')

    # Close the plot to free up resources
    plt.close()

    return image_base64

@app.route('/plot1')
def plot_data1():
    # Read data from a file and assign it to a numpy array
    data = np.loadtxt('voltage_data.txt')

    # Generate the plot for voltage
    plot_image1 = generate_plot(data, 'Voltage', 'Voltage Plot', 'Time[s]', 'Voltage[v]')
    
    return send_file(io.BytesIO(base64.b64decode(plot_image1)), mimetype='image1/png')

@app.route('/plot2')
def plot_data2():
    # Read data from a file and assign it to a numpy array
    data = np.loadtxt('current_data.txt')

    # Generate the plot for current
    plot_image2 = generate_plot(data, 'Current', 'Current Plot', 'Time[s]', 'Current[A]')

    return send_file(io.BytesIO(base64.b64decode(plot_image2)), mimetype='image2/png')

@app.route('/plot3')
def plot_data3():
    # Read data from a file and assign it to a numpy array
    data = np.loadtxt('power_data.txt')

    # Generate the plot for power
    plot_image3 = generate_plot(data, 'Power', 'Power Plot', 'Time[s]', 'Power[W]')

    return send_file(io.BytesIO(base64.b64decode(plot_image3)), mimetype='image2/png')

@app.route('/plot', methods=['GET'])
def plot_data():
    # Read data from a file and assign it to a numpy array
    data = np.loadtxt('data.txt')

    # Generate the plot for all variables (for /plot endpoint)
    plot_image = generate_plot(data, 'All Variables', 'Combined Plot', 'Time[s]', 'Values')
    return jsonify({'plot': plot_image})

@app.route('/plot_page', methods=['GET'])
def plot_page():
    # Read data from a file and assign it to a numpy array
    data = np.loadtxt('data.txt')

    # Generate the plots for each variable and render an HTML page
    plot_image1 = generate_plot(data, 'Voltage', 'Voltage Plot', 'Time[s]', 'Voltage[v]')
    plot_image2 = generate_plot(data, 'Current', 'Current Plot', 'Time[s]', 'Current[A]')
    plot_image3 = generate_plot(data, 'Power', 'Power Plot', 'Time[s]', 'Power[W]')

    explanation_text = "The charge controller output is monitoring, the measure variables are voltage and current, the photovoltaic system output power is calculated with the values obtained."

    return render_template('plot_page.html', plot_image1=plot_image1, plot_image2=plot_image2, plot_image3=plot_image3, explanation_text=explanation_text)

@app.route('/plot_voltage', methods=['GET'])
def plot_voltage():
    # Read data from a file and assign it to a numpy array
    data = np.loadtxt('voltage_data.txt')

    # Generate the plots for each variable and render an HTML page
    plot_image1 = generate_plot(data, 'Voltage', 'Voltage Plot', 'Time[s]', 'Voltage[v]')

    explanation_text = "The charge controller output is monitoring, the measure variables are voltage and current, the photovoltaic system output power is calculated with the values obtained."

    return render_template('plot_voltage.html', plot_image1=plot_image1, explanation_text=explanation_text)

@app.route('/plot_current', methods=['GET'])
def plot_current():
    # Read data from a file and assign it to a numpy array
    data = np.loadtxt('current_data.txt')

    # Generate the plots for each variable and render an HTML page
    plot_image2 = generate_plot(data, 'Current', 'Current Plot', 'Time[s]', 'Current[A]')

    explanation_text = "The charge controller output is monitoring, the measure variables are voltage and current, the photovoltaic system output power is calculated with the values obtained."

    return render_template('plot_current.html', plot_image2=plot_image2, explanation_text=explanation_text)

@app.route('/plot_power', methods=['GET'])
def plot_power():
    # Read data from a file and assign it to a numpy array
    data = np.loadtxt('power_data.txt')

    # Generate the plots for each variable and render an HTML page
    plot_image3 = generate_plot(data, 'Power', 'Power Plot', 'Time[s]', 'Power[W]')

    explanation_text = "The charge controller output is monitoring, the measure variables are voltage and current, the photovoltaic system output power is calculated with the values obtained."

    return render_template('plot_power.html', plot_image3=plot_image3, explanation_text=explanation_text)

if __name__ == '__main__':
    app.run(debug=True)