import serial
from time import time

ser = serial.Serial('/dev/tty.usbserial-1410', 9600, timeout=1)
ser.flush()
while True:
    if ser.in_waiting > 0:
         if ser.readline().decode('utf-8').rstrip() == "Found RFID/NFC reader":
             print("Connect sucsed")
             break
while True:
    if ser.in_waiting > 0:
        smth = ser.readline().decode('utf-8').rstrip()[7:]
        if not smth == "":
            print({"card_id": smth, "date": time()})
