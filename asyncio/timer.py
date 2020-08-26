import timeit

def timer(number, repeate):
    def wrapper(func):
        runs = timeit.repeat(func, number=number, repeat=repeate)
        print (sum(runs)/len(runs))
    return wrapper