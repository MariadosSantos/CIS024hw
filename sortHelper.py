def sortNumbers(x):
    return sorted(x)

def myNumsort(x):
    for a in range(len(x)):
        for b in range(len(x)-1):
            if x[b]>x[b+1]:
                x[b],x[b+1]=x[b+1],x[b]
    return x

