import geocoder 
import geopandas
import pandas as pd
from shapely.geometry import LineString,point,shape
import matplotlib.pyplot as plt
from geopy import Nominatim
import folium
import webbrowser

def showMap(foliumMap,name="mapica"):
    fn=name+".html"
    foliumMap.save(fn)
    webbrowser.open(fn)

def troubleshootImput(inputString,typeError,rangeError):
    while type(inputString)!=int:
        try:
            integer=int(inputString)
            if(integer>0):
                return int(inputString)
            else:
                inputString=input(rangeError)
        except:
            inputString=input(typeError)

def addRoute(cities,routename=0):
    if routename==0:
        routename=input('PLEASE ADD IN THE NAME OF THE ROUTE!')
    maxCities=troubleshootImput(input('PLEASE ADD THE NUMBER OF DESIRED CITIES'),'PLEASE ONLY INTEGERS ALLOWED|','PLEASE ONLY POSITIVE INTEGERS!')
    print('great job! now add your desired ',maxCities,'cities')
    geolocator=Nominatim(user_agent='vpache3.12@gmail.com')
    for i in range(maxCities):
        city=input('ADD IN THE CITY')
        try:
            g=geolocator.geocode(query=city)
            cities[city]={'LONGITUDE':g.longitude,'LATITUDE':g.latitude,'ROUTE':routename}
            print(cities[city])
        except:
            city=input('wrong name for a city!')
    return cities

cities={}
maxRoutes=troubleshootImput(input('PLEASE ADD THE MAX NUMBER OF ROUTES'),'ONLY INTEGERS ALLOWED!','PLEASE ONLY POSITIVE INTEGERS!')
for i in range(maxRoutes):
    cities=addRoute(cities)

gdf=geopandas.GeoDataFrame(data={'City':pd.Series([key for key in cities]),
                                 'Longitude':pd.Series([cities[key]['LONGITUDE'] for key in cities]),
                                 'Latitude':pd.Series([cities[key]['LATITUDE'] for key in cities]),
                                 'Route':pd.Series([cities[key]['ROUTE'] for key in cities])})
print(gdf)
gdf['geometry']=geopandas.points_from_xy(x=gdf['Longitude'],y=gdf['Latitude'],crs=4326)
routes=geopandas.GeoDataFrame(gdf.groupby(['Route'])['geometry'].apply(lambda x: LineString(x.tolist())),geometry='geometry',crs=4326)
print(gdf)
print(routes)
gdf.plot()
mapa=routes.explore()
folium.TileLayer('openstreetmap').add_to(mapa)
folium.LayerControl().add_to(mapa)

showMap(mapa)
routes.plot()
#countriesDf=geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
#countriesDf.plot()
plt.show()
#g = geocoder.mapquest(['Mountain View, CA', 'Boulder, Co'], method='batch')
#for result in g:
#    print(result.address, result.latlng)
