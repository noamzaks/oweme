from django.db.models.fields import mixins
from .models import Debts

def get_debts(bro, not_to):
    return Debts.objects.filter(one=bro, amount__gt=0).exclude(two=not_to) | Debts.objects.filter(two=bro, amount__lt=0).exclude(one=not_to)

def find_path(x, y):
    if x == y:
        return True
    for debt in get_debts(y,y):
        next = debt.one if debt.one != y else debt.two
        if (next == x):
            #print("Found")
            return True
    #print(f"Not connected: {x} {y}")
    return False
        
def eliminate(one, two, scanned):
    #print("checking")
    if find_path(one, two):
        #print(f"{two} owes {one}")
        return [one, two]
    for debt in get_debts(two, one):
        next_brother = debt.one if debt.one != two else debt.two
        if next_brother not in scanned:
            #print(next_brother)
            scanned.append(next_brother)
            path = find_path(next_brother, one)
            if path:
                #print(path)
                #print(f"returning: {one}, {two}, {next_brother}")
                return [one, two, next_brother]
    #print(scanned)
    for debt in get_debts(two, one):
        next_brother = debt.one if debt.one != two else debt.two
        #print(f"trying from {one} to {next_brother}")
        test = eliminate(one, next_brother, scanned)
        #print(f"{test}")
        if test:
            test.insert(1, two)
            #print(f"returning: {test}")
            return test
    return None
    
def check():
    a = Debts.objects.all().first().one
    b = Debts.objects.all()[2].one
    #print(a)
    #print(b)
    fix(a,b)

def fun(loop, i):
    return Debts.objects.filter(one=loop[i], two=loop[i+1]) | Debts.objects.filter(two=loop[i], one=loop[i+1])

def remove_circle(loop):
    mini = 999999 # max int
    for i in range(len(loop)-1):
        cost = fun(loop, i)
        if cost.exists():
            mini = min(mini, abs(cost.first().amount))
    x = (Debts.objects.filter(one=loop[-1], two=loop[0]) | Debts.objects.filter(two=loop[-1], one=loop[0])).first()
    mini = min(mini, x.amount)
    print(f"Removing {mini} from {loop}")
    for i in range(len(loop)-1):
        #print(i)
        t = fun(loop,i).first()
        if t:
            print(t)
            print(t.amount)
            if t.amount == mini:
                t.delete()
            else:
                t.amount -= mini
                t.save()
    x.amount -= mini
    if x.amount == 0:
        x.delete()
    else:
        x.save()
        
    return mini, loop


def fix(one, two):
    test = eliminate(one, two, [])
    #print(test)
    if test:
        return remove_circle(test)
    return None, None