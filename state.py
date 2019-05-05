import time
class State(object):
    next_state = None
    colour = 0x000000
    light_on = True
    def __init__(self, start, next_s, start_col, end_col, name):
        self.start = start
        self.next_state = next_s
        self.start_col = start_col
        self.end_col = end_col
        self.name = name

    """
    Returns true if time t is valid for state
    """
    def is_valid(self, t):
        if self.next_state.start.tm_mday == 0 and self.start.tm_mday == 1:
            b_time = time.struct_time((0, 0, 0, self.start.tm_hour, self.start.tm_min, 0, 1, -1, -1))
        else:
            b_time = self.start
        return self.next_state.start > t and not b_time > t

    def enter(self, light_on):
        self.light_on = light_on
        
    def display(self, t):
        if self.light_on:
            return self.start_col
        else:
            return 0x000000
        # work out ratio and write to LEDs 