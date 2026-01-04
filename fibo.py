def fib(n):
    
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)
    
def fac(p):
if p == 0:
    
return 1

else 
return p*fac(p-1)
def power(base, a, b):
    if a == 0:
    return 1
temp = power(base, a//2,b)
temp = (temp*temp)% b 
if a%2 == 0:
    return temp 
else: 
    return (trmp*base)% b
    
    