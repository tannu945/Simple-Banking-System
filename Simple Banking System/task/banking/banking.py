# Write your code here
import random
import sqlite3


conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS card;")
conn.commit()
create_query = """CREATE TABLE IF NOT EXISTS card (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            number TEXT NOT NULL UNIQUE,
                            pin text NOT NULL,
                            balance INTEGER DEFAULT 0);"""
cur.execute(create_query)
conn.commit()
cur.close()


#dbms connectivity
def save_acc(card, pin):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    insert_query = "INSERT INTO card(number, pin) values({}, {});".format(card, pin)
    cur.execute(insert_query)
    conn.commit()
    cur.close()

def load_acc(number, pin):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    select_query = "SELECT * FROM card WHERE number = {} AND pin = {};".format(number, pin)
    cur.execute(select_query)
    result = cur.fetchone()
    cur.close()
    return result

def update_income(number, pin, balance):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    money = balance_(number, pin) + int(balance)
    #y = ''.join(map(str, money))
    cur.execute("UPDATE card SET balance = ? WHERE number = ? AND pin = ?", (money, number, pin))
    conn.commit()
    cur.close()
    print("Income was added!")

def balance_(number, pin):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("SELECT balance FROM card WHERE number = {} AND pin = {};".format(number, pin))
    amt = cur.fetchone()
    cur.close()
    y = int(''.join(map(str, amt)))
    return y

def dest_balance(dest_number):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("SELECT balance FROM card WHERE number = {};".format(dest_number))
    dest_balance = cur.fetchone()
    cur.close()
    des = int(''.join(map(str, dest_balance)))
    return des

def update_balance(number, pin, balance):
    amt = balance_(number, pin)
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    amt_ = str(amt - int(balance))
    cur.execute("UPDATE card SET balance = {} WHERE number = {} AND pin = {};".format(amt_, number, pin))
    conn.commit()
    cur.close()

def update_des_balance(balance, number):
    amt = dest_balance(number)
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    amt_ = str(int(balance) + amt)
    cur.execute("UPDATE card SET balance = {} WHERE number = {};".format(amt_, number))
    conn.commit()
    cur.close()

def transfer(number, number1, pin):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("SELECT number FROM card ;")
    result = cur.fetchall()
    cur.close()
    string = []
    for i in result:
        for res in i:
            string.append(''.join(res))

    if check_luhn(number):

        if number in string:

            if number == number1:
                print("You can't transfer money to same account.")
            else:
                amt = input("Enter how much money you want to transfer:\n")
                x = balance_(number1, pin)
                if int(amt) < x or int(amt) == x:
                    update_balance(number1, pin, amt)
                    update_des_balance(amt, number)
                    print("Success!")
                else:
                    print("Not enough Money!")
        else:
            print("Such card does not exist")
    else:
        print("Probably you made a mistake in the card number. Please try again!")


def close_account(number):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("DELETE FROM card WHERE number = {};".format(number))
    conn.commit()
    cur.close()
    print("The account has been closed!")


#luhn algo
def luhn_algo(number):
    card1 = [int(a) for a in str(number)]
    card2 = [int(a) for a in str(number)]
    length = len(card1)
    for i in range(length):
        if i % 2 == 0:
            card1[i] *= 2
        if card1[i] > 9:
            card1[i] -= 9
    sum = 0
    dif =0
    for i in range(length):
        sum += card1[i]
    if sum % 10 != 0:
        rem = sum % 10
        dif = 10 - rem
    card2.append(dif)
    return card2

def check_luhn(cardNo):
    nDigits = len(cardNo)
    nSum = 0
    isSecond = False

    for i in range(nDigits - 1, -1, -1):
        d = ord(cardNo[i]) - ord('0')

        if (isSecond == True):
            d = d * 2

        # We add two digits to handle
        # cases that make two digits after
        # doubling
        nSum += d // 10
        nSum += d % 10

        isSecond = not isSecond

    if (nSum % 10 == 0):
        return True
    else:
        return False

card_number = 0
pin = 0
count = 0
input_pin = 0
input_card = 0
choice_login =0
id_ = 0
while True:
    print("""1. Create an account
2. Log into account
0. Exit""")
    choice = int(input())
    count += 1
    if choice == 1:
        card_number = luhn_algo(random.randint(400000000000000, 400000999999999))
        card_number1 = ''.join(map(str, card_number))
        pin = random.randint(0000, 9999)
        save_acc(card_number1, pin)
        print("Your card has been created")
        print("Your card number:")
        print(card_number1)
        print("Your card PIN:")
        print(pin)

    elif choice == 2:
        while True:
            input_card = input("Enter your card number:\n")
#input_pin = int(input("Enter your PIN:\n"))
            if int(input_card) == 0:
                print("Bye!")
                break
            input_pin = int(input("Enter your PIN:\n"))
            if input_pin == 0:
                print("Bye!")
                break
            acc_ = load_acc(input_card, input_pin)
            if acc_:
                print("You have successfully logged in!")
                while True:
                    print("""1. Balance
                    2. Add income
                    3. Do transfer
                    4. Close account
                    5. Log out
                    0. Exit""")
                    choice_login = int(input())
                    if choice_login == 1:
                        print("Balance: {}".format(balance_(input_card, input_pin)))
                    elif choice_login == 2:
                        money = input("Enter income:\n")
                        update_income(input_card, input_pin, money)
                        #print("Income was added!")
                    elif choice_login == 3:
                        print("Transfer")
                        transfer_money = input("Enter card number:\n")
                        transfer(transfer_money, input_card, input_pin)
                    elif choice_login == 4:
                        close_account(input_card)
                        break
                    elif choice_login == 5:
                        print("You have successfully logged out!")
                        break
                    elif choice_login == 0:
                        print("Bye!")
                        break
                if choice_login == 0 or choice_login == 4 or choice_login == 5:
                    break
            else:
                print("Wrong card number or PIN!")
        if int(input_card) == 0 or input_pin == 0 or choice_login == 0 or choice_login == 5:
            break
    elif choice == 0:
        print("Bye!")
        break

