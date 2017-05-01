import FAdo.fio as fio
from FAdo.fa import *
import FAdo.codes as codes
import FAdo.fl as fl

N = 5
ell = 8
s=2
n=2000
#
t2s = fio.readOneFromString('@Transducer 0 1 2 * 0\n0 0 0 0\n0 1 1 0\n0 0 1 1\n0 1 0 1\n1 0 0 1\n1 1 1 1\n1 0 1 2\n1 1 0 2\n2 0 0 2\n2 1 1 2\n')
#
t2id = fio.readOneFromString('@Transducer 0 1 2 * 0\n0 0 0 0\n0 1 1 0\n0 0 @epsilon 1\n0 1 @epsilon 1\n0 @epsilon 0 1\n0 @epsilon 1 1\n1 0 0 1\n1 1 1 1\n1 0 @epsilon 2\n1 1 @epsilon 2\n1 @epsilon 0 2\n1 @epsilon 1 2\n2 0 0 2\n2 1 1 2\n')
#
t1d_ieee = fio.readOneFromString('@Transducer 0 2 * 0\n0 0 0 0\n0 1 1 0\n0 0 @epsilon 1\n0 1 @epsilon 1\n1 0 0 1\n1 1 1 1\n1 @epsilon 0 2\n1 @epsilon 1 2\n')
#
t2s_ia = fio.readOneFromString('@Transducer 1 2 * 0\n0 0 0 0\n0 1 1 0\n0 0 1 1\n0 1 0 1\n1 0 0 1\n1 1 1 1\n1 0 1 2\n1 1 0 2\n2 0 0 2\n2 1 1 2\n')

print
p = codes.ErrDetectProp(t2s)     # ErrDetectProp is same as IPTProp
a, W = p.makeCode(N, ell, s)
print 'code for the error-detecting property described by t2s\n-'
for w in W: print w

print
p = codes.ErrDetectProp(t2id)
a, W = p.makeCode(N, ell, s)
print 'code for the error-detecting property described by t2id\n-'
for w in W: print w

print t2s_ia
p = codes.IATProp(t2s_ia)     
a, W = p.makeCode(N, ell, s)
print 'code for the input-altering transducer property described by t2s_ia\n-'
for w in W: print w

print
p = codes.UDCodeProp({'0','1'})

print 'UD code\n-', p
a, W = p.makeCode(5, 8, 2)
for w in W: print w

print
