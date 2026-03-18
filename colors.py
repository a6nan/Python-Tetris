class Colors:
    darkGrey = (26,31,40)
    green = (47,230,23)
    red = (255,0,0)
    orange = (226,116,17)
    yellow = (237,234,4)
    purple = (166,0,247)
    cyan = (21,204,209)
    blue = (13,64,216)
    darkBlue = (44,44,127)
    lightBlue = (59,85,162)
    white = (255,255,255)

    @classmethod
    def get_cell_colors(cls):
        return [cls.darkGrey, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue]
