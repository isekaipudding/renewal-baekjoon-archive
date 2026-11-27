# 링크 : https://acmicpc.net/problem/30919
import sys,math
from array import array as A
from itertools import accumulate as acc,compress

R=sys.stdin.readline
W=sys.stdout.write
S=math.isqrt

def C(n):
 x=int(round(n**(1/3)))
 while(x+1)**3<=n:x+=1
 while x**3>n:x-=1
 return x

def sv(L):
 h=(L+1)>>1
 o=bytearray([1])*h
 o[0]=0
 z=memoryview(bytes(h))
 for p in range(3,S(L)+1,2):
  if o[p>>1]:s=p*p>>1;o[s::p]=z[:(h-1-s)//p+1]
 P=[2]+list(compress(range(1,h<<1,2),o))
 o[0]=1
 b=A('I',acc(o)).tobytes()
 f=bytearray(4+(len(b)<<1))
 for i in range(4):f[4+i::8]=f[8+i::8]=b[i::4]
 pi=A('I');pi.frombytes(f);pi[1]=0
 return P,pi

T=int(R())
Q=[int(R())for _ in range(T)]
M=max(Q)if Q else 0
L=max(100,M)if M<=2000000 else min(2000000,max(100000,S(M)+100,M//C(M)))
L+=L&1
P,pi=sv(L)
G=pi.__getitem__
if M<=L:W('\n'.join(map(str,map(G,Q)))+'\n');sys.exit()

w=bytearray([1])*510510;w[0]=0
for p in(2,3,5,7,11,13,17):w[p::p]=bytes((510509-p)//p+1)
F=A('I',acc(w))

def ph(x,m):
 if x<1:return 0
 if m<=7:return x//510510*92160+F[x%510510]
 if x<P[m-1]:return 1
 if x<=L:
  q=P[m]
  if x<q*q:return pi[x]-m+1
  if x<q*q*q:
   l=pi[S(x)]
   return pi[x]-m+1-((l+m-1)*(l-m)>>1)+sum(map(G,map(x.__floordiv__,P[m:l])))
 r=x//510510*92160+F[x%510510]
 k=pi[S(x)]
 if k<m:
  k=7 if k<7 else k;r-=m-k;m=k
  if m<=7:return r
 t=max(C(x),x//(L+1))
 if t<P[m-1]:
  k=pi[t]
  if k<7:k=7
  if k<m:
   c=m-k
   r-=sum(map(G,map(x.__floordiv__,P[k:m])))
   r+=((k+1+m)*c>>1)-(c<<1);m=k
 for k in range(8,m+1):r-=ph(x//P[k-1],k-1)
 return r

def p2(n,c,mid):
 U=15015;D=U*18;w=bytearray([1])*U
 for p in(3,5,7,11,13):w[p>>1::p]=bytes((U-1-(p>>1))//p+1)
 B=bytes(w)*19;z=memoryview(bytes(D))
 mq=n//P[c];lo=L+1;rp=pi[L];s=0;qi=mid-1;sp=P[6:]
 while qi>=c:
  rm=((mq-lo)>>1)+1;sl=D if rm>D else rm;hi=lo+((sl-1)<<1)
  wo=(lo>>1)%U;sg=bytearray(B[wo:wo+sl])
  for p in sp:
   t=p*p
   if t>hi:break
   if t<lo:
    t=lo+(-lo%p)
    if~t&1:t+=p
   if t<=hi:st=(t-lo)>>1;sg[st::p]=z[:(sl-1-st)//p+1]
  pp=0;lm=hi+1
  while qi>=c:
   qv=n//P[qi]
   if qv>lm:break
   cp=((qv-lo)>>1)+1
   if cp>pp:rp+=sg.count(1,pp,cp);pp=cp
   s+=rp;qi-=1
  if qi<c:break
  rp+=sg.count(1,pp,sl);lo=hi+2
 return s

def f(n):
 if n<=L:return pi[n]
 a,c,b=pi[S(S(n))],pi[C(n)],pi[S(n)]
 r=ph(n,a)
 for i in range(a,c):r-=ph(n//P[i],a)
 for j in range(a,c-1):r+=sum(map(G,map((n//P[j]).__floordiv__,P[j+1:c])))+(c-j-1)*(1-j)
 r+=c-1+((c+b-1)*(b-c)>>1)
 m=max(c,pi[n//(L+1)])
 if m<b:r-=sum(map(G,map(n.__floordiv__,P[m:b])))
 if m>c:r-=p2(n,c,m)
 return r

W('\n'.join(map(str,map(f,Q)))+'\n')