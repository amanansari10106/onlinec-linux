def fib(n):
    if n==1:
        return 1
    return n*fib(n-1)


global b
def numpalindrome(n):
    b=0
    z=n
    while(True):
        if n<10:
            b = (b*10)+n
            
            break
        a = n%10
        n = int(n/10)

        b = (b*10)+a
    if z==n:
        print("number is palindrome")
    else:
        print("number is not palindrome")
    return b

def armstrong(n):
    c=0
    z=n
    while True:
        if n<1:
            break
        n = int(n/10)
        c = c+1
    n =z
    sum =0
    while(True):
        if n<10:
            sum = sum + (n**c)
            print(sum)
            break
        r = n%10
        n = int(n/10)
        sum = sum + (r**c)

def sumofdigit(n):
    sum =0
    
    while(True):
        if n<10:
            sum = sum + n
            print(sum)
            break
        r = n%10
        n = int(n/10)
        sum = sum + r

def prime(n,i):
    if n==0 or n==1:
        return True
    
    if n == i:
        return True

    if n%i == 0:
        return False

    return prime(n, i+1)

def reversenum(n):
    b=0
    while(True):
        if n<10:
            b = (b*10)+n
            
            break
        a = n%10
        n = int(n/10)

        b = (b*10)+a
    print(b)
    return b
reversenum(100)

def smallest():
    a = input("enter the number")
    min =a
    for x in range(3):
        a = input("enter the number")
        if a<min:
            min =a
    print("smallest number is ", min)

# smallest()
def custom1():
    a = int(input("Enter a"))
    e = int(input("Enter e"))
    if a<0 or e<0:
        z=a
        a=e
        e=z
        print("a : ",a, "| e : ",e )
    print("the power is ",a**e)

custom1()
# b = int(input("Enter the number"))
# a = prime(b, 2)
# if(a):
#     print("number is prime")
# else:
#     print("number is not prime")

# sumofdigit(123)
# armstrong(211)
# p = numpalindrome(101)


# a = fib(3)
# print(a)