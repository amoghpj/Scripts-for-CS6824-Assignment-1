import numpy as np
import matplotlib.pyplot as plt
#plt.cla()
#plt.clf()
val=[0.25,0.5,0.75]
k=np.arange(0,20,1)
symb=['ko','ko','ko']
st=['a=0.25','a=0.5','a=0.75']
low=[]
mid=[]
high=[]
for j in range(0,len(k)):
    low=np.append(low,val[0]**k[j])
    mid=np.append(mid,val[1]**k[j])
    high=np.append(high,val[2]**k[j])
x0=[val[0],val[0]]
x1=[val[1],val[1]]
x2=[val[2],val[2]]
y0=[min(low),max(low)]
y1=[min(mid),max(mid)]
y2=[min(high),max(high)]
plt.plot(x0,y0,symb[0])
plt.plot(x1,y1,symb[1])
plt.plot(x2,y2,symb[2])
plt.plot(x0,y0,'k')
plt.plot(x1,y1,'k')
plt.plot(x2,y2,'k')

x=[0.25,0.5,0.75]
plt.xticks(x,[0.25,0.50,0.75])

plt.ylim([1,10**(-13)])
plt.gca().set_yscale('log')
#plt.legend()

plt.xlabel('$a$')
plt.ylabel('$a^{k}$')
#plt.show()
plt.savefig('scale-justification.png')
    
