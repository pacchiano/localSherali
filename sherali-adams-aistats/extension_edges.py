import itertools
import numpy as np
from extension import *
import os

def get_edge_lk(n, k, avoid_set = set([])):
	if k>= 5:
		raise ValueError("Not yet implemented!")

	#variables = get_variable_names_list(n,k, avoid_set=avoid_set)
	size_k_subsets = get_size_j_subsets(n,k, avoid_set = avoid_set)
	#num_constraints = len(size_k_subsets)*(2**k) + 1

	all_variables = []
	all_edge_variables = []

	all_edge_constraints = []

	for s in size_k_subsets:
	
		if len(avoid_set) > 0 and avoid_set.issubset(set(s)):
			continue
		else:
	
			code = ""
			for v in s:
				code += "z" + str(v) 

			constraint_matrix, variables = 	get_lk(n, k, avoid_set = avoid_set, input_set = s)

			#import IPython
			#IPython.embed()


			filename = "./extension_edge_files/support" +  code + ".txt"

			save_constraint_matrix( constraint_matrix, variables, filename)

			edge_and_singleton_variables = [x for x in variables if x.count("z") <= 2 ]

			edge_var_string_projection = ""

			output_filename = "./extension_edge_files/support" +  code + "_edge.txt"

			for v in edge_and_singleton_variables:
				edge_var_string_projection += v + " "

			os.system( "fme " + filename + " -o " + output_filename + " -p -s " + '"' +  edge_var_string_projection +  '"'  + " -v")

			f = open(output_filename, "r")
			
			constraints = f.readlines()

			f.close()

			all_edge_constraints += constraints[1:]

			#import IPython
			#IPython.embed()

			all_variables += variables

			all_edge_variables += edge_and_singleton_variables

	return set(all_edge_variables), list(set(all_edge_constraints))





def run_tri():
	chordal_variables, constraints_chordal  = get_edge_lk(4,3,avoid_set = set([0,1]))
	variables, constraints  = get_edge_lk(4,3)#avoid_set = set([0,1]))

	print("chordal variables ", chordal_variables)
	print("all variables ", variables)

def run_quad():
	chordal_variables, constraints_chordal  = get_edge_lk(5,4,avoid_set = set([0,1]))
	header = "#::"
	for v in chordal_variables:
		header += " " + v
	header += "\n"

	f = open("./extension_edge_files/quad_edge_5_chordal.txt", "w")

	f.write(header)
	for l in constraints_chordal:
		f.write(l)
	f.close()


	all_variables, constraints = get_edge_lk(5,4)#avoid_set = set([0,1]))
	header = "#::"
	for v in all_variables:
		header += " " + v
	header += "\n"

	f = open("./extension_edge_files/quad_edge_5.txt", "w")

	f.write(header)
	for l in constraints:
		f.write(l)
	f.close()
	


	print(constraints)

	final_text = ""
	for u in list(all_variables):
		if u not in list(chordal_variables):
			final_text += u + " "

	print("to eliminate variables ", final_text)

	final_text = ""
	for u in list(all_variables):
			final_text += u + " "

	print("all variables ", final_text)

	final_text = ""
	for u in list(chordal_variables):
			final_text += u + " "


	print("chordal variables ", final_text)


#run_tri()
run_tri()

