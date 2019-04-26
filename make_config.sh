#! /bin/bash
source sandbox/bin/activate
./parts/server/odoo.py -c runbot.cfg --save -d runbot --addons-path=parts/server/addons,parts/server/openerp/addons,parts/odoo-extra,parts/runbot-addons,parts/server-tools,parts/website,specific-parts/specific-addons --db-filter=runbot$ --stop-after-init
