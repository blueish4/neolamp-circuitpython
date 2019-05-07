def mod_brightness(colour, modifier):
    red   = min(int(((colour & 0xff0000) >> 16) * modifier), 0xff)
    green = min(int(((colour & 0x00ff00) >> 8)  * modifier), 0xff)
    blue  = min(int((colour & 0x0000ff)     * modifier), 0xff)
    return red << 16 | green << 8 | blue