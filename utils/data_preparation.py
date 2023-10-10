from math import radians, sin, cos, sqrt, atan2
import pandas as pd

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
    
    df.drop(columns=['Cumulative Time'], inplace=True)
    
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

def speed_info(df):
    """
    Calculates different information about Speed.
    """
    average = calc_total_distance(df) / (calc_moving_time(df).total_seconds() / 3600)
    fastest = df['Segment Speed'].max()
    slowest = df['Segment Speed'].min()
    
    return average, fastest, slowest

def basic_info(df):
    """
    Returns basic information about the ride.
    """
    print(
        f'The total distance is {round(calc_total_distance(df), 2)} Km.\n'
        '------------------------------------------------------\n'
        f'The total moving time is {calc_moving_time(df)}.\n'
        '------------------------------------------------------\n'
        f'The total ascent was {elevation_info(df)[0]} Metres.\n'
        f'The total descent was {elevation_info(df)[1]} Metres.\n'
        f'The total change was {round(elevation_info(df)[2], 2)} Metres.\n'
        '------------------------------------------------------\n'
        f'The lowest altitude was {round(elevation_info(df)[3], 2)} Metres.\n'
        f'The highest altitude was {round(elevation_info(df)[4], 2)} Metres.\n'
        '------------------------------------------------------\n'
        f'The average speed was {round(speed_info(df)[0], 2)} Km/h.\n'
        f'The fastest speed was {round(speed_info(df)[1], 2)} Km/h.\n'
        f'The slowest speed was {round(speed_info(df)[2], 2)} Km/h.'
    )
    