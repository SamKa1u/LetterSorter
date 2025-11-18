import serial
from time import sleep
                    
            
class Coms:
    def __init__(self, shared):
        self.shared = shared
        
    def run(self):
        while True:
            with serial.Serial ("/dev/ttyAMA0", 9600, timeout = 1) as ser:  # open port with baud rate    
                received_line = ser.readline()              				# read serial port
                if received_line:
                    print("[Coms] Received on RX:", received_line)              # print received line of data
            
                if b'IR_DETECTED' in received_line:
                    sleep(1)
                self.shared["RX"] = received_line;
                
                if self.shared.get("TX") != None:
                    ser.write(self.shared.get("TX").encode("utf-8"))
                    self.shared["TX"] = None
                sleep(.5)
