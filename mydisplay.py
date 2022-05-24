import board, displayio, digitalio, busio, time, pwmio
from st7735r import ST7735R


global display
lcd_dc = board.GP8
lcd_cs = board.GP9
lcd_clk = board.GP10
lcd_din = board.GP11
lcd_rst = board.GP12
#lcd_bl = board.GP25

displayio.release_displays()
lcd_spi = busio.SPI(clock=lcd_clk, MOSI=lcd_din)
lcd_bus = displayio.FourWire(lcd_spi, command=lcd_dc, chip_select=lcd_cs, reset=lcd_rst)
brightness = pwmio.PWMOut(board.LED)
brightness.duty_cycle = int(65535*0.3)
display = ST7735R(lcd_bus, width=160, height=80, invert=True, colstart=26, rowstart=1, rotation=90)#, backlight_pin=lcd_bl, auto_brightness=False, brightness=0.1)

def hcenter(target, container):
    target.x = container.width/2 - target.width/2

