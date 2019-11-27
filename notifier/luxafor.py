from contextlib import suppress
import usb.core, usb.util, asyncio, sys

device = None
color_list = []

def enable():
    global device
    # We first start by testing if the system is running on windows.
    # Windows is not supported and will probaby break the program
    if sys.platform == "win32":
        print('Windows is not supported please run this on Linux')
        sys.exit(1)

    # Looks like we are running in Linux
    # First we look the our Luxafor device
    device = usb.core.find(idVendor=0x04d8, idProduct=0xf372)

    # Now we check if the Luxafor actually exists
    # We need the Luxafor for our project so we kill the program when it's not found.
    if device is None:
        print('the Luxafor is not found')
        sys.exit(1)

     # Linux kernel sets up a device driver for USB device, which you have to detach.
    # Otherwise trying to interact with the device gives a 'Resource Busy' error.  
    with suppress(Exception):
        device.detach_kernel_driver(0)
        print('test')

    # Setup default configuration for the Luxafor
    device.set_configuration()

    # Turn the Luxafor off by resetting it's colour
    set_solid_color()

def set_solid_color(red=0 ,green=0, blue=0,led=255):
    # 1st: 1 for solid colour
    # 2nd: 1-6 for specific LED, 65 for front, 66 for back, 0 for all, 255 for all one color
    # 3rd: for red (0-255)
    # 4th: for green (0-255)
    # 5th: for blue (0-255)
    device.write(1 ,[1,led,red,green,blue])

def set_fade_color(red , green, blue,led=255,duration=80):
    # 1st: 2 for a beautiful fade effect
    # 2nd: 1-6 for specific LED, 65 for front, 66 for back, 0 for all, 255 for all one color
    # 3rd: for red (0-255)
    # 4th: for green (0-255)
    # 5th: for blue (0-255)
    # 6th: for duration
    device.write(1 ,[2, led, red, green, blue, duration])

def add_color(red,green,blue):
    # This is where we add colors we want to display
    # We first create an object where the colors are stored
    color_object = [red, green, blue]

    # Then we check if this object is found in our list with colours. We don't copies of colours in here so we cancel the appending process
    if color_list in color_list:
        return

    # Now we add the color
    color_list.append(color_object)

def remove_color(red,green,blue):
    # This is where we delete colors we don't want to see anymore
    # First we create a color object
    color_object = [red, green, blue]

    # Only try to delete it when it is actually in the list
    if color_object in color_list:
        color_list.remove(color_object)

async def loop():
    # Here we loop through all the colors and display them one by one
    # Create a variable for the index and one to make the Luxafor dark again
    index = 0
    reset_color = False

    # Create an infinite loop and a timeout so it won't update too fast
    while True:
        await asyncio.sleep(2.5)

        # First check if the index isn't too high of a number
        if index >= len(color_list):
            index = 0

        # Make the Luxafor dark when there are no colors to display
        if not color_list:
            set_fade_color(0,0,0)
            continue

        if reset_color:
            # Reset the color when the reset option is enabled
            # After that we disable the reset option and add +1 to our index
            set_fade_color(0,0,0)
            turn_off = False
            index+=1

        else:
            # Enable reset to create a good looking fade for the Luxafor
            # Also set the color based in the index
            reset_color = True
            set_fade_color(*color_list[index])

