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

def authorizathion():
    for i in range(1, 6):
        public_key = input("Введите ваш публичный ключ: ")
        password = input("Введите пароль: ")
        try:
            w3.geth.personal.unlock_account(public_key, password)
            print("Авторизация прошла успешно!")
            return public_key
        except Exception as e:
            print(f"Ошибка авторизации: {e}")
    
def send_eth(account):
    try:
        value = int(input("Введите кол-во WEI для отправки: "))
        tx_hash = contract.functions.senEth().transcat({
            'from': account,
            'value': value,
        })

        print(f"Ваша транзакция успешно отправлена. Хэш транзакции: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка отправки WEI: {e}")

def create_estate(account):
    try:
        size = int(input("Площадь кв. м. - "))
        estate_address = input("Адрес - ")
        print('0. House \n 1. Flat \n 2. Loft')
        estate_type = int(input("Индекс типа недвижимости - "))
        if estate_type < 0 or estate_type > 2:
            print("Такого типа недвижимости нет!")
            return None
    except:
        print('Данные введены неверно!')
        return None
    
    try:
        contract.functions.createEstate(size, estate_address, estate_type).transact(
            {'from' : account}
        )
        print(f'Была успешно создана недвижимость по адресу {estate_address}')
    except Exception as e:
        print(f'Ошибка создания недвижимости: {e}')

def create_advertisment(account):
        try:
            buyer = input("Покупатель - ")
            id_estate = int(input("Индекс недвижимости - "))
            price = int(input("Цена - "))
        except:
            print('Данные введены неверно!')
            return None
        
        try:
            contract.functions.createAd(buyer, id_estate, price).transact(
                {'from': account}
            )
        except Exception as e:
            print(f'Ошибка создания объявления: {e}')


def change_status_estate(account):
    try:
        id_estate = int(input("Индекс недвижимости - "))
    except:
        print("Ошибка ввода данных!")

    try:
        contract.functions.changeStatusEstate(id_estate).transact(
            {'from': account})
        print('Статус недвижимости успешно поменялся!')
    except Exception as e:
        print(f'Ошибка смены статуса - {e}')

def change_status_advertisment(account):
    try:
        id_advertisment = int(input("Индекс объявления - "))
    except:
        print("Ошибка ввода данных!")

    try:
        contract.functions.changeStatusAd(id_advertisment).transact(
            {'from': account})
        print('Статус объявления успешно поменялся!')
    except Exception as e:
        print(f'Ошибка смены статуса - {e}')

def buy_estate(account):
    try:
        id_advertisment = int(input("Индекс объявления - "))
    except:
        print("Ошибка ввода данных!")

    try:
        contract.functions.buy_estate(id_advertisment).transact(
            {'from': account}
        )
        print('Недвидимость по указанному объявлению была успешно куплена!')
    except Exception as e:
        print(f'Ошибка покупки недвижимости: {e}')
        
        

def withdrawal_money(account):
    try:
        count_of_eth = int(input("Кол-во WEI для отправки - "))
    except:
        print("Ошибка ввода данных!")

    try:
        contract.functions.withDraw(count_of_eth).transact(
            {'from': account}
        )
        print('Средства успешно сняты с контракта!')
    except Exception as e:
        print(f'Ошибка снятия криптовалюты со смарт-контракта {e}')

def get_estates(account):
    try:
        estates = contract.functions.getEstates().call(
            {'from': account})
        if len(estates) == 0:
            print("Список пуст!")
            return estates
        
        for i in estates:
            print(f"Площадь - {i[0]} Адрес - {i[1]} Владелец - {i[2]} Тип - {i[3]} Владелец - {i[2]}")
        
        return estates
    except Exception as e:
        print(f'Ошибка вывода недвижимости - {e}')

def get_advertisments(account):
    try:
        advertisments = contract.functions.getAds().call(
            {'from': account})
        if len(advertisments) == 0:
            print("Список пуст!")
            return advertisments
        for i in advertisments:
            print(i)
    except Exception as e:
        print(f'Ошибка вывода объявлений - {e}')

def get_balance_contract(account):
    try:
        eth_on_contract = contract.functions.getBalance().call(
            {'from': account})
        print(f'Кол-во WEI на контракте - {eth_on_contract}')
    except Exception as e:
        print(f'Ошибка вывода баланса - {e}')

def get_balance_account(account):
    try:
        balance = w3.eth.get_balance(account)
        print(f'Баланс аккаунта WEI - {balance}')
    except Exception as e:
        print(f'Ошибка вывода информации - {e}')

def send_to_contract(account):
    try:
        count_of_eth = int(input("Кол-во WEI для отправки на контракт - "))
    except:
        print("Ошибка ввода данных!") 

    try:
        contract.functions.send_to_contract().transact({
            'from' : account,
            'value' : count_of_eth
        })
    except Exception as e:
        print(f'Ошибка вывода информации - {e}')

def main():
    change_user = -1
    current_account = ' '
    while(change_user != 0):
        check = True
        print('Выберите действие: \n \
              1. Регистрация \n \
              2. Вход \n \
              3. Создать недвижимость \n \
              4. Создать объявление \n \
              5. Изменить статус недвижимости \n \
              6. Изменить статус объявления \n \
              7. Купить недвижимость \n \
              8. Вывести средства \n \
              9. Список всей недвижимости \n \
              10. Список всех объявлений \n \
              11. Баланс на смарт-контракте \n \
              12. Баланс ка аккаунте \n \
              13. Вывести WEI на контракт \n \
              0. Выход')
        try:
            change_user = int(input())
        except:
            print('Вы неправильно ввели данные! Нужно ввести число.')
            check = False
        if (check == True):
            if (change_user == 0):
                print('Сессия закончена!')
                break
            elif (change_user == 1):
                current_account = register()
            elif (change_user == 2):
                current_account  = authorizathion()

            if current_account != ' ':
                if (change_user == 3):
                    create_estate(current_account)
                elif (change_user == 4):
                    create_advertisment(current_account)
                elif (change_user == 5):
                    change_status_estate(current_account)
                elif (change_user == 6):
                    change_status_advertisment(current_account)
                elif (change_user == 7):
                    buy_estate(current_account)
                elif (change_user == 8):
                    withdrawal_money(current_account)
                elif (change_user == 9):
                    get_estates(current_account)
                elif (change_user == 10):
                    get_advertisments(current_account)
                elif (change_user == 11):
                    get_balance_contract(current_account)
                elif (change_user == 12):
                    get_balance_account(current_account)
                elif (change_user == 13):
                    send_to_contract(current_account)
            else:
                print("Аккаунт еще не введён!")

if __name__ == "__main__":
    main()