from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory, render_template_string
from flask_bootstrap import Bootstrap

from utils import data_preparation, data_visualisation

#---------------------- FLASK ----------------------#
app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
app.config['SESSION_TYPE'] = 'filesystem'
# app.config['TEMPLATES_AUTO_RELOAD'] = True
# app.add_url_rule('/temp/<path:filename>', endpoint='temp', view_func=app.send_static_file)

Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

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
            
    
    return render_template('dashboard.html', basic_info=basic_info, graphical=graphical, equator=equator, peak_info=closest_peak, animal_speed=animal_speed)

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

@app.route('/iframe')
def iframe():
    map_html = data_visualisation.plot_line_map(uploaded_file_data)  

    return render_template('iframe.html', map_html=map_html)


@app.route('/temp/<path:filename>')
def serve_temp(filename):
    return send_from_directory('temp', filename)


if __name__ == "__main__":
    app.run(debug=True)