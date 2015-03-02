import ClassicLiquidCrystal
import RPi.GPIO as GPIO
import time

lcd = ClassicLiquidCrystal.ClassicLiquidCrystal()

partI = (
  3,
  3,
  3,
  3,
  3,
  3,
  3,
  3
)

partD = (
  31,
  31,
  3,
  3,
  3,
  3,
  31,
  31
)

partC = (
  31,
  31,
  24,
  24,
  24,
  24,
  31,
  31
)

partO = (
  31,
  31,
  27,
  27,
  27,
  27,
  31,
  31
)

partU = (
  27,
  27,
  27,
  27,
  27,
  27,
  31,
  31
)

partUf = (
  31,
  31,
  27,
  27,
  27,
  27,
  27,
  27
)

part4 = (
  24,
  24,
  24,
  24,
  24,
  24,
  31,
  31
)

numbers = ( (5, 4), (0, 0), (1, 2), (1, 1), (6, 0), (2, 1), (2, 3), (1, 0), (3, 3), (3, 1), (205, 205) )

def writeNum(col, num):
    lcd.setCursor(col, 0)
    lcd.write(numbers[num][0])
    lcd.setCursor(col, 1)
    lcd.write(numbers[num][1])

lcd.begin(32, 2)

lcd.createChar(0, partI)
lcd.createChar(1, partD)
lcd.createChar(2, partC)
lcd.createChar(3, partO)
lcd.createChar(4, partU)
lcd.createChar(5, partUf)
lcd.createChar(6, part4)

while True:
    tm = time.localtime()
    hr = tm[3]
    mn = tm[4]
    sc = tm[5]

    toWrite = ( int(hr / 10), hr % 10, 10, int(mn / 10), mn % 10, 10, int(sc / 10), sc % 10 )

    for i in range(8):
        writeNum(15 + i, toWrite[i])

    time.sleep(0.5)