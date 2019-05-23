#!/usr/bin/python
# -*- coding: UTF-8 -*-


import pandas as pd 
import os
import argparse
"""
function: Transform the configuration files of each simulator of the neural 
		  network processor, so that you can compare the performance of the simulator.
"""
class convert_NPU:

	def __init__(self, file_path):

		"""
		file_path : the file will be convert to another format
		file_name : Get the file name 
		"""
		self.file_path = file_path
		self.file_name = file_path.split('/')[-1].split('.')[0]

	def mkdir(self, dir_name):
		"""
		Determine if the configuration file directory exists
		"""
		dir_path = './'+ dir_name
		folder = os.path.exists(dir_path)

		if not folder:
			os.makedirs(dir_path)
			print "----- new folder -----"
			print "-------- ok -------"
		else:
			print "--- There is this folder! ---"



	def SCALE_to_MAE(self):

		""" 
		This is a convert func that able to convert the layer of 
		SCALE-SIM to the layer of MAESTRO 
		"""
		
		# Create a new directory to place the MAESTRO configuration file
		self.mkdir(self.file_name)

		# read csv file
		df = pd.read_csv(self.file_path,dtype= str)

		"""
		 Create a new MAESTRO configuration file for each layer of SCALE configuration
		"""
# ----------------------------------------------------
		for i in range(0,11):
# ----------------------------------------------------scope 
			with open('./'+self.file_name+'/'+df["Layer name"][i],'w+') as file:
				
				file.write('K '+df[' Channels'][i]+'\n'+
						   'C '+df[' Num Filter'][i]+'\n'+
						   'R '+df[' Filter Height'][i]+'\n'+
						   'S '+df[' Filter Width'][i]+'\n'+
						   'Y '+df[' IFMAP Height'][i]+'\n'+
						   'X '+df[' IFMAP Width'][i])
				

	def SCALE_to_nn(self):

		""" 
		This is a convert func that able to convert the layer of 
		SCALE-SIM to the layer of nn-dataflow 
		"""
		df = pd.read_csv(self.file_path,dtype= str)
		with open('./' +self.file_name+'.py','w') as file:
			file.write(
				'from nn_dataflow.core import Network \n'+
				'from nn_dataflow.core import InputLayer, ConvLayer, FCLayer, PoolingLayer \n'+
				'NN = Network(\''+self.file_name+'\') \n'+
				'NN.set_input_layer(InputLayer(3, 224)) \n'
				)
		# write Nerual network structure
			for i in range(0,11):
				file.write(
				'NN.add(\''+'conv'+'\', ConvLayer('+df[' Channels'][i]+', '+ df[' Num Filter'][i]+', '+ df[' IFMAP Height'][i]+', '+df[' Filter Height'][i] +')) \n'
				)		
def Option():
	
	#Interpret command line parameters

	parser = argparse.ArgumentParser(description='This is a conversion script that converts the SCALE-sim configuration file into two other NPU simulators (nn-dataflow, MAESTRO). It is designed to let you freely convert your network configuration file between the three simulators as soon as possible.')
	parser.add_argument('--file_path', dest='file_path',
	            default='./SCALE-Sim/topologies/CSV/LSTM.csv',
	                    help='Please specify the path to the SCLAE-sim simulator neural network configuration file')
	parser.add_argument('--mode', dest='mode',
	           default='nn-dataflow',
	                    help='Please specify the simulator you want to convert')

	args = parser.parse_args()
	return args.file_path,args.mode


def main():

	# SCALE_sim configure file  
	SCALE_FILE_PATH,mode = Option()

	# Judging the operating mode
	cvt = convert_NPU(SCALE_FILE_PATH)
	if mode == "nn-dataflow":
		cvt.SCALE_to_nn()
		if mode == "MAESTRO":
			cvt.SCALE_to_MAE()
	else:
		print "Simulator name is incorrect！" 

	cvt = convert_NPU(SCALE_FILE_PATH)
	cvt.SCALE_to_nn()


if __name__ == '__main__':
	main()