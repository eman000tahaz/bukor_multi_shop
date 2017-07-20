from openerp import api, models
from odoo import api, fields, models


class ReportUserSaleDetails(models.AbstractModel):

    _name = 'report.bu_multi_shop.report_user_saledetails'

    @api.model
    def get_sale_details(self, date_start=False, date_stop=False, user_id=False):

        if not user_id:
            self.env.uid

        if date_start:
            date_start = fields.Datetime.from_string(date_start)
        if date_stop:
            date_stop = fields.Datetime.from_string(date_stop)
        # avoid a date_stop smaller than date_start
        date_stop = max(date_stop, date_start)
        date_start = fields.Datetime.to_string(date_start)
        date_stop = fields.Datetime.to_string(date_stop)

        orders = self.env['pos.order'].search([
            ('date_order', '>=', date_start),
            ('date_order', '<=', date_stop),
            ('state', 'in', ['paid','invoiced','done']),
            ('user_id', '=', user_id)
            ])

        user_currency = self.env.user.company_id.currency_id

        total = 0.0
        products_sold = {}
        taxes = {}
        for order in orders:
            if user_currency != order.pricelist_id.currency_id:
                total += order.pricelist_id.currency_id.compute(order.amount_total, user_currency)
            else:
                total += order.amount_total
            currency = order.session_id.currency_id

            for line in order.lines:
                key = (line.product_id, line.price_unit, line.discount)
                products_sold.setdefault(key, 0.0)
                products_sold[key] += line.qty

                if line.tax_ids_after_fiscal_position:
                    line_taxes = line.tax_ids_after_fiscal_position.compute_all(line.price_unit * (1-(line.discount or 0.0)/100.0), currency, line.qty, product=line.product_id, partner=line.order_id.partner_id or False)
                    for tax in line_taxes['taxes']:
                        taxes.setdefault(tax['id'], {'name': tax['name'], 'total':0.0})
                        taxes[tax['id']]['total'] += tax['amount']

        st_line_ids = self.env["account.bank.statement.line"].search([('pos_statement_id', 'in', orders.ids)]).ids
        if st_line_ids:
            self.env.cr.execute("""
                SELECT aj.name, sum(amount) total
                FROM account_bank_statement_line AS absl,
                     account_bank_statement AS abs,
                     account_journal AS aj 
                WHERE absl.statement_id = abs.id
                    AND abs.journal_id = aj.id 
                    AND absl.id IN %s 
                GROUP BY aj.name
            """, (tuple(st_line_ids),))
            payments = self.env.cr.dictfetchall()
        else:
            payments = []

        return {
            'total_paid': user_currency.round(total),
            'payments': payments,
            'company_name': self.env.user.company_id.name,
            'taxes': taxes.values(),
            'user': self.env['res.users'].search([('id', '=', user_id)]),
            'products': sorted([{
                'product_id': product.id,
                'product_name': product.name,
                'code': product.default_code,
                'quantity': qty,
                'price_unit': price_unit,
                'discount': discount,
                'uom': product.uom_id.name
            } for (product, price_unit, discount), qty in products_sold.items()], key=lambda l: l['product_name'])
        }

    @api.multi
    def render_html(self, docids, data=None):
        data = dict(data or {})
        user_id = self.env['res.users'].browse(data['user_id']).id
        data.update(self.get_sale_details(data['date_start'], data['date_stop'], user_id))
        return self.env['report'].render('bu_multi_shop.report_user_saledetails', data)