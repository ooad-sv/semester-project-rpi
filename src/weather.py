import Adafruit_DHT
import bmp1801
import time
from time import sleep
import http.client

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
u_humidity, u_temperature = 0, 0
u_temp, u_pressure, u_altitude = 0, 0, 0
conn = http.client.HTTPSConnection("ooad-sv-wms.herokuapp.com")
while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    temp, pressure, altitude = bmp1801.readBmp180()
    humidity, temperature, pressure, altitude = round(humidity,1), round(temperature,1), round(pressure,1), round(altitude,1)
    if u_humidity != humidity or u_temperature != temperature or u_pressure != pressure or u_altitude != altitude:
        
        u_humidity, u_temperature, u_pressure, u_altitude = humidity, temperature, pressure, altitude
        # check for an update every minute
        # if there is a difference in one of the weather metrics, 
        # make a http post call with updated values
        if u_humidity and u_temperature and u_pressure and u_altitude and u_humidity<100:
            # key is specific to the weather stations
            # Station 1: gekpeiakemwnrjhlckmimicinuocbkgc
            # Station 2: kkztpimkpbsyauczeekmnrgkyopnbpws
            # Station 3: lpjvpcrhqbgumkarsxkwrpkmvdvwjkaj
            # Station 4: kxovumoysaslqalizjapnbkhvmhunrdd
            payload = 'key=kkztpimkpbsyauczeekmnrgkyopnbpws&temperature='+str(u_temperature)+'&pressure='+str(u_pressure)+'&humidity='+str(u_humidity)+'&altitude='+str(u_altitude)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            conn.request("POST", "/weather-station/update", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
            print("Temp={0:0.1f}*C  Humidity={1:0.1f}%  Pressure={2:0.1f} Pa  Altitude={3:0.1f} m".format(u_temperature, u_humidity, u_pressure, u_altitude))
        else:
            print("Failed to retrieve data from the sensors")
    sleep(60)
        
