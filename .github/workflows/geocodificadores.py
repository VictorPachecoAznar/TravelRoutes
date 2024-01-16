#VÍCTOR PACHECO AZNAR
#JAN, 16TH 2024

import geocoder 
import geopandas
import pandas as pd
from shapely.geometry import LineString,point,shape
import matplotlib.pyplot as plt
from geopy import Nominatim
import folium
import webbrowser

#THIS FUNCTION ALLOWS FOLIUM MAP VISUALIZATION IN HTML DOCUMENTS
def showMap(foliumMap,name="routes"):
    fn=name+".html"
    foliumMap.save(fn)
    webbrowser.open(fn)
            
#FUNCTION TO ADD THE ELEMENTS TO THE DICTIONARY OF CITIES
def addRoute(cities,routename):
    geolocator=Nominatim(user_agent='your_email')
    while True:
        city=input('ADD IN THE CITY\n')
        if city=='STOP':
            return cities
        try:
            g=geolocator.geocode(query=city)
            cities[city]={'LONGITUDE':g.longitude,'LATITUDE':g.latitude,'ROUTE':routename}
        except:
            city=input('WRONG ADDRESS!\n')
cities={}
print('WELCOME, THIS CODE WILL HELP YOU CREATE POLYLINES IN A FOLIUM MAP COMING FROM ADDRESSES OR CITY LOCATIONS\n REMEBER THAT THE WORD \'STOP\' WILL STOP THE CURRENT QUESTION')
while True:
    routename=input('PLEASE ADD IN THE NAME OF THE ROUTE!')
    if routename.upper()=='STOP':
        break
    else:
        cities=addRoute(cities,routename)

#CREATING A GEODATAFRAME WITH THE VALUES FROM 
gdf=geopandas.GeoDataFrame(data={'CITY':pd.Series([key for key in cities]),
                                 'LONGITUDE':pd.Series([cities[key]['LONGITUDE'] for key in cities]),
                                 'LATITUDE':pd.Series([cities[key]['LATITUDE'] for key in cities]),
                                 'ROUTE':pd.Series([cities[key]['ROUTE'] for key in cities])})

#CREATING A POINT FOR EACH CITY IN THE DATAFRAME
gdf['geometry']=geopandas.points_from_xy(x=gdf['LONGITUDE'],y=gdf['LATITUDE'],crs=4326)

#CREATING A LINE THAT CONNECTS THE POINTS FROM EACH ROUTE
routes=geopandas.GeoDataFrame(gdf.groupby(['ROUTE'])['geometry'].apply(lambda x: LineString(x.tolist())),geometry='geometry',crs=4326)

#CREATING A FOLIUM MAP FROM THE GEODATAFRAME, ADDING A BASEMAP AND A LAYER MANAGER
mapa=routes.explore()
folium.TileLayer('openstreetmap').add_to(mapa)
folium.LayerControl().add_to(mapa)

#DISPLAYING A MAP
showMap(mapa)
