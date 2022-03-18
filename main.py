from bokeh.models import ColumnDataSource
from bokeh.tile_providers import get_provider, STAMEN_TERRAIN
import time
from datetime import datetime
import numpy as np
from bokeh.io import export_png
from bokeh.plotting import figure
import requests
import json
import pandas as pd
from url_image_save import save_image


lat = 31.3131 #your location (lat)
long = 31.3131  #your location (long)
threshold = 0.03 #radius as degreee 0.03 or 0.05 is OK. But you can try different values

air_labs_api_key=" " #air labs api (max 1K request in a month for free account), we are getting plane registration number from this site
#https://airlabs.co/      (you can use temp mail :D )

bot_token = " " #telegram bot token
bot_ChatID =" " #telegram bot chat id

lon_min, lat_min = long-threshold, lat-threshold
lon_max, lat_max = long+threshold, lat+threshold

def send_message(status): #telegram bot send message with http requests
    print("Message Sending..")

    requests.get("https://api.telegram.org/bot" + bot_token +"/sendMessage?chat_id=" +bot_ChatID +  "&parse_mode=Html&text=" + status)

    files={"photo":open("map.png","rb")}
    requests.post("https://api.telegram.org/bot" + bot_token +"/sendPhoto?chat_id=" +bot_ChatID , files=files)

    files={"photo":open("plane.png","rb")}
    requests.post("https://api.telegram.org/bot" + bot_token +"/sendPhoto?chat_id=" +bot_ChatID , files=files)


while True:
    try:
        plane = True
        #get plane's location and data from OpenSky
        url_data = "https://opensky-network.org/api/states/all?lamin=" + \ 
            str(lat_min)+"&lomin="+str(lon_min)+"&lamax=" + \
            str(lat_max)+"&lomax="+str(lon_max)
        response = requests.get(url_data).json()
        
        # LOAD TO PANDAS DATAFRAME
        col_name = ['icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 'long', 'lat', 'baro_altitude', 'on_ground', 'velocity',
                    'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk', 'spi', 'position_source']
        flight_df = pd.DataFrame(response['states'])
        flight_df = flight_df.loc[:, 0:16]
        flight_df.columns = col_name
        flight_df = flight_df.fillna('No Data')  # replace NAN with No Data
        flight_df.head()
        icao_data=(flight_df.iloc[:, 0])  # icao
        long_datas = (flight_df.iloc[:, 5])  # long
        lat_datas = (flight_df.iloc[:, 6])  # lat
        name_data = (flight_df.iloc[:, 1])  # callsign

        # FUNCTION TO CONVERT GCS WGS84 TO WEB MERCATOR
        # POINT
        def wgs84_web_mercator_point(lon, lat):
            k = 6378137
            x = lon * (k * np.pi/180.0)
            y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
            return x, y

        # DATA FRAME
        def wgs84_to_web_mercator(df, lon="long", lat="lat"):
            k = 6378137
            df["x"] = df[lon] * (k * np.pi/180.0)
            df["y"] = np.log(np.tan((90 + df[lat]) * np.pi/360.0)) * k
            return df

        # COORDINATE CONVERSION
        xy_min = wgs84_web_mercator_point(lon_min, lat_min)
        xy_max = wgs84_web_mercator_point(lon_max, lat_max)
        wgs84_to_web_mercator(flight_df)
        flight_df['rot_angle'] = flight_df['true_track']*-1  # Rotation angle
        icon_url = ''  # Icon url
        flight_df['url'] = icon_url

        # FIGURE SETTING
        x_range, y_range = ([xy_min[0], xy_max[0]], [xy_min[1], xy_max[1]])
        p = figure(x_range=x_range, y_range=y_range, x_axis_type='mercator',
                   y_axis_type='mercator', sizing_mode='scale_width', plot_height=300)

        # PLOT BASEMAP AND AIRPLANE POINTS
        flight_source = ColumnDataSource(flight_df.iloc[:1])
        tile_prov = get_provider(STAMEN_TERRAIN)
        p.add_tile(tile_prov, level='image')
        p.image_url(url='url', x='x', y='y', source=flight_source, anchor='center',
                    angle_units='deg', angle='rot_angle', h_units='screen', w_units='screen', w=40, h=40)
        p.circle('x', 'y', source=flight_source, fill_color='red',
                 hover_color='yellow', size=30, fill_alpha=0.8, line_width=0)

        export_png(p, filename="map.png")
       

    except TypeError: #no plane found
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"No plane found, Time: {current_time}")
        plane = False
        time.sleep(11)

    reg_number=[]

    if plane: #plane found
        print("Processing...")
        reg_url_data="https://airlabs.co/api/v9/flights?api_key="+air_labs_api_key
        reg_response=requests.get(reg_url_data).json()
        reg_flight_df=pd.DataFrame(reg_response['response'])
        reg_flight_df=reg_flight_df.loc[reg_flight_df["hex"] == icao_data[0].upper()]
        reg_number_df=(reg_flight_df['reg_number'].to_string(index=False))

        if reg_number_df=="Series([], )":  #if didnt get Registration number
            reg_number_df="None"
  
        reg_number.append(reg_number_df)

        if reg_number_df!="None":    
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            message = "Plane found: \nICAO:" +str(icao_data[0])+"\nName:" +str(name_data[0])+ "\nLat:"+str(lat_datas[0])+"\nLong:"+str(long_datas[0])+"\nReg:@"+str(reg_number[0])+"\nTime:" +current_time
            
            print(message)
            print("Map Succesfully Created")


            if save_image(reg_number[0]):
                send_message(message)
            
            print("Done.")
            time.sleep(120)

        else:
            print("Plane found but didn't get Registration Number of plane, will not send message")
            time.sleep(11)
