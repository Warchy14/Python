def fibo(n):
    n = int(n)
    tab = range(0,n)
    if n <= 1:
        return n
    elif n >= 2:
        tab [0] = 1
        tab [1] = 1 
        for i in range (2,n):
            tab [i] = tab [i-1] + tab[i-2]
        for x in range (0,n):
            print tab[x]

z = input("Nombre maximum : ")
print fibo(z)
