#! /usr/bin/env python3

import time
import subprocess
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

def button_callback(channel):
  print('pairing device')
  command = "echo 'discoverable on'| bluetoothctl;echo 'pairable on' | bluetoothctl"
  with subprocess.Popen(["bash","-c",command],stdout=subprocess.PIPE) as proc:
    try:
      l = proc.stdout.read()
      print(l)
    except AttributeError:
      print()
  time.sleep(30)
  command = "echo 'discoverable off'| bluetoothctl;echo 'pairable off' | bluetoothctl"

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge

message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup() # Clean up 
