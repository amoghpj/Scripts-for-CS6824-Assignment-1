import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import sys
import random
from tqdm import tqdm
def wsmodel(N,K,P):
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
        
    print "Number of nodes in G is %i"% nx.number_of_edges(G)
    MAX_AV_SP=nx.average_shortest_path_length(G)
    print "Average shortest path length in ring lattice is "
    print MAX_AV_SP
    def rewire(H,p):
        
        nodeset=set(H.nodes())
        
#        for edge in H.edges():
#            r=random.random()
#            n1,n2=edge
#            if r<p:
#                neighborset=set(H.neighbors(n1))
#                targetlist=list(nodeset-neighborset)
#                node_selection=random.randint(0,len(targetlist)-1)
#                H.remove_edge(n1,n2)
#                H.add_edge(n1,targetlist[node_selection])
#        
        for node in H.nodes():
            neighborset=set(H.neighbors(node))
            targetlist=list(nodeset-neighborset)
            for tailnode in H.neighbors(node):
                r=random.random()
                if r<p:
                    node_selection=random.randint(0,len(targetlist)-1)
                    H.remove_edge(node,tailnode)
                    H.add_edge(node,targetlist[node_selection])
        asp=[]
        for g in nx.connected_component_subgraphs(H):
            asp=np.append(asp,nx.average_shortest_path_length(H))
        ASP=max(asp)
        print "At p = %f," %p
        print "ASP= %f" %ASP
        ACL=nx.average_clustering(H)
        SP=[]
        nodecollec=[]
        return H
    print "G has %i edges" %nx.number_of_edges(G)
    J=rewire(G.copy(),P)
    return G,J
    
