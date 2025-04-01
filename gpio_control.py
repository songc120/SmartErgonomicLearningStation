import RPi.GPIO as GPIO
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
import time


class GPIOPubNubController:
    def __init__(self, output_pins=(17, 27)):
        """
        Initialize GPIO setup and PubNub configuration
        
        :param output_pins: Tuple of two GPIO pin numbers (default: 17, 27)
        """
        self.output_pins = output_pins
        
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Set both pins as outputs
        for pin in self.output_pins:
            GPIO.setup(pin, GPIO.OUT)
            
        # PubNub Configuration
        pnconfig = PNConfiguration()
        pnconfig.publish_key = 'pub-c-85ba3694-4855-4861-a14b-fdfcb90cf839'
        pnconfig.subscribe_key = 'sub-c-7c1de1d9-ea5b-451f-bb88-35ae502a81c4'
        pnconfig.uuid = 'userId'
        self.channel = 'chenweisong728'
        self.pubnub = PubNub(pnconfig)
        
        # Add message listener
        self.pubnub.add_listener(self.MySubscribeCallback())
        
    def set_output(self, value):
        """
        Set 2-bit output based on input value
        Value mapping:
        - 0 (00) = stop
        - 1 (01) = up
        - 2 (10) = down
        
        :param value: Integer between 0-2 representing movement direction
        """
        if value < 0 or value > 2:
            print(f"Invalid input: {value}. Must be between 0-2.")
            return
        
        # Convert value to binary and set pins
        GPIO.output(self.output_pins[0], value & 1)  # Least significant bit
        GPIO.output(
            self.output_pins[1], 
            (value >> 1) & 1
        )  # Most significant bit
        
        # Print status with movement direction
        direction = "Stop" if value == 0 else "Up" if value == 1 else "Down"
        print(f"Movement: {direction} (Binary: {value:02b})")
        print(f"Pin {self.output_pins[1]}: {(value >> 1) & 1}")
        print(f"Pin {self.output_pins[0]}: {value & 1}")

    class MySubscribeCallback(SubscribeCallback):
        def __init__(self, controller):
            self.controller = controller
            
        def message(self, pubnub, message):
            try:
                value = message.message.get("value")
                if value is not None:
                    self.controller.set_output(value)
            except Exception as e:
                print(f"Error processing message: {e}")

    def run(self):
        """Main control loop for PubNub subscription"""
        try:
            print("Starting PubNub subscription...")
            print("Movement Control:")
            print("0 = Stop (00)")
            print("1 = Up (01)")
            print("2 = Down (10)")
            self.pubnub.subscribe().channels(self.channel).execute()
            
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nProgram terminated by user")
        finally:
            # Clean up GPIO and unsubscribe
            GPIO.cleanup()
            self.pubnub.unsubscribe_all()


def main():
    # Create controller with default pins 17 and 27
    controller = GPIOPubNubController()
    controller.run()


if __name__ == "__main__":
    main() 