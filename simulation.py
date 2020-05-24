from enum import Enum
import functools
import psutil
import random
import simpy
import sys
import time

import networkx as nx
from scipy.stats import norm

import graph
import network
import utility as util


def init_input_parameters(parameters):

	input_parameters = {}
	#initiate input parameters from the entries on the XML file
	input_parameters["switchTime"] = float(parameters["InputParameters"].find("switchTime").text)
	input_parameters["frameProcTime"] = float(parameters["InputParameters"].find("frameProcTime").text)
	input_parameters["transmissionTime"] = float(parameters["InputParameters"].find("transmissionTime").text)
	input_parameters["localTransmissionTime"] = float(parameters["InputParameters"].find("localTransmissionTime").text)
	input_parameters["cpriFrameGenerationTime"] = float(parameters["InputParameters"].find("cpriFrameGenerationTime").text)
	input_parameters["distributionAverage"] = float(parameters["InputParameters"].find("distributionAverage").text)
	input_parameters["cpriMode"] = parameters["InputParameters"].find("cpriMode").text
	input_parameters["distribution"] = lambda x: random.expovariate(1000)
	#limit of axis Y of the network topology on a cartesian plane
	input_parameters["limitAxisY"] = int(parameters["InputParameters"].find("limitAxisY").text)
	#limit of axis X of the network topology on a cartesian plane
	input_parameters["limitAxisX"] = int(parameters["InputParameters"].find("limitAxisX").text)
	#increasing step on axis Y when defining the size of the base station
	input_parameters["stepAxisY"] = int(parameters["InputParameters"].find("stepAxisY").text)
	#increasing step on axis X when defining the size of the base station
	input_parameters["stepAxisX"] = int(parameters["InputParameters"].find("stepAxisX").text)

	return input_parameters

def get_attributes(parameters, param_type):

	attributes = []

	for i in parameters[param_type]:
		attributes.append(i.attrib)

	return attributes

def start_simulation(env, env_duration = 3600):

    print("-"*80)
    print(f"SIMULATION STARTED AT {env.now}")
    print("-"*80)

    env.run(until = env_duration)

    print("-"*80)
    print(f"SIMULATION ENDED AT {env.now}")
    print("-"*80)

    print(f"Memory consumption {psutil.virtual_memory()}")

def validate_graph():
	#Tests
	#print the graph
	print([i for i in nx.edges(G)])
	print(G.edges())
	print(G["RRH:0"]["Switch:0"]["weight"])
	print(G.graph)
	for i in nx.edges(G):
		print("{} --> {} Weight: {}".format(i[0], i[1], G[i[0]][i[1]]["weight"]))

	#calling Dijkstra to calculate the shortest path. Returning variables 
	# "length" and "path" are the total cost of the path and the path itself, respectively
	length, path = nx.single_source_dijkstra(G, "RRH:0", "Cloud:0")
	print(path)

	for i in range(len(rrhs)):
	 print(g["s"]["RRH{}".format(i)]["capacity"])

	print("-----------------RRHs-------------------")
	for i in rrhsParameters:
		print(i)

	print("-----------------Network Nodes-------------------")
	for i in netNodesParameters:
		print(i)

	print("-----------------Processing Nodes-------------------")
	for i in procNodesParameters:
		print(i)

	print("-----------------Edges-------------------")
	for i in networkEdges:
		print(i)

if __name__ == '__main__':

	try:
		xml_file = sys.argv[1] 
	except FileNotFoundError:
		util.create_config_file("configurations.xml")

	env = simpy.Environment()

	parameters = util.xmlParser(xml_file)
	input_parameters = init_input_parameters(parameters)

	rrhs_attributes = get_attributes(parameters, "RRHs")
	net_nodes_attributes = get_attributes(parameters, "NetworkNodes")
	proc_nodes_attributes = get_attributes(parameters, "ProcessingNodes")
	network_edges = get_attributes(parameters, "Edges")


	#save the id of each element to create the graph
	vertex = []
	#RRHs
	for r in rrhs_attributes:
		vertex.append("RRH:"+str(r["aId"]))
	#Network nodes
	for node in net_nodes_attributes:
		vertex.append(node["aType"]+":"+str(node["aId"]))
	#Processing nodes
	for proc in proc_nodes_attributes:
		vertex.append(proc["aType"]+":"+str(node["aId"]))

	#create the graph
	G = nx.Graph()
	#add the nodes to the graph
	for u in vertex:
		G.add_node(u)
	#add the edges and weights to the graph
	for edge in network_edges:
		G.add_edge(edge["source"], edge["destiny"], weight= float(edge["weight"]))

	#create the elements
	#create the RRHs
	for r in rrhs_attributes:
		rrh = network.RRH(env, r["aId"], input_parameters["distribution"], 
			input_parameters["cpriFrameGenerationTime"], 
			input_parameters["transmissionTime"], 
			input_parameters["localTransmissionTime"], G, 
			input_parameters["cpriMode"])
		network.elements[rrh.aId] = rrh

	#create the network nodes
	for node in net_nodes_attributes:
		net_node = network.NetworkNode(env, node["aId"], node["aType"], 
			float(node["capacity"]), node["qos"], input_parameters["switchTime"], 
			input_parameters["transmissionTime"], G)
		network.elements[net_node.aId] = net_node

	#create the processing nodes
	for proc in proc_nodes_attributes:
		proc_node = network.ProcessingNode(env, proc["aId"], proc["aType"], 
			float(proc["capacity"]), proc["qos"], 
			input_parameters["frameProcTime"], 
			input_parameters["transmissionTime"], G)
		network.elements[proc_node.aId] = proc_node

	#set the limit area of each base station
	util.createNetworkLimits(input_parameters["limitAxisX"],
		input_parameters["limitAxisY"],
		input_parameters["stepAxisX"],
		input_parameters["stepAxisY"],
		network.elements)

	#print the coordinate of each base station
	util.printBaseStationCoordinates(rrhs_attributes, network.elements)


	start_simulation(env)
