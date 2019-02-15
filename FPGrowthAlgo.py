# -*- coding: utf-8 -*-
"""
@author: Kunal
"""
#Importing Libraries

import math as mt
import pandas as pd

#List of frequent itemsets

frequent_itemsets = {}

#FP Tree's node data type

class FPTreeNode(object):
    def __init__(self,item_name: str, item_value: float):
        self.name = item_name
        self.value = item_value
        self.children = []

#Method to add a node to the FP tree

def add(root,record):
    itr = root
    for i in record:
        found = False
        for j in itr.children:
            if j.name == i:
                itr=j
                found = True
                break
        if found == True:
            itr.value = itr.value+1
        else:
            newNode = FPTreeNode(i,1)
            itr.children.append(newNode)
            itr=newNode

#Depth First Search to mine frequent itemsets

def dfs(node,current_list,support_count: int,total_elements: float):
    going_down = False
    if node.name != "*":
        if node.name not in current_list:
            current_list.append(node.name)
    for i in node.children:
        if i.value >= support_count:
            new_list = current_list
            dfs(i,new_list,support_count,total_elements)
            going_down = True
    if going_down == False:
        if len(current_list)!=0:
            temp_list = current_list
            tmp = tuple(temp_list)
            val = node.value
            support_value = val/total_elements
            print(support_value)
            temp_list.sort()
            if tmp not in frequent_itemsets:
                frequent_itemsets[tmp] = support_count
                
        
#Importing the dataset

dataset =  pd.read_csv("groceries.csv",header = None)

#Assigning support and finding support count

support = 0.03
support_count = support * dataset.shape[0]
support_count = mt.ceil(support_count) 

#Finding number of frequencies of each item in dataset

item_count = {}
for i in range(0,dataset.shape[0]):
    for j in range(0,dataset.shape[1]):
        if(type(dataset.values[i,j])!=str):
            break
        if dataset.values[i,j] in item_count:
            item_count[dataset.values[i,j]]=item_count[dataset.values[i,j]]+1
        else:
            item_count[dataset.values[i,j]]=1
            
#Removing items with frequencies below support count

temp_key_list = list(item_count.keys())
for i in temp_key_list:
    if item_count[i] < support_count:
        item_count.pop(i)

#Ordering items in descending order based on count
            
ordered_list_of_items = []
for i in item_count:
    new_item = (item_count[i],i)
    ordered_list_of_items.append(new_item)
ordered_list_of_items.sort()


#Ordered transactions

ordered_transactions = []
for i in range(0,dataset.shape[0]):
    new_transaction = []
    for j in reversed(ordered_list_of_items):    
        for k in range(0,dataset.shape[1]):
            if(type(dataset.values[i,k])!=str):
                break
            if(j[1] == dataset.values[i,k]):
                new_transaction.append(j[1])
                break
    ordered_transactions.append(new_transaction)


#Creation of the FP Tree

root = FPTreeNode("*",100000)
for i in ordered_transactions:
    if(len(i)>0):
        add(root,i)

#Mining for frequent itemsets

current_list = []
dfs(root,current_list,support_count,dataset.shape[0])
for i in frequent_itemsets:
    print(i)
