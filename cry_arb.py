import sys
import ccxt
import numpy as np
import time
import datetime
from pytz import timezone
import cry_arb_evaluator
import json

dash = '-' * 25
space = '	' * 2
tz = timezone('EST')
kraken   = ccxt.kraken({'enableRateLimit': True})
exmo   = ccxt.exmo({ 'enableRateLimit': True})
binance = ccxt.binance({'enableRateLimit': True})
hitbtc   = ccxt.hitbtc2({'enableRateLimit': True})
coinbasepro = ccxt.coinbasepro({'enableRateLimit': True,})
gemini = ccxt.gemini({'enableRateLimit': True,})
bitfinex = ccxt.bitfinex({'enableRateLimit': True,})
livecoin = ccxt.livecoin({'enableRateLimit': True,})
kucoin   = ccxt.kucoin({'enableRateLimit': True,})
cex   = ccxt.cex({'enableRateLimit': True,})
bitstamp = ccxt.bitstamp({'enableRateLimit': True,})


binance_ltc_address = 'LLmWdKju3aHzS8q5azoVGSfPV6NY6a4PvY'
exmo_ltc_address = 'LThC9vNBvyJz7UesBAmpMaJNfHFhxXqhb6'
#----------XRP------------
hitbtc_xrp_deposit_address = 'rhL5Va5tDbUUuozS9isvEuv7Uk1uuJaY1T'
hitbtc_xrp_tag = '1492555998'

exmo_xrp_deposit_address = 'rUocf1ixKzTuEe34kmVhRvGqNCofY1NJzV'
exmo_xrp_tag = '363160755'

#----------DAI------------
hitbtc_dai_deposit_address = '0x391a04d8cb95a5a8f22af609abefe4067b7cc4d8'

#----------BTC------------
exmo_btc_deposit_address = '1DN3qUSw5oVvH5YVfvEia3m7Xr3e3txA9v'

#exchanges = [ "binance", "bitfinex","cex","cryptopia","exmo", "hitbtc","kraken"]
exchanges = [ "binance", "bitfinex","cex","exmo","kraken"]

clients = [getattr(ccxt, e.lower())() for e in exchanges]

coin_pairs = ["ETH/BTC","ETH/USD","XRP/BTC","XLM/BTC","XRP/USD","XLM/USD","XRP/BTC", "ZEC/BTC","USDT/XRP"]
#coin_pairs = ["ETH/USD"]

fees_by_exchange= {
    'binance':{'taker':0.001,'maker':0.001},
    'bitfinex':{'taker':0.001,'maker':0.002},
    'bitstamp':{'taker':0.0025,'maker':0.0025},
    'cex':{'taker':0.0025,'maker':0.0016},
    'hitbtc':{'taker':0.001,'maker':-0.0001},
	'exmo':{'taker':0.002,'maker':0.002},
	'kraken':{'taker':0.0026,'maker':0.0016},
	'livecoin':{'taker':0.0018,'maker':0.0018},
	'kucoin':{'taker':0.001,'maker':0.002},
	'Coinbase Pro':{'taker':0.0025,'maker':0.0025}
	}
transfer_fee ={
	'XRP':0.001,
	'BTC':0.000082,
	'DAI':1.0,
	'XLM':0.00001,
	'XEM':0,
	'USD':0,
	'USDT':5,
	'LTC':0.00064,
	'ZEC':0,
	'EOS':0,
	'ETH':0.00065,
	'DASH':0.00017,
	'DOGE':2,
	'ENJ':0,
	'PPT':0,
	'BTT':0,
	'VEN':0,
	'TRX':0
	}
exchange_1 = livecoin
exchange_2 = exmo
exchange_3 = binance
ex1_currency_code ='DOGE'
ex2_currency_code ='DOGE'
ex3_currency_code ='BTC'
ex1_transfer_currency_code = 'DOGE'
ex2_transfer_currency_code = 'XRP'
ex3_transfer_currency_code = 'BTC'
ex1_coin_pair = "DOGE/USD"
ex2_coin_pair = "DOGE/USD"
ex3_coin_pair = "ENJ/BTC"
ex1_convert_coin_pair='XRP/USD'
ex2_convert_coin_pair='XRP/USD'
#ex1_coin_pair = "DAI/BTC"
#ex2_coin_pair = "DAI/BTC"

class detect_arb(object):
	def __init__(self,arb_type):
		#initialize keys
		self.arb_type = arb_type

	def initalize_bot():
		trade_on_exchange = None
		#user_input = int(input("(1) - Start ARB_BOT\n(2) - Trade\n(3) - Place Order\n(4) - Check Order Status\n(5) - Cancel Order\n(6) - Transfer Funds\n:"))
		user_input = int(input("(1) - Start ARB_BOT\n(2) - Trade\n:"))
		if user_input == 1:
			print("{}Crypto Arbitrage Bot{}\n{}  {} {}".format(dash,dash,dash,datetime.datetime.now().strftime('%m-%d-%y %H:%M:%S'),dash))
			#detect_arb_opportunities()
			evaluate_arb_opportunities()
		elif user_input == 2:
			print('Please pick exchange')
			exchange_input = int(input('(21) {}\n(22) {}\n:'.format(exchange_1.name,exchange_2.name)))
			if exchange_input ==21:
				trade_on_exchange = exchange_1
				coin_pair = ex1_coin_pair
			elif exchange_input ==22:
				trade_on_exchange = exchange_2
				coin_pair = ex2_coin_pair
			else:
				print('You picked {}. This is not a valid option'.format(exchange_input))
				return
			print ('Trading on\n{}\n-----------'.format(trade_on_exchange.name))
			order_input = int(input("(1) Buy\n(2) Sell\n(3) Check Order Status\n(4) Transfer Funds\n(5) Transfer BTC\n(6) Get Trades\n(7) View Balances\n:"))
			if order_input == 1:
				print('BUY ORDER\n--------\n')
				coin_quantity = input("Enter quantity\n:")
				buy_price = input("Buy Price\n:")
				#coin_pair = "XRP/BTC"
				#coin_trade_quantity = 100
				#buy_price = 0.00008962
				print('Placing order in {} to buy {} of {} at the the price of {}'.format(trade_on_exchange.name, coin_quantity,coin_pair,buy_price))
				try: 
					buy_order = trade_on_exchange.create_order(coin_pair, 'limit', 'buy', coin_quantity, buy_price)
					print(buy_order)
					print('BUY ORDER ID:{}'.format(buy_order.get('id')))
				except (ccxt.ExchangeError, ccxt.NetworkError) as error:
					print('Got an error', type(error).__name__, error.args)
					# add necessary handling code according to your needs or rethrow the exception
					raise 
			elif order_input == 2:
				print('SELL order')
				coin_quantity = input("Enter quantity\n:")
				sell_price = input("Sell Price\n:")
				#coin_pair = "XRP/BTC"
				#coin_trade_quantity = 10
				#sell_price = 0.33730000
				try: 
					print('Placing order in {} to sell {} of {} at the the price of {}'.format(trade_on_exchange.name, coin_quantity,coin_pair,sell_price))
					sell_order = trade_on_exchange.create_order(coin_pair, 'limit', 'sell', coin_quantity, sell_price)
					print(sell_order)
					print('SELL ORDER ID:{}'.format(sell_order.get('id')))
					#print(trade_on_exchange.name)
				except (ccxt.ExchangeError, ccxt.NetworkError) as error:
					print('Got an error', type(error).__name__, error.args)
					# add necessary handling code according to your needs or rethrow the exception
					raise 
			elif order_input == 3:
				print('checking order status')
				order_no = input("Please enter the order number\n:")
				# First one works for HITBTC, second one works for Exmo
				order_status_raw=trade_on_exchange.fetch_order(order_no,symbol=coin_pair, params={})
				#order_status_raw=trade_on_exchange.fetch_orders(symbol=coin_pair, params={})
				if type(order_status_raw)==list:
					print(order_status_raw)
					print(order_status_raw[0].get('status'))
					order_status=order_status_raw[0].get('status')
				else:
					print(order_status_raw)
					order_status = order_status_raw.get('status')
				print(order_status)
				if order_status!='closed':
					cancel_order = input("This order is not yet filled.\n Enter YES to cancel it\n:")
					if cancel_order == 'YES':
						order_status_raw= trade_on_exchange.cancel_order (order_no)
						print(order_status_raw)
					else:
						print('------Bye Bye-------')
			elif order_input == 4:
				print('Transfering funds')
				print('This action will transfer XRP')
				#ex1_currency_code = 'DAI'
				if trade_on_exchange.name =='HitBTC v2':
					transfer_input = int(input("Additional actions availabale in HitBTC.\n1)Transfer to Trading Account\n2)Transfer to Main Account\n3)Transfer funds to Exmo:\n"))
					ex1_currency_code = input("Enter Currency Code\n:")
					coin_quantity = input("Enter Quantiy\n:")
					if transfer_input==1:
						status = hitbtc.private_post_account_transfer({'currency': ex1_currency_code, 'amount': coin_quantity, 'type': 'bankToExchange'})
						main_account_balance = hitbtc.fetch_balance({'type':'account'})[ex1_currency_code]['free']
						trading_account_balance = hitbtc.fetch_balance({'type':'trading'})[ex1_currency_code]['free']
						print("Account Balances are\nMainAccount:{}\nTrading{}\nStatus:{}".format(main_account_balance,trading_account_balance,status))
					elif transfer_input==2:
						status = hitbtc.private_post_account_transfer({'currency': ex1_currency_code, 'amount': coin_quantity, 'type': 'exchangeToBank'})
						main_account_balance = hitbtc.fetch_balance({'type':'account'})[ex1_currency_code]['free']
						trading_account_balance = hitbtc.fetch_balance({'type':'trading'})[ex1_currency_code]['free']
						print("Account Balances are\nMainAccount:{}\nTrading:{}\nStatus:{}".format(main_account_balance,trading_account_balance,status))
					#transfer_confirm = str(input("Do you want to transfer these funds to HitBTC. Enter Y\n:"))
					elif transfer_input==3:
						transfer_bw_exchanges = int(input("1)HitBTC-Exmo\n:"))
						if transfer_bw_exchanges==1:
							print('Initiating transfer of XRPfrom HitBTC - Exmo\n')
							destination_deposit_address=exmo_xrp_deposit_address
							destination_tag=exmo_xrp_tag
							
							print("Transfering to {} and tag {}".format(destination_deposit_address,destination_tag))
							withdraw_status = trade_on_exchange.withdraw(ex1_currency_code, coin_quantity, destination_deposit_address, tag=destination_tag, params={})
							print(withdraw_status)
					else:
						print('Coming here')
				elif trade_on_exchange.name =='EXMO':
					print('----Transfer DAI to HitBTC---')
					ex1_currency_code = 'DAI'
					coin_quantity = input("Enter Quantiy\n:")
					transfer_confirm = str(input("Please enter Y to continue\n:"))
					if transfer_confirm == 'Y':
						destination_deposit_address=hitbtc_dai_deposit_address
						destination_invoice = '1234'
						print("Transfering to {}".format(destination_deposit_address))
						withdraw_status = trade_on_exchange.withdraw(ex1_currency_code, coin_quantity, destination_deposit_address, tag=None, params={})
						print(withdraw_status)
					else:
						print("Not going to withdraw money")
					#check if the money has reached Exmo
					money_transfer_progress = True
					starttime=time.time()
					while money_transfer_progress:
						balance = hitbtc.fetch_balance({'type':'account'})[ex1_currency_code]['free']
						time.sleep(5.0 - ((time.time() - starttime) % 1.0))
						print('At:{} Balance:{}'.format(datetime.datetime.now().strftime('%H:%M:%S'),balance))
						if float(balance)>float(coin_quantity-1):
							money_transfer_progress = False
							print('Coins are now available in the wallet')

						#Check the wallet status
			elif order_input == 5:
				print('Transfering BTC back to the original exchange')
				transfer_btc_input = str(input("Please enter OK to continue\n:"))
				if transfer_btc_input == 'YES':
					print('Going to transfer BTC')
			elif order_input ==6:
				trades = trade_on_exchange.fetch_trades(coin_pair, since=None, limit=None, params={})
				print(trades)
			elif order_input==7:
				print('Wallet: {}'.format(trade_on_exchange.name))
				balance = trade_on_exchange.fetch_balance()
				#print(balance.get('info').get('balances'))
				print(balance)
			elif order_input==0:
				print('------Thank you-------')
			#check_balance()
		elif user_input == 3:
			#this will buy Dai in Exmo
			coin_quantity = input("About to place a buy order for Dai. Enter Quantiy\n:")
			if coin_quantity!=0:
				try:
					order_status = exmo.create_market_buy_order('DAI/USD', coin_quantity)
					print(order_status,'\n')
					print(order_status.get('status'))
				except ccxt.base.errors.OrderNotFound as error:
					print('We could not find the order', type(error).__name__, error.args)
					raise
				except (ccxt.ExchangeError, ccxt.NetworkError) as error:
					print('This is an error', type(error).__name__, error.args)
					raise
			else:
				print("Good Bye")
			'''print('Please pick exchange')
			exchange_input = int(input('(31) {}\n(32) {}\n:'.format(exchange_1.name,exchange_2.name)))
			if exchange_input ==31:
				trade_on_exchange = exchange_1
				coin_pair = ex1_coin_pair
			elif exchange_input ==32:
				trade_on_exchange = exchange_2
				coin_pair = ex2_coin_pair
			order_input = int(input("(1) Buy\n(2) Sell\n:"))'''
			
		elif user_input == 4:
			order_no = int(input("Please enter the order number\n:"))
			try:
				order_status=binance.fetch_order(order_no,symbol='XLM/BTC', params={})
				#order_status=binance.fetch_closed_orders(symbol='XLM/BTC', since=None, limit=None, params={})
				print(order_status,'\n')
				print(order_status.get('status'))
			except ccxt.base.errors.OrderNotFound as error:
				print('We could not find the order', type(error).__name__, error.args)
				raise
			except (ccxt.ExchangeError, ccxt.NetworkError) as error:
				print('This is an error', type(error).__name__, error.args)
				raise
		elif user_input == 5:
			order_no = int(input("Please enter the order number\n:"))
			try:
				order_status= exmo.cancel_order (order_no)
			except (ccxt.ExchangeError, ccxt.NetworkError) as error:
				print('This is an error', type(error).__name__, error.args)
				raise
			print(order_status)
			#print("Order Status {:<5s}, price: {:>04.8f}".format(order_status.get('status'),order_status.get('price')))
			#1715016131
			#1720956509
		elif user_input == 6:
			transfer_input = str(input("Please enter YES to continue\n:"))
			if transfer_input == 'YES':
				bnb_deposit_address = '******************************'
				bnb_tag = '****'
				exmo_deposit_address = '******************************'
				exmo_tag = '****'
				hitbtc_deposit_address = '******************************'
				hitbtc_tag = '****'
				amount = 50
				ex1_currency_code = 'XRP'
				#withdraw_status = exmo.withdraw(ex1_currency_code, amount, exmo_deposit_address, tag=exmo_tag, params={})
				#withdraw_status = hitbtc.withdraw(ex1_currency_code, amount, bnb_deposit_address, tag=bnb_tag, params={})
				#withdraw_status = binance.withdraw(ex1_currency_code, amount, hitbtc_deposit_address, tag=hitbtc_tag, params={})
				print(withdraw_status)
			elif transfer_input==0:
				print('------Thank you-------')
		elif user_input==0:
				print('------Thank you-------')

	def detect_opportunities(self,capitalAllocated):
		#print('Going to detect opportunities')
		arb_results =[]
		coin_quantity = capitalAllocated
		ask = np.zeros((len(coin_pairs), len(clients)))
		bid = np.zeros((len(coin_pairs), len(clients)))
		#print("Retrieving Order Book")
		for row, coin_pair in enumerate(coin_pairs):
			for col, client in enumerate(clients):
				try:
					book = client.fetch_order_book(coin_pair)
					ask[row, col] = book['asks'][0][0]
					bid[row, col] = book['bids'][0][0]
				except (ccxt.ExchangeError, ccxt.NetworkError) as error:
					print('Got an error', type(error).__name__, error.args)
					pass

		for i, coin_pair in enumerate(coin_pairs):
			for j1, exchange1 in enumerate(exchanges):
				for j2, exchange2 in enumerate(exchanges):
					arb_result ={}
					exchange1_price = ask[i, j1]
					exchange2_price = bid[i, j2]
					exchange1_transfer_currency_price = exchange_1.fetch_ticker(ex1_convert_coin_pair).get('bid')
					exchange2_transfer_currency_price = exchange_2.fetch_ticker(ex2_convert_coin_pair).get('bid')
					exchange3_price = exchange_3.fetch_ticker(ex3_coin_pair).get('bid')

					#fee = 0.25
					roi = 0
					if j1 != j2 and ask[i, j1]>0:
						#print (j1)
						ex1_transfer_currency_code=coin_pair.split('/')[0]
						#Regular ROI
						#roi = ((bid[i, j2]*(1-fee/100)) / (ask[i, j1]*(1+fee/100)) - 1) * 100
						roi = ((bid[i, j2]*(1-fees_by_exchange.get(exchange2).get('taker'))) / (ask[i, j1]*(1+fees_by_exchange.get(exchange1).get('taker'))) - 1) * 100
						if roi>0:
							#print([coin_pair, exchange1, ask[i, j1], exchange2, bid[i, j2], round(roi,2)])
							#Adjusted ROI
							ex2_transfer_currency_code= coin_pair.split('/')[1]
							trade_strategy = [
							{'exchange':exchange1,'coin_pair':coin_pair,'type':'maker','side':'buy','price':exchange1_price,'quantity':coin_quantity},
							{'exchange':exchange1,'type':'transfer','side':'transfer','price':transfer_fee.get(ex1_transfer_currency_code),'transfer_currency_code':ex1_transfer_currency_code},
							{'exchange':exchange2,'coin_pair':coin_pair,'type':'maker','side':'sell','price':exchange2_price},
							{'exchange':exchange2,'coin_pair':ex2_convert_coin_pair,'type':'maker','side':'buy','price':exchange2_transfer_currency_price},
							{'exchange':exchange2,'type':'transfer','side':'transfer','price':transfer_fee.get(ex2_transfer_currency_code),'transfer_currency_code':ex2_transfer_currency_code},
							{'exchange':exchange1,'coin_pair':ex1_convert_coin_pair,'type':'maker','side':'sell','price':exchange1_transfer_currency_price}
							]
							ae = cry_arb_evaluator.evaluator('direct')
							arb_result = ae.expected_arb_result(fees_by_exchange,trade_strategy)
							arb_return = str(round(arb_result.get('arb_return')*100,2))
							arb_result.update({'base_coin':ex1_transfer_currency_code,'coin_quantity':coin_quantity,'exchange_1':exchange1,'exchange1_price':exchange1_price,'ex1_coin_pair':coin_pair,'exchange_2':exchange2,'exchange2_price':exchange2_price,'ex2_coin_pair':coin_pair,'arb_return':arb_return,'raw_roi':round(roi,2),'update_ts':datetime.datetime.now(tz).strftime('%H:%M:%S')})
							print(arb_result)
							arb_results.append(arb_result)
		return arb_results
	def execute_arb(ex1_currency_code,ex2_currency_code,arb_strategy,bot_state, coin_trade_quantity,buy_price,sell_price,btc_usd_rate):
		#buy_order_id = 'c665f44cc0bf4487931efaa274bd2e5b'
		#sell_order_id = '1758429294'
		bot_state='ORDERS_SUCCESSFUL'

		#Step 1: Buy the coin from the lower priced exchange
		if bot_state =='BOT_READY_FOR_ARB':
			if arb_strategy=='BUY_FROM_EXCH1_SELL_IN_EXCH2':
				print('---------------------------------\nArbitrage Condition Found\n----------------------------\nBuy: {}{} in {} at DAI{:<04.8f} ${:<04.8f}\nSell {}{} in {} at ${:<04.8f} ${}'.format(coin_trade_quantity+1,ex1_currency_code, exchange_1.name,buy_price,buy_price*(coin_trade_quantity+1),coin_trade_quantity,ex1_currency_code,exchange_2.name,sell_price,sell_price*coin_trade_quantity,))
				#bot_state = 'ORDERS_PLACED'
				
				try:
					buy_order = exchange_1.create_order(ex1_coin_pair, 'limit', 'buy', coin_trade_quantity+1, buy_price)
					print(buy_order)
					buy_order_id = buy_order.get('id')
					print(buy_order_id)
				except (ccxt.ExchangeError, ccxt.NetworkError) as error:
					print('Buy trade failed. Aborting arbitrage', type(error).__name__, error.args)
					return 
				try:
					sell_order = exchange_2.create_order(ex2_coin_pair, 'limit', 'sell', coin_trade_quantity, buy_price)
					#sell_order_id = sell_order.get('info')['order_id']
					print(sell_order)
					sell_order_id = sell_order.get('id')
					print(sell_order_id)
				except (ccxt.ExchangeError, ccxt.NetworkError) as error:
					print('Sell trade failed. Please cancel the buy trade manually', type(error).__name__, error.args)
				bot_state = 'ORDERS_PLACED'
			'''
			elif arb_strategy=='BUY_FROM_EXCH2_SELL_IN_EXCH1':
				print('Strategy is buy from {} and sell in {}'.format(exchange_2.name, exchange_1.name))
				buy_order = exchange_2.create_order(ex2_coin_pair, 'limit', 'buy', coin_trade_quantity, buy_price)
				print(buy_order)
				sell_order = exchange_1.create_order(ex1_coin_pair, 'limit', 'sell', coin_trade_quantity, buy_price)
				print(sell_order)
			#Buy little bit more coins in the buy exchange so that once transferred the quantity after fees will be same as the selling exchange.
			'''

			'''
			print("bought in one exchange")
			symbol = 'ETH/BTC'
			type = 'limit'  # or 'market', other types aren't unified yet
			side = 'sell'
			amount = 123.45  # your amount
			price = 54.321  # your price
			# overrides
			params = {
			'stopPrice': 123.45,  # your stop price
			'type': 'stopLimit',
			}
			#order = exchange.create_order(symbol, type, side, amount, price, params)
			'''
			#buy_order = buy_from_exchange.create_order(coin_pair, 'limit', 'buy', coin_trade_quantity, buy_price, params)
			#print('Buy Order: ',buy_order)
			#sell_order = sell_from_exchange.create_order(coin_pair, 'limit', 'sell', coin_trade_quantity, sell_price, params)
			#print('Sell Order: ',sell_order)
			#print("Place order for sell in second exchange")
			
		elif bot_state =='ORDERS_PLACED':
			exmo_xrp_deposit_address = '****************'
			exmo_xrp_tag = '363160755'
			#----------DAI------------
			hitbtc_dai_deposit_address = '****************'
			final_dai_quantity = 0
			final_xrp_quantity = 0

			print('{}\tChecking if the trades have been successful'.format(datetime.datetime.now().strftime('%H:%M:%S')))
			buy_order_status = 'Waiting'
			sell_order_status = 'Waiting'
			orders_in_progress = True
			starttime=time.time()
			while orders_in_progress: 
				try:
					buy_order_status_raw=exchange_1.fetch_order(buy_order_id,symbol='XRP/DAI', params={})
					buy_order_status = buy_order_status_raw.get('status')
					print('\tBuy Order Status:{}'.format(buy_order_status))
				except (ccxt.ExchangeError, ccxt.NetworkError) as error:
					print('\tBuy --', type(error).__name__, error.args)
				try:
					sell_order_status_raw=exchange_2.fetch_order(sell_order_id,symbol='XRP/USD', params={})
					#sell_order_status_raw=exchange_2.fetch_orders(symbol='XRP/USD', params={})
					sell_order_status = sell_order_status_raw.get('status')
					print('\tSell Order Status:{}'.format(sell_order_status))
				except (ccxt.ExchangeError, ccxt.NetworkError) as error:
					print('\tSell --', type(error).__name__, error.args)
				if buy_order_status =='closed' and sell_order_status =='closed':
					print('\tBoth trades are filled')
					bot_state ='ORDERS_SUCCESSFUL'
					orders_in_progress = False
				else :
					print('{}\tTrade statuses\n\t{} is {}\n\t{} is {}.\n\tWaiting for both trades to be closed'.format(datetime.datetime.now().strftime('%H:%M:%S'),exchange_1.name,buy_order_status,exchange_2.name,sell_order_status))
				time.sleep(5.0 - ((time.time() - starttime) % 1.0))
		elif bot_state =='ORDERS_SUCCESSFUL':
			exmo_xrp_deposit_address = '****************'
			exmo_xrp_tag = '363160755'
			#----------DAI------------
			hitbtc_dai_deposit_address = '****************'
			'''
			print('{}\tCheck if the coins are available in the buying exchange'.format(datetime.datetime.now().strftime('%H:%M:%S')))
			waiting_for_coins = True
			starttime=time.time()
			while waiting_for_coins:
				exchange_1_balance = exchange_1.fetch_balance({'type':'trading'})[ex1_currency_code]['free']
				print('\tBalance in {}:{}'.format(exchange_1.name,exchange_1_balance))
				# If the coins are available in the trading account. exchange_1_balance will be higher than coin_trade_quantity because we ordered one extra coin
				if exchange_1_balance > coin_trade_quantity:
					status = exchange_1.private_post_account_transfer({'currency': ex1_currency_code, 'amount': exchange_1_balance, 'type': 'exchangeToBank'})
					print('\t Moving coins from trading to main account. Status of transfer: '.format(status))
					# Now transfer the coins from the main account to exchange_2 for the next cycle
				main_account_balance = exchange_1.fetch_balance({'type':'account'})[ex1_currency_code]['free']
				if main_account_balance>exchange_1_balance:
					#Coins have been transfered to the main account. No need to check now.
					print('\t Coins are now available in the main account: '.format(status))
					waiting_for_coins = False
				time.sleep(5.0 - ((time.time() - starttime) % 1.0))
			
			# Now move the coins
			print('{}\tInitiating transfer of {} {} from {} - {}\n'.format(datetime.datetime.now().strftime('%H:%M:%S'),ex1_currency_code,main_account_balance, exchange_1.name,exchange_2.name))

			destination_deposit_address=exmo_xrp_deposit_address
			destination_tag=exmo_xrp_tag
			print("\tTransfering XRP from HitBTC to EXMO {} and tag {}".format(destination_deposit_address,destination_tag))
			withdraw_status = exchange_1.withdraw(ex1_currency_code, exchange_1_balance, destination_deposit_address, tag=destination_tag, params={})
			print('\tStatus of withdrawl: '.format(withdraw_status))

			# Check exchange 2. 
			exchange_2_balance = exchange_2.fetch_balance()[ex2_currency_code]['free']
			print('\tUSD Balance in {}:{:<04.8f}'.format(exchange_2.name,exchange_2_balance))
			# If coins are available in exchange 2, convert them to DAI. This balance should be available because the trade is already closed.
			# This number should be calculated from the order fulfilment status
			dai_order_id = 00
			dai_order_status = 'Open'
			if exchange_2_balance >85:
				try:
					#coin_quantity = exchange_2_balance/1.03
					print('{}\tConvert USD to DAI'.format(datetime.datetime.now().strftime('%H:%M:%S')))
					#Convert all USD to DAI. We need to wait till this order is closed.
					market_buy_order = exmo.create_market_buy_order('DAI/USD', exchange_2_balance)
					print('\tStatus from exchange is {} and the order status is {}'.format(market_buy_order,market_buy_order.get('status')))
					order_id = market_buy_order.get('id')
					print(market_buy_order)
				except (ccxt.ExchangeError, ccxt.NetworkError) as error:
					print('Got an error', type(error).__name__, error.args)

			waiting_for_dai_order = True
			starttime=time.time()
			dai_order_status ='waiting'
			while waiting_for_dai_order:
				# Keep on checking the order status
				try:
					#dai_order_status = exmo.fetch_order(dai_order_id,symbol='DAI/USD', params={})
					dai_order_status_raw = exmo.fetch_orders(symbol='DAI/USD', params={})
					dai_order_status = dai_order_status_raw[0].get('status')
					print('\t Market Buy Order Status:{}'.format(dai_order_status_raw[0].get('status')))
				except (ccxt.ExchangeError, ccxt.NetworkError) as error:
					print('Got an error', type(error).__name__, error.args)
				if dai_order_status=='closed':
					print('{}\tUSD-DAI Conversion complete'.format(datetime.datetime.now().strftime('%H:%M:%S')))
					waiting_for_dai_order = False
				time.sleep(5.0 - ((time.time() - starttime) % 1.0))
	'''
			dai_order_status ='another'
			if dai_order_status =='closed':
				#Transfer the coins to Exchange 1
				print('\tDai is available in the {}. Transfering it to {}'.format(exchange_2.name,exchange_1.name))
				final_dai_quantity=exchange_2.fetch_balance()['DAI']['free']
				destination_deposit_address=hitbtc_dai_deposit_address
				destination_invoice = '1234'
				print("\nTransfering {} to {}".format(final_dai_quantity, destination_deposit_address))
				withdraw_status = exchange_2.withdraw(ex2_transfer_currency_code, final_dai_quantity, destination_deposit_address, tag=None, params={})
				print(withdraw_status)
				#final_xrp_quantity = main_account_balance
				bot_state ='COIN_TRANSFER_INITIATED'

			print('{}\tChecking if the coin transfers is complete'.format(datetime.datetime.now().strftime('%H:%M:%S')))
			verify_coin_transfers=True
			starttime=time.time()
			while verify_coin_transfers:
				exchange_1_balance = exchange_1.fetch_balance({'type':'account'})['DAI']['free']
				exchange_2_balance = exchange_2.fetch_balance()['XRP']['free']
				print('{}\tBalance in {} is: {:>04.4f}\n\t\tBalance in {} is: {}'.format(datetime.datetime.now().strftime('%H:%M:%S'), exchange_1.name,exchange_1_balance,exchange_2.name,exchange_2_balance))
				if exchange_1_balance>10 and exchange_2_balance > 300:
					bot_state = 'ARBITRAGE_COMPLETE'
					verify_coin_transfers=False
					print('Arbitrage trades successfully completed.')
				time.sleep(10.0 - ((time.time() - starttime) % 1.0))
		elif bot_state =='COIN_TRANSFER_INITIATED':
			print('{}\tChecking if the coin transfers is complete'.format(datetime.datetime.now().strftime('%H:%M:%S')))
			verify_coin_transfers=True
			starttime=time.time()
			while verify_coin_transfers:
				exchange_1_balance = exchange_1.fetch_balance({'type':'account'})['DAI']['free']
				exchange_2_balance = exchange_2.fetch_balance()['XRP']['free']
				print('{}\tBalance in {} is:{}\nBalance in {} is:{}'.format(datetime.datetime.now().strftime('%H:%M:%S'), exchange_1.name,exchange_1_balance,exchange_2.name,exchange_2_balance))
				if exchange_1_balance>10 and exchange_2_balance > 300:
					bot_state = 'ARBITRAGE_COMPLETE'
					verify_coin_transfers=False
					print('Arbitrage trades successfully completed.')
				time.sleep(5.0 - ((time.time() - starttime) % 1.0))
		'''
			if  exchange_2_balance >= expected_no_of_coins:
				#TODO: Above is not a good check. Exchange wallet could have more coins.
				print("Arbitrage is complete")
				bot_state = 'BOT_READY_FOR_ARB'
			else:
				print("Coins have not yet reached selling exchange")
			
			bot_state = 'INITIATE_TRANSFER_OF_BTC_TO_BUYING_EXCHANGE'
		elif bot_state == 'INITIATE_TRANSFER_OF_BTC_TO_BUYING_EXCHANGE':
			print("Transfer BTC to the buying exchange")
			bot_state = 'BTC_TRANSFER_IN_PROCESS'
		elif bot_state == 'BTC_TRANSFER_IN_PROCESS':
			print("Check if BTC transfer is complete")
			bot_state = 'BTC_TRANSFER_COMPLETE'
		elif bot_state =='BTC_TRANSFER_COMPLETE':
			bot_state = 'BOT_READY_FOR_ARB'
		else:
			print("Unknown Bot State",bot_state)
		
		'''
		return bot_state