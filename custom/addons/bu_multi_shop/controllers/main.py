
from odoo import http
from odoo.http import request
from openerp.addons import point_of_sale

# _logger = logging.getLogger(__name__)

class PosControllerInherit(point_of_sale.controllers.main.PosController):
	@http.route('/pos/shop_sale_details_report', type='http', auth='user')
	def print_sale_details(self, date_start=False, date_stop=False, **kw):
		r = request.env['report.bu_multi_shop.report_shop_saledetails']
		pdf = request.env['report'].with_context(date_start=date_start, date_stop=date_stop).get_pdf(r, 'bu_multi_shop.report_shop_saledetails')
		pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
		return request.make_response(pdf, headers=pdfhttpheaders)

	@http.route('/pos/user_sale_details_report', type='http', auth='user')
	def print_sale_details(self, date_start=False, date_stop=False, **kw):
		r = request.env['report.bu_multi_shop.report_user_saledetails']
		pdf = request.env['report'].with_context(date_start=date_start, date_stop=date_stop).get_pdf(r, 'bu_multi_shop.report_user_saledetails')
		pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
		return request.make_response(pdf, headers=pdfhttpheaders)