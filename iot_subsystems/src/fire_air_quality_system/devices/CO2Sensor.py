from dataclasses import dataclass
from common.devices.sensor import Measurement, Reading, Sensor
import logging
import time
import board
import busio
import adafruit_sgp30
# Refer to https://wiki.seeedstudio.com/Grove-VOC_and_eCO2_Gas_Sensor-SGP30/

logger = logging.getLogger(__name__)


@dataclass
class GroveVOCeCO2Sensor(object):    
    sgp30: adafruit_sgp30
    
    def __init__(self):
        # Create I2C bus
        i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
        
        # Create sensor instance
        self.sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

        # Initialize
        print("SGP30 serial #", [hex(i) for i in self.sgp30.serial])
        self.sgp30.iaq_init()
        self.sgp30.set_iaq_baseline(0x8973, 0x8aae)
    
    def read_CO2_level(self):      
        eCO2 = self.sgp30.eCO2
        print("eCO2", eCO2)
        #TVOC = self.spg30.TVOC

        return eCO2
        

@dataclass
class CO2Sensor(Sensor):    
    device: GroveVOCeCO2Sensor
    measurement: Measurement

    def read_sensor(self) -> Reading:
        """See base class."""
        value = self.device.read_CO2_level()
        print(value,self.measurement)
        logger.info(Reading(value, self.measurement))
        return Reading(value, self.measurement)


def main():
    sensor = GroveVOCeCO2Sensor()
    CO2Level = CO2Sensor(sensor, Measurement.CO2LEVEL)

    while True:        
        co2Reading= CO2Level.read_sensor()
        print("eCO2 = {} ppm".format(co2Reading))   
        time.sleep(1)
       

if __name__ == "__main__":
    """
    Usage:
        $ PYTHONPATH=${PYTHONPATH}:src python src/Alex_system/devices/CO2Sensor.py
    Alternatively:
        $ export PYTHONPATH=${PYTHONPATH}:${HOME}/path-to-repository/src
        $ python src/Alex_system/devices/CO2Sensor.py
    """
    main()
