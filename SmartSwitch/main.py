###############################################################################
# Simple IoT Smart Switch using NodeMCU v3
###############################################################################

# Libraries
import streams
from wireless import wifi
from espressif.esp8266wifi import esp8266wifi as wifi_driver # espressif esp8266 wifi driver 
from zerynthapp import zerynthapp # Zerynth APP library


streams.serial()
sleep(1000)
print("Initializing APP...")


# Import webpage to NodeMCU flash
try:
    new_resource("template/index.html")
    print("Imported resource.")
except Exception as e:
    print(e)


# Variable constants
SSID = "Turbulence"
PASSWORD = "qwertyuiop"
RELAY_PIN = D5
UID = "BiZcDz1DRKqwbQ63WKnDCw" #  Get this from "Connected Devices"
TOKEN = "yDYfLuntSgeBYIR7xHt9Wg" #  Get this from "Connected Devices"



# functions:

def connectWifi(SSID, PASSWORD):
    print("Connecting to Wi-Fi router...")
    
    for i in range(0,5):
    try:
        wifi.link(SSID,wifi.WIFI_WPA2,PASSWORD)
        break
    except Exception as e:
        print("Error: ", e)
    else:
        print("Cannot connect.")
        while True:
            sleep(1000)
            


def on_switch():
    digitalWrite(D5,LOW)
    print("ON")

def off_switch():
    digitalWrite(D5,HIGH)
    print("OFF")
    




# Intialize APP
pinMode(RELAY_PIN, OUTPUT)
wifi_driver.auto_init()
connectWifi(SSID,PASSWORD)
info = wifi.link_info()
print("Connected to WiFI IP:",info[0])

zapp = zerynthapp.ZerynthApp(UID, TOKEN, log=True)
zapp.on("on_switch", on_switch)
zapp.on("off_switch",off_switch)
zapp.run()

while True:
    try:
        sleep(1000)
    except Exception as e:
        print("Error: ",e)

