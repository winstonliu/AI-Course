#Implement the function DecisionSupport

'''
For this question you may use the code from part 1

Note however that part 2 will be marked independent of part 1

The solution for VariableElimination.py will be used for testing part2 instead
of the copy you submit. 
'''

from MedicalBayesianNetwork import *
from VariableElimination import *

def multi_min_fill_ordering(Factors, QueryVars):
    '''Compute a min fill ordering given a list of factors. Return a list
    of variables from the scopes of the factors in Factors. All factors in QueryVar are
    NOT part of the returned ordering'''
    scopes = []
    for f in Factors:
        scopes.append(list(f.get_scope()))
    Vars = []
    for s in scopes:
        for v in s:
            if not v in Vars and not v in QueryVars:
                Vars.append(v)
    
    ordering = []
    while Vars:
        (var,new_scope) = min_fill_var(scopes,Vars)
        ordering.append(var)
        if var in Vars:
            Vars.remove(var)
        scopes = remove_var(var, new_scope, scopes)
    return ordering

def MultiVarElim(net, queryVars, evidenceVars):
    """
        NOTE * Result not normalized
    """
    mod_factors = net.factors()

    # Replace factors with "evidence"
    for i,f in enumerate(net.factors()):
        for e in evidenceVars:
            if e in f.get_scope():
                mod_factors[i] = restrict_factor(f,e,e.get_evidence())

    order = multi_min_fill_ordering(net.factors(), queryVars)

    # Eliminate
    for r in order:
        # Find factors that contain r
        elim_list = [s for s in mod_factors if r in s.get_scope()]
        if not elim_list: continue
        new_fac = sum_out_variable(multiply_factors(elim_list), r)

        # Remove elim_list from mod_factors
        mod_factors = [x for x in mod_factors if x not in elim_list]
        mod_factors.append(new_fac)


    # Remaining factors in mod_factors should now only contain queryVars
    mult_fac = multiply_factors(mod_factors)
    
    # RESULT NOT NORMALIZED

    return mult_fac

'''
Parameters:
             medicalNet - A MedicalBayesianNetwork object                        

             patient    - A Patient object
                          The patient to calculate treatment-outcome
                          probabilites for
Return:
         -A factor object

         This factor should be a probability table relating all possible
         Treatments to all possible outcomes
'''
def DecisionSupport(medicalNet, patient):
    # Set evidence
    medicalNet.set_evidence_by_patient(patient)

    ret_list =  medicalNet.getOutcomeVars() + medicalNet.getTreatmentVars()
    ret_fac = Factor("Decision Support", ret_list)

    # Norm dict - normalization dictionary
    # Key: tuple of T values, Values: value
    norm_dict = {}
    add_list = []

    tmp_treat = Factor("do not use", medicalNet.getTreatmentVars())
    for treat_assign in tmp_treat.get_assignment_iterator():
        # Set "evidence" variables
        treatVar = medicalNet.getTreatmentVars() 
        for i,v in enumerate(treatVar):
            v.set_evidence(treat_assign[i])

        outcome_fac = MultiVarElim(medicalNet.net, medicalNet.getOutcomeVars(), treatVar+patient.evidenceVariables())

        for out_assign in outcome_fac.get_assignment_iterator():
            add_list += [out_assign + treat_assign + [outcome_fac.get_value(out_assign)]]

        norm_dict[tuple(treat_assign)] = sum(outcome_fac.values)
    
    # Normalize
    out_size = len(medicalNet.getOutcomeVars()) 
    treat_loc = len(medicalNet.getTreatmentVars()) + out_size
    for p in add_list:
        nd_sum = norm_dict[tuple(p[out_size:treat_loc])]
        norm = 1/nd_sum
        norm_ans = p[-1]*norm
        ret_fac.add_value_at_assignment(norm_ans, p)

    return ret_fac
