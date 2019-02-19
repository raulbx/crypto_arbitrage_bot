import sys
import ccxt

gemini = ccxt.gemini({'enableRateLimit': True,})

class evaluator(object):
	def __init__(self,arb_type):
		self.arb_type = arb_type

	def expected_arb_result(self,fees_by_exchange,trades):
		cost = None
		trading_fee = 0
		amount_paid = 0
		amount_recieved = 0
		input_quantity = 0
		btc_usd_rate = gemini.fetch_ticker('BTC/USD').get('close')
		#print(btc_usd_rate)
		trade_log = []
		for i, trade in enumerate(trades):
			exchange = trade.get('exchange')
			transfer_currency_code = trade.get('transfer_currency_code')
			fees_by_order_type = trade.get('type')
			if trade.get('side')=='buy' or trade.get('side')=='sell':
				coin_pair = trade.get('coin_pair')
				base_coin = coin_pair.split('/')[0]
				quote_coin = coin_pair.split('/')[1]
			exchange_fee_structure = fees_by_exchange.get(exchange)
			if i==0:
				input_quantity = trade.get('quantity')
				#This is the beginning quantity. Rest of the quantities will be calculated from here.
				if trade.get('side')=='buy':
					trade_amount = trade.get('price')*input_quantity*(1+exchange_fee_structure.get(fees_by_order_type))
					#print ()
					trade_log.append('{} ({}) {} = {:>06.8f} {} : Bought {} {} for {:>06.8f} {}'.format(exchange,coin_pair,base_coin, trade.get('price'),quote_coin,input_quantity,base_coin,trade_amount,quote_coin))
				elif trade.get('side')=='sell':
					trade_amount = trade.get('price')*input_quantity*(1-exchange_fee_structure.get(fees_by_order_type))
					#print ('Sold {}'.format(i))
				amount_paid = trade_amount
			else:
				if trade.get('side')=='buy':
					# this is different Buy trade than the one above. Here we want to find the quantity for certain quote coin 
					trade_return = (1/trade.get('price'))*input_quantity*(1-exchange_fee_structure.get(fees_by_order_type))
					#trade_return= trade.get('price')*input_quantity*(1-exchange_fee_structure.get(fees_by_order_type))
					#print ('{} ({}) {} = {:>06.8f} {}: Bought {} {} and paid {} {} '.format(exchange,coin_pair, base_coin,trade.get('price'),quote_coin, trade_return,base_coin,input_quantity,quote_coin))
					trade_log.append('{} ({}) {} = {:>06.8f} {}: Bought {} {} and paid {} {} '.format(exchange,coin_pair, base_coin,trade.get('price'),quote_coin, trade_return,base_coin,input_quantity,quote_coin))
					input_quantity = trade_return
				elif trade.get('side')=='sell':
					trade_return = trade.get('price')*input_quantity*(1-exchange_fee_structure.get(fees_by_order_type))
					#print ('{} ({}) {} = {:>06.8f} {}: Sold {:>04.8f} {} recieved {:>06.8f} {}'.format(exchange,coin_pair,base_coin,trade.get('price'),quote_coin,input_quantity,base_coin,trade_return,quote_coin))
					trade_log.append('{} ({}) {} = {:>06.8f} {}: Sold {:>04.8f} {} recieved {:>06.8f} {}'.format(exchange,coin_pair,base_coin,trade.get('price'),quote_coin,input_quantity,base_coin,trade_return,quote_coin))
					input_quantity =trade_return
				elif trade.get('side')=='transfer':
					input_quantity=input_quantity-trade.get('price')
					#This means that the coin was transfered.
					#print ('{}: Transfered {:>06.8f} {}'.format(exchange, input_quantity,transfer_currency_code))
					trade_log.append('{}: Transfered {:>06.8f} {}'.format(exchange, input_quantity,transfer_currency_code))
				amount_recieved = input_quantity
		spread = amount_recieved - amount_paid
		arb_return = spread/amount_paid
		arb_result = {
		'capital_invested':str(round(amount_paid,6)),
		'capital_recieved':str(round(amount_recieved,6)),
		'spread':str(round(spread,2)),
		'arb_return':arb_return,
		'trade_log':trade_log
		}
		return arb_result