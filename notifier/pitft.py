"""Module to read inputs from the GPIO pins and draw on the tft display

Contributors: Arjan de Haan (Vepnar)
Last edited: 4/12/2019 (dd/mm/yyyy)
"""

import asyncio
import pygame  # pylint: disable=E0401
from gpiozero import Button  # pylint: disable=E0401
from . import configuration

DISPLAY_SIZE = (320, 240)


class PiTFT:
    """Module to render images and handle button presses"""

    def __init__(self, config, luxafor):
        self.luxafor = luxafor
        options = configuration.get_enabled_actions(config)
        self.actions = []
        for option in options:
            action = {
                'pin': option['gpiopin'],
                'gpio': Button(option['gpiopin']),
                'color': [int(option['red']),
                          int(option['green']),
                          int(option['blue'])
                          ],
                'name': option['name']
            }
            self.actions.append(action)

            # Display init
            pygame.init()
            pygame.font.init()
            self.lcd = pygame.Surface(DISPLAY_SIZE)
            self.font = pygame.font.SysFont(None, 30)
            self.create_display()

    async def gpio_loop(self):
        """Loop through all enabled gpio pins and check if the buttons are pressed"""
        while True:
            await asyncio.sleep(0.2)
            for action in self.actions:
                if action['gpio'].is_pressed:
                    self.luxafor.remove_color(*action['color'])

    def draw_buffer(self):
        """Access the frame made in pygame and write it to the display"""
        framebuffer = open('/dev/fb1', 'wb')
        framebuffer.write(self.lcd.convert(16, 0).get_buffer())
        framebuffer.close()

    def create_display(self):
        """Create a responsive display based on the information stored in config"""
        self.lcd.fill((0, 0, 0))
        amount_actions = len(self.actions)
        current_action = 0
        height_available = DISPLAY_SIZE[1] / amount_actions
        for action in self.actions:
            # Draw the background box
            startx = height_available * current_action
            endx = height_available * (current_action+1)
            pygame.draw.rect(
                self.lcd, action['color'], (0, startx, DISPLAY_SIZE[0], endx))
            # Draw the text title of the mail
            display_string = '[{}] {}'.format(action['pin'], action['name'])
            _, font_height = self.font.size(display_string)
            start_font = (startx + endx) / 2 - font_height / 2
            text = self.font.render(display_string, False, (255, 255, 255))
            self.lcd.blit(text, (10, start_font))
            current_action += 1
        self.draw_buffer()
