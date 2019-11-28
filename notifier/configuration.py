"""Configuration builder/reader for the rpi-email-notifier

Contributors: Arjan de Haan (Vepnar)
Last edited: 28/10/2019 (dd/mm/yyyy)

"""
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
    """Load the configuration file and check if there is information missing.

    Checks if there is a configuration file and create one if it doesn't exist.
    After that will check if the required items exist in the configuration file.

    Args:
        path: location where the configuration file should be

    Raises:
        Closes application when something is wrong
    """

    if not (os.path.exists(path) and os.path.isfile(path)): # Create config if doesn't exist
        with open(path, 'w') as config_file:
            config_file.write(DEFAULT_CONFIG)

        print('Config file created please edit this file and restart the application')
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(path) # Parse configuration file

    # Checks if required sections exist
    if not (config.has_section('SMTP CREDENTIALS') or config.has_section('DEFAULT')):
        print(f'Your configuration at {path} is missing settings. '
              'please edit this file and solve the problem')
        sys.exit(1)

    # Check if required E-Mail settings exist
    if not check_email_requirements(config):
        print('There is information missing for the SMTP server.'
              f'Please add these to your configuration file at "{path}""')
        sys.exit(1)

    # Check if there are actions are enabled
    if not check_enabled_actions(config):
        print('There are no enabled actions in the configuration file.')
        sys.exit(1)

def check_email_requirements(config):
    """Checks if all required options for the IMAP protocol exist in the configuration file.

    Args:
        config: Configuration file

    Returns:
        True when there is no information missing and false when there is.
    """
    items = ['email', 'password', 'server', 'port', 'interval']

    for item in items:
        if not config.has_option('SMTP CREDENTIALS', item):
            return False
    return True

def check_enabled_actions(config):
    """Check if there is one action enabled in the configuration file.

    Args:
        config: Configuration file

    Returns:
        True when there is atleast one action enabled
    """
    sections = config.sections()

    # Delete the SMTP section from the sections.
    del sections[0]

    for section in sections:
        if config.getboolean(section, 'enabled'):
            return True
    return False
