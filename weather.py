import pandas as pd
import requests
import datetime

circuits = pd.read_csv('../data/circuits.csv')
races = pd.read_csv('../data/races.csv')

cols = ['raceId', 'circuitId', 'lat', 'lng', 'date', 'time']

final_df = circuits.merge(races, on='circuitId', how='left').loc[:, cols]

## https://archive-api.open-meteo.com/v1/archive?latitude=52.52&longitude=13.41&start_date=2023-04-18&end_date=2023-05-02&hourly=

def get_weather(lat, lng, start_date, end_date):
    url = 'https://archive-api.open-meteo.com/v1/archive'
    params = {
        'latitude': lat,
        'longitude': lng,
        'start_date': start_date,
        'end_date': end_date,
        'hourly': 'temperature_2m,precipitation',
    }
    response = requests.get(url, params=params)
    return response.json()

def get_weather_df(lat, lng, start_date, end_date):
    data = get_weather(lat, lng, start_date, end_date)
    print(data)
    if 'hourly' not in data.keys(): return None

    df = pd.DataFrame(data['hourly'])

    return df

def get_weather_df_list(df):
    for i, row in df.iterrows():
        lat = row['lat']
        lng = row['lng']
        date = datetime.datetime.strptime(row['date'], '%Y-%m-%d').date()
        start_date = date
        end_date = date + datetime.timedelta(days=1)

        if int(date.year) < 2014: continue

        weather_df = get_weather_df(lat, lng, start_date, end_date)

        if weather_df is None: continue

        df.loc[i, 'temp'] = weather_df['temperature_2m'].mean() if 'temperature_2m' in weather_df.columns else None
        df.loc[i, 'precipitation'] = weather_df['precipitation'].sum() if 'precipitation' in weather_df.columns else None

    df.drop(columns=['time'])

    return df

weather_list = get_weather_df_list(final_df)

weather_list.to_csv('../data/weather.csv')
