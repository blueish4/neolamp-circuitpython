import board
import neopixel
import busio
import adafruit_ds3231
import digitalio
import time
import datetime
import state

pixels = neopixel.NeoPixel(board.D5, 118, brightness=1, auto_write=False)
i2c = None

while (i2c is None):
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
    except RuntimeError:
        print("Error starting clock")
        pixels.fill((0, 64, 0))
        time.sleep(1)
    
ds3231 = adafruit_ds3231.DS3231(i2c)


if False:   # change to True if you want to set the time!
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2018,  11,    8,   23,  18,   30,    4,   -1,    -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with
    print("Setting time to:", t)     # uncomment for debugging
    ds3231.datetime = t
    print()


light_on = True
silenced = False
midnight = datetime.Time(0,  0)
sleep    = datetime.Time(2,  0)
morning  = datetime.Time(7, 30)
day      = datetime.Time(9,  0)
evening  = datetime.Time(18, 0)
night    = datetime.Time(22, 0)
morning_state = state.State(morning,  day,      0x661100, 0xff6600, "morning")
day_state     = state.State(day,      evening,  0x404040, 0x404040, "day")
evening_state = state.State(evening,  night,    0x404040, 0x661100, "evening")
night_state   = state.State(night,    midnight, 0xff0000, 0xff0000, "night")
late_night_state = state.State(midnight, sleep, 0xff0000, 0xff0000, "latenight")
sleep_state  = state.State(sleep,     morning,  0x000000, 0x000000, "BEDTIME")
current_state = night_state
current_state.next_state = morning_state
morning_state.next_state = day_state
day_state.next_state     = evening_state
evening_state.next_state = night_state
night_state.next_state   = late_night_state
late_night_state.next_state = sleep_state
sleep_state.next_state   = morning_state

current_state.enter(light_on)
while True:
    t = ds3231.datetime
    if current_state.is_valid(t):
        if light_on:
            pixels.fill(current_state.display(t))
    else:
        current_state = current_state.next_state
        print(current_state.name)
    
    if t.tm_hour > 9:
        # reset silencing button
        silenced = False
    silenced = t.tm_wday in (0, 6)
    if (current_state.name == "morning") and not silenced:
        light_on = True
    current_state.enter(light_on)

    time.sleep(1)
    # Set silenced switch
    # Set light_on switch
    pixels.show()