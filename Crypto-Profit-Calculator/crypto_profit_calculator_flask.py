from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Function to get real-time crypto price
def get_crypto_price(crypto="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd"
    response = requests.get(url).json()
    return response.get(crypto, {}).get("usd", None)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        buy_price = float(request.form['buy_price'])
        sell_price = float(request.form['sell_price'])
        investment = float(request.form['investment'])
        
        quantity = investment / buy_price
        total_sell_value = quantity * sell_price
        profit_loss = total_sell_value - investment
        percentage = (profit_loss / investment) * 100

        return jsonify({
            "profit_loss": round(profit_loss, 2),
            "percentage": round(percentage, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/get_price', methods=['GET'])
def get_price():
    crypto = request.args.get('crypto', 'bitcoin')
    price = get_crypto_price(crypto)
    return jsonify({"crypto": crypto, "price": price})

if __name__ == '__main__':
    app.run(debug=True)
