#!/usr/bin/env python3

import time
from SX127x.LoRa import *
from SX127x.board_config import BOARD

import board
import busio
import adafruit_bme280


# Set up i2c for BME280
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# Set node number here
node = 1

# Initialize LoRa board
BOARD.setup()
BOARD.reset()





import array
class mylora(LoRa):
    def __init__(self, verbose=False):
        super(mylora, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def on_rx_done(self):
        BOARD.led_on()
        
        # Listen for requests from server
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True )# Receive INF
       
        # Converts payload to readable string
        mens=bytes(payload).decode("utf-8",'ignore')
        
        # Print RX data
        print("RX: " + mens)
        
        BOARD.led_off()
        
        # Reply the TH data if "ENVI" is received
        if mens=="ENVI":
            time.sleep(2)

            # Get TH data from BME280
            t = bme280.temperature
            h = bme280.humidity
            t = round(t, 2)
            h = round(h, 2)
            t = str(t)
            h = str(h)
            
            # Create TX message with ";" as delimiter
            TX_message = str(node) + ";" + t + ";" + h + ";"
            print("TX: " + TX_message)
            
            # Convert TX message to bytes
            b = list()
            b.extend(TX_message.encode())
 
            # Send TX message to server
            self.write_payload(b)
            self.set_mode(MODE.TX)
            
        if mens=="ACK":
            print("The server received the last message you sent.")
            
        # Set back client to receiver mode
        time.sleep(2)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

    def on_tx_done(self):
        print("\nTxDone")
        print(self.get_irq_flags())

    def on_cad_done(self):
        print("\non_CadDone")
        print(self.get_irq_flags())

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())

    def on_valid_header(self):
        print("\non_ValidHeader")
        print(self.get_irq_flags())

    def on_payload_crc_error(self):
        print("\non_PayloadCrcError")
        print(self.get_irq_flags())

    def on_fhss_change_channel(self):
        print("\non_FhssChangeChannel")
        print(self.get_irq_flags())

    def start(self):          
        while True:
            # Set client to receiver mode to listen for server data requests
            self.reset_ptr_rx()
            self.set_mode(MODE.RXCONT) 
            while True:
                pass;
            

lora = mylora(verbose=False)

# Slow+long range mode
# f = 915 MHz
# Bw = 125 kHz
# Cr = 4/8
# Sf = 4096chips/symbol
# CRC on. 13 dBm
lora.set_freq(915.0)  
lora.set_pa_config(pa_select=1, max_power=21, output_power=15)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_8)
lora.set_spreading_factor(12)
lora.set_rx_crc(True)
lora.set_low_data_rate_optim(True)


# Medium Range
# Defaults:
# f = 434.0MHz
# Bw = 125 kHz
# Cr = 4/5
# Sf = 128chips/symbol
# CRC on 13 dBm
# lora.set_pa_config(pa_select=1)



assert(lora.get_agc_auto_on() == 1)

try:
    print("START")
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("Exit")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("Exit")
    lora.set_mode(MODE.SLEEP)
BOARD.teardown()

