# source: https://github.com/mskrotka/projekt/blob/main/zadania.py

# 1. Napisz funkcję, która przyjmie rok urodzenia, a następnie zwróci informację o tym, czy jest pełnoletni czy nie.
# UWAGA: Modyfikacja: z uwagi na fakt, iż napisano, że funkcja ma przyjmować rok urodzenia a nie wiek,
# zmodyfikowano zadanie podając do funkcji jako parametr rok urodzenia

#####################################################################################################################

import datetime
def check_adult(birth_year):
    current_year = datetime.datetime.now().year
    if current_year-birth_year>18:
        respond = "Pełnoletni"
    elif current_year<birth_year:
        respond = "Niepełnoletni, wciąż nienarodzony :)"
    else:
        respond = "Niepełnoletni"
    return print(respond)

check_adult(1999) # Pełnoletni
check_adult(2006) # Niepełnoletni
check_adult(2033) # błąd: "ujemny wiek"


# 2. Napisz funkcję, która zwraca listę wszystkich podzielnych przez n liczb z zakresu [1, 100].

def divisible(n):
    div_by_n = []
    try:
        for x in range(1,101):
            if x%n == 0:
                div_by_n.append(x)
        return print(div_by_n)
    except ZeroDivisionError:
        print("Nie dziel przez zero!")

divisible(3) # [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78,
# 81, 84, 87, 90, 93, 96, 99]
divisible(5) # [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
divisible(8) # [8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96]
divisible(0) # błąd: "div by 0"

# 3. Napisz funkcję, która przyjmuje kwotę (value) i jej walutę (currency), a następnie zwróci ile wart jest dana kwota
# w danej walucie w złotówkach.

def check_currency(value, currency):
    curr = [{
            "currency": "USD",
            "value": 4.56
        },{
            "currency": "CHF",
            "value": 5.03
        },{
            "currency": "EUR",
            "value": 4.9
        }
    ]
    while True:
        for pos in curr:
            if pos["currency"]==currency:
                exchange = pos['value']
                return print("Kwota {} {} po kursie {} {}/PLN jest warta {:.2f} PLN.".format(value, currency, exchange,
                                                                                             currency, value*exchange))
            else:
                continue
        print("Podanej waluty nie ma w kantorze.")
        break

check_currency(745, "CHF") # 3747,35 zł
check_currency(812.5, "USD") # 3705 zł
check_currency(18, "EUR") # 88,2 zł
check_currency(50, "GBP") # błąd: "no currency"
