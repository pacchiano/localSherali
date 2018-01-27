import itertools
import numpy as np
import os


def get_size_j_subsets(n, j, avoid_set = set([]), input_set = set([])):
	nlist = list(range(n))
	if len(input_set) > 0:
		nlist = list(input_set)

	all_size_j_sets = list(itertools.combinations(nlist, j))
	if len(avoid_set) > 0:
		filtered_size_j_sets = []
		for s in all_size_j_sets:
			if not avoid_set.issubset(set(s)):
				filtered_size_j_sets.append(s)
		return filtered_size_j_sets
	else:

		return all_size_j_sets



def get_variable_names_list(n,k, avoid_set = set([]), input_set = set([])):
	variables = ["u"]
	for j in range(1, k+1):
		if len(input_set) > 0:
			size_j_subsets = get_size_j_subsets(n, j, avoid_set = avoid_set, input_set = input_set)
		else:
			size_j_subsets = get_size_j_subsets(n, j, avoid_set = avoid_set)
		for s in size_j_subsets:
				var_name = ""
				for i in s:
					var_name += "z" + str(i)
				variables.append(var_name)
	return variables


def save_constraint_matrix( constraint_matrix, variables, filename   ):
	header = "::"

	for v in variables:
		header += " " + v

	np.savetxt( filename, constraint_matrix, fmt="%d", delimiter = "\t", header = header)


def get_lk(n, k, avoid_set = set([]), input_set = set([])):
	if k >= 5:
		raise ValueError("K>=5 not implemented!!!!!")
	
	if len(input_set) > 0:
		variables = get_variable_names_list(n,k, avoid_set=avoid_set, input_set = input_set)
		size_k_subsets = get_size_j_subsets(n,k, avoid_set = avoid_set, input_set = input_set)		
	else:
		variables = get_variable_names_list(n,k, avoid_set=avoid_set)
		size_k_subsets = get_size_j_subsets(n,k, avoid_set = avoid_set)
	
	num_constraints = len(size_k_subsets)*(2**k) + 1

	#print(variables)
	constraint_matrix = np.zeros( (num_constraints, len(variables)))
	u_index = variables.index("u")
	constraint_matrix[:,u_index] = 1

	const_matrix_index = 0

	signs = [-1,1]
	for s in size_k_subsets:
	
		if len(avoid_set) > 0 and avoid_set.issubset(set(s)):
			continue
		else:
			### cartesian product of (-1,1)\times .... (-1,1) k times
			if k == 2:
				assigments = itertools.product(signs, signs)
			if k == 3:
				assigments = itertools.product(signs, signs, signs)
			if k == 4:
				assigments = itertools.product(signs, signs, signs, signs)
			#print(s)
			for x in assigments:
				#print(x)
				for i in range(1, k+1):
					#print(i)
					subsets_size_i_of_s = list(itertools.combinations(s,i))
					#print(subsets_size_i_of_s)
					for s_i in subsets_size_i_of_s:
						variable_name = ""
						entry_value = 1
						for node in s_i:
							index = s.index(node)
							entry_value = entry_value*x[index]
							variable_name += "z" + str(node)
						#print( variable_name, entry_value)
						variable_index = variables.index(variable_name)
						constraint_matrix[const_matrix_index, variable_index] = entry_value 

				const_matrix_index += 1

	return constraint_matrix, variables

def run_tri():
	constraint_matrix, variables  = get_lk(4,3,avoid_set = set([0,1]))
	header = "::"

	for v in variables:
		header += " " + v

	np.savetxt( "chordal_tri.txt", constraint_matrix, fmt="%d", delimiter = "\t", header = header)


	constraint_matrix, variables  = get_lk(4,3)#avoid_set = set([0,1]))
	header = "::"
	for v in variables:
		header += " " + v

	np.savetxt( "all_tri.txt", constraint_matrix, fmt="%d", delimiter = "\t", header = header)


def run_quad():
	constraint_matrix, variables  = get_lk(6,4,avoid_set = set([0,1]))
	header = "::"

	for v in variables:
		header += " " + v

	np.savetxt( "chordal_quad6.txt", constraint_matrix, fmt="%d", delimiter = "\t", header = header)


	constraint_matrix, variablesfull  = get_lk(6,4)#avoid_set = set([0,1]))
	header = "::"
	for v in variablesfull:
		header += " " + v

	np.savetxt( "all_quad6.txt", constraint_matrix, fmt="%d", delimiter = "\t", header = header)

	final_text = ""
	for u in variablesfull:
		if u not in variables:
			final_text += u + " "

	print(final_text)



def run_quadrilateral_tri():
	constraint_matrix, variables = get_lk(4,3)
	header = "::"
	
	for v in variables:
		header += " " + v

	np.savetxt( "quadrilateral_tri.txt", constraint_matrix, fmt="%d", delimiter = "\t", header = header)


def run_edge_loc():
	constraint_matrix, variables = get_lk(2,2)
	header = "::"
	
	for v in variables:
		header += " " + v

	np.savetxt( "loc_edge.txt", constraint_matrix, fmt="%d", delimiter = "\t", header = header)


def get_quadrilateral_edges_loc():
	avoid_set = set([])
	n=2
	k=2
	#variables = get_variable_names_list(n,k, avoid_set=avoid_set)
	#size_k_subsets = get_size_j_subsets(n,k, avoid_set = avoid_set)
	#num_constraints = len(size_k_subsets)*(2**k) + 1

	size_k_subsets = [set([0,1]), set([1,2]), set([2,3]), set([0,3])]

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


			filename = "./quadrilateral_edge_loc_files/support" +  code + ".txt"

			save_constraint_matrix( constraint_matrix, variables, filename)

			edge_and_singleton_variables = [x for x in variables if x.count("z") <= 2 ]

			edge_var_string_projection = ""

			output_filename = "./quadrilateral_edge_loc_files/support" +  code + "_edge.txt"

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


def run_quadrilateral_edge_loc():
	
	chordal_variables, constraints_chordal  = get_quadrilateral_edges_loc()
	header = "#::"
	for v in chordal_variables:
		header += " " + v
	header += "\n"

	f = open("./quadrilateral_edge_loc.txt", "w")

	f.write(header)
	for l in constraints_chordal:
		f.write(l)
	f.close()





run_edge_loc()
run_quadrilateral_tri()

run_quadrilateral_edge_loc()