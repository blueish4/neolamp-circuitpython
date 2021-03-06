import board
import neopixel
import busio
import adafruit_ds3231
import digitalio
import time
import state
import random
import colour
pixel_count = 120
pixels = neopixel.NeoPixel(board.D5, pixel_count, brightness=1, auto_write=False)
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

def mktime(hour, minute, next_day=False):
    return time.struct_time((0, 0, (1 if next_day else 0), hour, minute, 0, 0, 0, 0))

light_on = True
midnight = mktime(0,  0, True)
sleep    = mktime(2,  0, True)
morning  = mktime(7, 30)
day      = mktime(9,  0)
evening  = mktime(18, 0)
night    = mktime(22, 0)
morning_state = state.State(morning,  day,      0x661100, 0xff6600, "morning")
day_state     = state.State(day,      evening,  0x404040, 0x404040, "day")
evening_state = state.State(evening,  night,    0x404040, 0x661100, "evening")
night_state   = state.State(night,    midnight, 0x600066, 0xff0000, "night")
late_night_state = state.State(midnight, sleep, 0xff0000, 0xff0000, "latenight")
sleep_state  = state.State(sleep,     morning,  0x000000, 0x000000, "BEDTIME")
current_state = morning_state
current_state.next_state = morning_state
morning_state.next_state = day_state
day_state.next_state     = evening_state
evening_state.next_state = night_state
night_state.next_state   = late_night_state
late_night_state.next_state = sleep_state
sleep_state.next_state   = morning_state

current_state.enter(light_on)
while True:
    t = mktime(*ds3231.datetime[3:5], next_day=ds3231.datetime[3] < 2)
    if current_state.is_valid(t):
        if light_on:
            # Needs more gay
            flag = colour.int_scale_flag("trans", pixel_count)
            for i in range(pixel_count):
                #col = colour.mod_brightness(current_state.display(t), random.uniform(0.8, 1.2))
                #pixels[i] = col
                pixels[i] = colour.mod_brightness(flag[i], 0.5)
            time.sleep(1)
            pixels.show()
    else:
        current_state = current_state.next_state

    # Set light_on switch
    if (current_state.name == "morning"):
        light_on = True
    current_state.enter(light_on)

