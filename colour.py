def mod_brightness(colour, modifier):
    red   = int(((colour & 0xff0000) >> 16) * modifier)
    green = int(((colour & 0x00ff00) >> 8)  * modifier)
    blue  = int((colour & 0x0000ff)         * modifier)
    return red << 16 | green << 8 | blue