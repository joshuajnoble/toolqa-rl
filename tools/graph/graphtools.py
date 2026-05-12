import networkx as nx
import numpy as np
import pandas as pd
import pickle
import os
from langchain_core.tools import tool

class graph_toolkits():
    # init
    def __init__(self, path):
        self.graph = None
        self.id2title_dict = None
        self.title2id_dict = None
        self.id2author_dict = None
        self.author2id_dict = None
        self.path = path
    
    @tool("graph_load_graph")
    def load_graph(self, graph_name: str) -> str:
        """
        
        Load a graph by name (e.g., 'dblp'). Returns a status string.
        
        Args:

            graph_name: Name of the graph, options are 'dblp'
        
        """
        if graph_name == 'dblp':
            with open('{}/external_corpus/dblp/paper_net.pkl'.format(self.path), 'rb') as f:
                self.paper_net = pickle.load(f)

            with open('{}/external_corpus/dblp/author_net.pkl'.format(self.path), 'rb') as f:
                self.author_net = pickle.load(f)
            
            with open("{}/external_corpus/dblp/title2id_dict.pkl".format(self.path), "rb") as f:
                self.title2id_dict = pickle.load(f)
            with open("{}/external_corpus/dblp/author2id_dict.pkl".format(self.path), "rb") as f:
                self.author2id_dict = pickle.load(f)
            with open("{}/external_corpus/dblp/id2title_dict.pkl".format(self.path), "rb") as f:
                self.id2title_dict = pickle.load(f)
            with open("{}/external_corpus/dblp/id2author_dict.pkl".format(self.path), "rb") as f:
                self.id2author_dict = pickle.load(f)
            return "DBLP data is loaded, including two graphs: AuthorNet and PaperNet."

    @tool("graph_check_neighbours")
    def check_neighbours(self, argument: str) -> str:
        """
        
        Check neighbors for a node in a graph. 
        
        Args: 
            This is the argument to the graph which should be structured like 'GraphName, NodeName'
            
        """
        graph, node = argument.split(', ')
        if graph == 'PaperNet':
            graph = self.paper_net
            dictionary = self.title2id_dict
            inv_dict = self.id2title_dict
        elif graph == 'AuthorNet':
            graph = self.author_net
            dictionary = self.author2id_dict
            inv_dict = self.id2author_dict
        neighbour_list = []
        for neighbour in graph.neighbors(dictionary[node]):
            neighbour_list.append(inv_dict[neighbour])
        return str(neighbour_list)

    @tool
    def check_nodes(self, argument: str) -> str:
        """Check node attributes. Argument: 'GraphName, NodeName'"""
        graph, node = argument.split(', ')
        if graph == 'PaperNet':
            graph = self.paper_net
            dictionary = self.title2id_dict
            inv_dict = self.id2title_dict
        elif graph == 'AuthorNet':
            graph = self.author_net
            dictionary = self.author2id_dict
            inv_dict = self.id2author_dict
        return str(graph.nodes[dictionary[node]])

    @tool("graph_check_edges")
    def check_edges(self, argument: str) -> str:
        """
        
        Check edge attributes 
        
        Args: 
            This is the argument to the graph which should be structured like 'GraphName, Node1, Node2'
            
        """
        graph, node1, node2 = argument.split(', ')
        if graph == 'PaperNet':
            graph = self.paper_net
            dictionary = self.title2id_dict
            inv_dict = self.id2title_dict
            edge = graph.edges[dictionary[node1], dictionary[node2]]
            return str(edge)
        elif graph == 'AuthorNet':
            graph = self.author_net
            dictionary = self.author2id_dict
            inv_dict = self.id2author_dict
            edge = graph.edges[dictionary[node1], dictionary[node2]]
            for id in range(len(edge['papers'])):
                edge['papers'][id] = inv_dict[edge['papers'][id]]
            return str(edge)

if __name__ == '__main__':
    # test
    graph_toolkits = graph_toolkits(".")
    logs = graph_toolkits.load_graph('dblp')
    print(str(graph_toolkits.check_neighbours('PaperNet, HRFormer: High-Resolution Vision Transformer for Dense Predict.')))
    print(str(graph_toolkits.check_neighbours('AuthorNet, Chao Zhang')))
    print(str(graph_toolkits.check_nodes('PaperNet, Learning the Principle of Least Action with Reinforcement Learning.')))
    print(str(graph_toolkits.check_nodes('AuthorNet, He Zhang')))
    # print(graph_toolkits.check_edges('PaperNet, 5fbe62d191e011e6e11b3d73, 5fbe62d191e011e6e11b3d73'))
    print(str(graph_toolkits.check_edges('AuthorNet, Chao Zhang, Weihong Lin')))
    print(str(graph_toolkits.check_neighbours('AuthorNet, Weihong Lin')))
