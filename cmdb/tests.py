from django.test import TestCase

# Create your tests here.


def ge():
    for i in range(10):
        yield i

for x in ge():
    print x

print "=============="

def ge(n):
    e = 0
    for i in range(n):
        yield e
        e = e+1


for x in ge(10):
    print x

print "+++++++++++++++++++++"
def fibon(n):
    a = b = 1
    for i in range(n):
        yield a
        a, b = b, a + b

for x in fibon(5):
    print x
