import copy
import decimal
from .models import Debts

# temp for test
my_new_debts = []

def minExcess(coins, price):
    if sum(coins) < price:
        return [-1, [[]]]
    else:
        usedCoins = []
        return minExcessRec(sorted(coins), price, usedCoins)


def minExcessRec(coins, price, usedCoins):
    if (price <= 0):
        # print(str(-price)+str(usedCoins))
        return [-price, [usedCoins + []]]  # by value
    if (len(coins) == 0):
        return [9999999, [[]]]  # change to max int
    usedCoins.append(coins[0])
    a = minExcessRec(coins[1:len(coins)], float(price) - float(coins[0]), usedCoins)
    usedCoins.pop()
    b = minExcessRec(coins[1:len(coins)], price, usedCoins)
    return minUnitListed(a, b)


def minUnitListed(a, b):
    if a[0] == b[0]:
        unitSortedLists(a[1], b[1])
    if a[0] <= b[0]:
        return a
    return b


def sum(list):
    c = 0
    for i in list:
        c += i
    return c


def unitSortedLists(lists1, lists2):
    for l2 in lists2:
        if l2 not in lists1:
            lists1.append(l2)


def howToPay(users, debts, wallets, bills):  # winningDebtsForUser is empty dict
    winningOption = dict()
    winningDebtsForUserTest = dict()
    allCoins = []
    minDebt = 999999  # change to max int
    for coins in wallets.values():
        allCoins += coins
    totalPrice = 0
    for bill in bills.values():
        totalPrice += bill
    CoinsMinExcess = minExcess(allCoins, totalPrice)
    if CoinsMinExcess[0] == -1:
        return -1  # Not Enough Money
    debtsForUser = initDict(users, 0)
    for debt in debts:
        debtsForUser[debt.one] += debt.amount
        debtsForUser[debt.two] -= debt.amount

    allOptions = []
    for coinsToPay in CoinsMinExcess[1]:
        allOptions += optionsToPayWithCoins(wallets, coinsToPay)
    for option in allOptions:
        temp = calNewDebt(users, debtsForUser, option, bills)
        if temp < minDebt:
            minDebt = temp
            winningOption = option
            winningDebtsForUser = newDebtsForUser(users, debtsForUser, winningOption, bills)
            global my_new_debts
            my_new_debts = []
            winingDebts = newDebts(winningDebtsForUser)
    return [winningOption, winingDebts[0], winingDebts[1]]


def optionsToPayWithCoins(wallets, coinsToPay):
    newWallets = dict()  # maybe change to newWallets=initDict(user,[])
    for user in wallets:
        newWallets[user] = []
    options = []
    optionsToPayWithCoinsRec(wallets, coinsToPay, newWallets, options)
    return options


def optionsToPayWithCoinsRec(wallets, coinsToPay, newWallets, options):  # newWallets is dict user->[] (empty list)
    if len(coinsToPay) == 0:
        options.append(copy.deepcopy(newWallets))  # pass copy
        # print("options:" + str(options))    #for debug
        return
    usersCanPay = False
    for user in wallets:  # run on key (users)
        # print("wallets: " + str(wallets))  #for debug
        # print("coins:  " +str(coinsToPay))  #for debug
        if coinsToPay[0] in wallets[user]:
            usersCanPay = True
            wallets[user].remove(coinsToPay[0])
            newWallets[user].append(coinsToPay[0])
            optionsToPayWithCoinsRec(wallets, coinsToPay[1:], newWallets, options)
            wallets[user].append(coinsToPay[0])
            newWallets[user].remove(coinsToPay[0])
    if not usersCanPay:
        return


def newDebtsForUser(users, debtsForUser, optionToPay, bills):
    re = initDict(users, 0)
    for user in users:
        paid = 0
        for coin in optionToPay[user]:
            paid += coin
        re[user] += float(paid) - float(bills[user]) - float(debtsForUser[user])
    return copy.deepcopy(re)


def calNewDebt(users, debtsForUser, optionToPay, bills):  # debtsForUser is dict per user how meny dolars owe users
    sumOfDebt = 0
    for user in users:
        paid = 0
        for coin in optionToPay[user]:
            paid += coin
        sumOfDebt += abs(float(paid) - float(bills[user]) - float(debtsForUser[user]))
    return sumOfDebt



def newDebts(debtsForUser):
    global my_new_debts
    for userI in debtsForUser:
        if debtsForUser[userI] != 0:
            for userJ in debtsForUser:
                if debtsForUser[userJ] != 0:
                    if sign(debtsForUser[userI]) != sign(debtsForUser[userJ]):
                        if debtsForUser[userI] < debtsForUser[userJ]:
                            one = userJ
                            two = userI
                        else:
                            one = userI
                            two = userJ
                        amount = min(abs(debtsForUser[userI]), abs(debtsForUser[userJ]))
                        
                        if amount!=0:
                            newDebt = Debts(one=one, two=two, amount=amount)
                            newDebt.save()
                            my_new_debts.append(newDebt)
                            # print(len(debts))
                            debtsForUser[one] -= amount
                            debtsForUser[two] += amount
    m = maxList(list(debtsForUser.values()))
    for user in debtsForUser.keys():
        if debtsForUser[user] == m:
            userGetExcess = user
    for user in debtsForUser:
        if user != userGetExcess and debtsForUser[user]:
            newDebt = Debts(one=userGetExcess, two=user, amount=debtsForUser[user])
            newDebt.save()
            my_new_debts.append(newDebt)
    return [my_new_debts, userGetExcess]


def min(a, b):
    if (a < b):
        return a
    return b


def abs(a):
    if a > 0:
        return a
    return -a


def sign(a):
    if a > 0:
        return 1
    if a < 0:
        return -1
    return 0


def initDict(keys, value):
    d = dict()
    for k in keys:
        d[k] = value
    return d

def maxList(l):
    m = l[0]
    for i in l:
        if i > m:
            m = i
    return m