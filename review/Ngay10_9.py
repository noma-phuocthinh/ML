def giaiphuong(a,b):
    '''
    Đây là phương trình bật một
    :param a: hệ số a
    :param b: hệ số b
    :return: nghiệm theo a,b
    '''

    if a==0 and b==0:
        return "vô số nghiệm"
    elif a==0 and b!=0:
        return "vô nghiệp"
    else:
        return -b/a

def fib(n):
    if n<=2:
        return n
    return fib(n-1) + fib(n-2)

def pick_fib(n):
    fi = fib(n)
    list_fib = []
    for i in range(1, n+1):
        f_item = fib(i)
        list_fib.append(f_item)
    return fi, list_fib

"""
k1 = giaiphuong(0,0)
k2= giaiphuong(0,1)
k3 = giaiphuong(1,12)
print(k1)
print(k2)
print(k3)
"""

x,y=pick_fib(6)
print(x)
print(y)