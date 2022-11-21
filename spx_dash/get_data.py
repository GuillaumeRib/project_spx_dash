import gpxpy
import pandas as pd

####################################
# GPX DATA PARSING
####################################
test_path = 'gpx_viewer/data/Morvan_day2.gpx'
test_fit_path = 'gpx_viewer/data/8685365728.fit'
def get_gpx(gpx_path):
    '''
    Convert a gpx file as INPUT to a pd DataFrame as OUTPUT
    '''
    # Parse gpx file.
    with open(gpx_path) as f:
        gpx = gpxpy.parse(f)

    # Convert to a dataframe one point at a time.
    points = []
    for segment in gpx.tracks[0].segments:
        for p in segment.points:
            points.append({
                'time': p.time,
                'latitude': p.latitude,
                'longitude': p.longitude,
                'elevation': p.elevation,
            })
    df = pd.DataFrame.from_records(points)
    return df


####################################
# FIT DATA PARSING
####################################
import fitdecode
from typing import Dict, Union, Optional,Tuple
from datetime import datetime, timedelta

# The names of the columns we will use in our points DataFrame. For the data we will be getting
# from the FIT data, we use the same name as the field names to make it easier to parse the data.
POINTS_COLUMN_NAMES = ['latitude', 'longitude', 'lap', 'altitude', 'timestamp', 'heart_rate', 'cadence', 'speed']

# The names of the columns we will use in our laps DataFrame.
LAPS_COLUMN_NAMES = ['number', 'start_time', 'total_distance', 'total_elapsed_time',
                     'max_speed', 'max_heart_rate', 'avg_heart_rate']


def get_fit_lap_data(frame: fitdecode.records.FitDataMessage) -> Dict[str, Union[float, datetime, timedelta, int]]:
    """Extract some data from a FIT frame representing a lap and return
    it as a dict.
    """

    data: Dict[str, Union[float, datetime, timedelta, int]] = {}

    for field in LAPS_COLUMN_NAMES[1:]:  # Exclude 'number' (lap number) because we don't get that
                                        # from the data but rather count it ourselves
        if frame.has_field(field):
            data[field] = frame.get_value(field)

    return data


def get_fit_point_data(frame: fitdecode.records.FitDataMessage) -> Optional[Dict[str, Union[float, int, str, datetime]]]:
    """Extract some data from an FIT frame representing a track point
    and return it as a dict.
    """

    data: Dict[str, Union[float, int, str, datetime]] = {}

    if not (frame.has_field('position_lat') and frame.has_field('position_long')):
        # Frame does not have any latitude or longitude data. We will ignore these frames in order to keep things
        # simple, as we did when parsing the TCX file.
        return None
    else:
        data['latitude'] = frame.get_value('position_lat') / ((2**32) / 360)
        data['longitude'] = frame.get_value('position_long') / ((2**32) / 360)

    for field in POINTS_COLUMN_NAMES[3:]:
        if frame.has_field(field):
            data[field] = frame.get_value(field)

    return data


def get_dataframes(fname: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Takes the path to a FIT file (as a string) and returns two Pandas
    DataFrames: one containing data about the laps, and one containing
    data about the individual points.
    """

    points_data = []
    laps_data = []
    lap_no = 1
    with fitdecode.FitReader(fname) as fit_file:
        for frame in fit_file:
            if isinstance(frame, fitdecode.records.FitDataMessage):
                if frame.name == 'record':
                    single_point_data = get_fit_point_data(frame)
                    if single_point_data is not None:
                        single_point_data['lap'] = lap_no
                        points_data.append(single_point_data)
                elif frame.name == 'lap':
                    single_lap_data = get_fit_lap_data(frame)
                    single_lap_data['number'] = lap_no
                    laps_data.append(single_lap_data)
                    lap_no += 1

    # Create DataFrames from the data we have collected. If any information is missing from a particular lap or track
    # point, it will show up as a null value or "NaN" in the DataFrame.

    laps_df = pd.DataFrame(laps_data, columns=LAPS_COLUMN_NAMES)
    laps_df.set_index('number', inplace=True)
    points_df = pd.DataFrame(points_data, columns=POINTS_COLUMN_NAMES)

    return points_df


####################################
# FEATURE ENGINEERING
####################################
def data_feat_eng(df):
    '''
    pd DataFrame from gpx file as INPUT.
    Create new features, enriching df
    OUTPUT pd DataFrame with added features
    '''

    # Duration
    df[['duration']] = df[['time']] - df[['time']].iloc[0]
    df['duration'] = pd.to_datetime(df['duration'].dt.total_seconds(),unit='s').dt.strftime("%H:%M:%S")

    # D+
    df[['elev_diff']] = df[['elevation']].diff()
    df['d+'] = df[df['elev_diff']>0]['elev_diff'].cumsum().round(2)
    df = df.fillna(method='ffill')

    # Cumul Elevation
    df['elev_cum'] = df.elev_diff.cumsum().round(2)

    # Avg deniv for color
    n=60
    df['d_avg'] = df['elev_diff'].rolling(n).sum().round(2)
    return df


def data_feat_eng_FIT(df):
    '''
    pd DataFrame from FIT file as INPUT.
    Create new features, enriching df
    OUTPUT pd DataFrame with added features
    '''
    df = df.rename(columns={'altitude':'elevation','timestamp':'time'})

    # Duration
    df[['duration']] = df[['time']] - df[['time']].iloc[0]
    df['duration'] = pd.to_datetime(df['duration'].dt.total_seconds(),unit='s').dt.strftime("%H:%M:%S")

    # D+
    df[['elev_diff']] = df[['elevation']].diff()
    df['d+'] = df[df['elev_diff']>0]['elev_diff'].cumsum().round(2)
    df = df.fillna(method='ffill')

    # Cumul Elevation
    df['elev_cum'] = df.elev_diff.cumsum().round(2)

    # Avg deniv for color
    n=60
    df['d_avg'] = df['elev_diff'].rolling(n).sum().round(2)

    # Distance in km
    df[['distance']] = df[['speed']].cumsum()/1000
    df[['distance']]= df[['distance']].round(3)

    # Speed in km/h
    df[['speed']] = df[['speed']]*3600/1000
    df[['speed']] = df[['speed']].rolling(5).mean()

    # Smooth HR
    df[['heart_rate']] = df[['heart_rate']].rolling(5).mean()

    return df
