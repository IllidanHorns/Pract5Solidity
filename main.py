from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import address_contract, abi
from functions_eth import *
from flask import Flask, render_template, request, redirect, url_for

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=address_contract, abi=abi)

app = Flask(__name__)

actual_address = "adsfgafadfgdfdsfsd"

@app.route('/', methods=['GET', 'POST'])
def index():
    global actual_address
    if request.method == 'POST':
        address = request.form.get('username')
        password = request.form.get('password')
        if request.form["button"] == 'enter':
            if authorizathion(address, password) == True:
                actual_address = address
                return redirect(url_for('actions'))
            else:
                error = "Вы неправильно ввели адрес аккаунта или пароль!"
                return render_template("index.html", error=error)
    else: return render_template("index.html", error=None)

@app.route('/actions', methods=['GET', 'POST'])
def actions():
    action = None
    global actual_address
    if request.method == 'POST':
        if request.form['redirect'] == "create_estate":
            return render_template("actions.html", actual_address=actual_address, action='create_estate')
        elif request.form['redirect'] == 'create_adviresment':
            return render_template("actions.html", actual_address=actual_address, action='create_adviresment')
        elif request.form['redirect'] == 'change_estate_status':
            return render_template("actions.html", actual_address=actual_address, action='change_estate_status')
        elif request.form['redirect'] == 'change_adviresment_status':
            return render_template("actions.html", actual_address=actual_address, action='change_adviresment_status')
        elif request.form['redirect'] == 'buy_estate':
            return render_template("actions.html", actual_address=actual_address, action='buy_estate')
        elif request.form['redirect'] == 'withdraw_from_contract':
            return render_template("actions.html", actual_address=actual_address, action='withdraw_from_contract')
        elif request.form['redirect'] == 'all_estates':
            estates = get_estates(actual_address)
            if estates[0] == True:
                return render_template("actions.html", actual_address=actual_address, action='all_estates', estates = estates[2])
            else:
                return render_template("actions.html", actual_address=actual_address, action='all_estates', error = estates[1])
        elif request.form['redirect'] == 'all_adviresments':
            adviresments = get_advertisments(actual_address)
            if adviresments[0] == True:
                return render_template("actions.html", actual_address=actual_address, action='all_adviresments', adviresments = adviresments[2])
            else: 
                return render_template("actions.html", actual_address=actual_address, action='all_adviresments', error = adviresments[1])
        elif request.form['redirect'] == 'get_balance_contract':
            balance_contract = get_balance_contract(actual_address)
            if balance_contract[0] == True:
                return render_template("actions.html", actual_address=actual_address, action='get_balance_contract', balance_from_contract=balance_contract[1])
            else:
                return render_template("actions.html", actual_address=actual_address, action='get_balance_contract', error = balance_contract[1])
        elif request.form['redirect'] == 'get_balance_account':
            balance_account_ = get_balance_account(actual_address)
            if balance_account_[0] == True:
                return render_template("actions.html", actual_address=actual_address, action='get_balance_account', balance_from_account= balance_account_[1])
            else:
                return render_template("actions.html", actual_address=actual_address, action='get_balance_account', error = balance_account_[1])
        elif request.form['redirect'] == 'top_up_contract':
            return render_template("actions.html", actual_address=actual_address, action='top_up_contract')
        elif request.form['redirect'] == 'exit': 
            return redirect(url_for('index'))
        elif request.form['redirect'] == 'create_estate_real':
            estate_size = request.form.get('estate_size')
            estate_address = request.form.get('estate_address')
            estate_type = request.form.get('estate_type')
            estate = create_estate(actual_address, estate_size, estate_address, estate_type)
            if estate[0] == True:
                return render_template("actions.html", actual_address=actual_address, action='create_estate', good_result=estate[1])
            else:
                return render_template("actions.html", actual_address=actual_address, action='create_estate', error=estate[1])
            
        elif request.form['redirect'] == 'create_ad_real':
            buyer = request.form.get('buyer_ad')
            estate_id= request.form.get('id_estate_ad')
            estate_price = request.form.get('estate_price_ad')
            ad = create_advertisment(actual_address, buyer, estate_id, estate_price)
            if ad[0] == True:
                return render_template("actions.html", actual_address=actual_address, action='create_adviresment', good_result=ad[1])
            else:
                return render_template("actions.html", actual_address=actual_address, action='create_adviresment', error=ad[1])
            
        elif request.form['redirect'] == 'change_estate_status_real':
            estate_id = request.form.get('estate_id_enter')
            estate = change_status_estate(actual_address, estate_id)
            if estate[0] == True:
                return render_template("actions.html", actual_address=actual_address, action='change_estate_status', good_result=estate[1])
            else:
                return render_template("actions.html", actual_address=actual_address, action='change_estate_status', error=estate[1])
            
        elif request.form['redirect'] == 'change_ad_status_real':
            ad_id = request.form.get('ad_id_enter')
            ads = change_status_estate(actual_address, ad_id)
            if ads[0] == True:
                return render_template("actions.html", actual_address=actual_address, action='change_estate_status', good_result=ads[1])
            else:
                return render_template("actions.html", actual_address=actual_address, action='change_estate_status', error=ads[1])
        elif request.form['redirect'] == 'buy_estate_real':
            estate_id = request.form.get('estate_id_enter_buy')
            estate = buy_estate(actual_address, estate_id)
            if estate[0] == True:
                return render_template("actions.html", actual_address=actual_address, action='buy_estate', good_result=estate[1])
            else:
                return render_template("actions.html", actual_address=actual_address, action='buy_estate', error=estate[1])
        elif request.form['redirect'] == 'withdraw_from_contract_real':
            amount = request.form.get('amount_eth_withdraw')
            result = withdrawal_money(actual_address, amount)
            if result[0] == True:
                return render_template("actions.html", actual_address=actual_address, action='withdraw_from_contract', good_result=result[1])
            else:
                return render_template("actions.html", actual_address=actual_address, action='withdraw_from_contract', error=result[1])
        elif request.form['redirect'] == 'top_up_contract_real':
            amount = request.form.get('amount_eth_top_up')
            result = send_to_contract(actual_address, amount)
            if result[0] == True:
                return render_template("actions.html", actual_address=actual_address, action='top_up_contract', good_result=result[1])
            else:
                return render_template("actions.html", actual_address=actual_address, action='top_up_contract', error=result[1])
        else:
            pass
    else:
        return render_template("actions.html", actual_address=actual_address)
    

if __name__ == '__main__':
    app.run(debug=True)
