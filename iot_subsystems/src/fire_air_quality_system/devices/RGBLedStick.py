import time
import neopixel
import board   
from gpiozero import PWMLED
from time import sleep
from dataclasses import dataclass
from common.devices.actuator import Action, Command, Actuator
import logging

logger = logging.getLogger(__name__)


@dataclass
class RBGLedStickActuator(Actuator):
    """Actuator to control the state of a digital gpio LED"""

    device: neopixel
    action: Action
    state: float = 0

    def control_actuator(self, command: Command) -> bool:
        """Function that controls the RGB Led actuator"""       
        if (command.data == self.state):
            print("Is already on or off")            
            self.device.value = command.data 
            logger.info(f"{self.action.name}: DEVICE ALREADY ON OR OFF")          
            return False
        else:
            print(command.action)
            if (command.action == Action.RGB_LED_TOGGLE):
                self.state = command.data
                self.action = command.action
                if (command.data == 1):
                    self.device.fill((255, 255, 255))
                    self.device.show()
                else:
                    self.device.fill((0, 0, 0))
                    self.device.show() 
                               
                logger.info(f"{self.action.name}: DEVICE TOGGLED")    
            
            elif (command.action == Action.RGB_LED_RED):                 
                self.state = command.data
                self.action = command.action
                if (command.data == 1):
                    self.device.fill((255, 0, 0))
                    self.device.show()
                else:
                    self.device.fill((0, 0, 0))
                    self.device.show() 

                logger.info(f"{self.action.name}: DEVICE TOGGLED") 
            elif (command.action == Action.RGB_LED_YELLOW):
                self.state = command.data
                self.action = command.action
                if (command.data == 1):
                    self.device.fill((255, 255, 0))
                    self.device.show()
                else:
                    self.device.fill((0, 0, 0))
                    self.device.show() 

                logger.info(f"{self.action.name}: DEVICE TOGGLED")           
            elif (command.action == Action.RGB_LED_GREEN):
                self.state = command.data
                self.action = command.action
                if (command.data == 1):
                    self.device.fill((0, 255, 0))
                    self.device.show()
                else:
                    self.device.fill((0, 0, 0))
                    self.device.show()
                     
                logger.info(f"{self.action.name}: DEVICE TOGGLED") 
            else :
                self.state = command.data
                self.action = command.action
                self.device.fill((0, 0, 0))
                self.device.show()                
                logger.info(f"{self.action.name}: DEVICE TOGGLED")           
            return True

TEST_SLEEP_TIME = 5

def main():
    print("Called main")
    pixels = neopixel.NeoPixel(board.D18, 10, auto_write=False) 
    rbg_led_actuator = RBGLedStickActuator(device=pixels, action=(Action.RGB_LED_TOGGLE))    
    rgb_led_on = Command(Action.RGB_LED_TOGGLE, 1)
    rgb_led_off = Command(Action.RGB_LED_TOGGLE, 0)


    while True:
        rbg_led_actuator.control_actuator(rgb_led_on)    
        print("RGB LED ON")   
        sleep(TEST_SLEEP_TIME)
        rbg_led_actuator.control_actuator(rgb_led_off)
        print("RGB LED OFF") 
        sleep(TEST_SLEEP_TIME)


if __name__ == "__main__":
    """
    Usage:         
        $ sudo PYTHONPATH=${PYTHONPATH}:src ~/Documents/repositories/final-project-refarminal/iot_subsystems/.venv/bin/python src/Alex_system/devices/RGBLedStick.py
    Alternatively:
        $ export PYTHONPATH=${PYTHONPATH}:${HOME}/path-to-repository/src 
        $ sudo ~/Documents/repositories/final-project-refarminal/iot_subsystems/.venv/bin/python src/Alex_system/devices/RGBLedStick.py
    """
    main()































#from rpi_ws281x import PixelStrip, Color
# # LED strip configuration:
# LED_COUNT = 10         # Number of LED pixels.
# LED_PIN = 18          # GPIO pin connected to the pixels (must support PWM! GPIO18 is good)
# LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
# LED_DMA = 10          # DMA channel to use for generating signal (try 10)
# LED_BRIGHTNESS = 180  # Set to 0 for darkest and 255 for brightest
# LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
# LED_CHANNEL = 0

# # Create PixelStrip object
# strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# strip.begin()

# def main():
#     while True:
#         # Red
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, Color(255, 0, 0))
#         strip.show()
#         time.sleep(1)

#         # Green
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, Color(0, 255, 0))
#         strip.show()
#         time.sleep(1)

#         # Blue
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, Color(0, 0, 255))
#         strip.show()
#         time.sleep(1)

# if __name__ == "__main__":
#     main()