# Importing required libraries
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
import RPi.GPIO as GPIO
import time
import threading

# PubNub Configuration
pnconf = PNConfiguration()
pnconf.publish_key = 'pub-c-85ba3694-4855-4861-a14b-fdfcb90cf839'
pnconf.subscribe_key = 'sub-c-7c1de1d9-ea5b-451f-bb88-35ae502a81c4'
pnconf.uuid = 'userId'
pubnub = PubNub(pnconf)
channel = 'chenweisong728'

# GPIO Setup for motion sensor
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pir_pin = 19  # Motion sensor on GPIO pin 26
GPIO.setup(pir_pin, GPIO.IN)

# Global variables
last_motion_time = time.time()
no_motion_threshold = 10  # seconds before sending alert
alert_sent = False  # Flag to track if alert has been sent

def check_motion():
    """Thread function to continuously check for motion"""
    global last_motion_time, alert_sent
    
    while True:
        if GPIO.input(pir_pin):  # Motion detected
            print("Motion detected!")
            last_motion_time = time.time()  # Reset the timer
            alert_sent = False  # Reset alert flag when motion is detected
            time.sleep(0.5)  # Small delay to avoid multiple detections
        time.sleep(0.1)  # Loop delay

def monitor_no_motion():
    """Thread function to monitor for lack of motion and send alerts"""
    global last_motion_time, alert_sent
    
    while True:
        current_time = time.time()
        time_since_last_motion = current_time - last_motion_time
        
        # Check if no motion for threshold period and alert hasn't been sent
        if (time_since_last_motion >= no_motion_threshold and 
                not alert_sent):
            print(f"ALERT: No motion detected for {no_motion_threshold} seconds!")
            
            # Send alert to PubNub
            try:
                pubnub.publish().channel(channel).message({
                    'alert': 'no_motion',
                    'seconds_inactive': time_since_last_motion,
                    'timestamp': current_time,
                    'device_id': pnconf.uuid
                }).sync()
                print("Alert sent to PubNub")
                alert_sent = True  # Mark alert as sent
                
            except Exception as e:
                print(f"Failed to send alert: {e}")
        
        time.sleep(1)  # Check every second

# Start the threads
motion_thread = threading.Thread(target=check_motion, daemon=True)
alert_thread = threading.Thread(target=monitor_no_motion, daemon=True)

print("Starting motion detection system...")
motion_thread.start()
alert_thread.start()

try:
    # Keep the main thread alive
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting program")
    GPIO.cleanup()  # Clean up GPIO on exit
