import RPi.GPIO as GPIO
import sys
import termios
import tty

from pubnub.pubnub import PubNub, SubscribeListener, SubscribeCallback, PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.exceptions import PubNubException
import time
import threading
import json
import adafruit_dht
import board


pnconf = PNConfiguration()
pnconf.publish_key = 'pub-c-85ba3694-4855-4861-a14b-fdfcb90cf839'
pnconf.subscribe_key = 'sub-c-7c1de1d9-ea5b-451f-bb88-35ae502a81c4'
pnconf.uuid = 'userId'
pubnub = PubNub(pnconf)
channel = 'chenweisong728'

def setup_gpio():
    """Set up GPIO mode and pin configuration"""
    GPIO.setmode(GPIO.BCM)  # Use BCM numbering scheme
    GPIO.setwarnings(False)  # Disable GPIO warnings
    
    # Set GPIO pin 17 as output (you can change this to your desired pin)
    GPIO.setup(17, GPIO.OUT)

def get_char():
    """Read a single character from keyboard input without requiring Enter key"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def main():
    """Main function to handle GPIO output based on keyboard input"""
    try:
        setup_gpio()
        print("GPIO Keyboard Control")
        print("Press '0' to set GPIO pin LOW")
        print("Press '1' to set GPIO pin HIGH")
        print("Press 'q' to quit")
        
        while True:
            # Get keyboard input
            key = get_char()
            
            # Check input and set GPIO accordingly
            if key == '0':
                GPIO.output(17, GPIO.LOW)
                print("GPIO pin set to LOW")
            elif key == '1':
                GPIO.output(17, GPIO.HIGH)
                print("GPIO pin set to HIGH")
            elif key.lower() == 'q':
                print("Exiting...")
                break
            else:
                print("Invalid input. Use '0', '1', or 'q'")
    
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    finally:
        # Clean up GPIO on exit
        GPIO.cleanup()

if __name__ == "__main__":
    main()
