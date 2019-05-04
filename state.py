class State(object):
    next_state = None
    colour = 0x000000
    light_on = True
    def __init__(self, start, end, start_col, end_col, name):
        self.start = start
        self.end = end
        self.start_col = start_col
        self.end_col = end_col
        self.name = name

    """
    Returns true if time t is valid for state
    """
    def is_valid(self, t):
        return self.end.time_cmp(t) == -1 and not self.start.time_cmp(t) == -1
    
    def next_state(self):
        return self.child_state

    def enter(self, light_on):
        self.light_on = light_on
        
    def display(self, t):
        if self.light_on:
            return self.start_col
        else:
            return 0x000000
        # work out ratio and write to LEDs