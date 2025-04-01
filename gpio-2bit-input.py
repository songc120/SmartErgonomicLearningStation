import RPi.GPIO as GPIO
import select
import sys

class TwoBitGPIOController:
    def __init__(self, output_pins=(17, 27)):
        """
        Initialize GPIO setup for 2-bit input/output
        
        :param output_pins: Tuple of two GPIO pin numbers (default: 17, 27)
        """
        self.output_pins = output_pins
        
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Set both pins as outputs
        for pin in self.output_pins:
            GPIO.setup(pin, GPIO.OUT)

    def set_output(self, value):
        """
        Set 2-bit output based on input value
        
        :param value: Integer between 0-3 representing 2-bit output
        """
        if value < 0 or value > 3:
            print(f"Invalid input: {value}. Must be between 0-3.")
            return
        
        # Convert value to binary and set pins
        GPIO.output(self.output_pins[0], value & 1)      # Least significant bit
        GPIO.output(self.output_pins[1], (value >> 1) & 1)  # Most significant bit
        
        print(f"Output set to: {value} (Binary: {value:02b})")
        print(f"Pin {self.output_pins[1]}: {(value >> 1) & 1}")
        print(f"Pin {self.output_pins[0]}: {value & 1}")

    def run(self):
        """Main control loop for 2-bit GPIO input"""
        try:
            print("2-Bit GPIO Keyboard Control")
            print("Input values 0-3 (binary 00-11)")
            print("Press keys 0, 1, 2, 3")
            print("Press 'q' to quit")
            
            while True:
                # Use select to handle input
                rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
                
                if rlist:
                    key = sys.stdin.read(1)
                    
                    # Check input and set GPIO accordingly
                    if key in '0123':
                        self.set_output(int(key))
                    elif key.lower() == 'q':
                        print("Exiting...")
                        break
                    elif key == '\n':
                        # Ignore newline characters
                        continue
                    else:
                        print("Invalid input. Use 0, 1, 2, 3, or 'q'")
        
        except KeyboardInterrupt:
            print("\nProgram terminated by user")
        finally:
            # Clean up GPIO on exit
            GPIO.cleanup()

def main():
    # Create controller with default pins 17 and 27
    controller = TwoBitGPIOController()
    controller.run()

if __name__ == "__main__":
    main()
