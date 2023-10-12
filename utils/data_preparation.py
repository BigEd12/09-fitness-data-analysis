from math import radians, sin, cos, sqrt, atan2
import pandas as pd
import datetime

import xml.etree.ElementTree as ET


def create_df(path):
    """
    Takes a directory path and returns a Pandas DF
    """
    tree = ET.parse(path)
    root = tree.getroot()
    
    data = []
    for trackpoint in root.findall('.//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Trackpoint'):
        time = trackpoint.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Time').text
        lat = trackpoint.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Position/{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LatitudeDegrees').text
        lon = trackpoint.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Position/{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LongitudeDegrees').text
        altitude = trackpoint.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}AltitudeMeters').text
        distance = trackpoint.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}DistanceMeters').text
        data.append([time, float(lat), float(lon), float(altitude), float(distance), float(float(distance) / 1000)])

    df = pd.DataFrame(data, columns=['Time', 'Latitude', 'Longitude', 'Altitude (M)', 'Total Distance (M)', 'Total Distance (KM)'])
    return df

def seg_speed(row, df):
    """
    Calculates speed in KM/H for a segment
    """
    if row.name == 0:
        return float('NaN')
    
    seconds = row['Time Difference'].total_seconds()
    distance_diff = row['Total Distance (M)'] - df.loc[row.name - 1, 'Total Distance (M)']
    
    return (distance_diff / 1000) / (seconds / 3600)

def prepare_df(df):
    df['Time'] = pd.to_datetime(df['Time'])

    df['Time Difference'] = df['Time'].diff()
    
    df['Altitude Difference'] = df['Altitude (M)'].diff()
    
    df['Segment Speed'] = df.apply(seg_speed, axis=1, df=df)
    
    df['Cumulative Time'] = df['Time Difference'].cumsum()
    
    df['Total Time (M)'] = df['Cumulative Time'].dt.total_seconds() / 60
    
    df.drop(columns=['Cumulative Time', ], inplace=True)
    
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
    total_distance = 0
    for i in range(1, len(df)):
        lat1, lon1 = df['Latitude'][i - 1], df['Longitude'][i - 1]
        lat2, lon2 = df['Latitude'][i], df['Longitude'][i]

        seg_distance = haversine(lat1, lon1, lat2, lon2)
        total_distance += seg_distance
        
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
    max_avg = -1
    max_avg_index = -1

    for i in range(len(df) - window_size + 1):
        window = df.iloc[i:i + window_size]
        avg = window['Segment Speed'].mean()
        
        if avg > max_avg:
            max_avg = avg
            max_avg_index = i + window_size // 2

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
    date_start_pre = df.iloc[0].Time + datetime.timedelta(days=4) - datetime.timedelta(hours=12) - datetime.timedelta(minutes=38)
    
    start_date = date_start_pre.strftime("%d-%m-%Y")
    start_time = date_start_pre.strftime("%H:%M")
    
    return [start_date, start_time]

def basic_info(df):
    """
    Returns basic information about the ride.
    """
    
    distance = round(calc_total_distance(df), 2)
    moving_time = calc_moving_time(df)
    total_ascent = elevation_info(df)[0]
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
        'panda': '0',
        'african_bush_elephant': '1',
        'anaconda': '9',
        'grey_squirrel': '11',
        'giraffe': '12',
        'grizzly_bear': '13',
        'brown_bear': '13',
        'house_mouse': '15',
        'polar_bear': '14',
        'cheetah': 0,
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
    