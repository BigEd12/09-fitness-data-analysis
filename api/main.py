import os

from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory
from flask_bootstrap import Bootstrap

from datetime import datetime

from utils import data_preparation, data_visualisation

#---------------------- FLASK ----------------------#
app = Flask(__name__, template_folder=os.path.abspath("templates"), static_folder=os.path.abspath("static"))

app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
app.config['SESSION_TYPE'] = 'filesystem'

Bootstrap(app)

@app.route('/')
def index():
    """
    Load file page
    """
    year = datetime.now().year
    footer_info = [year]
    
    return render_template('index.html', footer_info=footer_info)

uploaded_file_data = None

@app.route('/dash', methods=['GET', 'POST'])
def dash():
    global uploaded_file_data
    if not uploaded_file_data.empty:
        df = uploaded_file_data
        basic_info = data_preparation.basic_info(df)

        time = [basic_info[1].seconds // 3600, (basic_info[1].seconds % 3600) // 60]
        basic_info[1] = time
        
        map_data = data_visualisation.plot_line_map(df)
        chart_1 = data_visualisation.time_speed_graph(df)
        chart_2 = data_visualisation.altitude_time_distance_speed_graph(df, 'distance')
        

        equator = data_preparation.closest_route(basic_info[0])
        
        closest_peak = data_preparation.closest_peak(basic_info[2])
        ascent_percent = round((basic_info[2] / closest_peak[2]) * 100, 2)
        closest_peak.append(ascent_percent)
        
        animal_speed = data_preparation.find_faster_slower_animals(basic_info[8])
        basic_info
        
        year = datetime.now().year
        footer_info = [year]

        
        if request.method == 'POST':
            if request.form['form_name'] == 'form1':
                parameter1 = request.form.get('parameter1')
                parameter2 = request.form.get('parameter2')
                chart_1 = data_visualisation.create_custom_graph(df, parameter1, parameter2)
                
            elif request.form['form_name'] == 'form2':
                print(f'name: {request.form["form_name"]}')
                parameter = request.form.get('parameter')
                chart_2 = data_visualisation.altitude_time_distance_speed_graph(df, parameter)
                
        graphical = [chart_1, map_data, chart_2]
        fun_stats = [equator, closest_peak, animal_speed]
            
    
    return render_template('dashboard.html', basic_info=basic_info, graphical=graphical, fun_stats=fun_stats, footer_info=footer_info)

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     global uploaded_file_data

#     if 'file' not in request.files:
#         return "No file part"

#     file = request.files['file']

#     if file.filename == '':
#         return "No selected file"
    
#     df = data_preparation.create_df(file)
#     data_preparation.prepare_df(df)
    

#     uploaded_file_data = df

#     return redirect(url_for('dash'))

@app.route('/upload', methods=['POST'])
def upload_file():
    global uploaded_file_data

    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            df = data_preparation.create_df(file)
            data_preparation.prepare_df(df)
            uploaded_file_data = df
            return redirect(url_for('dash'))
    
    path_1 = 'sample_data/1.gpx'
    path_2 = 'sample_data/2.gpx'
    path_3 = 'sample_data/3.gpx'
    selected_radio_option = request.form.get('inlineRadioOptions')
    if selected_radio_option:

        if selected_radio_option == 'option1':
            print(selected_radio_option)
            df = data_preparation.create_prepare_df(path_1)
            print(df.head())
            uploaded_file_data = df
            pass
        elif selected_radio_option == 'option2':
            df = data_preparation.create_prepare_df(path_2)
            uploaded_file_data = df
            pass
        elif selected_radio_option == 'option3':
            df = data_preparation.create_prepare_df(path_3)
            uploaded_file_data = df
            pass    
        return redirect(url_for('dash'))
    
    return "No file or radio option selected"

@app.route('/iframe')
def iframe():
    global uploaded_file_data
    if uploaded_file_data is not None:
        map_html = data_visualisation.plot_line_map(uploaded_file_data)
    else:
        map_html = "<p>No data available</p>"

    return render_template('iframe.html', map_html=map_html)


@app.route('/temp/<path:filename>')
def serve_temp(filename):
    return send_from_directory('temp', filename)


if __name__ == "__main__":
    app.run(debug=True)