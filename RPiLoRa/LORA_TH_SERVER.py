#!/usr/bin/env python3

import time
from SX127x.LoRa import *
from SX127x.board_config import BOARD

BOARD.setup()
BOARD.reset()


class mylora(LoRa):
    def __init__(self, verbose=False):
        super(mylora, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.var=0

    def on_rx_done(self):
        BOARD.led_on()
        
        # Set rx flag to 1
        self.clear_irq_flags(RxDone=1)
        
        # Get payload and decode
        payload = self.read_payload(nocheck=True)
        payload_conv = bytes(payload).decode("utf-8",'ignore')
        
        # Prints payload
        print ("RX: " + payload_conv)
        
        # Extract node number, t, and h from sender
        s = payload_conv.split(";")
        if len(s) >= 2:
            node = s[0]
            t = s[1]
            h = s[2]
            print("Node: " + node)
            print("Temperature: " + t)
            print("Humidity: " + h)
        
        
        BOARD.led_off()
        
        # Compulsary waiting time for client to get ready
        time.sleep(2)
        
        # Send acknowledgement to client
        ACK_message = "ACK"
        b = list()
        b.extend(ACK_message.encode())
        print ("TX: " + ACK_message)
        self.write_payload(b)
        
        # Set back server to TX mode
        self.set_mode(MODE.TX)
        self.var=1

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
            while (self.var==0):
                
                # Request ENVI data from clients
                TX_message = "ENVI"
                b = list()
                b.extend(TX_message.encode())
                print ("TX: " + TX_message)
                self.write_payload(b)
                self.set_mode(MODE.TX)
                time.sleep(3)
                
                # Set server to receiver mode
                self.reset_ptr_rx()
                self.set_mode(MODE.RXCONT) 
            
                start_time = time.time()
                while (time.time() - start_time < 5): # wait until data is received before sending again
                    pass;
            
            # Set server to receiver mode
            self.var=0
            self.reset_ptr_rx()
            self.set_mode(MODE.RXCONT) 
            time.sleep(5)

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


# Medium Range  Defaults:
# f = 434.0MHz
# Bw = 125 kHz
# Cr = 4/5
# Sf = 128chips/symbol
# CRC on 13 dBm
# lora.set_pa_config(pa_select=1)



# Begin server program
assert(lora.get_agc_auto_on() == 1)
try:
    print("START SERVER")
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

