#!/usr/bin/python3.7
"""You probably understand what this does

Contributors: Arjan de Haan (Vepnar)
Last edited: 2/12/2019 (dd/mm/yyyy)
"""
import asyncio
from notifier import configuration, luxafor, mailbox, pitft

def main():
    """ First load the modules and after that we need to startthe asynchronous loop"""

    print('Loading... ')
    config = configuration.get_config()
    device = luxafor.Luxafor()
    email_box = mailbox.EmailBox(device, config)
    tft = pitft.PiTFT(config,device)
    async_loop = asyncio.get_event_loop()

    print('Running')
    asyncio.ensure_future(device.loop(), loop=async_loop)
    asyncio.ensure_future(tft.gpio_loop(),loop=async_loop)
    async_loop.run_until_complete(email_box.loop())

if __name__ == '__main__':
    main()
