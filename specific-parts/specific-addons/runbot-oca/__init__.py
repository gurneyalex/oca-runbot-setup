from openerp.addons.runbot import runbot as orig_runbot
from openerp.tools import config
import socket

def fqdn():
    return config.get('fqdn', socket.getfqdn())

orig_runbot.fqdn = fqdn

from . import runbot
