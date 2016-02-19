from cspbase import *
import itertools
import traceback

import propagators as soln_propagators

##Checking that importing a board into model 1 works as expected.
##Passing this test is a prereq for passing check_model_1_constraints.
def model_1_import(stu_models):
	score = 0
	print("---starting model_1_import---")
	try:
		board = [[3,'.',0,'.',0,'<',0],[0,'.',0,'.',0,'.',0],[0,'.',0,'<',0,'.',0],[0,'.',0,'>',0,'.',1]];
		answer = [[3], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1]]

		csp, var_array = stu_models.futoshiki_csp_model_1(board)
		lister = [] 

		for i in range(4):
			for j in range(4):
				lister.append(var_array[i][j].cur_domain())

		if lister != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister))
		else:
			print("PASS")
			score = 1
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
	print("---finished model_1_import---\n")
	return score

##Checking that importing a board into model 2 works as expected.
##Passing this test is a prereq for passing check_model_2_constraints.
def model_2_import(stu_models):
	score = 0
	print("---starting model_2_import---")
	try:
		board = [[3,'.',0,'.',0,'<',0],[0,'.',0,'.',0,'.',0],[0,'.',0,'<',0,'.',0],[0,'.',0,'>',0,'.',1]];
		answer = [[3], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1]]

		csp, var_array = stu_models.futoshiki_csp_model_2(board)
		lister = [] 

		for i in range(4):
			for j in range(4):
				lister.append(var_array[i][j].cur_domain())

		if lister != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister))
		else:
			print("PASS")
			score = 1
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
	print("---finished model_2_import---\n")
	return score

##Checks that model 1 constraints pass when all different, and fail when not all different
def check_model_1_constraints_enum(stu_models):
	score = 2
	print("---starting check_model_1_constraints_enum---")
	try: 
		board = [[3,'.',0,'.',0,'<',0],[0,'.',0,'.',0,'.',0],[0,'.',0,'<',0,'.',0],[0,'.',0,'>',0,'.',1]];

		csp, var_array = stu_models.futoshiki_csp_model_1(board)

		for cons in csp.get_all_cons():
			all_vars = cons.get_scope()
			taken = [] 
			domain_list = [] 
			should_pass = []
			should_fail = [] 
			for va in all_vars:
				domain_list.append(va.cur_domain())
				if len(va.cur_domain()) == 1:
					taken.append(va.cur_domain()[0])
			for i in range(len(all_vars)):
				va = all_vars[i]
				domain = domain_list[i] 
				if len(domain) == 1:
					should_pass.append(domain[0])
					should_fail.append(domain[0])
				else:
					for i in range(1,5):
						if i in domain and i in taken:
							should_fail.append(i)
							break
					for i in range(1,5):
						if i in domain and i not in taken:
							should_pass.append(i)
							taken.append(i)
							break
			if cons.check(should_fail) != cons.check(should_pass):
				if cons.check(should_fail) or not cons.check(should_pass):
					if not cons.check(should_fail):
						print("FAILED\nConstraint %s should be falsified by %r" % (str(cons),should_fail))
						print("var domains:")
						for va in all_vars:
							print(va.cur_domain())
					if cons.check(should_pass):
						print("FAILED\nConstraint %s should be satisfied by %r" % (str(cons),should_pass))
						print("var domains:")
						for va in all_vars:
							print(va.cur_domain())
					print("---finished check_model_1_constraints_enum---\n")
					return 0

	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
		print("---finished check_model_1_constraints_enum---\n")
		return 0

	print("PASS")
	print("---finished check_model_1_constraints_enum---\n")
	return score


##Checks that model 1 constraints are implemented as expected.
##Both model_1_import must pass and prop_FC must be implemented correctly for this test to behave as intended.
def check_model_1_constraints_FC(stu_model):
	score = 0
	print("---starting check_model_1_constraints_FC---")
	try: 
		board = [[3,'.',0,'.',0,'<',0],[0,'.',0,'.',0,'.',0],[0,'.',0,'<',0,'.',0],[0,'.',0,'>',0,'.',1]];
		answer = [[3], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1]]

		csp, var_array = stu_model.futoshiki_csp_model_1(board)
		lister = [] 
		soln_propagators.prop_FC(csp)
		for i in range(4):
			for j in range(4):
				lister.append(var_array[i][j].cur_domain())

		if lister != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister))
		else:
			print("PASS")
			score = 2
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
	print("---finished check_model_1_constraints_FC---\n")
	return score

##Checks that model 1 constraints are implemented as expected.
##Both model_1_import must pass and prop_GAC must be implemented correctly for this test to behave as intended.
def check_model_1_constraints_GAC(stu_model):
	score = 0
	print("---starting check_model_1_constraints_GAC---")
	try: 
		board = [[3,'.',0,'.',0,'<',0],[0,'.',0,'.',0,'.',0],[0,'.',0,'<',0,'.',0],[0,'.',0,'>',0,'.',1]];
		answer = [[3], [1, 2, 4], [1, 2], [2, 4], [1, 2, 4], [1, 2, 3, 4], [1, 2, 3, 4], [2, 3, 4], [1, 2, 4], [1, 2, 3], [2, 3, 4], [2, 3, 4], [2, 4], [3, 4], [2, 3], [1]]

		csp, var_array = stu_model.futoshiki_csp_model_1(board)
		lister = [] 
		soln_propagators.prop_GAC(csp)
		for i in range(4):
			for j in range(4):
				lister.append(var_array[i][j].cur_domain())

		if lister != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister))
		else:
			print("PASS")
			score = 2
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
	print("---finished check_model_1_constraints_GAC---\n")
	return score

##Both model_1_import must pass and prop_GAC must be implemented correctly for this test to behave as intended.
def check_model_1_constraints_GAC(stu_model):
	score = 0
	print("---starting check_model_1_constraints_GAC---")
	try: 
		board = [[3,'.',0,'.',0,'<',0],[0,'.',0,'.',0,'.',0],[0,'.',0,'<',0,'.',0],[0,'.',0,'>',0,'.',1]];
		answer = [[3], [1, 2, 4], [1, 2], [2, 4], [1, 2, 4], [1, 2, 3, 4], [1, 2, 3, 4], [2, 3, 4], [1, 2, 4], [1, 2, 3], [2, 3, 4], [2, 3, 4], [2, 4], [3, 4], [2, 3], [1]]

		csp, var_array = stu_model.futoshiki_csp_model_1(board)
		lister = [] 
		soln_propagators.prop_GAC(csp)
		for i in range(4):
			for j in range(4):
				lister.append(var_array[i][j].cur_domain())

		if lister != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister))
		else:
			print("PASS")
			score = 2
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
	print("---finished check_model_1_constraints_GAC---\n")
	return score

##Checks that model 2 constraints are implemented as expected.
##Both model_2_import must pass and prop_GAC must be implemented correctly for this test to behave as intended.
def check_model_2_constraints_FC(stu_model):
	score = 0
	print("---starting check_model_2_constraints_FC---")
	try: 
		board = [[3,'.',0,'.',0,'<',0],[0,'.',0,'.',0,'.',0],[0,'.',0,'<',0,'.',0],[0,'.',0,'>',0,'.',1]];
		answer = [[3], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1]]

		csp, var_array = stu_model.futoshiki_csp_model_2(board)
		lister = [] 
		soln_propagators.prop_FC(csp)
		for i in range(4):
			for j in range(4):
				lister.append(var_array[i][j].cur_domain())

		if lister != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister))
		else:
			print("PASS")
			score = 2
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
	print("---finished check_model_2_constraints_FC---\n")
	return score

##Checks that model 2 constraints are implemented as expected.
##Both model_2_import must pass and prop_GAC must be implemented correctly for this test to behave as intended.
def check_model_2_constraints_GAC(stu_model):
	score = 0
	print("---starting check_model_2_constraints_GAC---")
	try: 
		board = [[3,'.',0,'.',0,'<',0],[0,'.',0,'.',0,'.',0],[0,'.',0,'<',0,'.',0],[0,'.',0,'>',0,'.',1]];
		answer = [[3], [1, 2, 4], [1, 2], [2, 4], [1, 2, 4], [1, 2, 3, 4], [1, 2, 3, 4], [2, 3, 4], [1, 2, 4], [1, 2, 3], [2, 3, 4], [2, 3, 4], [2, 4], [3, 4], [2, 3], [1]]

		csp, var_array = stu_model.futoshiki_csp_model_2(board)
		lister = [] 
		soln_propagators.prop_GAC(csp)
		for i in range(4):
			for j in range(4):
				lister.append(var_array[i][j].cur_domain())

		if lister != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister))
		else:
			print("PASS")
			score = 2
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
	print("---finished check_model_2_constraints_GAC---\n")
	return score


def main(stu_propagators=None, stu_models=None):
	TOTAL_POINTS = 12
	total_score = 0

	import propagators as propagators_soln

	if stu_propagators == None:
		import propagators as stu_propagators
	else:
		import stu_propagators
	if stu_models ==None:
		import futoshiki_csp as stu_models
	else:
		import stu_models

	total_score += model_1_import(stu_models)
	total_score += check_model_1_constraints_enum(stu_models)
	total_score += check_model_1_constraints_FC(stu_models)
	total_score += check_model_1_constraints_GAC(stu_models)
	
	
	total_score += model_2_import(stu_models)
	total_score += check_model_2_constraints_FC(stu_models)
	total_score += check_model_2_constraints_GAC(stu_models)


	if total_score == TOTAL_POINTS:
		print("Score: %d/%d; Passed all tests." % (total_score,TOTAL_POINTS))
	else:
		print("Score: %d/%d; Did not pass all tests." % (total_score,TOTAL_POINTS))


if __name__=="__main__":
	main()
