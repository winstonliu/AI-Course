#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

'''
Construct and return Futoshiki CSP models.
'''

from cspbase import *
import itertools

import pprint
pp = pprint.PrettyPrinter(indent=4)
def DEBUG(x):
    # pp.pprint ("                                         <<|{}".format(x))
    pp.pprint (x)
    pass

def futoshiki_csp_model_1(initial_futoshiki_board):
    '''Return a CSP object representing a Futoshiki CSP problem along with an
    array of variables for the problem. That is return

    futoshiki_csp, variable_array

    where futoshiki_csp is a csp representing futoshiki using model_1 and
    variable_array is a list of lists

    [ [  ]
      [  ]
      .
      .
      .
      [  ] ]

    such that variable_array[i][j] is the Variable (object) that you built to
    represent the value to be placed in cell i,j of the futoshiki board
    (indexed from (0,0) to (n-1,n-1))


    The input board is specified as a list of n lists. Each of the n lists
    represents a row of the board. If a 0 is in the list it represents an empty
    cell. Otherwise if a number between 1--n is in the list then this
    represents a pre-set board position.

    Each list is of length 2n-1, with each space on the board being separated
    by the potential inequality constraints. '>' denotes that the previous
    space must be bigger than the next space; '<' denotes that the previous
    space must be smaller than the next; '.' denotes that there is no
    inequality constraint.

    E.g., the board

    -------------------
    | > |2| |9| | |6| |
    | |4| | | |1| | |8|
    | |7| <4|2| | | |3|
    |5| | | | | |3| | |
    | | |1| |6| |5| | |
    | | <3| | | | | |6|
    |1| | | |5|7| |4| |
    |6> | |9| < | |2| |
    | |2| | |8| <1| | |
    -------------------
    would be represented by the list of lists

    [[0,'>',0,'.',2,'.',0,'.',9,'.',0,'.',0,'.',6,'.',0],
     [0,'.',4,'.',0,'.',0,'.',0,'.',1,'.',0,'.',0,'.',8],
     [0,'.',7,'.',0,'<',4,'.',2,'.',0,'.',0,'.',0,'.',3],
     [5,'.',0,'.',0,'.',0,'.',0,'.',0,'.',3,'.',0,'.',0],
     [0,'.',0,'.',1,'.',0,'.',6,'.',0,'.',5,'.',0,'.',0],
     [0,'.',0,'<',3,'.',0,'.',0,'.',0,'.',0,'.',0,'.',6],
     [1,'.',0,'.',0,'.',0,'.',5,'.',7,'.',0,'.',4,'.',0],
     [6,'>',0,'.',0,'.',9,'.',0,'<',0,'.',0,'.',2,'.',0],
     [0,'.',2,'.',0,'.',0,'.',8,'.',0,'<',1,'.',0,'.',0]]


    This routine returns Model_1 which consists of a variable for each cell of
    the board, with domain equal to [1,...,n] if the board has a 0 at that
    position, and domain equal [i] if the board has a fixed number i at that
    cell.

    Model_1 also contains BINARY CONSTRAINTS OF NOT-EQUAL between all relevant
    variables (e.g., all pairs of variables in the same row, etc.).

    All of the constraints of Model_1 MUST BE binary constraints (i.e.,
    constraints whose scope includes two and only two variables).
    '''

    var_list = [] 
    cons = []
    # Get numerical length of the board
    n = len(initial_futoshiki_board)
    dom = [x+1 for x in range(n)]
    proc_queue = []

    # Grab variables and inequality constraints
    for i,row in enumerate(initial_futoshiki_board):
        var_row = []
        for j,col in enumerate(row[::2]):   # Variables only
            # Variable name is in format [y,x]
            if col == 0:
                var_row.append(Variable('V{},{}'.format(i,j), dom))
            else:
                var_row.append(Variable('V{},{}'.format(i,j), [col]))
        var_list.append(var_row)

        # Inequality constraints 
        for k,col in enumerate(row[1::2]):    # Ineqs only
            if col == '.':
                continue
            
            vc = var_list[i][k]     # Current variable
            ve = var_list[i][k+1]   # Next variable

            if col == '<':
                con = Constraint('LEQ[{},{}]<[{},{}]'.format(i,k,i,k+1),[vc,ve])
                sat_tuples = [t for t in itertools.product(vc.domain(),ve.domain()) if t[0]<t[1]] 
            elif col == '>':
                con = Constraint('GEQ[{},{}]>[{},{}]'.format(i,k,i,k+1),[vc,ve])
                sat_tuples = [t for t in itertools.product(vc.domain(),ve.domain()) if t[0]>t[1]] 

            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

    # Construct variable constraints
    # Make constraints of form:  FH[i,j]:[i+1 to end,j         ]
    # and ...                    FV[i,j]:[i         ,j+1 to end]
    for nrow in range(n):
        for ncol in range(n):
            vc = var_list[nrow][ncol]      # Current var

            # Horizontal elements
            for elem in range(ncol+1,n):    
                ve = var_list[nrow][elem]
                con = Constraint('FH[{},{}]:[{},{}]'.format(nrow,ncol,nrow,elem),[vc,ve])

                sat_tuples = [t for t in itertools.product(vc.domain(),ve.domain()) if not t[0]==t[1]] 
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

            # Vertical elements
            for elem in range(nrow+1,n):
                ve = var_list[elem][ncol]
                con = Constraint('FV[{},{}]:[{},{}]'.format(nrow,ncol,elem,ncol),[vc,ve])

                sat_tuples = [t for t in itertools.product(vc.domain(),ve.domain()) if not t[0]==t[1]] 
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

    # Flatten var_list and put into csp
    csp = CSP('{}-futoshiki'.format(n), [v for s in var_list for v in s])

    for c in cons:
        csp.add_constraint(c)


    return csp, var_list

##############################

def futoshiki_csp_model_2(initial_futoshiki_board):
    '''Return a CSP object representing a futoshiki CSP problem along with an
    array of variables for the problem. That is return

    futoshiki_csp, variable_array

    where futoshiki_csp is a csp representing futoshiki using model_2 and
    variable_array is a list of lists

    [ [  ]
      [  ]
      .
      .
      .
      [  ] ]

    such that variable_array[i][j] is the Variable (object) that you built to
    represent the value to be placed in cell i,j of the futoshiki board
    (indexed from (0,0) to (n-1,n-1))

    The input board takes the same input format (a list of n lists of size 2n-1
    specifying the board) as futoshiki_csp_model_1.

    The variables of Model_2 are the same as for Model_1: a variable for each
    cell of the board, with domain equal to [1,...,n] if the board has a 0 at
    that position, and domain equal [n] if the board has a fixed number i at
    that cell.

    However, Model_2 has different constraints. In particular, instead of
    binary non-equals constaints Model_2 has 2*n all-different constraints:
    all-different constraints for the variables in each of the n rows, and n
    columns. Each of these constraints is over n-variables (some of these
    variables will have a single value in their domain). Model_2 should create
    these all-different constraints between the relevant variables, and then
    separately generate the appropriate binary inequality constraints as
    required by the board. There should be j of these constraints, where j is
    the number of inequality symbols found on the board.  
    '''

    # want 2*n + j constraints

#IMPLEMENT
    var_list = [] 
    cons = []
    # Get numerical length of the board
    n = len(initial_futoshiki_board)
    dom = [x+1 for x in range(n)]
    proc_queue = []

    # Grab variables and inequality constraints
    for i,row in enumerate(initial_futoshiki_board):
        var_row = []
        for j,col in enumerate(row[::2]):   # Variables only
            # Variable name is in format [y,x]
            if col == 0:
                var_row.append(Variable('V{},{}'.format(i,j), dom))
            else:
                var_row.append(Variable('V{},{}'.format(i,j), [col]))
        var_list.append(var_row)

        # Inequality constraints 
        for k,col in enumerate(row[1::2]):    # Ineqs only
            if col == '.':
                continue
            
            vc = var_list[i][k]     # Current variable
            ve = var_list[i][k+1]   # Next variable

            if col == '<':
                con = Constraint('LEQ[{},{}]<[{},{}]'.format(i,k,i,k+1),[vc,ve])
                sat_tuples = [t for t in itertools.product(vc.domain(),ve.domain()) if t[0]<t[1]] 
            elif col == '>':
                con = Constraint('GEQ[{},{}]>[{},{}]'.format(i,k,i,k+1),[vc,ve])
                sat_tuples = [t for t in itertools.product(vc.domain(),ve.domain()) if t[0]>t[1]] 

            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

    # Construct all-different variable constraints
    # Make constraints of form:  FH[i    ,1:end]
    for nrow in range(n):
        con = Constraint('FH[{}]'.format(nrow),var_list[nrow])
        sat_tuples = []
        for t in itertools.permutations(dom, n):
            in_doms = True
            # Check to make sure all numbers in permutation are in domain
            for col in range(n):
                if t[col] not in var_list[nrow][col].domain():
                    in_doms = False
                    break;
            if in_doms:
                sat_tuples.append(t) 
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    # and ...                    FV[1:end,j    ]
    for ncol in range(n):
        con = Constraint('FV[{}]'.format(ncol),[p[ncol] for p in var_list])
        sat_tuples = []
        for t in itertools.permutations(dom, n):
            in_doms = True
            # Check to make sure all numbers in permutation are in domain
            for row in range(n):
                if t[row] not in var_list[row][ncol].domain():
                    in_doms = False
                    break;
            if in_doms:
                sat_tuples.append(t) 
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    # Flatten var_list and put into csp
    csp = CSP('{}-futoshiki'.format(n), [v for s in var_list for v in s])

    for c in cons:
        csp.add_constraint(c)


    return csp, var_list

