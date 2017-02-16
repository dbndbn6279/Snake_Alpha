from tkFont import *
class StyleManager:
    def __init__(self):
        #Main Manu:
        self.headFont = Font(size = 20, weight = 'bold')
        self.hintFont = Font(size = 12, weight = 'normal')
        #Game Manu:
        self.scoreFont = Font(size = 12, weight = 'bold')
        self.getScoreFont = Font(size = 16, weight = 'bold')
        #Game Color:
        self.initSnakeColor = '#328CFF'  #DarkBlue

    def DimColor(self, color):
        #Convert Color to RGB
        red = int('0x' + color[1:3], 16)
        green = int('0x' + color[3:5], 16)
        blue = int('0x' + color[5:7], 16)
        #Do Dimming:
        if green < 255:
            green += 3
            if green > 255:
                green = 255
        elif blue > 100:
            blue -= 3
            if blue < 100:
                blue = 100
        elif red < 255:
            red += 3
            if red > 255:
                red = 255
        elif green > 150:
            green -= 3
            if  green < 150:
                green = 150
        #Convert RGB back to Color:
        return '#' + hex(red)[2:4] + hex(green)[2:4] + hex(blue)[2:4]
