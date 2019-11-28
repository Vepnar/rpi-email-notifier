"""Module to access the Luxafor

Contributors: Arjan de Haan (Vepnar)
Last edited: 28/10/2019 (dd/mm/yyyy)
"""
from contextlib import suppress
import sys
import asyncio
import usb.core
import usb.util

class Luxafor:
    """Class to access and use the Luxafor easily with simple commands"""

    def __init__(self):
        """Test requirements for the Luxafor, and exit requirements are not met.

        First the operation system is tested.
        Then that we look for the device by their vendor id & product id.
        After that we take control of the device and turn it's lights off
        """

        if sys.platform == "win32":
            print('Windows is not supported please run this on Linux')
            sys.exit(1)

        # Look for the Luxafor
        self.device = usb.core.find(idVendor=0x04d8, idProduct=0xf372)
        if self.device is None:
            print('the Luxafor is not found')
            sys.exit(1)

        with suppress(Exception):
            self.device.detach_kernel_driver(0)
        self.device.set_configuration()

        # Reset the colors
        self.set_solid_color([0, 0, 0])
        self.color_list = []

    def set_solid_color(self, color, led=255):
        """Send RGB values in binary to the Luxafor, and set it in solid color mode.

        Args:
            color:
                red: brightness of the red led (0-255)
                green: brightness of the green led (0-255)
                blue: brightness of the blue led (0-255)
            led: 1-6 for specific LED, 65 for front, 66 for back, 0 for all, 255 for all one color

        Raw binary values:
            [
                Solid color (1),
                led (1-6, 66, 255),
                red (0-255),
                green (0-255),
                blue (0-255),
            ]
        """
        self.device.write(1, [1, led, color[0], color[1], color[1]])

    def set_fade_color(self, color, led=255, duration=80):
        """Send RGB values for the Luxafor, and set it in fade mode.

        Args:
            color & led: see set_solid_color docstring
            duration: time it will take to fade into the given color

        Raw binary values:
            [
                Solid color (1),
                led (1-6, 66, 255),
                red (0-255),
                green (0-255),
                blue (0-255),
                duraction (0-255),
            ]

        """
        self.device.write(1, [2, led, color[0], color[1], color[2], duration])

    def add_color(self, red, green, blue):
        '''Add colors to the display list

        This will add colors to the list we will loop through.
        Each variable should be a number between 0 and 255.
        0 is off and 255 is the brighest color it can be.

        Args:
            red: number for the color red between 0-255
            green: number for the color green between 0-255
            blue number for the color blue between 0-255

        Typical usage example:
            add_color(255, 0, 0) # to make everything red
            add_color(0, 255, 0) # Green
            add_color(0, 0, 255) # Blue
            add_color(255, 255, 255) # White
            add_color(255, 0, 255) # Magenta
        '''
        color_object = [red, green, blue]

        if color_object in self.color_list:
            return
        self.color_list.append(color_object)

    def remove_color(self, red, green, blue):
        """This will remove the color from the display list.

        See add_color for the description for this one.
        """
        color_object = [red, green, blue]
        # Only try to delete it when it is actually in the list
        if color_object in self.color_list:
            self.color_list.remove(color_object)

    async def loop(self):
        """Asynchronous loop between colours.

        This will fade between the colors added to the color_list.
        It will turn the Luxafor off when there are no colors found in the list
        Between each update it will wait 2.5 seconds
        """
        index = 0
        reset_color = False

        while True:
            await asyncio.sleep(2.5)

            if index >= len(self.color_list):
                index = 0

            if not self.color_list:
                self.set_fade_color([0, 0, 0])
                continue

            if reset_color:
                self.set_fade_color([0, 0, 0])
                reset_color = False
                index += 1

            else:
                reset_color = True
                self.set_fade_color(self.color_list[index])
