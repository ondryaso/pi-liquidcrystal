import PiLiquidCrystal
import RPi.GPIO as GPIO

class ClassicLiquidCrystal(PiLiquidCrystal.LiquidCrystal):
    # ---- Init methods ---- #
    def __init__(self, pin_rs=26, pin_e=11, pins_db=[15, 13, 16, 12], GPIO_mode = GPIO.BOARD):
        GPIO.setmode(GPIO_mode)
        self.initFirst(pin_rs, pin_e)

        if len(pins_db) == 4:
            self.init4bit(pins_db[0], pins_db[1], pins_db[2], pins_db[3])
        else:
            self.init8bit(pins_db[0], pins_db[1], pins_db[2], pins_db[3], pins_db[4], pins_db[5], pins_db[6], pins_db[7])

        for i in range(8):
            if self.data_pins[i] != 0:
                GPIO.setup(self.data_pins[i], GPIO.OUT)

    def initFirst(self, pin_rs, pin_e):
        self.pin_rs = pin_rs
        self.pin_e = pin_e
        
        GPIO.setup(pin_rs, GPIO.OUT)
        GPIO.setup(pin_e, GPIO.OUT)

    def init4bit(self, pin_d4, pin_d5, pin_d6, pin_d7):
        self.data_pins = [pin_d4, pin_d5, pin_d6, pin_d7, 0, 0, 0, 0]
        self.display_function = self.LCD_4BITMODE | self.LCD_1LINE | self.LCD_5x8DOTS


    def init8bit(self, pin_d0, pin_d1, pin_d2, pin_d3, pin_d4, pin_d5, pin_d6, pin_d7):
        self.data_pins = [pin_d0, pin_d1, pin_d2, pin_d3, pin_d4, pin_d5, pin_d6, pin_d7]
        self.display_function = self.LCD_8BITMODE | self.LCD_1LINE | self.LCD_5x8DOTS

    def pulseEnable(self):
        GPIO.output(self.pin_e, False)
        self.sleep_us(1)
        GPIO.output(self.pin_e, True)
        self.sleep_us(1)
        GPIO.output(self.pin_e, False)
        self.sleep_us(100)

    def write4bits(self, val):
        for i in range(4):
            GPIO.output(self.data_pins[i], (val >> i) & 0x01)

        self.pulseEnable()

    def write8bits(self, val):
        for i in range(8):
            GPIO.output(self.data_pins[i], (val >> i) & 0x01)

        self.pulseEnable()

    def output(self, pin, mode):
        GPIO.output(pin, mode)