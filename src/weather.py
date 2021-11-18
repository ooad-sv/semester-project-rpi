import Adafruit_DHT
import bmp1801
import time
import http.client

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    temp, pressure, altitude = bmp1801.readBmp180()

    if humidity is not None and temperature is not None and pressure is not None and altitude is not None:
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%  Pressure={2:0.1f} Pa  Altitude={3:0.1f} m".format(temperature, humidity, pressure, altitude))
    else:
        print("Failed to retrieve data from the sensors")
