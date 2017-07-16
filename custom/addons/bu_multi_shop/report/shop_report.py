from openerp import api, models

class ShopSaleDetailsReport(models.AbstractModel):
    _name = 'report.bu_multi_shop.details'
    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('bu_multi_shop.report_shop_saledetails')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
        }
        return report_obj.render('bu_multi_shop.report_shop_saledetails', docargs)