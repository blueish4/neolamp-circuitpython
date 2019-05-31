def mod_brightness(colour, modifier):
    red   = min(int(((colour & 0xff0000) >> 16) * modifier), 0xff)
    green = min(int(((colour & 0x00ff00) >> 8)  * modifier), 0xff)
    blue  = min(int((colour & 0x0000ff)         * modifier), 0xff)
    return red << 16 | green << 8 | blue

def int_scale_flag(flag_name, max_size):
    flag = bmp_data(flag_name)
    scale_factor = max_size // len(flag)
    output = []
    for colour in flag:
        output.extend([colour]*scale_factor)
    output.extend([0]*(max_size-len(output)))
    return output

def bmp_data(flag_name):
    with open('flags/' + flag_name + '.bmp', 'rb') as flag:
        # http://www.ue.eti.pg.gda.pl/fpgalab/zadania.spartan3/zad_vga_struktura_pliku_bmp_en.html
        flag.read(0x36) # skip header info
        raster_data = flag.read()
        # There is probably a way to make this all comprehensions, but meh
        col_bytes = [int(raster_data[len(raster_data)-x-1]) for x in range(len(raster_data)) if x%4 != 0]
        colours = []
        for pack in range(0,len(col_bytes),3):
            colours.append((col_bytes[pack]<<16)+(col_bytes[pack+1]<<8)+col_bytes[pack+2])
        return colours