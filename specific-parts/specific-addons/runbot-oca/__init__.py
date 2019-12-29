from odoo.addons.runbot import common as orig_runbot
from odoo.tools import config
import socket

def fqdn():
    return config.get('fqdn', socket.getfqdn())

orig_runbot.fqdn = fqdn

from . import runbot
