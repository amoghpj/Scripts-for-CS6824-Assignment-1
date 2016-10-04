import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import sys
import random
from tqdm import tqdm
def generate_watts_strogatz_graph(N,K):
    #n=raw_input('Please enter Graph name (eg. graph1): ') or 'test'
    #name=str(fn)+'.txt'
    n=N #int(raw_input('Please enter number of nodes in graph: ') or "10")
    if n<=0:
        sys.exit('n has to be positive!')

    nodelist=np.arange(0,n)
    k=K #int(raw_input('Please enter average degree of each node.\nFor n=%i, enter an even integer between 1 and n: ' % n) or '2')
    if k%2 !=0:
        sys.exit('k is not even!')
    if k >n:
        sys.exit('k is too large!')

    degreecount=np.arange(-k/2,(k+2)/2)
    G=nx.Graph()
 
    for i in range(0,len(nodelist)):
        for j in range(0,len(degreecount)):
            if i+degreecount[j]>n-1:
                G.add_edge(str(nodelist[i]),str(nodelist[i+degreecount[j]-n-1]))
                #print i,"\t",j,"\t",nodelist[i],nodelist[i+degreecount[j]-n-1]
            else:
                if nodelist[i+degreecount[j]]!=nodelist[i]:
                    G.add_edge(str(nodelist[i]),str(nodelist[i+degreecount[j]]))
                    
    #f.close()
    for node in G.nodes():
        if node in G.neighbors(node):
            G.remove_edge(node,node)
            print "removed an edge"
        
    
    def rewire(H,p): #Function takes in a graph and a probability p, and returns average shortest path length and average clustering coefficient of the rewired graph
        
        nodeset=set(H.nodes())
        
        for node in H.nodes(): #rewiring
            neighborset=set(H.neighbors(node))
            targetlist=list(nodeset-neighborset)
            for tailnode in H.neighbors(node):
                r=random.random()
                if r<p:
                    node_selection=random.randint(0,len(targetlist)-1)
                    H.remove_edge(node,tailnode)
                    H.add_edge(node,targetlist[node_selection])
        asp=[]
        for g in nx.connected_component_subgraphs(H): # ensures that every value of p still returns a ASP
            if nx.number_of_nodes(g)>2:
                asp=np.append(asp,nx.average_shortest_path_length(g))

        ASP=np.max(asp)
        #ASP=nx.average_shortest_path_length(H)
        ACL=nx.average_clustering(H)
        return ASP,ACL  
    
    av_sp=[]
    av_cl=[]
    A=[]
    Am=[]
    C=[]
    Cm=[]
    rg=6
    P1=[]
    k_prob=np.arange(20,0,-1)
    AUX_PLOTS=int(raw_input("Do you want to generate comparison plots for linear and log scale variation in p?(1/0): ") or '0')
    # Type 1: linear
    for i in range(0,len(k_prob)):
        P1=np.append(P1,0.05*k_prob[i])
    # Type 2: exponential
    P2=[]
    for i in range(0,len(k_prob)):
        P2=np.append(P2,0.5**k_prob[i])
    

    MAX_AV_SP=nx.average_shortest_path_length(G)
    MAX_AV_CL=nx.average_clustering(G)
    print MAX_AV_SP
    print MAX_AV_CL

    if AUX_PLOTS==1:
        
        f,arr=plt.subplots(2,1)
       
        av_sp=[]
        av_cl=[]
        A=[]
        Am=[]
        C=[]
        Cm=[]
        p=0
        for p in tqdm(P1):
            L=[]
            Lm=[]
            Cm=[]
            C=[]
            l=0
            c=0
            for i in range(0,10):
                I=G.copy()
                l,c=rewire(I,p)
                L=np.append(L,l/MAX_AV_SP)
                C=np.append(C,c/MAX_AV_CL)
            Lm=np.mean(L)
            Cm=np.mean(C)
            arr[0].errorbar(p,Lm,np.std(L),ecolor='k')
            arr[0].errorbar(p,Cm,np.std(C),ecolor='k')
            arr[0].plot(p,Lm,'ko')
            arr[0].plot(p,Cm,'wo')
            arr[0].set_ylim([0,1])
            arr[0].set_xlabel('p')
            arr[0].set_title('Linear p')
            arr[0].set_ylabel('L/L0,C/C0')

        I=G.copy()
        av_sp=[]
        av_cl=[]
        A=[]
        Am=[]
        C=[]
        Cm=[]
        p=0
        for p in tqdm(P2):
            L=[]
            C=[]
            Lm=[]
            Cm=[]
            l=0
            c=0
            for i in range(0,10):
                I=G.copy()
                l,c=rewire(I,p)
                L=np.append(L,l/MAX_AV_SP)
                C=np.append(C,c/MAX_AV_CL)
            Lm=np.mean(L)
            Cm=np.mean(C)
            arr[1].errorbar(p,Lm,np.std(L),ecolor='k')
            arr[1].errorbar(p,Cm,np.std(C),ecolor='k')
            arr[1].set_xscale('log')
            arr[1].plot(p,Lm,'ko')
            arr[1].plot(p,Cm,'wo')
            arr[1].set_ylim([0,1])
            arr[1].set_xlabel('p')
            arr[1].set_title('Exponential p')
            arr[1].set_ylabel('L/L0,C/C0')
    else:
        I=G.copy()
        av_sp=[]
        av_cl=[]
        A=[]
        Am=[]
        C=[]
        Cm=[]

        for p in tqdm(P2):
            L=[]
            C=[]
            for i in range(0,10):
                l,c=rewire(I,p)
                L=np.append(L,l)
                C=np.append(C,c)
            Lm=np.mean(L)
            Cm=np.mean(C)
        #    plt.errorbar(p,Lm/MAX_AV_SP,np.std(L))
        #    plt.errorbar(p,Cm/MAX_AV_CL,np.std(C))
            plt.xscale('log')

    #pos=nx.spring_layout(G)
    #pos2=nx.spring_layout(H)
    #f,axarr=plt.subplots(1,2)
    #A=aa.AxisArtist(axarr,axis_direction='bottom')
    #A.toggle(all=False)
    #nx.draw_networkx(G,pos,ax=axarr[0])
    #nx.draw_networkx(H,pos,ax=axarr[1])
#   axarr[1]=nx.draw(H,pos)
#    plt.show()
    plt.tight_layout()
    plt.savefig("./Results_Assignment1/ws_N="+str(N)+"_k="+str(K)+"_iter="+str(10)+".pdf",bbox_inches='tight')
