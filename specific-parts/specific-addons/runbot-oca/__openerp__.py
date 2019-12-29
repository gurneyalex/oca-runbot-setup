# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    This module copyright (C) 2015 Camptocamp
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Runbot OCA',
    'category': 'Website',
    'summary': 'OCA specific customizations',
    'version': '1.0',
    'description': """
Runbot OCA Customizations
=========================

* fix nginx config to match OCA setup


Contributors
------------

Alexandre Fayolle <alexandre.fayolle@camptocamp.com>

""",
    'author': "Odoo Community Association (OCA)",
    'depends': ['runbot'],
    'data': [
        'runbot_qweb.xml',
        'runbot_repo.xml'
    ],
    'installable': True,
}
