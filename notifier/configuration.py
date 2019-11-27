import configparser
import os.path
import sys

DEFAULT_CONFIG = '''# Don't edit the default settings
[DEFAULT]
enabled     = False
address     = example@example.com
red         = 0
green       = 0
blue        = 0
gpiopin     = 17


[SMTP CREDENTIALS]
email       = example@gmail.com
password    = password1
server      = imap.gmail.com
port        = 993
interval    = 5

[EXAMPLECOMPANY]
enabled     = False
address     = example@example.com
red         = 255
green       = 0
blue        = 127
gpiopin     = 17
'''


def enable(path='config.cfg'):
    # First of we begin by checking if the configuration file exists.
    if not (os.path.exists(path) and os.path.isfile(path)):

        # Looks like it doesn't exist.
        # So we create new one with the default configuration settings
        with open(path, 'w') as f:
            f.write(DEFAULT_CONFIG)

        # Now we print a message to the user about what they should do
        print('Config file created please edit this file and restart the application')
        sys.exit(1)

    # Initialize the Configuration parser.
    # Then we try to read file given configuration file.
    config = configparser.ConfigParser()
    config.read(path)

    # Now we test if the required sections are there
    # After that we inform the user about the damaged configuration file.
    if not (config.has_section('SMTP CREDENTIALS') or config.has_section('DEFAULT')):
        print(
            f'Your configuration at `{path}` is missing settings. please edit this file and solve the problem`')
        sys.exit(1)

    # Now we check if there are some SMTP values missing
    # We end the process when there is anything missing
    if not check_email(config):
        print(
            f'There is information missing for the SMTP server. Please add these to your configuration file at "{path}""`')
        sys.exit(1)
    
    # Then we check if there are any enabled actions. because we got nothing to do when there are none enabled
    # Kill the process when there are no actions enabled
    if not check_enabled_actions(config):
        print('There are no enabled actions in the configuration file.')
        sys.exit(1)

def check_email(config):
    # Here we will check if all items required for the SMTP function are there.
    items = ['email', 'password', 'server', 'port', 'interval']

    # Now we loop trough them and return False when there is something missing,
    # and of course return True when nothing is missing.
    for item in items:
        if not config.has_option('SMTP CREDENTIALS', item):
            return False
    return True

def check_enabled_actions(config):
    # Receive all sections from the configuration file.
    sections = config.sections()

    # Delete the SMTP section from the list of options.
    del sections[0]
    
    # Loop through all remaining options to check if there is one enabled.
    # Return true when there is 1 enabled. return false when there are none enabled.
    for section in sections:
        if config.getboolean(section,'enabled'):
            return True
    return False

