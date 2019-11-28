#!/usr/bin/python3.7
"""You probably understand what this does

Contributors: Arjan de Haan (Vepnar)
Last edited: 28/10/2019 (dd/mm/yyyy)
"""
import asyncio
from notifier import configuration, luxafor, mailbox

def main():
    """ First load the modules and after that we need to startthe asynchronous loop"""

    print('Loading... ')
    config = configuration.get_config()
    device = luxafor.Luxafor()
    email_box = mailbox.EmailBox(device, config)
    async_loop = asyncio.get_event_loop()

    print('Running')
    asyncio.ensure_future(device.loop(), loop=async_loop)
    async_loop.run_until_complete(email_box.loop())

if __name__ == '__main__':
    main()
