import odoo.addons.runbot.common as orig_runbot_common
import odoo.addons.runbot.models.repo as orig_runbot_repo
import odoo.addons.runbot.models.build as orig_runbot_build
from odoo.tools import config
import socket

def fqdn():
    return config.get('fqdn', socket.getfqdn())

orig_runbot_common.fqdn = fqdn

orig_runbot_models_repo.fqdn = fqdn
orig_runbot_models_build.fqdn = fqdn

from . import runbot
