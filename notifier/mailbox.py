"""Module to access the E-Mail box & check for new E-Mails.

Contributors: Arjan de Haan (Vepnar)
Last edited: 3/12/2019 (dd/mm/yyyy)
"""

import imaplib
import asyncio
from . import configuration


class EmailBox:
    """Access the E-Mail box and processes the read E-Mails"""

    def __init__(self, luxafor, config):
        """Connect to the E-Mail server and set some default settings"""

        server = config.get('SMTP CREDENTIALS', 'server')
        port = config.getint('SMTP CREDENTIALS', 'port')
        username = config.get('SMTP CREDENTIALS', 'email')
        password = config.get('SMTP CREDENTIALS', 'password')
        self.interval = config.getint('SMTP CREDENTIALS', 'interval')
        self.actions = configuration.get_enabled_actions(config)
        self.luxafor = luxafor

        # Connect to the E-Mail box
        self.mail_box = imaplib.IMAP4_SSL(server, port)
        self.mail_box.login(username, password)
        self.mail_box.select('inbox')

    async def loop(self):
        """Loop through all actions check, and update the Luxafor when there are new messages"""

        while True:
            await asyncio.sleep(self.interval)

            for action in self.actions:
                if self.check_emails(action['address']):
                    # Convert color strings to integers
                    colors = [int(action['red']), int(action['green']), int(action['blue'])]
                    self.luxafor.add_color(*colors)

    def check_emails(self, address):
        """Look in the E-Mail box if the selected address is found

        Send a request to the E-Mail box to look for the addresses.
        After that's done we deleted the found E-Mail to keep our E-Mail box clean.

        Args:
            address: Email address we should look for

        Return:
            return True when the E-Mail is found and False if it is not.
        """

        self.mail_box.recent()
        _, mail_ids = self.mail_box.search(None, f'(FROM {address})')
        
        if mail_ids[0]:
            for num in mail_ids[0].split():
                self.mail_box.store(num, '+FLAGS', r'(\Deleted)')
                print(num)
            self.mail_box.expunge()
            return True
        return False
