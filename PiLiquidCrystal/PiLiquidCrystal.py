import time

class LiquidCrystal(object):
    # commands
    LCD_CLEARDISPLAY        = 0x01
    LCD_RETURNHOME          = 0x02
    LCD_ENTRYMODESET        = 0x04
    LCD_DISPLAYCONTROL      = 0x08
    LCD_CURSORSHIFT         = 0x10
    LCD_FUNCTIONSET         = 0x20
    LCD_SETCGRAMADDR        = 0x40
    LCD_SETDDRAMADDR        = 0x80

    # flags for display entry mode
    LCD_ENTRYRIGHT          = 0x00
    LCD_ENTRYLEFT           = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    # flags for display on/off control
    LCD_DISPLAYON           = 0x04
    LCD_DISPLAYOFF          = 0x00
    LCD_CURSORON            = 0x02
    LCD_CURSOROFF           = 0x00
    LCD_BLINKON             = 0x01
    LCD_BLINKOFF            = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE         = 0x08
    LCD_CURSORMOVE          = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE         = 0x08
    LCD_CURSORMOVE          = 0x00
    LCD_MOVERIGHT           = 0x04
    LCD_MOVELEFT            = 0x00

    # flags for function set
    LCD_8BITMODE            = 0x10
    LCD_4BITMODE            = 0x00
    LCD_2LINE               = 0x08
    LCD_1LINE               = 0x00
    LCD_5x10DOTS            = 0x04
    LCD_5x8DOTS             = 0x00

    def begin(self, cols, lines, dot_size = 0):
        if lines > 1:
            self.display_function |= self.LCD_2LINE
        self.lines_count = lines
        self.row_offsets = (0x00, 0x40, 0x00 + cols, 0x40 + cols)

        if (dot_size != self.LCD_5x8DOTS) and (lines == 1):
            self.display_function |= self.LCD_5x10DOTS

        self.sleep_us(50000)

        self.output(self.pin_rs, False)
        self.output(self.pin_e, False)

        if not (self.display_function & self.LCD_8BITMODE):
            self.write4bits(0x03)
            self.sleep_us(4500)
            self.write4bits(0x03)
            self.sleep_us(4500)
            self.write4bits(0x03)
            self.sleep_us(150)
            self.write4bits(0x02)
        else:
            self.command(self.LCD_FUNCTIONSET | self.display_function)
            self.sleep_us(4500)
            self.command(self.LCD_FUNCTIONSET | self.display_function)
            self.sleep_us(150)
            self.command(self.LCD_FUNCTIONSET | self.display_function)

        self.command(self.LCD_FUNCTIONSET | self.display_function)
        self.display_control = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF
        self.display()
        self.clear()
        self.display_mode = self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
        self.command(self.LCD_ENTRYMODESET | self.display_mode)

    # ---- User methods ---- #
    def display(self):
        self.control(self.LCD_DISPLAYON, True)

    def noDisplay(self):
        self.control(self.LCD_DISPLAYON, False)

    def cursor(self):
        self.control(self.LCD_CURSORON, True)

    def noCursor(self):
        self.control(self.LCD_CURSORON, False)

    def blink(self):
        self.control(self.LCD_BLINKON, True)

    def noBlink(self):
        self.control(self.LCD_BLINKON, False)

    def scrollDisplayLeft(self):
        self.command(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVELEFT)

    def scrollDisplayRight(self):
        self.command(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVERIGHT)

    def leftToRight(self):
        self.mode(self.LCD_ENTRYLEFT, True)

    def rightToLeft(self):
        self.mode(self.LCD_ENTRYLEFT, False)

    def autoscroll(self):
        self.mode(self.LCD_ENTRYSHIFTINCREMENT, True)

    def noAutoscroll(self):
        self.mode(self.LCD_ENTRYSHIFTINCREMENT, False)

    def clear(self):
        self.command(self.LCD_CLEARDISPLAY)
        self.sleep_us(2000)

    def home(self):
        self.command(self.LCD_RETURNHOME)
        self.sleep_us(2000)

    def setCursor(self, col, row):
        if row >= 4:
            row = 3
        if row >= self.lines_count:
            row = self.lines_count - 1

        self.command(self.LCD_SETDDRAMADDR | (col + self.row_offsets[row]))

    def createChar(self, location, charmap):
        location &= 0x7
        self.command(self.LCD_SETCGRAMADDR | (location << 3))
        for i in range(8):
            self.write(charmap[i])

    def message(self, text):
        for char in text:
            if char == '\n':
                self.send(0xC0, False)
            else:
                self.send(ord(char), True)

    # ---- Low-level methods ---- #
    def command(self, val):
        self.send(val, False)

    def write(self, val):
        self.send(val, True)

    def pulseEnable(self):
        raise NotImplementedError("Abstract class")

    def write4bits(self, val):
        raise NotImplementedError("Abstract class")
    
    def write8bits(self, val):
        raise NotImplementedError("Abstract class") 

    def output(self, pin, mode):
        raise NotImplementedError("Abstract class")

    def send(self, val, mode):
        self.output(self.pin_rs, mode)

        if self.display_function & self.LCD_8BITMODE:
            self.write8bits(val)
        else:
            self.write4bits(val >> 4)
            self.write4bits(val)

    # ---- Other methods ---- #
    def sleep_us(self, microseconds):
        time.sleep(microseconds / float(1000000))

    def control(self, control_flag, state):
        if state:
            self.display_control |= control_flag
        else:
            self.display_control &= ~control_flag

        self.command(self.LCD_DISPLAYCONTROL | self.display_control)

    def mode(self, mode_flag, state):
        if state:
            self.display_mode |= mode_flag
        else:
            self.display_mode &= ~mode_flag

        self.command(self.LCD_ENTRYMODESET | self.display_mode)
