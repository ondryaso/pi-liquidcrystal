import PiLiquidCrystal
import RPi.GPIO as GPIO

lcd = PiLiquidCrystal.LiquidCrystal()

trueChar = (
  0,
  1,
  1,
  2,
  2,
  20,
  20,
  8
)

falseChar = (
  0,
  17,
  10,
  4,
  4,
  10,
  17,
  0
)

lcd.begin(32, 2)

lcd.createChar(3, trueChar)
lcd.createChar(4, falseChar)

lcd.setCursor(0, 0)
lcd.message("This sentence is ")
lcd.write(4)
lcd.message("! TTT \n")
lcd.setCursor(0, 1)
lcd.message("Uh... ")
lcd.write(3)
lcd.message(". I'll go \"")
lcd.write(3)
lcd.message("\". Huh, that was easy")

GPIO.cleanup()