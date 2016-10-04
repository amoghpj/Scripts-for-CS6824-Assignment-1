import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import matplotlib.transforms as mtransforms
#trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
# Read Graph
# Plot Graph specific
Graph_dict1={'macaque2013':'./Results_Assignment1/processedmacaque2013.txt'}
Graph_dict={'crossley2013':'./Results_Assignment1/2013-PNAS-Crossley-Cognitive-relevance-coactivation-matrix.txt',
            'honey2007':'./Results_Assignment1/2007-pnas-honey-network-structure-functional-connectivity-macaque47.txt',
            'macaque1993':'./Results_Assignment1/1993-Proc-Royal-Society-organization-neural-systems-macaque71.txt',
            'cat-cortex1995':'./Results_Assignment1/1995-journal-neuroscience-connectivity-cerebral-cortex-cat-cjall.txt',
         'felleman1991':'./Results_Assignment1/1991-cerebral-cortex-felleman-primate-cerebral-cortex-fv30.txt',
            'G29x29':'./Results_Assignment1/G29x29.txt'}
ref_Set= ['crossley2013','G29x29','honey2007','macaque1993','cat-cortex1995','felleman1991']#,'crossley2013']#,'mac2013']
av_sp=[]
av_cl=[]

J=nx.read_edgelist(Graph_dict1['macaque2013'],create_using=nx.DiGraph(),data=[])
K=J.subgraph(['24c','F1','F2','F7','F5','ProM','V1','V2','V4','TEO','MT','TEpd','STPc','STPi','STPr','PBr',
         '5','DP','7m','7A','7B','8B','8m','8l', '9/46d','46d','9/46v','2','10'])
nx.write_edgelist(K,'./Results_Assignment1/G29x29.txt')

#for G in tqdm(ref_Set):
#   H=[]
#   L=[]
#   H=nx.read_edgelist(Graph_dict[G],create_using=nx.DiGraph(),data=False)
#   L=nx.read_edgelist(Graph_dict[G],create_using=nx.Graph(),data=False)
#    #g=nx.connected_component_subgraphs(H)
##   print "%s has edges= " % G+"%i" % nx.number_of_edges(H)
##   av_sp=np.append(av_sp,nx.average_shortest_path_length(H))
##   av_cl=np.append(av_cl,nx.average_clustering(L))
#   plt.plot(nx.average_shortest_path_length(H),nx.average_clustering(L),'o',label=G)
#   print "\nplotted %s" %G
#plt.xlabel('Average shortest path length')
#plt.ylabel('Average clustering coefficient')
#plt.legend()
# #plt.show()
#plt.savefig('./Results_Assignment1/av_sp_vs_av_cc_comparison.png')
#
#############################################################################
############# Generate Density vs Average Shortest Path lengths
#H=[]
#dense=[]
#i=0
#G=[]
#for G in tqdm(ref_Set):
#   H=nx.read_edgelist(Graph_dict[G],create_using=nx.DiGraph(),data=False)
#    #g=nx.connected_component_subgraphs(H)
#   print "%s has edges= " % G+"%i" % nx.number_of_edges(H)
#   dense=np.append(dense,nx.density(H))
#   #av_sp=np.append(av_sp,nx.average_shortest_path_length(H))
#   #av_cl=np.append(av_cl,nx.average_clustering(H))
#   plt.plot(nx.density(H),nx.average_shortest_path_length(H),'o',label=G)
#   i=i+1
##print "\nplotted %s" %G
#plt.ylabel('Average shortest path length')
#plt.xlabel('Density of Graph')
#plt.legend()
##plt.show()
#plt.savefig('./Results_Assignment1/density_vs_asp.png')


###################################################################################################
############### Generate histograms for each network for average clustering coefficient and average shortest path length
avsp_node=[]
node_clustering=[]
for G in tqdm(ref_Set):
   H=[]
   L=[]
   H=nx.read_edgelist(Graph_dict[G],create_using=nx.DiGraph(),data=False)
   L=nx.read_edgelist(Graph_dict[G],create_using=nx.Graph(),data=False)
   Av_shortest_path_length=[]
   Shortest_Path_lengths=[]
   node_clustering=[]
   for node in H.nodes():
      All_shortest_paths_from_node=nx.single_source_shortest_path_length(H,node)
      Shortest_Path_lengths=np.append(Shortest_Path_lengths,np.mean(All_shortest_paths_from_node.values()))
   for node in L.nodes():
      node_clustering=np.append(node_clustering,np.mean(nx.clustering(L,node)))
   f, arr=plt.subplots(2,1)
   arr[0].hist(Shortest_Path_lengths)
   arr[1].hist(node_clustering)
   arr[0].set_xlabel('Av. SP')
   arr[1].set_xlabel('Av. Cl Coeff')
   arr[0].set_ylabel('Counts')
   arr[1].set_ylabel('Counts')
   arr[0].set_title(G)
   plt.tight_layout()
   plt.savefig(G+'_hist.pdf',bbox_inches='tight')


#import random
#G=nx.read_edgelist(Graph_dict['G29x29'],create_using=nx.DiGraph(),data=False)
#max_iter=100
#av_sp=[]
#d=[]
#y=[]
#x=[]
#lerror=[]
#uerror=[]
#I=np.arange(1,10,0.1)
#for i in tqdm(I):
#   av_sp=[]
#   d=[]
#   #print "Entering iteration %i" %iterval
#   for iterval in range(1,max_iter):
#      H=G.copy()
#      nodelist=H.nodes()
#      #print "Comparing at value %i" %i
#      #print H.number_of_nodes()
#      ##print ((float(i)/10)*nx.density(G))
#      while nx.density(H) > ((float(i)/10)*nx.density(G)):
#         edge_list=H.edges()
#         ed=random.choice(edge_list)
#         H.remove_edge(ed[0],ed[1])
#      g=max(nx.strongly_connected_components(H), key=len)
#      if nx.number_of_edges(H.subgraph(g))==0:
#         av_sp=np.append(av_sp,av_sp[-1])
#      else:
#         av_sp=np.append(av_sp,nx.average_shortest_path_length(H.subgraph(g)))
#   x=np.append(x,(float(i)/10)*nx.density(G))
#   y=np.append(y,np.mean(av_sp))
#   lerror=np.append(lerror,np.mean(av_sp)-np.std(av_sp))
#   uerror=np.append(uerror,np.mean(av_sp)+np.std(av_sp))
#
#plt.fill_between(x,lerror,uerror,facecolor='gray', alpha=0.5)#, transform=trans)
#plt.plot(x,y,'k')
#plt.xlim([0.0,0.7])
#plt.ylim([1.0,4.0])
#plt.xlabel('Density of Graph')
#plt.ylabel('Av SP of Graph')
#plt.show()
#
