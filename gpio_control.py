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
        pnconfig.subscribe_key = "sub-c-7c1de1d9-ea5b-451f-bb88-35ae502a81c4"
        pnconfig.publish_key = "pub-c-85ba3694-4855-4861-a14b-fdfcb90cf839"
        pnconfig.ssl = True
        self.pubnub = PubNub(pnconfig)
        
        # Add message listener
        self.pubnub.add_listener(self.MySubscribeCallback())
        
    def set_output(self, value):
        """
        Set 2-bit output based on input value
        
        :param value: Integer between 0-3 representing 2-bit output
        """
        if value < 0 or value > 3:
            print(f"Invalid input: {value}. Must be between 0-3.")
            return
        
        # Convert value to binary and set pins
        GPIO.output(self.output_pins[0], value & 1)  # Least significant bit
        GPIO.output(
            self.output_pins[1], 
            (value >> 1) & 1
        )  # Most significant bit
        
        print(f"Output set to: {value} (Binary: {value:02b})")
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
            self.pubnub.subscribe().channels("chenweisong728").execute()
            
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