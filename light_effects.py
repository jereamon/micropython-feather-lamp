import machine, neopixel
from time import sleep
from utime import ticks_ms

led_strip = neopixel.NeoPixel(machine.Pin(4), 17)
led_strip_2 = neopixel.NeoPixel(machine.Pin(2), 17)

color_arr = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]

"Corrects rgb led gamma"
NUMS = [
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
    10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
    17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
    25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
    37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
    51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
    69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
    90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
    115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
    144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
    177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
    215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255
    ]

# class LightEffectBase:
#     def __init__(self, led_strips):
#         self.led_strips = led_strips


class SideToSide:
    def __init__(self, led_strips):
        self.tracker = 0
        self.tracker_add_sub = 1
        self.led_strips = led_strips
        self.current_strip = False
        self.color = [0, 170, 170]

        self.fade_speed = 0.2

        self.led_numbers = (
            (16,),
            (15, 14, 13, 12, 11, 10, 9, 8),
            (7, 6, 5, 4, 3, 2, 1, 0)
        )

    def all_off(self):
        for strip in self.led_strips:
            strip.fill([0, 0, 0])
            strip.write()

    def cycle_lights(self):
        self.all_off()

        for num in self.led_numbers[self.tracker]:
            self.led_strips[self.current_strip][num] = self.color
        self.led_strips[self.current_strip].write()
        sleep(self.fade_speed)

        if self.tracker + self.tracker_add_sub > 2:
                self.current_strip = not self.current_strip
                self.tracker_add_sub *= -1
        else:
            if self.tracker + self.tracker_add_sub < 0:
                self.tracker_add_sub *= -1

            self.tracker += self.tracker_add_sub


# class Spiral:
#     def __init__(self, led_strips):
#         self.led_tracker = 16
#         self.led_add_sub = -1
#         self.current_strip = False
#         self.led_strips = led_strips

#         self.color = [NUMS[0], NUMS[100], NUMS[100]]
#         self.fade_speed = .001

#     def all_off(self):
#         for led_strip in self.led_strips:
#             led_strip.fill([0, 0, 0])
#             led_strip.write()

#     def cycle_lights(self):
#         self.all_off()
#         self.led_strips[self.current_strip][self.led_tracker] = self.color
#         self.led_strips[self.current_strip].write()
#         sleep(self.fade_speed)

#         if self.led_tracker + self.led_add_sub > 16:
#             self.led_add_sub *= -1
#         else:
#             if self.led_tracker + self.led_add_sub < 0:
#                 self.current_strip = not self.current_strip
#                 self.led_add_sub *= -1
#             self.led_tracker += self.led_add_sub


class FadeInHalf:
    def __init__(self, led_strips, colors):
        self.led_strips = led_strips

        self.incremental_colors = []
        self.set_incremental_colors(colors)
        
    def set_incremental_colors(self, colors):
        self.incremental_colors = [[] for i in range(6)]
        if len(colors) < 2:
            self.incremental_colors = [[NUMS[colors[0][0]], NUMS[colors[0][1]], NUMS[colors[0][2]]]]
        elif len(colors) > 1:
            self.incremental_colors[0] = colors[0]
            self.incremental_colors[5] = colors[1]
            for i in range(1, 5):
                for j in range(3):
                    cur_inc_color = NUMS[colors[0][j] + (((colors[1][j] - colors[0][j]) // 6) * i)]
                    self.incremental_colors[i].append(cur_inc_color)

    def cycle_lights(self):
        led_nums = [
            [16,],
            [15, 14, 13, 12, 11, 10, 9, 8],
            [7, 6, 5, 4, 3, 2, 1, 0]
        ]
        temp_inc = 0
        strip_selector = False

        for i in range(6):
            if i == 3:
                strip_selector = not strip_selector
            if i > 2:
                temp_inc = (i - 5) * -1
            else:
                temp_inc = i

            for led_num in led_nums[temp_inc]:
                self.led_strips[strip_selector][led_num] = self.incremental_colors[i]
            self.led_strips[strip_selector].write()


class FadeAlong:
    def __init__(self, colors):
        self.led_strips = [led_strip, led_strip_2]
        if len(colors) < 2:
            self.colors = [colors[0], colors[0]]
        elif len(colors) > 34:
            self.colors = colors[:33]
        else:
            self.colors = colors

        self.incremental_colors = [[] for i in range(34)]
        self.set_incremental_colors(self.colors)

        self.cycle_increment = 0

    def set_incremental_colors(self, colors):
        self.incremental_colors = [[] for i in range(34)]
        self.incremental_colors[0] = colors[0]
        self.incremental_colors[33] = colors[-1]

        color_increment = 0
        multiplier_reset = 0
        fade_distance = 34 // (len(colors) - 1)

        for i in range(1, 33):
            if i > (34 // ((len(colors) - 1)) * (color_increment + 1)) and color_increment + 1 < len(colors) - 1:
                # print("\nincrementing color_increment")
                color_increment += 1
                # print("color_increment now = {}".format(color_increment))
                multiplier_reset = (34 // (len(colors) - 1)) * color_increment
                # print("multiplier_reset = {}\n".format(multiplier_reset))
            for j in range(3):
                color_difference = (colors[color_increment + 1][j] - colors[color_increment][j]) / fade_distance
                new_color = NUMS[round(colors[color_increment][j] + (color_difference * (i - multiplier_reset)))]

                # cur_inc_color = NUMS[colors[color_increment][j] + (((colors[color_increment + 1][j] - colors[color_increment][j]) // 34) * i)]
                # self.incremental_colors[i].append(cur_inc_color)
                self.incremental_colors[i].append(new_color)

        # print("\n\nincremental_colors: {}\n\n".format(self.incremental_colors))

    def cycle_lights(self, light_offset=0):
        light_offset = light_offset % 34
        for i in range(34):
            if light_offset + i > 33:
                # print("\nlight_offset > 33")
                if i <= 16:
                    cur_led = abs(i - 16)
                    self.led_strips[0][cur_led] = self.incremental_colors[(light_offset + i) - 34]
                else:
                    self.led_strips[1][i - 17] = self.incremental_colors[(light_offset + i) - 34]
            else:
                # print("\nlight_offset < 33")
                if i <= 16:
                    cur_led = abs(i - 16)
                    self.led_strips[0][cur_led] = self.incremental_colors[light_offset + i]
                    # print("strip 0")
                    # print("i = {}, cur_led = {}, incremental_color = {}\n".format(i, cur_led, self.incremental_colors[light_offset]))
                else:
                    self.led_strips[1][i - 17] = self.incremental_colors[light_offset + i]
                    # print("strip 1")
                    # print("i = {}, cur_led = {}, incremental_color = {}\n".format(i, i - 17, self.incremental_colors[light_offset]))

        for strip in self.led_strips:
            strip.write()


class FadeComplete:
    def __init__(self):
        pass