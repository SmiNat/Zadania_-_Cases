# source: https://github.com/mskrotka/projekt/blob/main/zadania.py

# # Potrzebujemy przeliczyć trochę waluty, czasy niepewne,
# # warto mieć na uwadze swoją ulubioną walutę.
# # Napisz klasę, która będzie zawierać dwie metody:
#
# #       przeliczenie wybranej waluty z tabeli A na złotówki  <- dane wejściowe: kod waluty, ilość waluty
# #       wskazanie aktualnego kursu z tabeli A <- dane wejściowe: kod waluty
#
# # Klasa w celu przeliczenia waluty powinna skorzystać z aktualnych kursów z Narodowego Banku Polskiego
# # dokumentację API dla NBP znajdziesz pod adresem http://api.nbp.pl/

######################################################################################################################

# komentarz do wykonania:
# wymagane elementy: metoda current_avg_price i metoda to_pln
# pozostałe elementy: bonus :)

######################################################################################################################

import json
import requests


class Currency():
    '''Converts given currency to Polish zloty according to actual NBP's average exchange rate - https://api.nbp.pl/'''

    nbp_database = []   # database consistent of table A and table B (current average exchange rates)
    
    def __init__(self, currency_code: str, amount: int | float = 1):
        '''Exchange rates expressed in Polish zloty (PLN).

        Parameters:
        ----------
        currency_code: str
            ISO_4217 standard three-letter "alphabetic code" for given currency
        amount: int or float, optional
            Amount of currency, default: 1.

        For list of ISO_4217 currency codes see: https://en.wikipedia.org/wiki/ISO_4217'''

        self.currency = currency_code
        self.amount = amount

        # Loading data from NBP website.
        # Data loaded: average exchange rates form current table A and current table B
        # for currencies listed in NBP website.
        response1 = requests.get(r"https://api.nbp.pl/api/exchangerates/tables/A/?format=json")
        content1 = response1.content
        tableA = json.loads(content1)
        response2 = requests.get(r"https://api.nbp.pl/api/exchangerates/tables/B/?format=json")
        content2 = response2.content
        tableB = json.loads(content2)

        list_A = tableA[0]['rates']
        list_B = tableB[0]['rates']

        database = list_A + list_B
        Currency.nbp_database.extend(database)

        
    def __str__(self) -> str:
        '''Short information on the object.'''
        return f"Currency class object. Currency code: {self.currency}. Amount: {self.amount}"

    
    def update_database(self) -> None:
        '''Reload data from NBP website.
        For the purpose of updating database to current exchange rates.

        The currency database (NBP'S table A and table B) is being loaded at the moment of creating class object.
        The average exchange rates listed on table A and table B can vary between the time of loading the data at the
        initialization of class object and the actual time of using one of methods that uses exchange rates stored
        in created database.
        This method allows to update database at any time without the purpose of creating new class object.'''
        response1 = requests.get(r"https://api.nbp.pl/api/exchangerates/tables/A/?format=json")
        content1 = response1.content
        tableA = json.loads(content1)
        response2 = requests.get(r"https://api.nbp.pl/api/exchangerates/tables/B/?format=json")
        content2 = response2.content
        tableB = json.loads(content2)

        list_A = tableA[0]['rates']
        list_B = tableB[0]['rates']

        database_update = list_A + list_B
        Currency.nbp_database = database_update
    
    
    def nbp_code_database(self) -> dict[str]:
        '''Return information on codes (keys) and currencies (values) in form of a dictionary.
        Dictionary contains only currencies available in NBP's databases.'''
        available_currencies = {}
        for data in self.nbp_database:
            available_currencies[data['code']] = data['currency']
        available_currencies = dict(sorted(available_currencies.items()))
        return available_currencies


    def nbp_list_of_codes(self) -> None:
        '''Convert data from nbp_code_database method into string lines of code-currency data.'''
        print("Code: \t\tCurrency:")
        for key, value in self.nbp_code_database().items():
            print(f"{key} \t-\t{value}")


    def code_information(self, currency_code: str | None = None) -> str:
        '''Return currency name based on given currency code.

        Parameters:
        ----------
        currency_code: str, optional
            ISO_4217 standard three-letter "alphabetic code" for given currency. Default None.

        Only returns currency name if listed in NBP's database.'''
        if currency_code == None:
            currency_code = self.currency
        if currency_code in self.nbp_code_database().keys():
            for currency in self.nbp_database:
                if currency["code"] == currency_code:
                    return currency['currency']
        else:
            return "Invalid currency code"


    def current_avg_price(self, currency_code: str | None = None) -> float | str:
        '''Return current average price for given currency code.

        Parameters:
        ----------
        currency_code: str, optional
            ISO_4217 standard three-letter "alphabetic code" for given currency. Default None.

        Only returns average price if currency is listed in NBP's database.'''
        if currency_code == None:
            currency_code = self.currency
        if currency_code in self.nbp_code_database().keys():
            for currency in self.nbp_database:
                if currency["code"] == currency_code:
                    return currency['mid']
        else:
            return "Invalid currency code"


    def to_pln(self, amount:int|float|None = None, currency_code: str | None = None) -> float | str:
        '''Convert given currency to polish zloty (according to current average exchange rate).

        Parameters:
        ----------
        amount: int or float, optional
            Amount of currency, default: 1.
        currency_code: str, optional
            ISO_4217 standard three-letter "alphabetic code" for given currency. Default None.

        Only returns converted value if currency is listed in NBP's database'''
        if currency_code == None:
            currency_code = self.currency
        if amount == None:
            amount = self.amount
        if self.current_avg_price(currency_code) == "Invalid currency code":
            return "Invalid currency code"
        else:
            return self.current_avg_price(currency_code)*amount


    def bid_ask_price(self, currency_code: str | None = None) -> dict | str:
        '''Return bid/ask price for given currency.

        Parameters:
        ----------
        currency_code: str, optional
            ISO_4217 standard three-letter "alphabetic code" for given currency. Default None.

        Only returns bid/ask price if currency is listed in NBP's database (table C).'''
        if currency_code == None:
            currency_code = self.currency
        quote = {}
        response = requests.get(f"https://api.nbp.pl/api/exchangerates/rates/C/{currency_code.lower()}/?format=json")
        if response.status_code == 200:
            content = response.content
            exchange_rate_mid = json.loads(content)
            quote['bid'] = exchange_rate_mid["rates"][0]["bid"]
            quote['ask'] = exchange_rate_mid["rates"][0]["ask"]
            return quote
        else:
            return f"Unavailable bid/ask price for code: '{currency_code}'"


#####################################################################################################################

# TESTS:
# euro = Currency("EUR")
# lib = Currency(amount=10, currency_code="LBP")
# xxx = Currency("XXX")
# usd = Currency("USD", 50)
#
# print(usd.amount)
# print(xxx.amount)
#
# print(euro.currency)
# print(lib.currency)
# print(xxx.currency)
# print(usd.currency)
# print()
#
# print(euro.code_information())
# print(lib.code_information())
# print(xxx.code_information())
# print(usd.code_information())
# print(usd.code_information("EUR"))
# print(xxx.code_information("GBP"))
# print()
#
# print(euro.current_avg_price())
# print(lib.current_avg_price())
# print(xxx.current_avg_price())
# print(usd.current_avg_price())
# print(usd.current_avg_price("EUR"))
# print(xxx.code_information("GBP"))
# print()
#
# print(euro.to_pln(100))
# print(lib.to_pln(100))
# print(usd.to_pln(100))
# print(xxx.to_pln(100))
# # print(usd.to_pln('sto'))  # expected error
# print(euro.to_pln())
# print(lib.to_pln())
# print(xxx.to_pln())
# print(usd.to_pln())
# print(usd.to_pln(currency_code="EUR"))
# print(usd.to_pln(currency_code="EUR", amount=100))
# print(xxx.to_pln(50, "EUR"))
# print(euro.to_pln(50))
# print(lib.to_pln(currency_code="EUR"))
# print(lib.to_pln(1, "EUR"))
# print(usd.to_pln(10, "XXX"))
# print(xxx.to_pln(10, "EUR"))
# print()
#
# print(euro.bid_ask_price())
# print(lib.bid_ask_price())
# print(xxx.bid_ask_price())
# print(usd.bid_ask_price())
# print(usd.bid_ask_price("XXX"))
# print(xxx.bid_ask_price("EUR"))
# print()
#
# print(xxx.nbp_code_database())
# print()
#
# print(xxx.nbp_list_of_codes())

