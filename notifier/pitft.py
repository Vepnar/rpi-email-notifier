"""Module to read inputs from the GPIO pins and draw on the tft display

Contributors: Arjan de Haan (Vepnar)
Last edited: 2/12/2019 (dd/mm/yyyy)
"""

import asyncio
from gpiozero import Button #pylint: disable=E0401
from . import configuration



class PiTFT: 
    """Module to render images and handle button presses"""

    def __init__(self, config, luxafor):
        self.luxafor = luxafor
        options = configuration.get_enabled_actions(config)
        self.actions = []
        for option in options:
            action = {
                'gpio': Button(option['gpiopin']),
                'color': [int(option['red']),
                          int(option['green']),
                          int(option['blue'])
                          ]
            }
            self.actions.append(action)

    async def gpio_loop(self):
        """Loop through all enabled gpio pins and check if the buttons are pressed"""
        while True:
            await asyncio.sleep(0.2)
            for action in self.actions:
                if action['gpio'].is_pressed:
                    self.luxafor.remove_color(*action['color'])
