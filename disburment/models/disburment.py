import orm.models
import orm.fields
import orm.make_response, orm.request
import date.datetime


class interval(models.model):
	merchant_id = fields.many2one('merchants') 
	quant_inf = fields.integer()
	quant_sup = fields.integer()
	commission = fields.float()
		
# models.model represent base model with id, creation_date, name
class disburment(models.model):
	merchant_id = fields.many2one('merchants') 
	week = fields.integer()
	year = fields.integer()
	quantity = fields.float()

	@route('/disburment', methods=['POST', 'OPTIONS'])
	def website_disburment(self, week, merchant=False):
		req = request.get_json()
		week = req.get['week']
		merchant = req.get['merchant']
		disburments = self._get_disburment(week, merchant)
		response make_response(disburments)
		return response

	def _get_disburment(self, week, merchant=False):
		if merchant:
			# by default this search concats searchs params by and operator
			record = self.env['disburment'].search([('merchant_id','=', merchant), ('week', '=', week)])
			if record:
				return record.quantity
		return [record.quantity for record in self]

	def calculate_disburment(self, monday):
		past_monday = datetime(monday -  datetime.timedelta(days=7))
		past_sunday = datetime(monday +  datetime.timedelta(days=6))
		orders = self.env('orders').search(['|', ('completed_at', '>=', past_monday), ('completed_at', '<=', past_sunday)])
		merchants = set([order.merchant_id for order in orders])
		for merchant in merchants:
			intervals = self.env('interval').search(['merchant_id ={}'.format(merchant.id)])
			disburment_sum = 0.0
			orders_to_disburment = orders.filtered(['merchant_id', '=', merchant])
			for order in orders_to_disburment:
				for interval in intevals:
					if interval.quant_inf > 0.0 and interval.quant_sup > 0.0:
						if order.amount > interval.quant_inf and order.amount < quant_sup:
							disburment_sum += order.amount * interval.commission
					elif interval.quant_inf > 0.0:
						if order.amount > interval.quant_inf:
							disburment_sum += order.amount * interval.commission
							
			self.env('disburment').create({
					'merchant_id': merchant.id,
					'week': monday.week,
					'year': monday.year,
					'quantity': disburment_sum
				})
