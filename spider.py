from flask import Flask
from flask import render_template
from main import stock

app = Flask(__name__)

app.register_blueprint(stock.stock)

@app.route('/')
def Stock():
	return render_template('Stock.html')


if __name__ == '__main__':
	app.run(host = '0.0.0.0', debug = True)

