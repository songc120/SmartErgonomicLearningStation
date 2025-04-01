import RPi.GPIO as GPIO
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
import time

# Pin Setup
LED_PIN = 17
SERVO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz PWM
servo.start(0)

# PubNub Configuration
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-7c1de1d9-ea5b-451f-bb88-35ae502a81c4"
pnconfig.publish_key = "pub-c-85ba3694-4855-4861-a14b-fdfcb90cf839"
pnconfig.ssl = True
pubnub = PubNub(pnconfig)

# Message Callback
class MySubscribeCallback(SubscribeCallback):
    def message(self, pubnub, message):
        msg = message.message
        print(f"Received: {msg}")
        if msg == "on":
            GPIO.output(LED_PIN, GPIO.HIGH)
        # elif msg == "lightOff":
        #     GPIO.output(LED_PIN, GPIO.LOW)
        # elif msg == "servoOpen":
        #     servo.ChangeDutyCycle(7)  # Counter Clockwise
        #     time.sleep(1)
        #     servo.ChangeDutyCycle(0)
        # elif msg == "servoCloss":
        #     servo.ChangeDutyCycle(12)  # Clockwise
        #     time.sleep(1)
        #     servo.ChangeDutyCycle(0)

# Subscribe to PubNub Channel
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels("chenweisong728").execute()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping...")
    GPIO.cleanup()
    pubnub.unsubscribe_all()
