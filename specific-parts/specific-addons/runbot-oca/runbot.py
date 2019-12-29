import os
import os.path as osp
import logging
import re
import subprocess

from odoo import models, fields
from odoo.tools import config
from odoo.modules.module import get_module_resource

from odoo.addons.runbot.common import fqdn
_logger = logging.getLogger(__name__)


class RunbotRepo(models.Model):
    _inherit = "runbot.repo"

    active = fields.Boolean(default=True)

    def _reload_nginx(self):
        """
        completely override the method
        """
        settings = {}
        settings['port'] = config['http_port']
        settings['runbot_static'] = os.path.join(
            get_module_resource('runbot', 'static'), ''
        )
        nginx_dir = os.path.join(self._root(), 'nginx')
        settings['nginx_dir'] = nginx_dir
        settings['re_escape'] = re.escape
        settings['fqdn'] = fqdn()
        nginx_repos = self.search([('nginx', '=', True)], order='id')
        if nginx_repos:
            builds = self.env['runbot.build'].search(
                [
                    ('repo_id', 'in', nginx_repos.ids),
                    ('state', '=', 'running'),
                    ('host', '=', fqdn()),
                ]
            )
            settings['builds'] = builds

            nginx_config = self.env['ir.ui.view'].render_template(
                "runbot.nginx_config", settings
            )
            os.makedirs(nginx_dir, exist_ok=True)
            open(
                os.path.join(nginx_dir, 'nginx.conf'), 'wb'
            ).write(nginx_config)
            _logger.debug('reload nginx')
            subprocess.call(['sudo', '/usr/sbin/service', 'nginx', 'reload'])
            #_logger.warn('RELOAD NGINX!')


class RunbotBranch(models.Model):
    _inherit = 'runbot.branch'

    repo_name = fields.Char(string='Repo Name',
                            related='repo_id.name')


class RunbotBuild(models.Model):
    _inherit = 'runbot.build'

    def _checkout(self):
        super(RunbotBuild, self)._checkout()
        for build in self:
            dirname = osp.join(build.server('addons'),
                               'server_environment_files_sample')
            dirname_new = osp.join(build.server('addons'),
                                   'server_environment_files')
            if osp.isdir(dirname):
                os.rename(dirname, dirname_new)
            build.write({
                'modules': build.modules.replace(
                    'server_environment_files_sample',
                    'server_environment_files'),
                    })
        rcfile = osp.expanduser('~/.openerp_serverrc')
        with open(rcfile, 'w') as fobj:
            fobj.write('[options]\nrunning_env = dev\n')
