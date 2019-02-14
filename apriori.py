import pandas as pd
from itertools import combinations

data = pd.read_csv('groceries.csv',header=None)

dataset = []

dic = {} #Dictionary to store count of sets

#Data preprocessing -> Storing the data as a list of frozensets
for i in range(0,9835):
    fset = set()
    for j in range(0,32):
        if(type(data.values[i,j])==str):
            temp = set()
            temp.add(data.values[i,j])
            temp = frozenset(temp)
            dic[temp] = 0
            fset.add(data.values[i,j])
    dataset.append(frozenset(fset))
    


frequent = []     #Temporary list to store frequent itemsets
candidate = []    #Temporary list toStore candidate itemsets during apriori
support = 0.04    #minimum support 
confidence = 0.3  #minimum confidence

for key in dic.keys():
    candidate.append(key)

for j in range(0,len(candidate)):
    for i in range(0,9835):
        if(candidate[j].issubset(dataset[i])):
            dic[candidate[j]] = dic[candidate[j]] + 1

frequent.append([])

#Generating frequent itemsets of length 1            
for j in range(0,len(candidate)):
    if(dic[candidate[j]]/9835 > support):
        frequent[0].append(candidate[j])

#Generating frequent itemsets
for k in range(2,32):
    frequent.append([])
    candidate = []
    #Generating candidate itemsets of length k from frequent itemsets of length k-1
    for i in range(0,len(frequent[k-2])):
        for j in range(i+1,len(frequent[k-2])):
            l1 = list(frequent[k-2][i])[:k-2]
            l2 = list(frequent[k-2][j])[:k-2]
            if(l1==l2):
                candidate.append(frequent[k-2][i]|frequent[k-2][j])
                dic[frequent[k-2][i]|frequent[k-2][j]] = 0
    
    #Calcualting support of candidate itemsets
    for j in range(len(candidate)):
        for i in range(0,9835):
            if(candidate[j].issubset(dataset[i])):
                dic[candidate[j]] = dic[candidate[j]] + 1
                
    #Storing frequent itemsets of length k-1            
    for j in range(0,len(candidate)):
        if(dic[candidate[j]]/9835 > support):
            frequent[k-1].append(candidate[j]) 

frequent_itemsets = [] #Stores all frequent itemsets


for i in range(0,len(frequent)):
    for j in range(0,len(frequent[i])):
        frequent_itemsets.append(frequent[i][j])
        
#for i in range(0,len(frequent_itemsets)):
#    print(frequent_itemsets[i])

maximal_frequent_itemsets = [] #Stores maximal frequent itemsets
closed_frequent_itemsets = []  #Stores close frequent itemsets

#Finding maximal frequent itemsets
for i in range(0,len(frequent_itemsets)):
    flag = 1
    for j in range(0,len(frequent_itemsets)):
        if(i==j):
            continue
        if(frequent_itemsets[i].issubset(frequent_itemsets[j])):
            flag = 0
    
    if(flag == 1):
        maximal_frequent_itemsets.append(frequent_itemsets[i])

#Finding closed frequent itemsets
for i in range(0,len(frequent_itemsets)):
    flag = 1
    for j in range(0,len(frequent_itemsets)):
        if(i==j):
            continue
        
        if(frequent_itemsets[i].issubset(frequent_itemsets[j]) and dic[frequent_itemsets[i]] == dic[frequent_itemsets[j]]) :
            #print(frequent_itemsets[i],":",dic[frequent_itemsets[i]],"",frequent_itemsets[j],":",dic[frequent_itemsets[j]])
            flag = 0

    if(flag==1):
        closed_frequent_itemsets.append(frequent_itemsets[i])
#for i in range(0,len(maximal_frequent_itemsets)):
#    print(maximal_frequent_itemsets[i])

antecedent = [] #Stores the antecendent of the rules
consequent = [] #Stoes the consequent of the rules

#Generating the association rules
for i in range(0,len(closed_frequent_itemsets)):
    if(len(closed_frequent_itemsets[i])==1):
        continue
    #print(frequent_itemsets[i])
    for j in range(1,len(closed_frequent_itemsets[i])):
        sub = list(combinations(closed_frequent_itemsets[i],j))
        for k in range(0,len(sub)):
            ant = frozenset(sub[k])
            con = closed_frequent_itemsets[i] - ant
            if(dic[closed_frequent_itemsets[i]]/dic[ant] > confidence):
                antecedent.append(ant)
                consequent.append(con)
                
for i in range(len(antecedent)):
    print(antecedent[i],'->',consequent[i])
    
    