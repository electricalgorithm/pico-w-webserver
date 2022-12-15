import machine
from picozero import pico_temp_sensor, pico_led
from time import sleep
from server.logger import LOG

class Device():
    
    LED_NAME = "LED"
    TEMP_NAME = "TEMP"
    RTC_NAME = "CLOCK"
    LED_ENABLE_TEXT = "ON"
    LED_DISABLE_TEXT = "OFF"
    
    def __init__(self):
        # Initial attributes
        self.rtc = machine.RTC()
        
        # Default states
        self.states = {
            Device.LED_NAME: Device.LED_DISABLE_TEXT,
            Device.TEMP_NAME: 0,
            Device.RTC_NAME: (2022, 12, 15, 3, 4, 7, 14, 0),
        }
        self.led_set_low()
        self.update_information()
        
    @staticmethod
    def reset_board():
        LOG.logger.error("Resetting the hardware.")
        sleep(0.5)
        machine.reset()
        
    def update_information(self):
        self.set_temperature()
        self.set_rtc_state()
    
    def led_set_high(self):
        LOG.logger.info("Enabling onboard led.")
        pico_led.on()
        self.states[Device.LED_NAME] = Device.LED_ENABLE_TEXT
    
    def led_set_low(self):
        LOG.logger.info("Disabling onboard led.")
        pico_led.off()
        self.states[Device.LED_NAME] = Device.LED_DISABLE_TEXT
    
    def set_temperature(self):
        LOG.logger.info("Setting the temperature state.")
        self.states[Device.TEMP_NAME] = pico_temp_sensor.temp
    
    def set_rtc_state(self):
        LOG.logger.info("Setting the RTC time into state.")
        self.states[Device.RTC_NAME] = self.rtc.datetime()