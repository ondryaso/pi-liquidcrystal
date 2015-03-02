import ClassicLiquidCrystal
import RPi.GPIO as GPIO
import time

lcd = ClassicLiquidCrystal.ClassicLiquidCrystal()
lcd.begin(40, 2)

for i in range(256):
    if (i % 40) == 0:
        lcd.setCursor(0, 1)

    if (i % 80) == 0:
        lcd.clear()
        lcd.setCursor(0, 0)

    lcd.write(i)
    time.sleep(0.5)

GPIO.cleanup()