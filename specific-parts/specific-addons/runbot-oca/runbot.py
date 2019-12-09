import os
import os.path as osp
import logging

import openerp
from openerp import http, SUPERUSER_ID
from openerp.http import request
from openerp.osv import orm
from openerp import fields, models, api
from openerp.tools import config, appdirs

from openerp.addons.runbot.runbot import mkdirs, run, fqdn
_logger = logging.getLogger(__name__)


class RunbotRepo(orm.Model):
    _inherit = "runbot.repo"

    def reload_nginx(self, cr, uid, context=None):
        """
        completely override the method
        """
        settings = {}
        settings['port'] = config['xmlrpc_port']
        nginx_dir = os.path.join(self.root(cr, uid), 'nginx')
        settings['nginx_dir'] = nginx_dir
        ids = self.search(cr, uid, [('nginx','=',True)], order='id')
        if ids:
            build_ids = self.pool['runbot.build'].search(cr, uid, [('repo_id','in',ids), ('state','=','running')])
            settings['builds'] = self.pool['runbot.build'].browse(cr, uid, build_ids)

            nginx_config = self.pool['ir.ui.view'].render(cr, uid, "runbot.nginx_config", settings)
            mkdirs([nginx_dir])
            open(os.path.join(nginx_dir, 'nginx.conf'),'w').write(nginx_config)
            _logger.debug('reload nginx')
            run(['sudo', '/usr/sbin/service', 'nginx', 'reload'])

    def cron(self, cr, uid, ids=None, context=None):
        if fqdn() == 'runbot.odoo-communty.org':
            # phase out builds on main server
            return
        return super(RunbotRepo, self).cron(cr, uid, ids, context=context)


class RunbotBranch(models.Model):
    _inherit = 'runbot.branch'

    repo_name = fields.Char(string='Repo Name',
                            related='repo_id.name')
    mig_target_branch_name = fields.Char(string='PR target branch', readonly=1)
    mig_branch_name = fields.Char('MIG branch name')
    mig_pull_head_name = fields.Char('MIG pull head name')
    mig_branch_url = fields.Char('MIG branch url')

    def _get_branch_infos(self):
        """compute branch_name, branch_url, pull_head_name and target_branch_name based on name"""
        _re_patch = re.compile(r'.*patch-\d+$')
        tot = len(self)
        count = 0
        for i, branch in enumerate(self):
            if branch.name:
                _logger.info('[%d/%d] get branch info for %s %s', i+1, tot, branch.repo_id.name, branch.name)
                branch.mig_branch_name = branch.name.split('/')[-1]
                pi = branch._get_pull_info()
                if pi:
                    branch.mig_target_branch_name = pi['base']['ref']
                    if pi.get('head') and pi['head'].get('label') and not _re_patch.match(pi['head']['label']):
                        # label is used to disambiguate PR with same branch name
                        branch.mig_pull_head_name = pi['head']['label']
                if pi.get('head'):
                    branch.mig_branch_url = pi['head'].get('ref', '')
                _logger.info('Branch %s, branch_name %s, target_branch_name %s, pull_head_name %s, branch_url %s',
                             branch.name, branch.mig_branch_name, branch.mig_target_branch_name, branch.mig_pull_head_name, branch.mig_branch_url)

    @api.model
    def cron_branch_info(self):
        _logger.warning('update branch info cron')
        branches = self.search([('mig_target_branch_name', '=', False)], limit=500, order='id DESC')
        branches._get_branch_infos()
        _logger.warning('end update branch info cron')
        return True


class RunbotBuild(models.Model):
    _inherit = 'runbot.build'

    @api.multi
    def checkout(self):
        super(RunbotBuild, self).checkout()
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
