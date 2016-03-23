from BayesianNetwork import *
import collections

##Implement all of the following functions

## Do not modify any of the objects passed in as parameters!
## Create a new Factor object to return when performing factor operations



'''
multiply_factors(factors)

Parameters :
              factors : a list of factors to multiply
Return:
              a new factor that is the product of the factors in "factors"
'''
def multiply_factors(factors):
    old_fac = factors[0]
    for i,f in enumerate(factors):
        if i == 0: continue 
         
        # Scope intersection
        scope_int = list(set(old_fac.get_scope()) & set(f.get_scope()))
        if not scope_int: continue

        # Get new list of unique variables in previous order
        tmp_list = list(collections.OrderedDict.fromkeys(old_fac.get_scope() + f.get_scope()))
        tmp_list_name = [k.name for k in tmp_list]
        tmp_fac = Factor("M", tmp_list) 

        # Get indicies of unique variables
        old_fac_idx = [i for i,s in enumerate(old_fac.get_scope()) if s.name in tmp_list_name]
        f_idx = [i for i,s in enumerate(f.get_scope()) if s.name in tmp_list_name]

        for k in old_fac.get_assignment_iterator():        
            for n in f.get_assignment_iterator():
                # Check if the values are the same
                if [k[i] for i in old_fac_idx] == [n[i] for i in f_idx]:
                    tmp = list(collections.OrderedDict.fromkeys(k + n))
                    old_val = old_fac.get_value(k)
                    f_val = f.get_value(n)
                    tmp_fac.add_value_at_assignment(old_val*f_val, tmp)
                    
#       for a in tmp_fac.get_assignment_iterator():
#           old_fac_as = [a[i] for i in old_fac_idx]
#           old_val = old_fac.get_value(old_fac_as)

#           f_as = [a[i] for i in f_idx]
#           f_val = f.get_value(f_as)

#           tmp_fac.add_value_at_assignment(old_val*f_val, a)

        old_fac = tmp_fac
    
    return old_fac

'''
restrict_factor(factor, variable, value):

Parameters :
              factor : the factor to restrict
              variable : the variable to restrict "factor" on
              value : the value to restrict to
Return:
              A new factor that is the restriction of "factor" by
              "variable"="value"
      
              If "factor" has only one variable its restriction yields a 
              constant factor
'''
def restrict_factor(factor, variable, value):
    if not variable in factor.get_scope(): return None 

    var_idx = factor.get_scope().index(variable) # find idx of variable
    ret_list = [s for s in factor.get_scope() if s.name != variable.name]

    # Initialize returned factor
    ret_fac = Factor("R-"+variable.name+"-"+factor.name, ret_list)

    # Iterate through all factors, allocate those that correspond to value
    for c in factor.get_assignment_iterator():
        if c[var_idx] == value:
            tmp = list(c)
            del tmp[var_idx]
            ret_fac.add_value_at_assignment(factor.get_value(c), tmp)
    
    return ret_fac

    
'''    
sum_out_variable(factor, variable)

Parameters :
              factor : the factor to sum out "variable" on
              variable : the variable to sum out
Return:
              A new factor that is "factor" summed out over "variable"
'''
def sum_out_variable(factor, variable):
    if not variable in factor.get_scope(): return None 

    var_idx = factor.get_scope().index(variable) # find idx of variable
    ret_list = [s for s in factor.get_scope() if s.name != variable.name]

    # Initialize returned factor
    ret_fac = Factor("R-"+variable.name+"-"+factor.name, ret_list)

    # Iterate through all factors, allocate those that correspond to value
    for c in factor.get_assignment_iterator():
        tmp = list(c)
        del tmp[var_idx]
        # Sum with existing value
        last_val = ret_fac.get_value(tmp)
        ret_fac.add_value_at_assignment(factor.get_value(c)+last_val, tmp)
    
    return ret_fac


'''
VariableElimination(net, queryVar, evidenceVars)

 Parameters :
              net: a BayesianNetwork object
              queryVar: a Variable object
                        (the variable whose distribution we want to compute)
              evidenceVars: a list of Variable objects.
                            Each of these variables should have evidence set
                            to a particular value from its domain using
                            the set_evidence function. 

 Return:
         A distribution over the values of QueryVar
 Format:  A list of numbers, one for each value in QueryVar's Domain
         -The distribution should be normalized.
         -The i'th number is the probability that QueryVar is equal to its
          i'th value given the setting of the evidence
 Example:

 QueryVar = A with Dom[A] = ['a', 'b', 'c'], EvidenceVars = [B, C]
 prior function calls: B.set_evidence(1) and C.set_evidence('c')

 VE returns:  a list of three numbers. E.g. [0.5, 0.24, 0.26]

 These numbers would mean that Pr(A='a'|B=1, C='c') = 0.5
                               Pr(A='b'|B=1, C='c') = 0.24
                               Pr(A='c'|B=1, C='c') = 0.26
'''       
def VariableElimination(net, queryVar, evidenceVars):
    # XXX TODO
    order = min_fill_ordering(net.factors(), queryVar)
    mod_factors = net.factors()

    # Replace factors with evidence
    for i,f in enumerate(net.factors()):
        for e in evidenceVars:
            if e in f.get_scope():
                mod_factors[i] = restrict_factor(f,e,e.get_evidence())
    
    # Eliminate
    for r in order:
        # Find factors that contain r
        elim_list = [s for s in mod_factors if r in s.get_scope()]
        new_fac = sum_out_variable(multiply_factors(elim_list), r)

        # Remove elim_list from mod_factors
        mod_factors = [x for x in mod_factors if x not in elim_list]
        mod_factors.append(new_fac)

    # Remaining factors in mod_factors should now only contain queryVar
    mult_fac = multiply_factors(mod_factors)
    norm = 1/(sum(mult_fac))
    return [i*norm for i in mult_fac]
