#! /usr/bin/python
import numpy as np

from Matrix import Matrix
from time import time

a=Matrix(2,[[3,2],[3,4]],[2,3],0.000001,1)
t=time()

a.methodGaus()
print(a.getAnswer())

print(time()-t)
t=time()
a=Matrix(2,[[3,2],[3,4]],[2,3],0.000001,1)
a.methodJacobi();
print(a.getAnswer())
print(time()-t)

a=Matrix(2,[[3,2],[3,4]],[2,3],0.000001,4)
t=time()
a.methodJacobiPrallel();
print(a.getAnswer())
print(time()-t)
l=[]
n=1000
a=np.random.sample((n,n))
b=np.random.sample(n)
a*100;b*100
a=list(a);b=list(b)
for i in range(65):
    m = Matrix(n,a,b, 0.0001, i)
    t = time()
    m.methodJacobiPrallel()
    l.append(time() - t)
print(l)
print(min(l),l.index(min(l)))