# Neolamp

This is a project that may have experienced a *bit* of scope creep but that's OK.
It's designed to help me wake up and go to sleep in a more consistent manner,
since sunlight is a bit ... occasional where I live.

## Design

I use an [Adafruit ItsyBitsy M0 Express](https://www.adafruit.com/product/3727)
and a [DS3231](https://www.adafruit.com/product/3013) to keep time between resets.
The Itsy has a 5v logic pin on pin 5, so that controls the neopixels. The DS3231
is an I2C device so that plugs in to the SCL and SDA pins.

The time transitions are handled by a state machine model. Each time state had a
next state and a colour, which can all be tweaked in the main script. The strip
will twinkle a little bit too, and the default times might be a little indicative
of my poor sleep schedule. Even if the light is set to off it will turn on in the
morning.

## Possible improvements

* A button to switch the lights on and off
* ESP32 bluetooth/wifi connectivity
