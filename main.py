from flask import Flask, render_template, request
import json
import cry_arb

app = Flask(__name__)

@app.route('/hello')
def hello():
	"""Return a friendly HTTP greeting."""
	return 'Hello World!'

@app.route('/', methods=['GET', 'POST'])
def dashboard():
	'''
	coin_quantity = 80000
	ae = cry_arb.detect_arb('direct')
	arb_result = ae.detect_opportunities(coin_quantity)'''
	arb_result ={
	"base_coin":0,
	"coin_quantity":0,
	"exchange_1":0,
	"exchange_2":0,
	"ex1_coin_pair":0,
	"ex2_coin_pair":0,
	"exchange1_price":0,
	"exchange2_price":0,
	"capital_invested":0,
	"capital_recieved":0,
	"spread":0,
	"arb_return":0
	}
	return render_template('dashboard.html', **arb_result)

@app.route('/_add_numbers')
def add_numbers():
	capitalAllocated = request.args.get('capitalAllocated', 0, type=int)
	ae = cry_arb.detect_arb('direct')
	arb_results = ae.detect_opportunities(capitalAllocated)
	#a = request.args.get('a', 0, type=int)
	b = request.args.get('b', 0, type=int)
	return json.dumps(arb_results)

if __name__ == '__main__':
	app.run(host='0.0.0.0')