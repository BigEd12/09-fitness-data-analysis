from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap

from utils import data_preparation, data_visualisation

#---------------------- FLASK ----------------------#
app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
app.config['SESSION_TYPE'] = 'filesystem'
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

uploaded_file_data = None

@app.route('/dash')
def dash():
    global uploaded_file_data
    if not uploaded_file_data.empty:
        df = uploaded_file_data
        basic_info = data_preparation.basic_info(df)
        hours = basic_info[1].seconds // 3600
        minutes = (basic_info[1].seconds % 3600) // 60
        # time = (int(hours) * 60) + minutes
        time = [hours, minutes]
        basic_info[1] = time

    return render_template('dash.html', basic_info=basic_info)

@app.route('/upload', methods=['POST'])
def upload_file():
    global uploaded_file_data

    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"
    
    df = data_preparation.create_df(file)
    data_preparation.prepare_df(df)

    uploaded_file_data = df

    return redirect(url_for('dash'))



if __name__ == "__main__":
    app.run(debug=True)