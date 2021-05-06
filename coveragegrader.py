def f(a,b,c):
    x = (a+b+c)/3
    y = (10/60) * (x - 20)
    return max((0, min((10,y))))