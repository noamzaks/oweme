def minExcess(coins, price):
    if sum(coins) < price:
        return [-1, [[]]]
    else:
        usedCoins = []
        return minExcessRec(sorted(coins), price, usedCoins)


def minExcessRec(coins, price, usedCoins):
    if (price <= 0):
        # print(str(-price)+str(usedCoins))
        return [-price, [usedCoins + []]]
    if (len(coins) == 0):
        return [9999999, [[]]]  # change to max int
    usedCoins.append(coins[0])
    a = minExcessRec(coins[1:len(coins)], price - coins[0], usedCoins)
    usedCoins.pop()
    b = minExcessRec(coins[1:len(coins)], price, usedCoins)
    return min(a, b)


def min(a, b):
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


a = [20, 20, 10, 50, 20, 50 ,100]
print(minExcess(a, 120))


def howToPay(users, debts, wallets,bills):
    allCoins = []
    for coins in wallets.values():
        allCoins += coins
    totalPrice=0
    for bill in bills.values:
        totalPrice += bill
    minExcess = minExcess(allCoins,totalPrice)
    if minExcess[0] == -1:
        return -1 # Not Enough Money


def optionsToPayWithCoins(wallets,coins):
