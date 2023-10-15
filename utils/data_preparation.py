from math import radians, sin, cos, sqrt, atan2
import pandas as pd
import xml.etree.ElementTree as ET
import gpxpy

import xml.etree.ElementTree as ET

def create_prepare_df(path):
    df = create_df(path)
    df = prepare_df(df)
    return df


def create_df(file):
    """
    Takes a file path and returns a Pandas DataFrame
    """
    file_extension = file.filename.split('.')[-1].lower()
    
    if file_extension == 'tcx':
        return create_df_from_tcx(file)
    elif file_extension == 'gpx':
        return create_df_from_gpx(file)
    else:
        raise ValueError("Unsupported file format. Only TCX and GPX files are supported.")

def create_df_from_tcx(path):
    """
    Takes a TCX file and returns a Pandas DataFrame
    """
    tree = ET.parse(path)
    root = tree.getroot()
    
    data = [
        [
            trackpoint.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Time').text,
            float(trackpoint.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Position/{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LatitudeDegrees').text),
            float(trackpoint.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Position/{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LongitudeDegrees').text),
            float(trackpoint.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}AltitudeMeters').text),
            float(trackpoint.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}DistanceMeters').text),
            float(float(trackpoint.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}DistanceMeters').text) / 1000)
        ]
        for trackpoint in root.findall('.//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Trackpoint')
    ]

    df = pd.DataFrame(data, columns=['Time', 'Latitude', 'Longitude', 'Altitude (M)', 'Total Distance (M)', 'Total Distance (KM)'])
    return df

def create_df_from_gpx(file):
    """
    Takes a GPX file and returns a Pandas DataFrame
    """
    gpx = gpxpy.parse(file)
    
    data = []
    cumulative_distance = 0.0
    prev_point = None
    
    for track in gpx.tracks:
        for segment in track.segments:
            segment_data = []
            for point in segment.points:
                time = point.time
                lat = point.latitude
                lon = point.longitude
                altitude = point.elevation

                if prev_point is not None:
                    distance = point.distance_3d(prev_point)
                    cumulative_distance += distance
                else:
                    distance = 0.0

                segment_data.append([time, lat, lon, altitude, cumulative_distance, cumulative_distance / 1000.0])
                prev_point = point

            data.extend(segment_data)

    df = pd.DataFrame(data, columns=['Time', 'Latitude', 'Longitude', 'Altitude (M)', 'Total Distance (M)', 'Total Distance (KM)'])
    return df
# ----------------------------------------------------------------------------------------
def prepare_df(df):
    df['Time'] = pd.to_datetime(df['Time'])

    df['Time Difference'] = df['Time'].diff()
    
    df['Altitude Difference'] = df['Altitude (M)'].diff()
    
    df['Segment Speed'] = df.apply(seg_speed, axis=1, df=df)
    
    df['Cumulative Time'] = df['Time Difference'].cumsum()
    
    df['Total Time (M)'] = df['Cumulative Time'].dt.total_seconds() / 60
    
    df.drop(columns=['Cumulative Time', ], inplace=True)
    
    return df


def seg_speed(row, df):
    """
    Calculates speed in KM/H for a segment
    """
    if row.name == 0:
        return float('NaN')
    
    seconds = row['Time Difference'].total_seconds()
    if seconds == 0:
        return 0
    
    distance_diff = row['Total Distance (M)'] - df.loc[row.name - 1, 'Total Distance (M)']
    
    return (distance_diff / 1000) / (seconds / 3600)

    
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculates the distance between two points
    """
    R = 6371
    
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    return distance

def calc_total_distance(df):
    """
    Calculates the total distance in the ride in Km.
    """
    total_distance = sum(haversine(df['Latitude'][i - 1], df['Longitude'][i - 1], df['Latitude'][i], df['Longitude'][i])
                        for i in range(1, len(df))
                        )
    return total_distance

def calc_moving_time(df):
    """
    Calculates the total time of the ride.
    """
    return df['Time Difference'].sum()

def elevation_info(df):
    """
    Calculates different information from Altitude
    """
    total_ascent = df['Altitude Difference'][df['Altitude Difference'] > 0].sum()
    total_descent = df['Altitude Difference'][df['Altitude Difference'] < 0].sum()
    total_change = df['Altitude Difference'].sum()
    lowest = df['Altitude (M)'].min()
    highest = df['Altitude (M)'].max()
    
    return total_ascent, total_descent, total_change, lowest, highest

def highest_average_speed(df, window_size=6):
    max_avg, max_avg_index = max(
        (window['Segment Speed'].mean(), i + window_size // 2)
        for i, window in enumerate((df.iloc[i:i + window_size] for i in range(len(df) - window_size + 1)))
    )
    return [max_avg, max_avg_index]

def speed_info(df):
    """
    Calculates different information about Speed.
    """
    average = calc_total_distance(df) / (calc_moving_time(df).total_seconds() / 3600)
    fastest = highest_average_speed(df)[0]
    slowest = df['Segment Speed'].min()
    
    return average, fastest, slowest

def start_date_time(df):
    """
    Calculates the start date and time
    """
    date_start_pre = df.iloc[0].Time
    
    start_date = date_start_pre.strftime("%d-%m-%Y")
    start_time = date_start_pre.strftime("%H:%M")
    
    return [start_date, start_time]

def basic_info(df):
    """
    Returns basic information about the ride.
    """
    
    distance = round(calc_total_distance(df), 2)
    moving_time = calc_moving_time(df)
    total_ascent = round(elevation_info(df)[0], 2)
    total_descent = elevation_info(df)[1]
    altitude_change = round(elevation_info(df)[2], 2)
    lowest_altitude = round(elevation_info(df)[3], 2)
    highest_altitude = round(elevation_info(df)[4], 2)
    average_speed = round(speed_info(df)[0], 2)
    fastest_speed = round(speed_info(df)[1], 2)
    slowest_speed = round(speed_info(df)[2], 2)
    start_date = start_date_time(df)
    
    
    return [distance, moving_time, total_ascent, total_descent, altitude_change, lowest_altitude, highest_altitude, average_speed, fastest_speed, slowest_speed, start_date]

def find_faster_slower_animals(speed):
    animals = {
        'mountain_goat': 45,
        'cow': 40,
        'greyhound': 70,
        'cat': 48,
        'japanese_macaque': 16,
        'hippo': 30,
        'pig': 17,
        'alligator': 56,
        'panda': 32,
        'african_bush_elephant': 40,
        'anaconda': 8,
        'grey_squirrel': 20,
        'giraffe': 52,
        'grizzly_bear': 56,
        'brown_bear': 35,
        'house_mouse': 13,
        'polar_bear': 30,
        'cheetah': 120,
        'snail': 0.0085,
        'starfish': 0.000576,
        'koala': 30,
        'cockroach': 5.4,
        'Bertie - Guiness fastest tortoise': 1.007,
    }
    
    animal_images = {
        'mountain_goat': '2',
        'cow': '3',
        'greyhound': '4',
        'cat': '5',
        'japanese_macaque': '6',
        'hippo': '7',
        'pig': '10',
        'alligator': '8',
        'panda': '25',
        'african_bush_elephant': '1',
        'anaconda': '9',
        'grey_squirrel': '11',
        'giraffe': '12',
        'grizzly_bear': '13',
        'brown_bear': '13',
        'house_mouse': '15',
        'polar_bear': '14',
        'cheetah': '24',
        'snail': '19',
        'starfish': '20',
        'koala': '21',
        'cockroach': '22',
        'Bertie - Guiness fastest tortoise': '23',
    }

    above_speed = 1000
    above_animal = ''
    below_speed = 0
    below_animal = ''


    for idx, (key, value) in enumerate(animals.items()):
        if value > speed:
            if above_speed > value:
                above_speed = value
                above_animal = key
        elif value < speed:
            if below_speed < value:
                below_speed = value
                below_animal = key

        if idx == len(animals) -1:
            animal_images[above_animal]
            above_path = f'/static/images/{animal_images[above_animal]}.png'
            below_path = f'/static/images/{animal_images[below_animal]}.png'
            faster_animal = [above_animal, above_speed, above_path]
            slower_animal = [below_animal, below_speed, below_path]

    return [faster_animal, slower_animal]

peaks = {
    "Albania": ["Maja e Jezercës", 2694],
    "Andorra": ["Coma Pedrosa", 2942],
    "Austria": ["Grossglockner", 3798],
    "Belarus": ["Dzerzhinskaya Mountain", 345],
    "Belgium": ["Signal de Botrange", 694],
    "Bosnia and Herzegovina": ["Maglić", 2386],
    "Bulgaria": ["Musala", 2925],
    "Croatia": ["Dinara", 1831],
    "Cyprus": ["Mount Olympus", 1952],
    "Czech Republic": ["Snezka", 1603],
    "Denmark": ["Møllehøj", 170.86],
    "Estonia": ["Suur Munamägi", 318],
    "Finland": ["Halti", 1328],
    "France": ["Mont Blanc", 4810],
    "Germany": ["Zugspitze", 2962],
    "Greece": ["Mount Olympus", 2917],
    "Hungary": ["Kékes", 1014],
    "Iceland": ["Hvannadalshnjúkur", 2110],
    "Ireland": ["Carrauntoohil", 1039],
    "Italy": ["Monte Bianco (Mont Blanc)", 4810],
    "Latvia": ["Gaiziņkalns", 312],
    "Liechtenstein": ["Grauspitz", 2599],
    "Lithuania": ["Aukštojas", 294],
    "Luxembourg": ["Burgplatz", 559],
    "Malta": ["Ta' Dmejrek", 253],
    "Moldova": ["Bălăneşti Hill", 429],
    "Monaco": ["Chemins des Révoires", 162],
    "Montenegro": ["Bobotov Kuk", 2523],
    "Netherlands": ["Vaalserberg", 322.7],
    "North Macedonia": ["Mount Korab", 2764],
    "Norway": ["Galdhøpiggen", 2469],
    "Poland": ["Rysy", 2503],
    "Portugal": ["Serra da Estrela", 1993],
    "Romania": ["Moldoveanu Peak", 2544],
    "San Marino": ["Monte Titano", 739],
    "Serbia": ["Midžor", 2169],
    "Slovakia": ["Gerlachovský štít", 2655],
    "Slovenia": ["Triglav", 2864],
    "Spain": ["Mulhacén", 3479],
    "Sweden": ["Kebnekaise", 2097],
    "Switzerland": ["Dufourspitze", 4634],
    "Ukraine": ["Hoverla", 2061],
    "United Kingdom": ["Ben Nevis", 1345],
    "Vatican City": ["Vatican Hill", 75],
    "Morocco": ["Toubkal", 4167],
    "Kenya": ["Mount Kenya", 5199],
    "Nepal": ["Mount Everest", 8848],
    "Pakistan": ["K2", 8611],
    "United States": ["Denali (Mount McKinley)", 6190],
    "Canada": ["Mount Logan", 5959],
    "Australia": ["Mount Kosciuszko", 2228],
    "Indonesia": ["Puncak Jaya (Carstensz Pyramid)", 4884],
    "Argentina": ["Aconcagua", 6962],
    "Chile": ["Ojos del Salado", 6887]
}



def closest_peak(altitude, peaks=peaks):
    closest_peak = None
    closest_difference = float('inf')

    for country, data in peaks.items():
        peak_name, peak_altitude = data
        if peak_altitude > altitude:
            difference = peak_altitude - altitude
            if difference < closest_difference:
                closest_difference = difference
                closest_peak = [country, peak_name, peak_altitude]

    return closest_peak
    
    
routes = {
    'Italy': [('Amalfi Coast Drive', 50), ('Stelvio Pass', 24.7)],
    'France': [('Route 66', 2448), ('Trollstigen', 20)],
    'USA': [('Pacific Coast Highway', 1470), ('Blue Ridge Parkway', 755)],
    'Australia': [('Great Ocean Road', 243), ('Kangaroo Island Coastal Drive', 155)],
    'Canada': [('Icefields Parkway', 232), ('Cabot Trail', 298)],
    'Peru': [('Machu Picchu Inca Trail', 43)],
    'Nepal': [('Everest Base Camp Trek', 130)],
    'New Zealand': [('Milford Sound Road', 120)],
    'Argentina': [('Ruta 40', 5221)],
    'Scotland': [('North Coast 500', 516)],
    'Spain': [('Camino de Santiago', 800)],
    'Ireland': [('Wild Atlantic Way', 2500)],
    'Norway': [('Norwegian Scenic Routes', 2300), ('Atlantic Road', 8)],
    'Germany': [('Romantic Road', 350)],
    'Switzerland': [('Grand Tour of Switzerland', 1600)],
    'India': [('Manali-Leh Highway', 479)],
    'Chile': [('Carretera Austral', 1240)],
    'South Africa': [('Garden Route', 300)],
    'China': [('Guoliang Tunnel Road', 1.2)],
    'Vietnam': [('Hai Van Pass', 21)],
    'Turkey': [('Cappadocia', 20)],
    'Earth': [('Equator', 40075)]
}

def closest_route(distance, routes=routes):
    closest_route = None
    closest_difference = float('inf')

    for country, data_list in routes.items():
        for route_name, route_distance in data_list:
            if route_distance > distance:
                difference = route_distance - distance
                if difference < closest_difference:
                    closest_difference = difference
                    percent = round((distance / route_distance) * 100, 2)
                    closest_route = [country, route_name, route_distance, percent]

    return closest_route