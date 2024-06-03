from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import address_contract, abi

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=address_contract, abi=abi)

basic_forms_of_password = ('qwerty', 'zxcvb', 'user', 'password', 'batman',
                           'superman', 'spiderman', 'admin', 
                           '123', '456', '789', '000', '111', 
                           'guest', 'baseball', 'football',
                           'dragon', 'master', 'mustang', 
                           'king', 'rossia', 'leningrad', 'stop',
                           'freedom', 'unknown', 'usa', 'sunshine',
                           'monkey', 'letmein', 'princess', 'iloveyou',
                           'hello', 'hallo', 'fickken', 'passwort', 
                           'dennis', 'killer', 'sommer', 'arshloch',
                           'privet', 'chocolat', 'coucou', 'azerty',
                           'bonjour', 'caramel', 'qwe', 'qaz', 'wsx',
                           '777', '1q2w3e', 'klaster', 'valentina',
                           'asd', 'soccer', 'prince', 'basketball',
                           'london', 'paris', 'moscow', 'piter', 'new-york',
                           'real-madrid', 'barcelona', '321', '666', '1488', 
                           'asdfgh', 'asdfg', 'qweert', 'ytrewq', '1945',
                           'none', 'word', 'zxc', 'lol', 'love')

def authorizathion(public_key, password):
        try:
            w3.geth.personal.unlock_account(public_key, password)
            return True
        except Exception as e:
            return False
        
def check_password(password:str):
    result = [False, ""]
    capital_letters = 0
    lowers_letters = 0
    numbers = 0
    special_symbols = 0

    for i in password:
        if (ord(i) in range(33,48)) or (ord(i) in range(58, 65)):
            special_symbols += 1
        if ord(i) in range(48, 58):
            numbers += 1
        if (ord(i) in range(65, 91)) or (192, 224):
            capital_letters += 1
        if (ord(i) in range(97,123)) or (ord(i) in range(224,256)):
            lowers_letters += 1
    
    if len(password) < 12:
        result[1] = "Длинна пароля менее 12 символов"
        return result
    elif capital_letters == 0:
        result[1] = "В пароле нет заглавных букв"
        return result
    elif lowers_letters == 0:
        result[1] = "В пароле нет строчных букв"
        return result
    elif numbers == 0:
        result[1] = "В пароле нет цифр"
        return result
    elif special_symbols == 0:
        result[1] = "В пароле нет специальных символов"
        return result

    for i in basic_forms_of_password:
        if i in password.lower():
            result[1] = "Содержит часто повторяющееся сочетание - " + i
            return result
        
    result[0] = True
    result[1] = "Пароль прошел проверку!"
    return result

def register():
    for i in range(1, 6):
        password_check_result = []
        password = input("Введите пароль: ")
        password_check_result = check_password(password)
        if (password_check_result[0] == True):
            account = w3.geth.personal.new_account(password)
            print(f"Ваш публичный ключ: {account}")
            return account
        else:
            print(password_check_result[1])
    
def send_eth(account, value_):
    result = [False, ""]
    try:
        value = int(value_)
        tx_hash = contract.functions.senEth().transcat({
            'from': account,
            'value': value,
        })
        result[0] = True
        result[1] = f"Ваша транзакция успешно отправлена. Хэш транзакции: {tx_hash.hex()}"
    except Exception as e:
        result[0] = False
        result[1] = f"Ошибка отправки WEI: {e}"

def create_estate(account, size, estate_address, estate_type):
    result = [False, ""]
    try:
        size = int(size)
        estate_type = int(estate_type)
    except:
        result[0] = False
        result[1] = 'Неправильно введены данные!'
        return result
    try:
        contract.functions.createEstate(size, estate_address, estate_type).transact(
            {'from' : account}
        )
        result[0] = True
        result[1] = f'Была успешно создана недвижимость по адресу {estate_address}'
        return result
    except Exception as e:
        result[0] = False
        result[1] = f'Ошибка создания недвижимости - {e}'
        return result

def create_advertisment(account, buyer, id_estate, price):
        result = [False, ""]
        try:
            id_estate = int(id_estate)
            price = int(price)
        except:
            result[0] = False
            result[1] = 'Неправильно введены данные!'
            return result
        try:
            contract.functions.createAd(buyer, id_estate, price).transact(
                {'from': account}
            )
            result[0] = True
            result[1] = f'Было успешно создано объявление по недвижимости с индексом {id_estate}'
        except Exception as e:
            result[0] = False
            result[1] = f'Ошибка создания объявления - {e}'
        return result

def change_status_estate(account, id_estate_):
    result = [False, '']
    try:
        id_estate = int(id_estate_)
    except:
        result[0] = False
        result[1] = 'Неправильно введены данные!'
        return result

    try:
        contract.functions.changeStatusEstate(id_estate).transact(
            {'from': account})
        result[0] = True
        result[1] = f'Статус недвижимости с индексом {id_estate} успешно поменялся!'
        return result
    except Exception as e:
        result[0] = False
        result[1] = f'Ошибка смены статуса - {e}'
        return result

def change_status_advertisment(account, id_ad_):
    result = [False, '']
    try:
        id_advertisment = int(id_ad_)
    except:
        result[0] = False
        result[1] = 'Неправильно введены данные!'
        return result
    try:
        contract.functions.changeStatusAd(id_advertisment).transact(
            {'from': account})
        result[0] = True
        result[1] = f'Статус объявления с индексом {id_ad_} успешно поменялся!'
        return result
    except Exception as e:
        result[0] = False
        result[1] = f'Ошибка смены статуса - {e}'
        return result

def buy_estate(account, id_ad_):
    result = [False, '']
    try:
        id_advertisment = int(id_ad_)
    except:
        result[0] = False
        result[1] = 'Неправильно введены данные!'
        return result
    try:
        contract.functions.buy_estate(id_advertisment).transact(
            {'from': account}
        )
        result[0] = True
        result[1] = 'Недвидимость по указанному объявлению была успешно куплена!'
        return result
    except Exception as e:
        result[0] = False
        result[1] = f'Ошибка покупки - {e}'
        return result   

def withdrawal_money(account, amount_of_eth):
    result = [False, '']
    try:
        count_of_eth = int(amount_of_eth)
    except:
        result[0] = False
        result[1] = 'Неправильно введены данные!'
        return result
    try:
        contract.functions.withDraw(count_of_eth).transact(
            {'from': account}
        )
        result[0] = True
        result[1] = 'Средства успешно сняты с контракта!'
        return result
    except Exception as e:
        result[0] = False
        result[1] = f'Ошибка снятия криптовалюты со смарт-контракта {e}'
        return result

def get_estates(account):
    result = [False, '', None]
    try:
        estates = contract.functions.getEstates().call(
            {'from': account})
        if len(estates) == 0:
            result[0] = False
            result[1] = "Список пуст!"
            return result
        else:
            result[0] = True
            result[1] = "Список недвижимости"
            result[2] = estates
            return result
    except Exception as e:
        result[0] = False
        result[1] = f'Ошибка вывода недвижимости - {e}'

def get_advertisments(account):
    result = [False, '', None]
    try:
        advertisments = contract.functions.getAds().call(
            {'from': account})
        if len(advertisments) == 0:
            result[0] = False
            result[1] = "Список пуст!"
            return result
        else:
            result[0] = True
            result[1] = "Список объявлений"
            result[2] = advertisments
            return result
        
    except Exception as e:
        result[0] = False
        result[1] = f'Ошибка вывода объявлений - {e}'
        return result

def get_balance_contract(account):
    result = [False, '']
    try:
        eth_on_contract = contract.functions.getBalance().call(
            {'from': account})
        result[0] = True
        result[1] = eth_on_contract
        return result
    except Exception as e:
        result [0] = False
        result[1] = f'Ошибка вывода баланса - {e}'
        return result

def get_balance_account(account):
    result = [False, '', None]
    try:
        balance = w3.eth.get_balance(account)
        result[0] = True
        result[1] = balance
        return result
    except Exception as e:
        result[0] = False
        result[1] = f'Ошибка вывода баланса - {e}'
        return result

def send_to_contract(account, count_of_eth_):
    result = [False, '']   
    try:
        count_of_eth = count_of_eth_
    except:
        result[0] = False
        result[1] = 'Неправильно введены данные!'
        return result

    try:
        contract.functions.send_to_contract().transact({
            'from' : account,
            'value' : count_of_eth
        })
        result[0] = True
        result[1] = f'Средства успешно отправлены на смарт-контракт!'
        return result
    except Exception as e:
        result[0] = False
        result[1] = f'Ошибка вывода информации - {e}'
        return result


































