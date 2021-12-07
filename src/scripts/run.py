
import numpy as np
import os
import pandas as pd
import unittest
from causallearn.graph.GraphClass import CausalGraph
from causallearn.search.ConstraintBased.PC import pc
from causallearn.utils.PCUtils import SkeletonDiscovery
from causallearn.utils.PCUtils.BackgroundKnowledge import BackgroundKnowledge
from causallearn.utils.PCUtils.BackgroundKnowledgeOrientUtils import orient_by_background_knowledge
from causallearn.graph.GraphNode import GraphNode
from causallearn.utils.cit import fisherz

## Load the data in the three different offsets, clean the columns

cwd = os.getcwd()

off1 = pd.read_csv(f'{cwd}/src/final_data/temporal_offset_1_data.csv')
off2 = pd.read_csv(f'{cwd}/src/final_data/temporal_offset_2_data.csv')
off3 = pd.read_csv(f'{cwd}/src/final_data/temporal_offset_3_data.csv')

df = pd.read_csv(f'{cwd}/src/final_data/monthly_djf_data.csv')

off1 = off1[off1.columns[1:]]
off2 = off2[off2.columns[1:]]
off3 = off3[off3.columns[1:]]
new_df = df.set_index('date')

## Create three different dictionaries that tell us the oscillation corresponding to each node

d1 = {}
for i in range(len(off1.columns)):
    d1[i] = [off1.columns[i], float(off1.columns[i][3:])]

d2 = {}
for i in range(len(off2.columns)):
    d2[i] = [off2.columns[i], float(off2.columns[i][3:])]

d3 = {}
for i in range(len(off3.columns)):
    d3[i] = [off3.columns[i], float(off3.columns[i][3:])]
    
## Start with offset 3 because it runs the quickest    
## Run PC generally to get the names of all possible nodes    

cg = pc(np.array(off3), 0.01, fisherz, True, 0, -1)

## Create tiers so we can input forbidden nodes

tier_list = {}
for i in off3.columns:
    tier_list[i] = (int(int(i[3:])/3) + 9)
    
## Rename the nodes
    
nodes = cg.G.get_nodes()
names = list(off3.columns)
off = 3
for i in range(len(nodes)):
    
    node = nodes[i]
    name = names[i]
    node.set_name(name)
    
## Create the tiers

nodes = cg.G.get_nodes()
names = list(off3.columns)
tier = {}
off = 3
bk = BackgroundKnowledge()
for i in range(len(nodes)):
   #print(i.get_name())
    #print(d[int(i.get_name()[1])-1][1])
    
    node = nodes[i]
    name = names[i]
    #node.set_name(name)
    #tier[i.get_name()] = int(((d[int(i.get_name()[1:])-1][1])/3)+9) 
    
    t = tier_list[name]
    bk.add_node_to_tier(node,int(t))
    

## Run PC with background knowledge, graph relations, report names of causal relations

print('Results from Offset 3: ')

cg = pc(np.array(off3), 0.01, fisherz, True, 0, -1, background_knowledge = bk)
# Run PC and obtain the estimated graph (CausalGraph object)
cg.to_nx_graph()
cg.draw_nx_graph(skel=False)

#for i in sorted(cg.find_fully_directed()):
 #   print(d3[(i[0])][0] + '--->' + d3[(i[1])][0])
d = {}
for i in sorted(cg.find_fully_directed()):
    if (d3[(i[0])][0][:3] + '->' + d3[(i[1])][0][:3] + ', ' + str(d3[(i[1])][1] - d3[(i[0])][1])) in d.keys(): 
        d[(d3[(i[0])][0][:3] + '->' + d3[(i[1])][0][:3] + ', ' + str(d3[(i[1])][1] - d3[(i[0])][1]))] += 1
    else:
        d[(d3[(i[0])][0][:3] + '->' + d3[(i[1])][0][:3] + ', ' + str(d3[(i[1])][1] - d3[(i[0])][1]))] = 1  
print(d)

## Move to offset 2     
## Run PC generally to get the names of all possible nodes    

cg = pc(np.array(off2), 0.01, fisherz, True, 0, -1)

## Create tiers so we can input forbidden nodes

tier_list = {}
for i in off2.columns:
    tier_list[i] = (int(int(i[3:])/2) + 12)
    
## Rename the nodes
    
nodes = cg.G.get_nodes()
names = list(off2.columns)
for i in range(len(nodes)):
    
    node = nodes[i]
    name = names[i]
    node.set_name(name)
    
## Create the tiers

nodes = cg.G.get_nodes()
names = list(off2.columns)
tier = {}
bk = BackgroundKnowledge()
for i in range(len(nodes)):
   #print(i.get_name())
    #print(d[int(i.get_name()[1])-1][1])
    
    node = nodes[i]
    name = names[i]
    #node.set_name(name)
    #tier[i.get_name()] = int(((d[int(i.get_name()[1:])-1][1])/3)+9) 
    
    t = tier_list[name]
    bk.add_node_to_tier(node,int(t))
    

## Run PC with background knowledge, graph relations, report names of causal relations

print('Results from Offset 2: ')

cg = pc(np.array(off2), 0.01, fisherz, True, 0, -1, background_knowledge = bk)
# Run PC and obtain the estimated graph (CausalGraph object)
cg.to_nx_graph()
cg.draw_nx_graph(skel=False)

#for i in sorted(cg.find_fully_directed()):
#    print(d2[(i[0])][0] + '--->' + d2[(i[1])][0])
for i in sorted(cg.find_fully_directed()):
    if (d2[(i[0])][0][:3] + '->' + d2[(i[1])][0][:3] + ', ' + str(d2[(i[1])][1] - d2[(i[0])][1])) in d.keys(): 
        d[(d2[(i[0])][0][:3] + '->' + d2[(i[1])][0][:3] + ', ' + str(d2[(i[1])][1] - d2[(i[0])][1]))] += 1
    else:
        d[(d2[(i[0])][0][:3] + '->' + d2[(i[1])][0][:3] + ', ' + str(d2[(i[1])][1] - d2[(i[0])][1]))] = 1
print(d)

## Finish with Offset 1    
## Run PC generally to get the names of all possible nodes    

cg = pc(np.array(off1), 0.01, fisherz, True, 0, -1)

## Create tiers so we can input forbidden nodes

tier_list = {}
for i in off1.columns:
    tier_list[i] = (int(int(i[3:])) + 19)
    
## Rename the nodes
    
nodes = cg.G.get_nodes()
names = list(off1.columns)
for i in range(len(nodes)):
    
    node = nodes[i]
    name = names[i]
    node.set_name(name)
    
## Create the tiers

nodes = cg.G.get_nodes()
names = list(off1.columns)
tier = {}
bk = BackgroundKnowledge()
for i in range(len(nodes)):
   #print(i.get_name())
    #print(d[int(i.get_name()[1])-1][1])
    
    node = nodes[i]
    name = names[i]
    #node.set_name(name)
    #tier[i.get_name()] = int(((d[int(i.get_name()[1:])-1][1])/3)+9) 
    
    t = tier_list[name]
    bk.add_node_to_tier(node,int(t))
    

## Run PC with background knowledge, graph relations, report names of causal relations

print('Results from Offset 1: ')

cg = pc(np.array(off1), 0.01, fisherz, True, 0, -1, background_knowledge = bk)
# Run PC and obtain the estimated graph (CausalGraph object)
cg.to_nx_graph()
cg.draw_nx_graph(skel=False)

#for i in sorted(cg.find_fully_directed()):
#    print(d1[(i[0])][0] + '--->' + d1[(i[1])][0])    
for i in sorted(cg.find_fully_directed()):
    if (d1[(i[0])][0][:3] + '->' + d1[(i[1])][0][:3] + ', ' + str(d1[(i[1])][1] - d1[(i[0])][1])) in d.keys(): 
        d[(d1[(i[0])][0][:3] + '->' + d1[(i[1])][0][:3] + ', ' + str(d1[(i[1])][1] - d1[(i[0])][1]))] += 1
    else:
        d[(d1[(i[0])][0][:3] + '->' + d1[(i[1])][0][:3] + ', ' + str(d1[(i[1])][1] - d[(i[0])][1]))] = 1    
        
keys = []
values = []
for key, value in d.items():
    dist = float(key[10:])
    if (dist >= 0) & (value > 2):
        keys.append(key)
        values.append(value)
rel_df = pd.DataFrame({'relation':keys,'amount':values})
rel_df = rel_df.sort_values(by = 'amount', ascending= False)
print(rel_df)
    
    
    
## Monthly ENSO Values

cg = pc(np.array(new_df), 0.05, fisherz, True, 0, -1)
cg.to_nx_graph()
cg.draw_nx_graph(skel=False)
for i in range(len(new_df.columns)):
    print(str(i) + ': ' + new_df.columns[i])