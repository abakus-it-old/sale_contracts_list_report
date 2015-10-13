import logging

from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.report import report_sxw

_logger = logging.getLogger(__name__)

class employee_measurability(osv.osv_memory):
    _name = "contract.list.report"
    
    _columns = {
        'contract_type_id': fields.many2one('account.analytic.account.type', string='Type', required=True),
        'company_id': fields.many2one('res.company', string="Company", store=False),
        'landscape': fields.boolean('Landscape', default=True),
    }
    
    def _get_datas(self, cr, uid, ids, context=None):

        # Get all the contracts that have the desired type for the desired company
        wiz_data = self.browse(cr, uid, ids[0], context=context)
        #contract object
        account_analytic_account_obj = self.pool.get('account.analytic.account')
        account_analytic_account_ids = None
        if wiz_data.company_id:
            account_analytic_account_ids = account_analytic_account_obj.search(cr, uid, [('contract_type', '=', wiz_data.contract_type_id.id), ('state', '!=', 'cancelled'), ('state', '!=', 'close'), ('state', '!=', 'refused'), ('company_id', '=', wiz_data.company_id.id)])
        else:
            account_analytic_account_ids = account_analytic_account_obj.search(cr, uid, [('contract_type', '=', wiz_data.contract_type_id.id), ('state', '!=', 'cancelled'), ('state', '!=', 'close'), ('state', '!=', 'refused')])

        accounts = []
        for contract in account_analytic_account_obj.browse(cr, uid, account_analytic_account_ids):
            
            accounts.append({'name': contract.name, 'partner_id': contract.partner_id.name, 'code': contract.code, 'date_start': contract.date_start, 'date_end': contract.date, 'description': contract.description, 'state': contract.state})

        contracts = {'accounts':accounts,}
        return contracts

    def get_report(self, cr, uid, ids, context=None):
        data = self._get_datas(cr, uid, ids, context=context)
        
        wiz_data = self.browse(cr, uid, ids[0], context=context)
        report_paperformat_obj = self.pool.get('report.paperformat')
        ir_actions_report_xml_obj = self.pool.get('ir.actions.report.xml')

        report_id = ir_actions_report_xml_obj.search(cr, uid, [('report_name', '=', 'sale_contracts_list_report.contract_list_report_document')])
        if report_id: 
            report = ir_actions_report_xml_obj.browse(cr, uid, report_id[0])
            paperformat_id = report_paperformat_obj.search(cr, uid, [('name', '=', 'Default with Landscape')])
            if paperformat_id:
                paperformat_id = paperformat_id[0]
            else:
                paperformat_id = report_paperformat_obj.create(cr, uid, {'name':'Default with Landscape','orientation':'Landscape',})
            
            if wiz_data.landscape:
                report.paperformat_id = paperformat_id
            else:
                report.paperformat_id = None
        
        datas = {
             'ids': [],
             'model': 'contract.list.report',
             'form': data,
        }
        return self.pool['report'].get_action(cr, uid, [], 'sale_contracts_list_report.contract_list_report_document', data=datas, context=context)
