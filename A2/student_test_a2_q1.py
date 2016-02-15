from cspbase import *
import itertools
import traceback

import propagators as soln_propagators


########################################
##Necessary setup to generate problems

def queensCheck(qi, qj, i, j):
    '''Return true if i and j can be assigned to the queen in row qi and row qj 
       respectively. Used to find satisfying tuples.
    '''
    return i != j and abs(i-j) != abs(qi-qj)

def nQueens(n):
    '''Return an n-queens CSP'''
    i = 0
    dom = []
    for i in range(n):
        dom.append(i+1)

    vars = []
    for i in dom:
        vars.append(Variable('Q{}'.format(i), dom))

    cons = []    
    for qi in range(len(dom)):
        for qj in range(qi+1, len(dom)):
            con = Constraint("C(Q{},Q{})".format(qi+1,qj+1),[vars[qi], vars[qj]]) 
            sat_tuples = []
            for t in itertools.product(dom, dom):
                if queensCheck(qi, qj, t[0], t[1]):
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)
    
    csp = CSP("{}-Queens".format(n), vars)
    for c in cons:
        csp.add_constraint(c)
    return csp

############################################

#@max_grade(1)
##Tests FC after the first queen is placed in position 1.
def test_simple_FC(stu_propagators):
	score = 0

	print("---starting test_simple_FC---")
	did_fail = False
	try:
		queens = nQueens(8)
		curr_vars = queens.get_all_vars()
		curr_vars[0].assign(1)
		stu_propagators.prop_FC(queens,newVar=curr_vars[0])
		answer = [[1],[3, 4, 5, 6, 7, 8],[2, 4, 5, 6, 7, 8],[2, 3, 5, 6, 7, 8],[2, 3, 4, 6, 7, 8],[2, 3, 4, 5, 7, 8],[2, 3, 4, 5, 6, 8],[2, 3, 4, 5, 6, 7]]
		var_domain = [x.cur_domain() for x in curr_vars]
		for i in range(len(curr_vars)):
			if var_domain[i] != answer[i]:
				print("FAILED test_simple_FC\nExplanation:\nFC variable domains should be: %r\nFC variable domains are: %r" % (answer,var_domain))
				did_fail = True
				break
		if not did_fail:
			print("PASS")
			score = 2

	except Exception:
		print("Error occurred: %r" % traceback.print_exc())

	print("---finished test_simple_FC---\n")

	return score



#@max_grade(1)
##Tests GAC after the first queen is placed in position 1.
def test_simple_GAC(stu_propagators):
	score = 0
	print("---starting test_simple_GAC---")
	did_fail = False
	try:
		queens = nQueens(8)
		curr_vars = queens.get_all_vars()
		curr_vars[0].assign(1)
		stu_propagators.prop_GAC(queens,newVar=curr_vars[0])
		answer = [[1],[3, 4, 5, 6, 7, 8],[2, 4, 5, 6, 7, 8],[2, 3, 5, 6, 7, 8],[2, 3, 4, 6, 7, 8],[2, 3, 4, 5, 7, 8],[2, 3, 4, 5, 6, 8],[2, 3, 4, 5, 6, 7]]
		var_domain = [x.cur_domain() for x in curr_vars]
		for i in range(len(curr_vars)):
			if var_domain[i] != answer[i]:
				print("FAILED test_simple_GAC\nExplanation:\nGAC variable domains should be: %r\nGAC variable domains are: %r" % (answer,var_domain))
				did_fail = True
				break
		if not did_fail:
			print("PASS")
			score = 2

	except Exception:
		print("Error occurred: %r" % traceback.print_exc())

	print("---finished test_simple_GAC---\n")
	return score


#@max_grade(2)
##Simple example with 3 queens that results in different pruning for FC & GAC
##Q1 is placed in slot 2, q2 is placed in slot 4, and q8 is placed in slot 8.
##Checking GAC.
def three_queen_GAC(stu_propagators):
	score = 0
	print("---starting three_queen_GAC---")
	try:
		queens = nQueens(8)
		curr_vars = queens.get_all_vars()
		curr_vars[0].assign(4)
		curr_vars[2].assign(1)
		curr_vars[7].assign(5)
		stu_propagators.prop_GAC(queens)

		answer = [[4],[6, 7, 8],[1],[3, 8],[6, 7],[2, 8],[2, 3, 7, 8],[5]]
		var_vals = [x.cur_domain() for x in curr_vars]

		if var_vals != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,var_vals))

		else:
			print("PASS")
			score = 3
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())

	print("---finished three_queen_GAC---\n")
	return score

#@max_grade(2)
##Simple example with 3 queens that results in different pruning for FC & GAC
##Q1 is placed in slot 2, q2 is placed in slot 4, and q8 is placed in slot 8.
##Checking FC.
def three_queen_FC(stu_propagators):
	score = 0
	print("---starting three_queen_FC---")
	try:
		queens = nQueens(8)
		curr_vars = queens.get_all_vars()
		curr_vars[0].assign(4)
		curr_vars[2].assign(1)
		curr_vars[7].assign(5)
		stu_propagators.prop_FC(queens)

		answer = [[4],[6, 7, 8],[1],[3, 6, 8],[6, 7],[2, 6, 8],[2, 3, 7, 8],[5]]
		var_vals = [x.cur_domain() for x in curr_vars]

		if var_vals != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,var_vals))

		else:
			print("PASS")
			score = 3
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())

	print("---finished three_queen_FC---\n")
	return score


def w_eq_sum_x_y_z(wxyz):
	#note inputs lists of value
	w = wxyz[0]
	x = wxyz[1]
	y = wxyz[2]
	z = wxyz[3]
	return(w == x + y + z)

def test_1(propagator):
	score = 0
	try:
		x = Variable('X', [1, 2, 3])
		y = Variable('Y', [1, 2, 3])
		z = Variable('Z', [1, 2, 3])
		w = Variable('W', [1, 2, 3, 4])
		
		c1 = Constraint('C1', [x, y, z])
		#c1 is constraint x == y + z. Below are all of the satisfying tuples
		c1.add_satisfying_tuples([[2, 1, 1], [3, 1, 2], [3, 2, 1]])
		
		c2 = Constraint('C2', [w, x, y, z])
		#c2 is constraint w == x + y + z. Instead of writing down the satisfying
		#tuples we compute them
		
		varDoms = []
		for v in [w, x, y, z]:
		    varDoms.append(v.domain())    
		
		sat_tuples = []
		for t in itertools.product(*varDoms):
		    #NOTICE use of * to convert the list v to a sequence of arguments to product
		    if w_eq_sum_x_y_z(t):
		        sat_tuples.append(t)
		
		c2.add_satisfying_tuples(sat_tuples)
		
		simpleCSP = CSP("SimpleEqs", [x,y,z,w])
		simpleCSP.add_constraint(c1)
		simpleCSP.add_constraint(c2)
		
		btracker = BT(simpleCSP)
		#btracker.trace_on()
		
		btracker.bt_search(propagator)
		curr_vars = simpleCSP.get_all_vars()
		answer = [[2], [1], [1], [4]]
		var_vals = [x.cur_domain() for x in curr_vars]
		if var_vals != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,var_vals))
		else:
			print("PASS")
			score = 3
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())

	print("---finished test---\n")
	return score

def test_2(propagator):
	score = 0
	try:
		x = Variable('X', [1, 2, 3])
		y = Variable('Y', [1, 2, 3])
		z = Variable('Z', [1, 2, 3])
		
		c1 = Constraint('C1', [x, y, z])
		#c1 is constraint x == y + z. Below are all of the satisfying tuples
		c1.add_satisfying_tuples([[2, 1, 1], [3, 1, 2], [3, 2, 1]])
		
		c2 = Constraint('C2', [x, y])
		#c2 is constraint x + y = 1 mod 2.
		c2.add_satisfying_tuples([[1, 2], [2, 1], [2, 3], [3, 2]])
		
		c3 = Constraint('C2', [y, z])
		#c3 is constraint y != z
		c3.add_satisfying_tuples([[1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2]])
		
		
		
		simpleCSP = CSP("ParityEqs", [x,y,z])
		simpleCSP.add_constraint(c1)
		simpleCSP.add_constraint(c2)
		simpleCSP.add_constraint(c3)
		
		btracker = BT(simpleCSP)
		#btracker.trace_on()
		
		btracker.bt_search(propagator)
		curr_vars = simpleCSP.get_all_vars()
		answer = [[3], [2], [1]]
		var_vals = [x.cur_domain() for x in curr_vars]
		if var_vals != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,var_vals))
		else:
			print("PASS")
			score = 3
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())

	print("---finished test---\n")
	return score


def test_3(propagator):
	score = 0
	try:
		x = Variable('X', [1, 2, 3])
		y = Variable('Y', [1, 2, 3])
		z = Variable('Z', [1, 2, 3])
		
		c1 = Constraint('C1', [x, y, z])
		#c1 is constraint x == y + z. Below are all of the satisfying tuples
		c1.add_satisfying_tuples([[2, 1, 1], [3, 1, 2], [3, 2, 1]])
		
		c2 = Constraint('C2', [y, z])
		#c2 is constraint y + z = 0 mod 2.
		c2.add_satisfying_tuples([[1, 1], [1, 3], [2, 2], [3, 1], [3, 3]])
		
		c3 = Constraint('C3', [x, y])
		#c2 is constraint x + y = 0 mod 2.
		c3.add_satisfying_tuples([[1, 1], [1, 3], [2, 2], [3, 1], [3, 3]])
		
		
		simpleCSP = CSP("ParityEqs", [x,y,z])
		simpleCSP.add_constraint(c1)
		simpleCSP.add_constraint(c2)
		simpleCSP.add_constraint(c3)
		
		btracker = BT(simpleCSP)
		#btracker.trace_on()
		
		btracker.bt_search(propagator)
		curr_vars = simpleCSP.get_all_vars()
		answer = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
		var_vals = [x.cur_domain() for x in curr_vars]
		print(var_vals)
		if var_vals != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,var_vals))
		else:
			print("PASS")
			score = 3
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())

	print("---finished test---\n")
	return score


def main(stu_propagators=None, stu_models=None):
	TOTAL_POINTS = 28
	total_score = 0

	import propagators as propagators_soln

	if stu_propagators == None:
		import propagators as stu_propagators


	total_score += test_simple_FC(stu_propagators)
	total_score += test_simple_GAC(stu_propagators)
	total_score += three_queen_FC(stu_propagators)
	total_score += three_queen_GAC(stu_propagators)
	total_score += test_1(soln_propagators.prop_FC)
	total_score += test_1(soln_propagators.prop_GAC)
	total_score += test_2(soln_propagators.prop_FC)
	total_score += test_2(soln_propagators.prop_GAC)
	total_score += test_3(soln_propagators.prop_FC)
	total_score += test_3(soln_propagators.prop_GAC)


	if total_score == TOTAL_POINTS:
		print("Score: %d/%d; Passed all tests" % (total_score,TOTAL_POINTS))
	else:
		print("Score: %d/%d; Did not pass all tests." % (total_score,TOTAL_POINTS))







if __name__=="__main__":
	main()


