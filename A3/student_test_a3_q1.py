#Updated March 14, 2016

from BayesianNetwork import *
from VariableElimination import *
import traceback

#
#Note: The tests here are NOT Comprehensive
#
#You should consider all possible cases when implementing your code
#
#Cases not present in these tests will be used to evaluate your final submission
#
#You do not need to understand this code, but it may be useful to see how the functions you are to implement are used
#

#maximum difference allowed between equivalent values
epsilon = 0.01





#returns False if "value" is within "epsilon" of "answer", else True
def difference_check(value, answer):


    #handle the zero case differently
    if (answer == 0):
        if(abs(value) > 0.000000000001):
            return True
        else:
            return False
                        
    if(( abs(value - answer) / answer) <= epsilon):
        return False
    else:
        return True


#Helper function to reorder a factor's scope---produces a new factor.
#depends on the variables in the scope having names.
#Generates a new factor equivalent to the input factor f but with
#the scope ordered according to the list "scope_names" 
def reorder_factor_scope(f, scope_names):

    #Deal with the constant factor case
    if(scope_names == []):
        #technically for consistency this should be a copy of f
        #for the intended use case this should be fine
        return f

    
    d = dict()
    vdoms = []
    nscope = []
    for v in f.get_scope():
        d[v.name] = v
        vdoms.append(v.domain())
    for name in scope_names:
        nscope.append(d[name])
    nfactor = Factor(f.name, nscope)
    
    oldindex = []
    for name in scope_names:
        v = d[name]
        oldindex.append(f.scope.index(v))
        
    for assignment in nfactor.get_assignment_iterator():
        #construct the old assignment
        original_assignment = [0]*len(scope_names)
        for i in range(0,len(assignment)):
            original_assignment[oldindex[i]] = assignment[i]
        nfactor.add_value_at_assignment(f.get_value(original_assignment), assignment)
        
    return nfactor

#Helper function to test the equality of two scopes given that the variables in the
#scope lists might be ordered differently.
def scopesEquiv(s1, s2):
    #s1 and s2 are lists of variables.
    return set(s1) == set(s2)
    

#Helper function for testing.  Compares the probability table of a factor against expected results.
#Returns a two element list. Element 0 is the number of mismatches.  Element 1 is a string documenting the mismatches.
def comparetable(factor, values):

    outstring = ""
    counter = 0
    
    for i in range(0,len(values)):

        if(difference_check(factor.values[i],values[i])):
            counter += 1
            outstring += derankmismatch(factor,i) + " : Expected Value={} Actual Value={}".format(values[i],factor.values[i]) + '\n'

    return [counter, outstring]

#Helper Function for testing.  Given a factor and an index with respect to the factor.values list, returns a string
#corresponding to the variable assignment associated with that index
def derankmismatch(factor, index):

    outstr = "P("
    
    value = index
    scope = factor.get_scope()

    variableindex = []
    
    for v in reversed(scope):
        
        variableindex.append(int(value % v.domain_size()))        
        value = int(value / v.domain_size())
       
    variableindex = list(reversed(variableindex))

    for i in range(0, len(scope)):    
        outstr += ("{} = {},".format(scope[i].name, scope[i].dom[variableindex[i]]))
    
    return outstr[:-1] + ")"


#Helper function for testing purposes.  Not strictly necessary.
def scopefilter(scope):
    ret = []
    for i in scope:
        ret.append(repr(i))       
    return ret


#Factor Restriction Test Class
class RestrictionTest:

    #Factor is the factor to restrict such that variable = value
    def __init__(self, factor, variable, value, answer, name="factor restriction test"):
        self.name = name
        self.factor = factor
        self.variable = variable
        self.value = value
        self.answer = answer


    def test(self):
        #answer[0] : the desired scope
        #answer[1] : the desired table values               
        
        print("\nRunning Test : {}".format(self.name))
        
        try:

            result = restrict_factor(self.factor, self.variable, self.value)
            result2 = reorder_factor_scope(result, self.answer[0])
            scopetest = scopesEquiv(self.answer[0],scopefilter(result.get_scope()))


            if(not scopetest):
                print("\t[!] Scope of the resulting factor does not match expected result : ")
                print("\t\tExpected: " + repr(self.answer[0]))            
                print("\t\tActual:  " + repr(scopefilter(result.get_scope())))                
            else:
                print("\t[+] Scope of the resulting factor matches expected result")
                
                tabletest = comparetable(result2, self.answer[1])
                copytest = id(result) != id(self.factor)
                if(tabletest[0] == 0):
                    print("\t[+] Factor values match the expected result in all cases")
                    if copytest:
                        pass
                    else:                        
                        print("\t[!] input factor was changed")
                        
                else:
                    print("\t[!] Factor values mismatch the expected result in {} place{}:\n".format(tabletest[0], "" if (tabletest[0] == 1) else "s"))
                    print(tabletest[1]) 
            
        except:
            print("\t[!] Execution error:\n*****")
            traceback.print_exc()            
            
                
        
#Factor Variable Sum Out Test Class
class SummationTest:
    #factor is the factor to sum over, variable is the variable to sum out
    def __init__(self, factor, variable, answer, name="sum out variable test"):
        #answer[0] : the desired scope
        #answer[1] : the desired table values                
        self.name = name
        self.factor = factor
        self.variable = variable
        self.answer = answer

    def test(self):
        
        print("\nRunning Test : {}".format(self.name))       


        try:


            
            result = sum_out_variable(self.factor, self.variable)
            result2 = reorder_factor_scope(result, self.answer[0])
            

            scopetest = scopesEquiv(self.answer[0],scopefilter(result.get_scope()))

            if(not scopetest):
                
                print("\t[!] Scope of the resulting factor does not match expected result : ")
                print("\t\tExpected: " + repr(self.answer[0]))            
                print("\t\tActual:  " + repr(scopefilter(result.get_scope())))                
                
            else:
                print("\t[+] Scope of the resulting factor matches expected result")
                
                tabletest = comparetable(result2, self.answer[1])
                copytest = id(result) != id(self.factor)
                if(tabletest[0] == 0):
                    print("\t[+] Factor values match the expected result in all cases")
                    if(copytest):
                        pass
                    else:                        
                        print("\t[!] input factor was changed")                        
                else:
                    print("\t[!] Factor values mismatch the expected result in {} place{}:\n".format(tabletest[0], "" if (tabletest[0] == 1) else "s"))
                    print(tabletest[1])                            
                    
            
        except:

            print("\t[!] Execution error:\n*****")
            traceback.print_exc()            
                                    

                
#Factor Multiplication Test Class
class MultiplyTest:
    #factors is a list of factors to multiply
    def __init__(self, factors, answer,points, name="factor multiplication test"):
        self.name = name
        self.factors = factors
        self.answer = answer

                 
                 
    def test(self):

        #answer[0] : the desired scope
        #answer[1] : the desired table values                
        print("\nRunning Test : {}".format(self.name))
        
        try:
            
            result = multiply_factors(self.factors)
            result2 = reorder_factor_scope(result, self.answer[0])
            scopetest = scopesEquiv(self.answer[0],scopefilter(result.get_scope()))

            if(not scopetest):
                print("\t[!] Scope of the resulting factor does not match expected result : ")
                print("\t\tExpected: " + repr(self.answer[0]))            
                print("\t\tActual:  " + repr(scopefilter(result.get_scope())))                
            else:
                
                print("\t[+] Scope of the resulting factor matches expected result")                                
                tabletest = comparetable(result2, self.answer[1])
                if(tabletest[0] == 0):
                    print("\t[+] Factor values match the expected result in all cases")
                    copytest = id(result) != id(self.factors)
                    if(copytest):
                        pass
                    else:                    
                        print("\t[!] input factor was changed")                    
                else: 
                    print("\t[!] Factor values mismatch the expected result in {} place{}:\n".format(tabletest[0], "" if (tabletest[0] == 1) else "s"))
                    print(tabletest[1])                    

        except:

            print("\t[!] Execution error:\n*****")
            traceback.print_exc()            
                       


#Variable Elimination Test Class    
class VETest:


    #net is the bayes net, evidence is a list of pairs of the form [variable, value]
    def __init__(self, net, evidence, queryVariable, answer, name="variable elimination test"):
        self.name = name
        self.net = net
        self.evidence = evidence
        self.queryVariable = queryVariable
        self.answer = answer


        self.evidenceVars = []
        
        for i in self.evidence:
            i[0].set_evidence(i[1])
            self.evidenceVars.append(i[0])
                         
    def test(self):
        #answer[0] : a list of probabilities for the values for queryVariable



        print("\nRunning Test : {}".format(self.name))

        
        try:            
            for i in self.evidence:
                i[0].set_evidence(i[1])
            result = VariableElimination(self.net, self.queryVariable, self.evidenceVars)                 


            querytest = True 
            for i in range(0,len(self.answer[0])):
                if( difference_check(result[i],self.answer[0][i] )):
                    
                    querytest = False 

            if(querytest):
                print("\t[+] Probability distribution of the query variable matches the expected results")                
            else:
                print("\t[!] Probability distribution of the query variable does not match the expected results : ")
                print("\t\tExpected: " + repr(self.answer[0]))
                print("\t\tActual:  " + repr(result))                
            
        except:
            
            print("\t[!] Execution error:\n*****")
            traceback.print_exc()            
                        

        
if __name__ == '__main__':
    





    
    #Example Bayes Net
    VisitAsia = Variable('Visit_To_Asia', ['visit', 'no-visit'])
    F1 = Factor("F1", [VisitAsia])
    F1.add_values([['visit', 0.01], ['no-visit', 0.99]])
    
    Smoking = Variable('Smoking', ['smoker', 'non-smoker'])
    F2 = Factor("F2", [Smoking])
    F2.add_values([['smoker', 0.5], ['non-smoker', 0.5]])

    Tuberculosis = Variable('Tuberculosis', ['present', 'absent'])
    F3 = Factor("F3", [Tuberculosis, VisitAsia])
    F3.add_values([['present', 'visit', 0.05],
                   ['present', 'no-visit', 0.01],
                   ['absent', 'visit', 0.95],
                   ['absent', 'no-visit', 0.99]])

    Cancer = Variable('Lung Cancer', ['present', 'absent'])
    F4 = Factor("F4", [Cancer, Smoking])
    F4.add_values([['present', 'smoker', 0.10],
                   ['present', 'non-smoker', 0.01],
                   ['absent', 'smoker', 0.90],
                   ['absent', 'non-smoker', 0.99]])

    Bronchitis = Variable('Bronchitis', ['present', 'absent'])
    F5 = Factor("F5", [Bronchitis, Smoking])
    F5.add_values([['present', 'smoker', 0.60],
                   ['present', 'non-smoker', 0.30],
                   ['absent', 'smoker', 0.40],
                   ['absent', 'non-smoker', 0.70]])

    TBorCA = Variable('Tuberculosis or Lung Cancer', ['true', 'false'])
    F6 = Factor("F6", [TBorCA, Tuberculosis, Cancer])
    F6.add_values([['true', 'present', 'present', 1.0],
                   ['true', 'present', 'absent', 1.0],
                   ['true', 'absent', 'present', 1.0],
                   ['true', 'absent', 'absent', 0],
                   ['false', 'present', 'present', 0],
                   ['false', 'present', 'absent', 0],
                   ['false', 'absent', 'present', 0],
                   ['false', 'absent', 'absent', 1]])


    Dyspnea = Variable('Dyspnea', ['present', 'absent'])
    F7 = Factor("F7", [Dyspnea, TBorCA, Bronchitis])
    F7.add_values([['present', 'true', 'present', 0.9],
                   ['present', 'true', 'absent', 0.7],
                   ['present', 'false', 'present', 0.8],
                   ['present', 'false', 'absent', 0.1],
                   ['absent', 'true', 'present', 0.1],
                   ['absent', 'true', 'absent', 0.3],
                   ['absent', 'false', 'present', 0.2],
                   ['absent', 'false', 'absent', 0.9]])


    Xray = Variable('XRay Result', ['abnormal', 'normal'])
    F8 = Factor("F8", [Xray, TBorCA])
    F8.add_values([['abnormal', 'true', 0.98],
                   ['abnormal', 'false', 0.05],
                   ['normal', 'true', 0.02],
                   ['normal', 'false', 0.95]])

    Asia = BayesianNetwork("Asia", [VisitAsia, Smoking, Tuberculosis, Cancer,
                       Bronchitis, TBorCA, Dyspnea, Xray],
              [F1, F2, F3, F4, F5, F6, F7, F8])


    
    #This factor is for testing purposes only
    V1 = Variable('Colour', ['Red','Blue'])
    V2 = Variable('Distance', ['Close','Far'])
    V3 = Variable('Temperature', ['Cold','Hot'])
    F9 = Factor("F9", [V1,V2,V3])
    F9.add_values([['Red', 'Close', 'Cold', 0.3],
                   ['Red', 'Close', 'Hot', 0.05],
                   ['Red', 'Far', 'Cold', 0],
                   ['Red', 'Far', 'Hot', 0.2],
                   ['Blue', 'Close', 'Cold', 0.1],
                   ['Blue', 'Close', 'Hot', 0.15],
                   ['Blue', 'Far', 'Cold', 0.05],
                   ['Blue', 'Far', 'Hot',0.05]])


    #Based on the example from Russel and Norvig, Artificial Intelligence: A Modern Approach, 3rd Edition, Figure 14.2, Pg 512
    Burglary = Variable('Burglary', [True, False])
    Earthquake = Variable('Earthquake', [True, False])
    Alarm = Variable('Alarm', [True, False])
    John = Variable('John Calls', [True, False])
    Mary = Variable('Mary Calls', [True, False])


    #Duplicates
    Burglary2 = Variable('Burglary', [True, False])
    Earthquake2 = Variable('Earthquake', [True, False])
    Alarm2 = Variable('Alarm', [True, False])
    John2 = Variable('John Calls', [True, False])
    Mary2 = Variable('Mary Calls', [True, False])


    
    F10 = Factor("F10", [Burglary])
    F10.add_values([[True,  0.001],
                    [False, 0.999]])

    F10D = Factor("F10", [Burglary2])
    F10D.add_values([[True,  0.001],
                    [False, 0.999]])

    
    F11 = Factor("F11", [Earthquake])
    F11.add_values([[True,  0.002],
                    [False, 0.998]])


    F11D = Factor("F11", [Earthquake2])
    F11D.add_values([[True,  0.002],
                    [False, 0.998]])


    
    F12 = Factor("F12", [Burglary, Earthquake, Alarm])
    F12.add_values([[True, True, True, .95],
                    [True, True, False, .05],
                    [True, False, True, .94],
                    [True, False, False, .06],
                    [False, True, True, .29],
                    [False, True, False, .71],
                    [False, False, True, .001],
                    [False, False, False, .999]])


    F12D = Factor("F12", [Burglary2, Earthquake2, Alarm2])
    F12D.add_values([[True, True, True, .95],
                    [True, True, False, .05],
                    [True, False, True, .94],
                    [True, False, False, .06],
                    [False, True, True, .29],
                    [False, True, False, .71],
                    [False, False, True, .001],
                    [False, False, False, .999]])


    F13 = Factor("F13", [Alarm, John])
    F13.add_values([[True, True, .90],
                    [True, False, .10],
                    [False, True, .05],
                    [False, False, .95]])


    F13D = Factor("F13", [Alarm2, John2])
    F13D.add_values([[True, True, .90],
                    [True, False, .10],
                    [False, True, .05],
                    [False, False, .95]])


    F14 = Factor("F14", [Alarm, Mary])
    F14.add_values([[True, True, .70],
                    [True, False, .30],
                    [False, True, .01],
                    [False, False, .99]])


    F14D = Factor("F14", [Alarm2, Mary2])
    F14D.add_values([[True, True, .70],
                    [True, False, .30],
                    [False, True, .01],
                    [False, False, .99]])

    F17 = Factor("F17", [])
    F17.add_values([[.5]])
    
    
    AlarmNet = BayesianNetwork("Home Alarm", [Burglary, Earthquake, Alarm, John, Mary], [F10, F11, F12, F13, F14])

    AlarmNet2 = BayesianNetwork("Home Alarm", [Burglary2, Earthquake2, Alarm2, John2, Mary2], [F10D, F11D, F12D, F13D, F14D, F17])



    V4 = Variable('Response', ['Yes','No'])
    F15 = Factor("F15", [V4])
    F15.add_values([['Yes', .70],
                    ['No', .30]])

    
    V5 = Variable('Response', ['Yes','No'])
    F16 = Factor("F16", [V5])
    F16.add_values([['Yes', .98],
                    ['No', .45]])

    
    
    V6 = Variable('Arbitrary', [True,False])
    F17 = Factor("F17", [V6])
    F17.add_values([[True,  0.4],
                    [False, 0.6]])



    
    
    #The current list of tests
    t1 = RestrictionTest(F8, TBorCA, 'false', [['XRay Result',],[0.05,0.95]], "Factor Restriction Test 1")
    t2 = RestrictionTest(F9, V1, 'Blue', [['Distance','Temperature',],[0.1, 0.15, 0.05, 0.05]], "Factor Restriction Test 2")
    t3 = RestrictionTest(F9, V2, 'Close', [['Colour','Temperature',],[0.3, 0.05, 0.1, 0.15]], "Factor Restriction Test 3")
    t14 = RestrictionTest(F17, V6, True, [[],[0.4]], "Factor Restriction Test - Constant Factor")




    
    t4 = SummationTest(F6,Cancer,[['Tuberculosis or Lung Cancer','Tuberculosis',],[2.0, 1.0, 0, 1]], "Factor Sum Out Test 1")
    t5 = SummationTest(F9,V1,[['Distance','Temperature',],[0.4, 0.2, 0.05, 0.25]], "Factor Sum Out Test 2")
    t6 = SummationTest(F9,V2,[['Colour','Temperature',],[0.3, 0.25, 0.15000000000000002, 0.2]], "Factor Sum Out Test 3")


    

    t7 = MultiplyTest([F4,F5,F7],[['Lung Cancer','Smoking','Bronchitis','Dyspnea','Tuberculosis or Lung Cancer',],[0.054, 0.048, 0.006, 0.012, 0.028000000000000004, 0.004000000000000001, 0.012000000000000002, 0.03600000000000001, 0.0027, 0.0024000000000000002, 0.00030000000000000003, 0.0006000000000000001, 0.004899999999999999, 0.0007, 0.0021, 0.006299999999999999, 0.48600000000000004, 0.43200000000000005, 0.054000000000000006, 0.10800000000000001, 0.252, 0.036000000000000004, 0.10800000000000001, 0.32400000000000007, 0.2673, 0.2376, 0.0297, 0.0594, 0.4850999999999999, 0.0693, 0.20789999999999997, 0.6236999999999999]], "Factor Multiplication Test 1")
    t8 = MultiplyTest([F2,F5,F7],[['Smoking','Bronchitis','Dyspnea','Tuberculosis or Lung Cancer',],[0.27, 0.24, 0.03, 0.06, 0.13999999999999999, 0.020000000000000004, 0.06, 0.18000000000000002, 0.135, 0.12, 0.015, 0.03, 0.24499999999999997, 0.034999999999999996, 0.105, 0.315]], "Factor Multiplication Test 2")
    t9 = MultiplyTest([F2,F4,F5],[['Smoking','Lung Cancer','Bronchitis',],[0.03, 0.020000000000000004, 0.27, 0.18000000000000002, 0.0015, 0.0034999999999999996, 0.1485, 0.3465]], "Factor Multiplication Test 4")
     


    
    t10= VETest(Asia,[[Smoking,'smoker'], [Dyspnea,'present'], [Xray,'abnormal']],Cancer,[[0.7237140153108922, 0.27628598468910776]], "Variable Elimination Test 1")

    #This test is to make sure no input factors were altered!
    t11= VETest(Asia,[[Smoking,'smoker'], [Dyspnea,'present'], [Xray,'abnormal']],Cancer,[[0.7237140153108922, 0.27628598468910776]], "Variable Elimination Alteration Test (Repeat of 1)")

    t12 = VETest(Asia,[[VisitAsia,'visit'], [TBorCA,'true'], [Xray,'abnormal']],Cancer,[[0.5378973105134475, 0.4621026894865526]], "Variable Elimination Test 2")
    t13 = VETest(AlarmNet,[[John, True], [Mary, False]],Earthquake,[[0.0045386400007529125, 0.9954613599992471]], "Variable Elimination Test 3")
    



    
    #The following Bayes nets were generated randomly
    #Do not try and understand them
    
    

    AG_V0 = Variable('AG_V0',[0,1])
    AG_V1 = Variable('AG_V1',[0,1])
    AG_V2 = Variable('AG_V2',[0,1])
    AG_V3 = Variable('AG_V3',[0,1])
    AG_V4 = Variable('AG_V4',[0,1])
    AG_V5 = Variable('AG_V5',[0,1])
    AG_V6 = Variable('AG_V6',[0,1])
    AG_V7 = Variable('AG_V7',[0,1])
    AG_V8 = Variable('AG_V8',[0,1])
    AG_V9 = Variable('AG_V9',[0,1])
    AG_V10 = Variable('AG_V10',[0,1])
    AG_V11 = Variable('AG_V11',[0,1])
    AG_V12 = Variable('AG_V12',[0,1])
    AG_V13 = Variable('AG_V13',[0,1])
    AG_F0 = Factor('AG_F0', [AG_V0, AG_V1])
    AG_F0.add_values([[1,1, 0.07429569869316754],[1,0,0.9257043013068325],[0,1,0.5541586921164052],[0,0,0.4458413078835948]])
    AG_F1 = Factor('AG_F1', [AG_V1, AG_V2])
    AG_F1.add_values([[1,1, 0.8364892801191959],[1,0,0.16351071988080412],[0,1,0.9219795275133784],[0,0,0.07802047248662158]])
    AG_F2 = Factor('AG_F2', [AG_V2, AG_V3])
    AG_F2.add_values([[1,1, 0.6050977695825008],[1,0,0.39490223041749917],[0,1,0.8009421326997467],[0,0,0.19905786730025332]])
    AG_F3 = Factor('AG_F3', [AG_V3, AG_V4])
    AG_F3.add_values([[1,1, 0.370393133176665],[1,0,0.629606866823335],[0,1,0.9636089968642384],[0,0,0.0363910031357616]])
    AG_F4 = Factor('AG_F4', [AG_V4, AG_V5])
    AG_F4.add_values([[1,1, 0.5233804487453333],[1,0,0.4766195512546667],[0,1,0.6434102740875738],[0,0,0.3565897259124262]])
    AG_F5 = Factor('AG_F5', [AG_V5, AG_V6])
    AG_F5.add_values([[1,1, 0.6432760799970958],[1,0,0.3567239200029042],[0,1,0.4340785860631688],[0,0,0.5659214139368312]])
    AG_F6 = Factor('AG_F6', [AG_V6, AG_V7])
    AG_F6.add_values([[1,1, 0.37985255263865425],[1,0,0.6201474473613457],[0,1,0.5708819985773618],[0,0,0.42911800142263823]])
    AG_F7 = Factor('AG_F7', [AG_V7, AG_V8])
    AG_F7.add_values([[1,1, 0.4996827178134555],[1,0,0.5003172821865445],[0,1,0.8074703600365267],[0,0,0.19252963996347328]])
    AG_F8 = Factor('AG_F8', [AG_V8, AG_V9])
    AG_F8.add_values([[1,1, 0.9349444484371623],[1,0,0.06505555156283771],[0,1,0.1925788437551261],[0,0,0.8074211562448739]])
    AG_F9 = Factor('AG_F9', [AG_V9, AG_V10])
    AG_F9.add_values([[1,1, 0.5129803938194848],[1,0,0.4870196061805152],[0,1,0.5134130391347621],[0,0,0.4865869608652379]])
    AG_F10 = Factor('AG_F10', [AG_V10, AG_V11])
    AG_F10.add_values([[1,1, 0.5944184056608567],[1,0,0.4055815943391433],[0,1,0.9321491777596748],[0,0,0.06785082224032524]])
    AG_F11 = Factor('AG_F11', [AG_V11, AG_V12])
    AG_F11.add_values([[1,1, 0.7811979753641286],[1,0,0.2188020246358714],[0,1,0.31182714508612946],[0,0,0.6881728549138706]])
    AG_F12 = Factor('AG_F12', [AG_V12, AG_V13])
    AG_F12.add_values([[1,1, 0.5294236640645124],[1,0,0.47057633593548764],[0,1,0.12967343665007433],[0,0,0.8703265633499256]])
    AG_bayesnet1 = BayesianNetwork('Randomly generated net 1',[ AG_V0, AG_V1, AG_V2, AG_V3, AG_V4, AG_V5, AG_V6, AG_V7, AG_V8, AG_V9, AG_V10, AG_V11, AG_V12, AG_V13,],[AG_F0,AG_F2,AG_F4,AG_F6,AG_F8,AG_F10,AG_F12,AG_F1,AG_F3,AG_F5,AG_F7,AG_F9,AG_F11,])
    AG_t1 = VETest(AG_bayesnet1,[],AG_V13,[[0.6032889841851878, 0.3967110158148122]], 'Variable Elimination Test (Generated Bayes Net 1)')


    AG2_V0 = Variable('AG2_V0',[0,1])
    AG2_V1 = Variable('AG2_V1',[0,1])
    AG2_V2 = Variable('AG2_V2',[0,1])
    AG2_V3 = Variable('AG2_V3',[0,1])
    AG2_V4 = Variable('AG2_V4',[0,1])
    AG2_V5 = Variable('AG2_V5',[0,1])
    AG2_V6 = Variable('AG2_V6',[0,1])
    AG2_V7 = Variable('AG2_V7',[0,1])
    AG2_V8 = Variable('AG2_V8',[0,1])
    AG2_V9 = Variable('AG2_V9',[0,1])
    AG2_V10 = Variable('AG2_V10',[0,1])
    AG2_V11 = Variable('AG2_V11',[0,1])
    AG2_V12 = Variable('AG2_V12',[0,1])
    AG2_V13 = Variable('AG2_V13',[0,1])
    AG2_V14 = Variable('AG2_V14',[0,1])
    AG2_V15 = Variable('AG2_V15',[0,1])
    AG2_V16 = Variable('AG2_V16',[0,1])
    AG2_V17 = Variable('AG2_V17',[0,1])
    AG2_V18 = Variable('AG2_V18',[0,1])
    AG2_V19 = Variable('AG2_V19',[0,1])
    AG2_V20 = Variable('AG2_V20',[0,1])
    AG2_V21 = Variable('AG2_V21',[0,1])
    AG2_V22 = Variable('AG2_V22',[0,1])
    AG2_V23 = Variable('AG2_V23',[0,1])
    AG2_V24 = Variable('AG2_V24',[0,1])
    AG2_V25 = Variable('AG2_V25',[0,1])
    AG2_V26 = Variable('AG2_V26',[0,1])
    AG2_V27 = Variable('AG2_V27',[0,1])
    AG2_V28 = Variable('AG2_V28',[0,1])
    AG2_V29 = Variable('AG2_V29',[0,1])
    AG2_V30 = Variable('AG2_V30',[0,1])
    AG2_V31 = Variable('AG2_V31',[0,1])
    AG2_V32 = Variable('AG2_V32',[0,1])
    AG2_V33 = Variable('AG2_V33',[0,1])
    AG2_V34 = Variable('AG2_V34',[0,1])
    AG2_V35 = Variable('AG2_V35',[0,1])
    AG2_V36 = Variable('AG2_V36',[0,1])
    AG2_V37 = Variable('AG2_V37',[0,1])
    AG2_V38 = Variable('AG2_V38',[0,1])
    AG2_V39 = Variable('AG2_V39',[0,1])
    AG2_V40 = Variable('AG2_V40',[0,1])
    AG2_V41 = Variable('AG2_V41',[0,1])
    AG2_V42 = Variable('AG2_V42',[0,1])
    AG2_V43 = Variable('AG2_V43',[0,1])
    AG2_V44 = Variable('AG2_V44',[0,1])
    AG2_V45 = Variable('AG2_V45',[0,1])
    AG2_V46 = Variable('AG2_V46',[0,1])
    AG2_V47 = Variable('AG2_V47',[0,1])
    AG2_V48 = Variable('AG2_V48',[0,1])
    AG2_V49 = Variable('AG2_V49',[0,1])
    AG2_V50 = Variable('AG2_V50',[0,1])
    AG2_V51 = Variable('AG2_V51',[0,1])
    AG2_V52 = Variable('AG2_V52',[0,1])
    AG2_V53 = Variable('AG2_V53',[0,1])
    AG2_V54 = Variable('AG2_V54',[0,1])
    AG2_V55 = Variable('AG2_V55',[0,1])
    AG2_V56 = Variable('AG2_V56',[0,1])
    AG2_V57 = Variable('AG2_V57',[0,1])
    AG2_V58 = Variable('AG2_V58',[0,1])
    AG2_V59 = Variable('AG2_V59',[0,1])
    AG2_V60 = Variable('AG2_V60',[0,1])
    AG2_V61 = Variable('AG2_V61',[0,1])
    AG2_V62 = Variable('AG2_V62',[0,1])
    AG2_V63 = Variable('AG2_V63',[0,1])
    AG2_V64 = Variable('AG2_V64',[0,1])
    AG2_V65 = Variable('AG2_V65',[0,1])
    AG2_V66 = Variable('AG2_V66',[0,1])
    AG2_V67 = Variable('AG2_V67',[0,1])
    AG2_V68 = Variable('AG2_V68',[0,1])
    AG2_V69 = Variable('AG2_V69',[0,1])
    AG2_V70 = Variable('AG2_V70',[0,1])
    AG2_V71 = Variable('AG2_V71',[0,1])
    AG2_V72 = Variable('AG2_V72',[0,1])
    AG2_V73 = Variable('AG2_V73',[0,1])
    AG2_V74 = Variable('AG2_V74',[0,1])
    AG2_V75 = Variable('AG2_V75',[0,1])
    AG2_V76 = Variable('AG2_V76',[0,1])
    AG2_V77 = Variable('AG2_V77',[0,1])
    AG2_V78 = Variable('AG2_V78',[0,1])
    AG2_V79 = Variable('AG2_V79',[0,1])
    AG2_V80 = Variable('AG2_V80',[0,1])
    AG2_V81 = Variable('AG2_V81',[0,1])
    AG2_V82 = Variable('AG2_V82',[0,1])
    AG2_V83 = Variable('AG2_V83',[0,1])
    AG2_V84 = Variable('AG2_V84',[0,1])
    AG2_V85 = Variable('AG2_V85',[0,1])
    AG2_V86 = Variable('AG2_V86',[0,1])
    AG2_V87 = Variable('AG2_V87',[0,1])
    AG2_V88 = Variable('AG2_V88',[0,1])
    AG2_V89 = Variable('AG2_V89',[0,1])
    AG2_V90 = Variable('AG2_V90',[0,1])
    AG2_V91 = Variable('AG2_V91',[0,1])
    AG2_V92 = Variable('AG2_V92',[0,1])
    AG2_V93 = Variable('AG2_V93',[0,1])
    AG2_V94 = Variable('AG2_V94',[0,1])
    AG2_V95 = Variable('AG2_V95',[0,1])
    AG2_V96 = Variable('AG2_V96',[0,1])
    AG2_V97 = Variable('AG2_V97',[0,1])
    AG2_V98 = Variable('AG2_V98',[0,1])
    AG2_V99 = Variable('AG2_V99',[0,1])
    AG2_F0 = Factor('AG2_F0', [AG2_V0,AG2_V1,AG2_V2,AG2_V3,AG2_V4,])
    AG2_F0.add_values([[0,0,0,0,0,0.0971043780542812,],[0,0,0,0,1,0.7064844240593724,],[0,0,0,1,0,0.7281848121245953,],[0,0,0,1,1,0.9699631634542794,],[0,0,1,0,0,0.6679168408371359,],[0,0,1,0,1,0.3000806863074576,],[0,0,1,1,0,0.32268424884578467,],[0,0,1,1,1,0.5985983382235304,],[0,1,0,0,0,0.6084633565740311,],[0,1,0,0,1,0.10837614449319342,],[0,1,0,1,0,0.24704120260714288,],[0,1,0,1,1,0.2791546087749497,],[0,1,1,0,0,0.9291669435671034,],[0,1,1,0,1,0.44691364567148667,],[0,1,1,1,0,0.020779394947090486,],[0,1,1,1,1,0.696159375006128,],[1,0,0,0,0,0.28271607916149316,],[1,0,0,0,1,0.7910631191646453,],[1,0,0,1,0,0.8424138492326263,],[1,0,0,1,1,0.0767530261110908,],[1,0,1,0,0,0.8015913638282942,],[1,0,1,0,1,0.5657866012474805,],[1,0,1,1,0,0.5337130207315129,],[1,0,1,1,1,0.9845178196572417,],[1,1,0,0,0,0.5637747112266838,],[1,1,0,0,1,0.9582585961605075,],[1,1,0,1,0,0.23480919047506865,],[1,1,0,1,1,0.7529012577363927,],[1,1,1,0,0,0.3654271671485648,],[1,1,1,0,1,0.1044911957397518,],[1,1,1,1,0,0.6409695143739185,],[1,1,1,1,1,0.022236042543792495,],])
    AG2_F1 = Factor('AG2_F1', [AG2_V1,AG2_V2,AG2_V3,AG2_V4,AG2_V5,])
    AG2_F1.add_values([[0,0,0,0,0,0.11764684124944032,],[0,0,0,0,1,0.40043291736657693,],[0,0,0,1,0,0.2235167845633582,],[0,0,0,1,1,0.9498302680280583,],[0,0,1,0,0,0.9278826085756233,],[0,0,1,0,1,0.7269310640902987,],[0,0,1,1,0,0.5866155308233513,],[0,0,1,1,1,0.20253716348361112,],[0,1,0,0,0,0.6278074399737421,],[0,1,0,0,1,0.3278753678613632,],[0,1,0,1,0,0.861885219785158,],[0,1,0,1,1,0.6964056269634514,],[0,1,1,0,0,0.1152710377239672,],[0,1,1,0,1,0.14053526327753246,],[0,1,1,1,0,0.1876748249942973,],[0,1,1,1,1,0.4734209870414376,],[1,0,0,0,0,0.7158469097800554,],[1,0,0,0,1,0.8749628066147165,],[1,0,0,1,0,0.4855779648493297,],[1,0,0,1,1,0.8771588107579597,],[1,0,1,0,0,0.6559672369555306,],[1,0,1,0,1,0.39336077982604173,],[1,0,1,1,0,0.2863346574909178,],[1,0,1,1,1,0.8770585897577706,],[1,1,0,0,0,0.23823833391727275,],[1,1,0,0,1,0.4647496898668579,],[1,1,0,1,0,0.42563346070203834,],[1,1,0,1,1,0.16715192030052026,],[1,1,1,0,0,0.3546586160346031,],[1,1,1,0,1,0.7811365717600752,],[1,1,1,1,0,0.3388204634906658,],[1,1,1,1,1,0.8343598662260082,],])
    AG2_F2 = Factor('AG2_F2', [AG2_V2,AG2_V3,AG2_V4,AG2_V5,AG2_V6,])
    AG2_F2.add_values([[0,0,0,0,0,0.5470394359997954,],[0,0,0,0,1,0.26866194570887486,],[0,0,0,1,0,0.5725381602482904,],[0,0,0,1,1,0.8540699759703312,],[0,0,1,0,0,0.22516039588032064,],[0,0,1,0,1,0.7742007660385625,],[0,0,1,1,0,0.9699006066719696,],[0,0,1,1,1,0.8175358546810275,],[0,1,0,0,0,0.02515319067144357,],[0,1,0,0,1,0.8432169452632664,],[0,1,0,1,0,0.6610770505929257,],[0,1,0,1,1,0.3214816636693114,],[0,1,1,0,0,0.8272190344089363,],[0,1,1,0,1,0.07687865964204543,],[0,1,1,1,0,0.252182403085825,],[0,1,1,1,1,0.10256990502095467,],[1,0,0,0,0,0.8789499682794825,],[1,0,0,0,1,0.5542155915621891,],[1,0,0,1,0,0.7578037132687616,],[1,0,0,1,1,0.32915343468961644,],[1,0,1,0,0,0.06283841240977664,],[1,0,1,0,1,0.3628164749424673,],[1,0,1,1,0,0.6594149708339128,],[1,0,1,1,1,0.09933954417893909,],[1,1,0,0,0,0.2255150795779256,],[1,1,0,0,1,0.409024434082464,],[1,1,0,1,0,0.19614411367009624,],[1,1,0,1,1,0.8376041209550806,],[1,1,1,0,0,0.880944369918337,],[1,1,1,0,1,0.5061895165515232,],[1,1,1,1,0,0.1605174682012616,],[1,1,1,1,1,0.38057647090585794,],])
    AG2_F3 = Factor('AG2_F3', [AG2_V3,AG2_V4,AG2_V5,AG2_V6,AG2_V7,])
    AG2_F3.add_values([[0,0,0,0,0,0.49617303705780297,],[0,0,0,0,1,0.5223613213965298,],[0,0,0,1,0,0.15227871926279868,],[0,0,0,1,1,0.6689029072669638,],[0,0,1,0,0,0.17945404670637832,],[0,0,1,0,1,0.4272001585841244,],[0,0,1,1,0,0.8885364521243229,],[0,0,1,1,1,0.48310528961843274,],[0,1,0,0,0,0.9576775476271305,],[0,1,0,0,1,0.6049631500432738,],[0,1,0,1,0,0.6226889743637501,],[0,1,0,1,1,0.09510694962756723,],[0,1,1,0,0,0.2736235023670141,],[0,1,1,0,1,0.2743363826864794,],[0,1,1,1,0,0.6884827702838019,],[0,1,1,1,1,0.3446469839811945,],[1,0,0,0,0,0.47473984775038874,],[1,0,0,0,1,0.7124482347118218,],[1,0,0,1,0,0.8905993122552184,],[1,0,0,1,1,0.01985308786751397,],[1,0,1,0,0,0.9161898830069793,],[1,0,1,0,1,0.5669932307839352,],[1,0,1,1,0,0.15426981638635165,],[1,0,1,1,1,0.510447310932989,],[1,1,0,0,0,0.7899041640710188,],[1,1,0,0,1,0.11883379467392154,],[1,1,0,1,0,0.849686343104162,],[1,1,0,1,1,0.6466868173139331,],[1,1,1,0,0,0.7755301489813367,],[1,1,1,0,1,0.9261623969957855,],[1,1,1,1,0,0.39068807207870687,],[1,1,1,1,1,0.18709316842404594,],])
    AG2_F4 = Factor('AG2_F4', [AG2_V4,AG2_V5,AG2_V6,AG2_V7,AG2_V8,])
    AG2_F4.add_values([[0,0,0,0,0,0.2739115187798438,],[0,0,0,0,1,0.17153931338606432,],[0,0,0,1,0,0.9213152332065867,],[0,0,0,1,1,0.7793273946728266,],[0,0,1,0,0,0.2655184603514884,],[0,0,1,0,1,0.6841838992488288,],[0,0,1,1,0,0.8318716081004617,],[0,0,1,1,1,0.7850316977404077,],[0,1,0,0,0,0.06857165822612066,],[0,1,0,0,1,0.7442013117156379,],[0,1,0,1,0,0.9477045570757359,],[0,1,0,1,1,0.46188253579522004,],[0,1,1,0,0,0.9875636424852707,],[0,1,1,0,1,0.7073345823490564,],[0,1,1,1,0,0.7716018767938866,],[0,1,1,1,1,0.2720797085906948,],[1,0,0,0,0,0.16968078611728565,],[1,0,0,0,1,0.5509539091042962,],[1,0,0,1,0,0.30213916643268,],[1,0,0,1,1,0.5202426088620467,],[1,0,1,0,0,0.9489126454736756,],[1,0,1,0,1,0.381499080068528,],[1,0,1,1,0,0.3942828638269728,],[1,0,1,1,1,0.5534405644729827,],[1,1,0,0,0,0.4278885915968062,],[1,1,0,0,1,0.9834942788227651,],[1,1,0,1,0,0.13241800087210395,],[1,1,0,1,1,0.15923283875944702,],[1,1,1,0,0,0.42389543824891546,],[1,1,1,0,1,0.5782612819701376,],[1,1,1,1,0,0.6187068026485424,],[1,1,1,1,1,0.25685509771367043,],])
    AG2_F5 = Factor('AG2_F5', [AG2_V5,AG2_V6,AG2_V7,AG2_V8,AG2_V9,])
    AG2_F5.add_values([[0,0,0,0,0,0.42785282598043406,],[0,0,0,0,1,0.8470877366178988,],[0,0,0,1,0,0.9291792961189903,],[0,0,0,1,1,0.22006341338616026,],[0,0,1,0,0,0.734299734647345,],[0,0,1,0,1,0.3453557616586027,],[0,0,1,1,0,0.7860676352906903,],[0,0,1,1,1,0.8902054988207331,],[0,1,0,0,0,0.9778591354341921,],[0,1,0,0,1,0.6786275328204122,],[0,1,0,1,0,0.5586557226316743,],[0,1,0,1,1,0.29970698522678363,],[0,1,1,0,0,0.8110754746790992,],[0,1,1,0,1,0.5982312026711686,],[0,1,1,1,0,0.22065923166286658,],[0,1,1,1,1,0.30151881664863484,],[1,0,0,0,0,0.6503231374225384,],[1,0,0,0,1,0.5261114593809574,],[1,0,0,1,0,0.23406535918357235,],[1,0,0,1,1,0.8170308144533788,],[1,0,1,0,0,0.6907552475525923,],[1,0,1,0,1,0.21882660893775732,],[1,0,1,1,0,0.548190890538947,],[1,0,1,1,1,0.5741803418416188,],[1,1,0,0,0,0.0694206528951243,],[1,1,0,0,1,0.9230568862789729,],[1,1,0,1,0,0.7871881922074094,],[1,1,0,1,1,0.6865311701749546,],[1,1,1,0,0,0.5857294695295834,],[1,1,1,0,1,0.21346755339743878,],[1,1,1,1,0,0.5769626589497787,],[1,1,1,1,1,0.8812200780269263,],])
    AG2_F6 = Factor('AG2_F6', [AG2_V6,AG2_V7,AG2_V8,AG2_V9,AG2_V10,])
    AG2_F6.add_values([[0,0,0,0,0,0.24088051134634678,],[0,0,0,0,1,0.21664121056259816,],[0,0,0,1,0,0.4674737528198354,],[0,0,0,1,1,0.23244848740221205,],[0,0,1,0,0,0.6590871462855185,],[0,0,1,0,1,0.7295960558411396,],[0,0,1,1,0,0.3528562886634077,],[0,0,1,1,1,0.8854778962177097,],[0,1,0,0,0,0.8950347116018496,],[0,1,0,0,1,0.2873150944525373,],[0,1,0,1,0,0.8655040387860622,],[0,1,0,1,1,0.0843073069334178,],[0,1,1,0,0,0.8528085573340488,],[0,1,1,0,1,0.6050503135522529,],[0,1,1,1,0,0.6304330340471863,],[0,1,1,1,1,0.37114595236911974,],[1,0,0,0,0,0.5394381002704399,],[1,0,0,0,1,0.6811506054848656,],[1,0,0,1,0,0.3045488142653902,],[1,0,0,1,1,0.05797378688585403,],[1,0,1,0,0,0.3077167432698096,],[1,0,1,0,1,0.4651724252987217,],[1,0,1,1,0,0.4723211620904876,],[1,0,1,1,1,0.7621400932659859,],[1,1,0,0,0,0.8368527680420619,],[1,1,0,0,1,0.3736192629096699,],[1,1,0,1,0,0.5022012103593917,],[1,1,0,1,1,0.6191079222125251,],[1,1,1,0,0,0.8089854212309445,],[1,1,1,0,1,0.1623028036973678,],[1,1,1,1,0,0.347305008160457,],[1,1,1,1,1,0.8541763475890624,],])
    AG2_F7 = Factor('AG2_F7', [AG2_V7,AG2_V8,AG2_V9,AG2_V10,AG2_V11,])
    AG2_F7.add_values([[0,0,0,0,0,0.06493518253821251,],[0,0,0,0,1,0.2582769833373186,],[0,0,0,1,0,0.18360935036333823,],[0,0,0,1,1,0.06663052756467995,],[0,0,1,0,0,0.23674597341184947,],[0,0,1,0,1,0.7244428296191457,],[0,0,1,1,0,0.9509536609395913,],[0,0,1,1,1,0.9131849738878938,],[0,1,0,0,0,0.5999126034630343,],[0,1,0,0,1,0.016467836891112163,],[0,1,0,1,0,0.5225626527268877,],[0,1,0,1,1,0.7158838199806903,],[0,1,1,0,0,0.48341166815234654,],[0,1,1,0,1,0.5024783120560576,],[0,1,1,1,0,0.03493533454153985,],[0,1,1,1,1,0.9666093916375993,],[1,0,0,0,0,0.3221785126275487,],[1,0,0,0,1,0.42164258071185956,],[1,0,0,1,0,0.3655529480211245,],[1,0,0,1,1,0.6691976267988542,],[1,0,1,0,0,0.23079268310755743,],[1,0,1,0,1,0.46019650608593293,],[1,0,1,1,0,0.1803722516833908,],[1,0,1,1,1,0.4077021550287888,],[1,1,0,0,0,0.4379819851976464,],[1,1,0,0,1,0.5343577408910017,],[1,1,0,1,0,0.5654486667390205,],[1,1,0,1,1,0.19441085798476426,],[1,1,1,0,0,0.859992390128539,],[1,1,1,0,1,0.3600202240499176,],[1,1,1,1,0,0.6491257391839836,],[1,1,1,1,1,0.6946078872019692,],])
    AG2_F8 = Factor('AG2_F8', [AG2_V8,AG2_V9,AG2_V10,AG2_V11,AG2_V12,])
    AG2_F8.add_values([[0,0,0,0,0,0.2585590789992009,],[0,0,0,0,1,0.5644936212175905,],[0,0,0,1,0,0.44841909570264826,],[0,0,0,1,1,0.8284515678936223,],[0,0,1,0,0,0.9179843111511757,],[0,0,1,0,1,0.4724675150321922,],[0,0,1,1,0,0.9499817353364587,],[0,0,1,1,1,0.7152913142428244,],[0,1,0,0,0,0.29312734228284915,],[0,1,0,0,1,0.038866045924802826,],[0,1,0,1,0,0.778687230352396,],[0,1,0,1,1,0.6257647206610817,],[0,1,1,0,0,0.9699063731505955,],[0,1,1,0,1,0.4014109769408935,],[0,1,1,1,0,0.36455545575853265,],[0,1,1,1,1,0.4225198735894929,],[1,0,0,0,0,0.5831041731199643,],[1,0,0,0,1,0.32114569177985186,],[1,0,0,1,0,0.15582684957372142,],[1,0,0,1,1,0.20085941906724525,],[1,0,1,0,0,0.07332258376407501,],[1,0,1,0,1,0.23093057704355588,],[1,0,1,1,0,0.13488580553826893,],[1,0,1,1,1,0.8917763351507968,],[1,1,0,0,0,0.2155849473709566,],[1,1,0,0,1,0.8758752424275174,],[1,1,0,1,0,0.45805921653152243,],[1,1,0,1,1,0.006754110798144574,],[1,1,1,0,0,0.4349731038849178,],[1,1,1,0,1,0.8309360290332775,],[1,1,1,1,0,0.44971539736471017,],[1,1,1,1,1,0.8649852527013299,],])
    AG2_F9 = Factor('AG2_F9', [AG2_V9,AG2_V10,AG2_V11,AG2_V12,AG2_V13,])
    AG2_F9.add_values([[0,0,0,0,0,0.4988943858592216,],[0,0,0,0,1,0.34419990976727116,],[0,0,0,1,0,0.6665313898800478,],[0,0,0,1,1,0.5491414349642231,],[0,0,1,0,0,0.6884480215820393,],[0,0,1,0,1,0.7049656351520327,],[0,0,1,1,0,0.5914464641373474,],[0,0,1,1,1,0.272539651337776,],[0,1,0,0,0,0.14028528368965937,],[0,1,0,0,1,0.13321801452878562,],[0,1,0,1,0,0.5045885844333409,],[0,1,0,1,1,0.9365413683173384,],[0,1,1,0,0,0.00832715596191297,],[0,1,1,0,1,0.2806760188218288,],[0,1,1,1,0,0.10391679698437428,],[0,1,1,1,1,0.6360562856114991,],[1,0,0,0,0,0.27945523955405477,],[1,0,0,0,1,0.8707327658122881,],[1,0,0,1,0,0.5037172484233456,],[1,0,0,1,1,0.07723213555956289,],[1,0,1,0,0,0.5596977020373505,],[1,0,1,0,1,0.8545435085382925,],[1,0,1,1,0,0.7339731289393986,],[1,0,1,1,1,0.1976575384453965,],[1,1,0,0,0,0.7782288455194716,],[1,1,0,0,1,0.09522812222710668,],[1,1,0,1,0,0.6092463357547622,],[1,1,0,1,1,0.07536594762215063,],[1,1,1,0,0,0.5556489475643929,],[1,1,1,0,1,0.028809490487748717,],[1,1,1,1,0,0.43336351127059475,],[1,1,1,1,1,0.8736131767765692,],])
    AG2_F10 = Factor('AG2_F10', [AG2_V10,AG2_V11,AG2_V12,AG2_V13,AG2_V14,])
    AG2_F10.add_values([[0,0,0,0,0,0.5311067120971941,],[0,0,0,0,1,0.1947329336674179,],[0,0,0,1,0,0.056684463955582305,],[0,0,0,1,1,0.7856114663360195,],[0,0,1,0,0,0.6352746158167752,],[0,0,1,0,1,0.5782413856818344,],[0,0,1,1,0,0.17769960461866405,],[0,0,1,1,1,0.45622189049513784,],[0,1,0,0,0,0.18605972959455283,],[0,1,0,0,1,0.4540755536195269,],[0,1,0,1,0,0.5062448265808509,],[0,1,0,1,1,0.27877796699210217,],[0,1,1,0,0,0.09428428926460485,],[0,1,1,0,1,0.5565203500501317,],[0,1,1,1,0,0.7839844666686855,],[0,1,1,1,1,0.31492777469257227,],[1,0,0,0,0,0.6568235196438454,],[1,0,0,0,1,0.36636225960743957,],[1,0,0,1,0,0.546066830224521,],[1,0,0,1,1,0.7902501194103735,],[1,0,1,0,0,0.012444319882030975,],[1,0,1,0,1,0.1431551238655976,],[1,0,1,1,0,0.8060463939954547,],[1,0,1,1,1,0.03988882716402061,],[1,1,0,0,0,0.8117344731781237,],[1,1,0,0,1,0.12566727850663598,],[1,1,0,1,0,0.567309337394032,],[1,1,0,1,1,0.12569445343769964,],[1,1,1,0,0,0.11620774505754869,],[1,1,1,0,1,0.5816955378589389,],[1,1,1,1,0,0.9500518503831157,],[1,1,1,1,1,0.35259863649564027,],])
    AG2_F11 = Factor('AG2_F11', [AG2_V11,AG2_V12,AG2_V13,AG2_V14,AG2_V15,])
    AG2_F11.add_values([[0,0,0,0,0,0.34342452722725625,],[0,0,0,0,1,0.05467209037681925,],[0,0,0,1,0,0.2663591952430879,],[0,0,0,1,1,0.5198178839718723,],[0,0,1,0,0,0.2599274718252059,],[0,0,1,0,1,0.292520630908561,],[0,0,1,1,0,0.07907114082679871,],[0,0,1,1,1,0.5032207632017306,],[0,1,0,0,0,0.5255459133918737,],[0,1,0,0,1,0.0688214601813974,],[0,1,0,1,0,0.8244166115253541,],[0,1,0,1,1,0.46093827691976674,],[0,1,1,0,0,0.436641275106979,],[0,1,1,0,1,0.027224816087912537,],[0,1,1,1,0,0.8882915344236988,],[0,1,1,1,1,0.055396327759184294,],[1,0,0,0,0,0.6517070376963344,],[1,0,0,0,1,0.7103797756696338,],[1,0,0,1,0,0.3653519262543458,],[1,0,0,1,1,0.30019865918906086,],[1,0,1,0,0,0.9214345359275365,],[1,0,1,0,1,0.17009728170985977,],[1,0,1,1,0,0.40727364362558344,],[1,0,1,1,1,0.3003403477522284,],[1,1,0,0,0,0.6842988402098252,],[1,1,0,0,1,0.6143468790959,],[1,1,0,1,0,0.7058689843208917,],[1,1,0,1,1,0.5098695217682865,],[1,1,1,0,0,0.8665832134772674,],[1,1,1,0,1,0.4449820448185846,],[1,1,1,1,0,0.297336932377939,],[1,1,1,1,1,0.5463221854966788,],])
    AG2_F12 = Factor('AG2_F12', [AG2_V12,AG2_V13,AG2_V14,AG2_V15,AG2_V16,])
    AG2_F12.add_values([[0,0,0,0,0,0.13744805551465206,],[0,0,0,0,1,0.8104031006922071,],[0,0,0,1,0,0.510752154835497,],[0,0,0,1,1,0.9042988970896836,],[0,0,1,0,0,0.07671253180934012,],[0,0,1,0,1,0.08331786415044198,],[0,0,1,1,0,0.5823158556492978,],[0,0,1,1,1,0.13539916061945897,],[0,1,0,0,0,0.9513929194687701,],[0,1,0,0,1,0.8402415707622133,],[0,1,0,1,0,0.7153498562904684,],[0,1,0,1,1,0.41379473262086225,],[0,1,1,0,0,0.8123712907732612,],[0,1,1,0,1,0.09319915775281708,],[0,1,1,1,0,0.06958612667283998,],[0,1,1,1,1,0.5514567624355072,],[1,0,0,0,0,0.6078651273924361,],[1,0,0,0,1,0.009376976696398575,],[1,0,0,1,0,0.6989477447585756,],[1,0,0,1,1,0.38352190455939195,],[1,0,1,0,0,0.309479044989179,],[1,0,1,0,1,0.9274469234860897,],[1,0,1,1,0,0.511006567523535,],[1,0,1,1,1,0.9163920525949341,],[1,1,0,0,0,0.4606513637524117,],[1,1,0,0,1,0.3658544812254549,],[1,1,0,1,0,0.7365314422326683,],[1,1,0,1,1,0.28667047712306254,],[1,1,1,0,0,0.887354117543021,],[1,1,1,0,1,0.03776994581546054,],[1,1,1,1,0,0.5539998613506918,],[1,1,1,1,1,0.18877753015544285,],])
    AG2_F13 = Factor('AG2_F13', [AG2_V13,AG2_V14,AG2_V15,AG2_V16,AG2_V17,])
    AG2_F13.add_values([[0,0,0,0,0,0.2571625309933141,],[0,0,0,0,1,0.6171774268507467,],[0,0,0,1,0,0.0016826460297735977,],[0,0,0,1,1,0.20014200805024596,],[0,0,1,0,0,0.4910662808460162,],[0,0,1,0,1,0.37302644579076943,],[0,0,1,1,0,0.8183997668880617,],[0,0,1,1,1,0.2537275685535083,],[0,1,0,0,0,0.6683058881761603,],[0,1,0,0,1,0.7204603583469883,],[0,1,0,1,0,0.36402355357109906,],[0,1,0,1,1,0.7990962897579639,],[0,1,1,0,0,0.047717126064170085,],[0,1,1,0,1,0.8748559559787448,],[0,1,1,1,0,0.2889166472002018,],[0,1,1,1,1,0.8208350412102596,],[1,0,0,0,0,0.279623002612193,],[1,0,0,0,1,0.04068929520380906,],[1,0,0,1,0,0.3444888072867644,],[1,0,0,1,1,0.6430401702827861,],[1,0,1,0,0,0.6441081828718125,],[1,0,1,0,1,0.29975064485869546,],[1,0,1,1,0,0.8001814823638564,],[1,0,1,1,1,0.7076242189720898,],[1,1,0,0,0,0.06589838110379012,],[1,1,0,0,1,0.5974263730831448,],[1,1,0,1,0,0.4212611053098894,],[1,1,0,1,1,0.599019359652665,],[1,1,1,0,0,0.9549037291724995,],[1,1,1,0,1,0.5658013676865102,],[1,1,1,1,0,0.43155262554146073,],[1,1,1,1,1,0.8837406416786685,],])
    AG2_F14 = Factor('AG2_F14', [AG2_V14,AG2_V15,AG2_V16,AG2_V17,AG2_V18,])
    AG2_F14.add_values([[0,0,0,0,0,0.7574651710244379,],[0,0,0,0,1,0.7099148643127323,],[0,0,0,1,0,0.9184761036736171,],[0,0,0,1,1,0.7759591491801179,],[0,0,1,0,0,0.9526337331162393,],[0,0,1,0,1,0.461729199352445,],[0,0,1,1,0,0.6457216470153645,],[0,0,1,1,1,0.9432595137560622,],[0,1,0,0,0,0.7530042429130267,],[0,1,0,0,1,0.025577915489644523,],[0,1,0,1,0,0.22697188026460013,],[0,1,0,1,1,0.2135608499402335,],[0,1,1,0,0,0.09764604858015616,],[0,1,1,0,1,0.7080541691175383,],[0,1,1,1,0,0.8696446431502115,],[0,1,1,1,1,0.7570097630180811,],[1,0,0,0,0,0.5554314552042016,],[1,0,0,0,1,0.948246763983742,],[1,0,0,1,0,0.5451921802229328,],[1,0,0,1,1,0.9549263710141076,],[1,0,1,0,0,0.9033858530765805,],[1,0,1,0,1,0.5125345829643414,],[1,0,1,1,0,0.464326627235819,],[1,0,1,1,1,0.8155014532983946,],[1,1,0,0,0,0.03878537567180833,],[1,1,0,0,1,0.22801395591352347,],[1,1,0,1,0,0.6489163947233427,],[1,1,0,1,1,0.018558103613395355,],[1,1,1,0,0,0.9941401275356915,],[1,1,1,0,1,0.702328129006521,],[1,1,1,1,0,0.43297194966394503,],[1,1,1,1,1,0.852245822068036,],])
    AG2_F15 = Factor('AG2_F15', [AG2_V15,AG2_V16,AG2_V17,AG2_V18,AG2_V19,])
    AG2_F15.add_values([[0,0,0,0,0,0.7060668035181757,],[0,0,0,0,1,0.7531337907810081,],[0,0,0,1,0,0.17875347186180773,],[0,0,0,1,1,0.9050003189822698,],[0,0,1,0,0,0.8836010895538026,],[0,0,1,0,1,0.5498316458448688,],[0,0,1,1,0,0.2720982262700738,],[0,0,1,1,1,0.21901700462946552,],[0,1,0,0,0,0.6844622006732084,],[0,1,0,0,1,0.8016598770920087,],[0,1,0,1,0,0.7376689526847531,],[0,1,0,1,1,0.889823141957435,],[0,1,1,0,0,0.8947964933406849,],[0,1,1,0,1,0.45934981776790973,],[0,1,1,1,0,0.581617789764507,],[0,1,1,1,1,0.48627811112352753,],[1,0,0,0,0,0.5994979682734652,],[1,0,0,0,1,0.09725334977784522,],[1,0,0,1,0,0.17592577094110565,],[1,0,0,1,1,0.09740133210044723,],[1,0,1,0,0,0.6847244980392022,],[1,0,1,0,1,0.1285800898953079,],[1,0,1,1,0,0.9129499313551306,],[1,0,1,1,1,0.10626618800534443,],[1,1,0,0,0,0.7112933576403183,],[1,1,0,0,1,0.04049152071474797,],[1,1,0,1,0,0.6562696738200525,],[1,1,0,1,1,0.8950571519326079,],[1,1,1,0,0,0.6295340276195365,],[1,1,1,0,1,0.8518629616993902,],[1,1,1,1,0,0.9204250170587659,],[1,1,1,1,1,0.47860755377159825,],])
    AG2_F16 = Factor('AG2_F16', [AG2_V16,AG2_V17,AG2_V18,AG2_V19,AG2_V20,])
    AG2_F16.add_values([[0,0,0,0,0,0.36270662860608904,],[0,0,0,0,1,0.24768833661381764,],[0,0,0,1,0,0.533133639465915,],[0,0,0,1,1,0.7389363852646865,],[0,0,1,0,0,0.3533796848856146,],[0,0,1,0,1,0.5062710737306694,],[0,0,1,1,0,0.26467499969152974,],[0,0,1,1,1,0.3926333333114696,],[0,1,0,0,0,0.44865109485187604,],[0,1,0,0,1,0.11036555404518272,],[0,1,0,1,0,0.3136572450750967,],[0,1,0,1,1,0.3560305648847703,],[0,1,1,0,0,0.8143187183614405,],[0,1,1,0,1,0.6965030189851547,],[0,1,1,1,0,0.20149095033372863,],[0,1,1,1,1,0.2424304796876883,],[1,0,0,0,0,0.11667641347604885,],[1,0,0,0,1,0.12446470130882248,],[1,0,0,1,0,0.8230660586278524,],[1,0,0,1,1,0.4826342981126704,],[1,0,1,0,0,0.9761171809408341,],[1,0,1,0,1,0.7540146126263156,],[1,0,1,1,0,0.3792229279293241,],[1,0,1,1,1,0.6248753107419922,],[1,1,0,0,0,0.34016457087973573,],[1,1,0,0,1,0.3425696673943592,],[1,1,0,1,0,0.3252787528372137,],[1,1,0,1,1,0.07545408190157729,],[1,1,1,0,0,0.038596808291073786,],[1,1,1,0,1,0.27027489419702133,],[1,1,1,1,0,0.38359161235380396,],[1,1,1,1,1,0.46830493716134713,],])
    AG2_F17 = Factor('AG2_F17', [AG2_V17,AG2_V18,AG2_V19,AG2_V20,AG2_V21,])
    AG2_F17.add_values([[0,0,0,0,0,0.9121153046034635,],[0,0,0,0,1,0.669482177389911,],[0,0,0,1,0,0.3642098080669884,],[0,0,0,1,1,0.46679563948857145,],[0,0,1,0,0,0.46190804101478566,],[0,0,1,0,1,0.23653356258591995,],[0,0,1,1,0,0.8284264704586314,],[0,0,1,1,1,0.6799128794309397,],[0,1,0,0,0,0.43343451605726685,],[0,1,0,0,1,0.8225950335282495,],[0,1,0,1,0,0.9714000259719725,],[0,1,0,1,1,0.03937661628779103,],[0,1,1,0,0,0.9022554334611491,],[0,1,1,0,1,0.9039900734096377,],[0,1,1,1,0,0.6899451382254653,],[0,1,1,1,1,0.9427607361448287,],[1,0,0,0,0,0.7187736918417051,],[1,0,0,0,1,0.052326853499753426,],[1,0,0,1,0,0.13056499302636432,],[1,0,0,1,1,0.6609251990903685,],[1,0,1,0,0,0.11845470308270928,],[1,0,1,0,1,0.24160931231070432,],[1,0,1,1,0,0.002645260284379817,],[1,0,1,1,1,0.43473465015723983,],[1,1,0,0,0,0.026712223504781054,],[1,1,0,0,1,0.6170084013716296,],[1,1,0,1,0,0.7754118839444628,],[1,1,0,1,1,0.4872866202609047,],[1,1,1,0,0,0.29953733302876195,],[1,1,1,0,1,0.841938885323087,],[1,1,1,1,0,0.9451993139181483,],[1,1,1,1,1,0.5076427739093669,],])
    AG2_F18 = Factor('AG2_F18', [AG2_V18,AG2_V19,AG2_V20,AG2_V21,AG2_V22,])
    AG2_F18.add_values([[0,0,0,0,0,0.6878578866926263,],[0,0,0,0,1,0.44955961606213835,],[0,0,0,1,0,0.9350138650802121,],[0,0,0,1,1,0.6575027649165439,],[0,0,1,0,0,0.44621201630325724,],[0,0,1,0,1,0.9249269299984764,],[0,0,1,1,0,0.8753854271040805,],[0,0,1,1,1,0.25266517994610926,],[0,1,0,0,0,0.41722448481187646,],[0,1,0,0,1,0.0708943090223136,],[0,1,0,1,0,0.879730890164582,],[0,1,0,1,1,0.33988520210170614,],[0,1,1,0,0,0.10147708867422102,],[0,1,1,0,1,0.47851868144297227,],[0,1,1,1,0,0.25721109055952923,],[0,1,1,1,1,0.2969802046867175,],[1,0,0,0,0,0.6952551683153548,],[1,0,0,0,1,0.4451653081340982,],[1,0,0,1,0,0.5485366178511872,],[1,0,0,1,1,0.7123312443667097,],[1,0,1,0,0,0.024075984637618616,],[1,0,1,0,1,0.7059760967647192,],[1,0,1,1,0,0.9491097625073297,],[1,0,1,1,1,0.5242696479677387,],[1,1,0,0,0,0.7311454213094507,],[1,1,0,0,1,0.4648304180068571,],[1,1,0,1,0,0.7013504231326579,],[1,1,0,1,1,0.661902433697116,],[1,1,1,0,0,0.0973335820313257,],[1,1,1,0,1,0.24102778693499927,],[1,1,1,1,0,0.6569411862774712,],[1,1,1,1,1,0.4042729649948211,],])
    AG2_F19 = Factor('AG2_F19', [AG2_V19,AG2_V20,AG2_V21,AG2_V22,AG2_V23,])
    AG2_F19.add_values([[0,0,0,0,0,0.39770176859971634,],[0,0,0,0,1,0.816420070398151,],[0,0,0,1,0,0.3832738219296725,],[0,0,0,1,1,0.7435910491025367,],[0,0,1,0,0,0.5375910861293058,],[0,0,1,0,1,0.9805623940066167,],[0,0,1,1,0,0.7538132119099009,],[0,0,1,1,1,0.44919466435883443,],[0,1,0,0,0,0.7059486484041636,],[0,1,0,0,1,0.5304403225452088,],[0,1,0,1,0,0.5923053024383605,],[0,1,0,1,1,0.4334353055231453,],[0,1,1,0,0,0.47734188752432727,],[0,1,1,0,1,0.8658499824430298,],[0,1,1,1,0,0.23076419423366099,],[0,1,1,1,1,0.3071207656256896,],[1,0,0,0,0,0.4862022506555502,],[1,0,0,0,1,0.4789614029984844,],[1,0,0,1,0,0.4399493872844278,],[1,0,0,1,1,0.9350118121457703,],[1,0,1,0,0,0.888323639695152,],[1,0,1,0,1,0.18449476339936796,],[1,0,1,1,0,0.37078082156335934,],[1,0,1,1,1,0.7624144222607088,],[1,1,0,0,0,0.09671824738874366,],[1,1,0,0,1,0.6207142033358134,],[1,1,0,1,0,0.8666391456512658,],[1,1,0,1,1,0.37653765858319294,],[1,1,1,0,0,0.2840185075593089,],[1,1,1,0,1,0.12184473706578222,],[1,1,1,1,0,0.3263383472447478,],[1,1,1,1,1,0.017509708412817494,],])
    AG2_F20 = Factor('AG2_F20', [AG2_V20,AG2_V21,AG2_V22,AG2_V23,AG2_V24,])
    AG2_F20.add_values([[0,0,0,0,0,0.8776973656400687,],[0,0,0,0,1,0.18793213747908594,],[0,0,0,1,0,0.8219055426581955,],[0,0,0,1,1,0.6115529449847548,],[0,0,1,0,0,0.5382941781553112,],[0,0,1,0,1,0.11324254845611893,],[0,0,1,1,0,0.29992295197294455,],[0,0,1,1,1,0.7831822034077904,],[0,1,0,0,0,0.4067324921742964,],[0,1,0,0,1,0.22776634483462965,],[0,1,0,1,0,0.08156394355652474,],[0,1,0,1,1,0.103770930452364,],[0,1,1,0,0,0.8788450429266081,],[0,1,1,0,1,0.3645789104967412,],[0,1,1,1,0,0.27268318280730847,],[0,1,1,1,1,0.17164988341785334,],[1,0,0,0,0,0.7481100572081111,],[1,0,0,0,1,0.6793852979778625,],[1,0,0,1,0,0.9399640093880468,],[1,0,0,1,1,0.9217907189781742,],[1,0,1,0,0,0.2004396181916235,],[1,0,1,0,1,0.37697525589191516,],[1,0,1,1,0,0.11537454701233738,],[1,0,1,1,1,0.6518219953601038,],[1,1,0,0,0,0.518985771456741,],[1,1,0,0,1,0.6090267226525335,],[1,1,0,1,0,0.3089296330027509,],[1,1,0,1,1,0.16487909351482385,],[1,1,1,0,0,0.9934947188103186,],[1,1,1,0,1,0.21209588984285677,],[1,1,1,1,0,0.8204730945537879,],[1,1,1,1,1,0.004488326140494225,],])
    AG2_F21 = Factor('AG2_F21', [AG2_V21,AG2_V22,AG2_V23,AG2_V24,AG2_V25,])
    AG2_F21.add_values([[0,0,0,0,0,0.7948816380868052,],[0,0,0,0,1,0.953885176325384,],[0,0,0,1,0,0.776852711500437,],[0,0,0,1,1,0.12137716100881016,],[0,0,1,0,0,0.19002978874547852,],[0,0,1,0,1,0.6829443205035309,],[0,0,1,1,0,0.922899414769068,],[0,0,1,1,1,0.8655083124250065,],[0,1,0,0,0,0.9850448756087815,],[0,1,0,0,1,0.805921740897074,],[0,1,0,1,0,0.09495495875406329,],[0,1,0,1,1,0.9249554564930033,],[0,1,1,0,0,0.326993947546937,],[0,1,1,0,1,0.35494898577871536,],[0,1,1,1,0,0.45028250089493366,],[0,1,1,1,1,0.578555954214762,],[1,0,0,0,0,0.19396191444019595,],[1,0,0,0,1,0.8211816657869755,],[1,0,0,1,0,0.4421500640423213,],[1,0,0,1,1,0.9261091837587918,],[1,0,1,0,0,0.05457080897491868,],[1,0,1,0,1,0.09084202122946064,],[1,0,1,1,0,0.017446208307365235,],[1,0,1,1,1,0.3562228341860795,],[1,1,0,0,0,0.8276302645600124,],[1,1,0,0,1,0.5380294841583936,],[1,1,0,1,0,0.8695675222786304,],[1,1,0,1,1,0.4456162686885201,],[1,1,1,0,0,0.010616777840165811,],[1,1,1,0,1,0.827023780768239,],[1,1,1,1,0,0.8992565340721841,],[1,1,1,1,1,0.7743103488080451,],])
    AG2_F22 = Factor('AG2_F22', [AG2_V22,AG2_V23,AG2_V24,AG2_V25,AG2_V26,])
    AG2_F22.add_values([[0,0,0,0,0,0.6334763904644294,],[0,0,0,0,1,0.830665982292087,],[0,0,0,1,0,0.5401519264966443,],[0,0,0,1,1,0.47792959757372555,],[0,0,1,0,0,0.6491818321079705,],[0,0,1,0,1,0.7130823827940816,],[0,0,1,1,0,0.43095381503573843,],[0,0,1,1,1,0.24422569847196307,],[0,1,0,0,0,0.8338787173775792,],[0,1,0,0,1,0.4622681712133486,],[0,1,0,1,0,0.4613301220885948,],[0,1,0,1,1,0.46487757419405834,],[0,1,1,0,0,0.943080686492003,],[0,1,1,0,1,0.37971236037319084,],[0,1,1,1,0,0.3705566425116788,],[0,1,1,1,1,0.8725078189824109,],[1,0,0,0,0,0.5815908276947706,],[1,0,0,0,1,0.6659200846116613,],[1,0,0,1,0,0.816632210852969,],[1,0,0,1,1,0.15470467851513944,],[1,0,1,0,0,0.6297596219331313,],[1,0,1,0,1,0.0881957808064805,],[1,0,1,1,0,0.43990458252813386,],[1,0,1,1,1,0.9397172232570236,],[1,1,0,0,0,0.1525270010405681,],[1,1,0,0,1,0.42000804353186116,],[1,1,0,1,0,0.0017935106435684814,],[1,1,0,1,1,0.5604482450912592,],[1,1,1,0,0,0.47131012310864817,],[1,1,1,0,1,0.277064217020956,],[1,1,1,1,0,0.6141716068186713,],[1,1,1,1,1,0.721266897932042,],])
    AG2_F23 = Factor('AG2_F23', [AG2_V23,AG2_V24,AG2_V25,AG2_V26,AG2_V27,])
    AG2_F23.add_values([[0,0,0,0,0,0.3738529230228788,],[0,0,0,0,1,0.6392786680403008,],[0,0,0,1,0,0.690737009252511,],[0,0,0,1,1,0.8301283798690343,],[0,0,1,0,0,0.0013939724545691417,],[0,0,1,0,1,0.890005027233527,],[0,0,1,1,0,0.6532306350748217,],[0,0,1,1,1,0.14031753564463684,],[0,1,0,0,0,0.054077586669722726,],[0,1,0,0,1,0.9323718209791375,],[0,1,0,1,0,0.28279669595198376,],[0,1,0,1,1,0.7024417830506935,],[0,1,1,0,0,0.08338875675471172,],[0,1,1,0,1,0.7289449396389235,],[0,1,1,1,0,0.3662556125710482,],[0,1,1,1,1,0.1641676647174389,],[1,0,0,0,0,0.9399503902808548,],[1,0,0,0,1,0.6433754389324231,],[1,0,0,1,0,0.08134265641457679,],[1,0,0,1,1,0.03409620586588573,],[1,0,1,0,0,0.7749803029625439,],[1,0,1,0,1,0.19066920920589966,],[1,0,1,1,0,0.4274583459656899,],[1,0,1,1,1,0.030306997400099078,],[1,1,0,0,0,0.5901021609206165,],[1,1,0,0,1,0.2479563223200761,],[1,1,0,1,0,0.32501598718651104,],[1,1,0,1,1,0.23469814713598752,],[1,1,1,0,0,0.5553174348077535,],[1,1,1,0,1,0.3337595039969986,],[1,1,1,1,0,0.23955088096363616,],[1,1,1,1,1,0.9936197715284543,],])
    AG2_F24 = Factor('AG2_F24', [AG2_V24,AG2_V25,AG2_V26,AG2_V27,AG2_V28,])
    AG2_F24.add_values([[0,0,0,0,0,0.5585083196479972,],[0,0,0,0,1,0.46772945568247554,],[0,0,0,1,0,0.1131140962230884,],[0,0,0,1,1,0.2398896608721134,],[0,0,1,0,0,0.8608827303854767,],[0,0,1,0,1,0.5221080888746731,],[0,0,1,1,0,0.6736154033447356,],[0,0,1,1,1,0.8978568759836882,],[0,1,0,0,0,0.3126167236380342,],[0,1,0,0,1,0.5916187656508174,],[0,1,0,1,0,0.8190329158135068,],[0,1,0,1,1,0.5690910654714584,],[0,1,1,0,0,0.6254926320764327,],[0,1,1,0,1,0.5903665685167832,],[0,1,1,1,0,0.857441204848729,],[0,1,1,1,1,0.3519299054493915,],[1,0,0,0,0,0.9633977197339446,],[1,0,0,0,1,0.21868013972449485,],[1,0,0,1,0,0.3760576959495847,],[1,0,0,1,1,0.8438622504681081,],[1,0,1,0,0,0.4119650340857796,],[1,0,1,0,1,0.8815233000869208,],[1,0,1,1,0,0.9463411834863856,],[1,0,1,1,1,0.9661986968043385,],[1,1,0,0,0,0.4063912254868429,],[1,1,0,0,1,0.45113530248790024,],[1,1,0,1,0,0.43224052550746744,],[1,1,0,1,1,0.8494710445100543,],[1,1,1,0,0,0.5571582125960785,],[1,1,1,0,1,0.548265115520853,],[1,1,1,1,0,0.22116697622917794,],[1,1,1,1,1,0.20421685924250302,],])
    AG2_F25 = Factor('AG2_F25', [AG2_V25,AG2_V26,AG2_V27,AG2_V28,AG2_V29,])
    AG2_F25.add_values([[0,0,0,0,0,0.09769130597150354,],[0,0,0,0,1,0.6962784143297529,],[0,0,0,1,0,0.5734975608271629,],[0,0,0,1,1,0.8431809242966862,],[0,0,1,0,0,0.7578366258479874,],[0,0,1,0,1,0.31816645352170775,],[0,0,1,1,0,0.9706827534288078,],[0,0,1,1,1,0.8651320334247871,],[0,1,0,0,0,0.5045229070918111,],[0,1,0,0,1,0.5438977779495008,],[0,1,0,1,0,0.49006379780526216,],[0,1,0,1,1,0.9631736839140477,],[0,1,1,0,0,0.07557723502381954,],[0,1,1,0,1,0.46493344008396764,],[0,1,1,1,0,0.1637879166365585,],[0,1,1,1,1,0.6801478572496451,],[1,0,0,0,0,0.02215166815116424,],[1,0,0,0,1,0.789945729598947,],[1,0,0,1,0,0.8617206728480509,],[1,0,0,1,1,0.4534410264569308,],[1,0,1,0,0,0.2552517828231028,],[1,0,1,0,1,0.07996389348171462,],[1,0,1,1,0,0.3544200515469406,],[1,0,1,1,1,0.22022763568574796,],[1,1,0,0,0,0.7009673407193542,],[1,1,0,0,1,0.5770948548827208,],[1,1,0,1,0,0.7746660507757358,],[1,1,0,1,1,0.8864525415393572,],[1,1,1,0,0,0.9456804382743464,],[1,1,1,0,1,0.2794452320816531,],[1,1,1,1,0,0.6228144672534194,],[1,1,1,1,1,0.4095142187091442,],])
    AG2_F26 = Factor('AG2_F26', [AG2_V26,AG2_V27,AG2_V28,AG2_V29,AG2_V30,])
    AG2_F26.add_values([[0,0,0,0,0,0.82957390342067,],[0,0,0,0,1,0.7287378817757035,],[0,0,0,1,0,0.6126738574223336,],[0,0,0,1,1,0.7351592204956525,],[0,0,1,0,0,0.8973400377756137,],[0,0,1,0,1,0.37861733624071975,],[0,0,1,1,0,0.9672482664395662,],[0,0,1,1,1,0.8255859342937323,],[0,1,0,0,0,0.19578621817846495,],[0,1,0,0,1,0.17738474520152936,],[0,1,0,1,0,0.4697602449917775,],[0,1,0,1,1,0.9336166125047225,],[0,1,1,0,0,0.7521092319421757,],[0,1,1,0,1,0.06447063194504478,],[0,1,1,1,0,0.6866875415832924,],[0,1,1,1,1,0.5438784470627801,],[1,0,0,0,0,0.29643731250383576,],[1,0,0,0,1,0.6264365482200833,],[1,0,0,1,0,0.6967383245028422,],[1,0,0,1,1,0.48758467116935245,],[1,0,1,0,0,0.7412934116392355,],[1,0,1,0,1,0.7470922828461828,],[1,0,1,1,0,0.5195165320001233,],[1,0,1,1,1,0.9218125669569318,],[1,1,0,0,0,0.9385335527002494,],[1,1,0,0,1,0.8599670957981285,],[1,1,0,1,0,0.16272838681773574,],[1,1,0,1,1,0.5929525110860794,],[1,1,1,0,0,0.8609076617811168,],[1,1,1,0,1,0.7615450975197627,],[1,1,1,1,0,0.19582865740917085,],[1,1,1,1,1,0.28200425904523696,],])
    AG2_F27 = Factor('AG2_F27', [AG2_V27,AG2_V28,AG2_V29,AG2_V30,AG2_V31,])
    AG2_F27.add_values([[0,0,0,0,0,0.24662317923242535,],[0,0,0,0,1,0.2327241261626352,],[0,0,0,1,0,0.8794050944009305,],[0,0,0,1,1,0.3813940439840562,],[0,0,1,0,0,0.24053724024498147,],[0,0,1,0,1,0.2640814049550081,],[0,0,1,1,0,0.3954177723953689,],[0,0,1,1,1,0.49641323824959926,],[0,1,0,0,0,0.4727137551771891,],[0,1,0,0,1,0.7989864657860534,],[0,1,0,1,0,0.7431031984282159,],[0,1,0,1,1,0.0855686085372611,],[0,1,1,0,0,0.3905715553771679,],[0,1,1,0,1,0.5755121707965848,],[0,1,1,1,0,0.23259428334214868,],[0,1,1,1,1,0.6923951486097321,],[1,0,0,0,0,0.9305172774465573,],[1,0,0,0,1,0.03271782924334831,],[1,0,0,1,0,0.11366567786165131,],[1,0,0,1,1,0.9070225257137331,],[1,0,1,0,0,0.5175833446573982,],[1,0,1,0,1,0.4135739274596638,],[1,0,1,1,0,0.8612986827422366,],[1,0,1,1,1,0.4231817013495655,],[1,1,0,0,0,0.08449384742346223,],[1,1,0,0,1,0.15459606763398132,],[1,1,0,1,0,0.3458580243841459,],[1,1,0,1,1,0.7658377638713163,],[1,1,1,0,0,0.3235146567679481,],[1,1,1,0,1,0.7385631239688218,],[1,1,1,1,0,0.4196824282698724,],[1,1,1,1,1,0.661643716416165,],])
    AG2_F28 = Factor('AG2_F28', [AG2_V28,AG2_V29,AG2_V30,AG2_V31,AG2_V32,])
    AG2_F28.add_values([[0,0,0,0,0,0.19781863372865283,],[0,0,0,0,1,0.13371764893253316,],[0,0,0,1,0,0.5852266448146326,],[0,0,0,1,1,0.614599745510047,],[0,0,1,0,0,0.611503642454729,],[0,0,1,0,1,0.47139086227281796,],[0,0,1,1,0,0.3688837706564846,],[0,0,1,1,1,0.17949050522626772,],[0,1,0,0,0,0.014122645505868019,],[0,1,0,0,1,0.7887886574546024,],[0,1,0,1,0,0.5177254914604411,],[0,1,0,1,1,0.11672996535580711,],[0,1,1,0,0,0.7327281740806025,],[0,1,1,0,1,0.8158249081467969,],[0,1,1,1,0,0.820770357679844,],[0,1,1,1,1,0.7769006221627328,],[1,0,0,0,0,0.7763995724440854,],[1,0,0,0,1,0.33690521326921335,],[1,0,0,1,0,0.48813503299864675,],[1,0,0,1,1,0.36377374990875877,],[1,0,1,0,0,0.6688710580862122,],[1,0,1,0,1,0.1214580338799278,],[1,0,1,1,0,0.39876458085996397,],[1,0,1,1,1,0.13869534221459287,],[1,1,0,0,0,0.9063807927458728,],[1,1,0,0,1,0.3904541838111582,],[1,1,0,1,0,0.2804314827583108,],[1,1,0,1,1,0.5347988780326665,],[1,1,1,0,0,0.11066238412867634,],[1,1,1,0,1,0.7825342576193195,],[1,1,1,1,0,0.45545529340611635,],[1,1,1,1,1,0.33689008287330446,],])
    AG2_F29 = Factor('AG2_F29', [AG2_V29,AG2_V30,AG2_V31,AG2_V32,AG2_V33,])
    AG2_F29.add_values([[0,0,0,0,0,0.022761481975514652,],[0,0,0,0,1,0.40201751796823215,],[0,0,0,1,0,0.054418175820239174,],[0,0,0,1,1,0.16065017863298492,],[0,0,1,0,0,0.5000406326872741,],[0,0,1,0,1,0.3369856986463782,],[0,0,1,1,0,0.22536616033413612,],[0,0,1,1,1,0.9353811110784557,],[0,1,0,0,0,0.19378689617088599,],[0,1,0,0,1,0.17439388878583556,],[0,1,0,1,0,0.5796232825996411,],[0,1,0,1,1,0.23494743457145012,],[0,1,1,0,0,0.2462199721890543,],[0,1,1,0,1,0.5437911468869514,],[0,1,1,1,0,0.008722421842949274,],[0,1,1,1,1,0.19955520275390562,],[1,0,0,0,0,0.42896869378214725,],[1,0,0,0,1,0.0029887549906354688,],[1,0,0,1,0,0.30783794813730103,],[1,0,0,1,1,0.8835942086738027,],[1,0,1,0,0,0.2790668149833658,],[1,0,1,0,1,0.9270493694382921,],[1,0,1,1,0,0.769142512659072,],[1,0,1,1,1,0.6581904592070037,],[1,1,0,0,0,0.5219022135796709,],[1,1,0,0,1,0.8734497989455381,],[1,1,0,1,0,0.40316351240640913,],[1,1,0,1,1,0.41848080396725573,],[1,1,1,0,0,0.6157664255804741,],[1,1,1,0,1,0.23377772927922735,],[1,1,1,1,0,0.30811106724367715,],[1,1,1,1,1,0.9171187521472548,],])
    AG2_F30 = Factor('AG2_F30', [AG2_V30,AG2_V31,AG2_V32,AG2_V33,AG2_V34,])
    AG2_F30.add_values([[0,0,0,0,0,0.6389655525237911,],[0,0,0,0,1,0.44381007949665385,],[0,0,0,1,0,0.5277792960603772,],[0,0,0,1,1,0.33865406287046473,],[0,0,1,0,0,0.9662724665677906,],[0,0,1,0,1,0.8158859461125724,],[0,0,1,1,0,0.9505526936463252,],[0,0,1,1,1,0.1998157586857699,],[0,1,0,0,0,0.544856959464812,],[0,1,0,0,1,0.7999929382251219,],[0,1,0,1,0,0.2082399063889471,],[0,1,0,1,1,0.490255759513058,],[0,1,1,0,0,0.11590339265969263,],[0,1,1,0,1,0.48269559535422146,],[0,1,1,1,0,0.11727073384326968,],[0,1,1,1,1,0.48131579845022954,],[1,0,0,0,0,0.9276708532228662,],[1,0,0,0,1,0.12652179908733796,],[1,0,0,1,0,0.2973613521541151,],[1,0,0,1,1,0.876710411900966,],[1,0,1,0,0,0.6678721577037955,],[1,0,1,0,1,0.6043741352606172,],[1,0,1,1,0,0.5384959684000109,],[1,0,1,1,1,0.7135570978569843,],[1,1,0,0,0,0.7030419729053187,],[1,1,0,0,1,0.20263995983371597,],[1,1,0,1,0,0.25721575777752853,],[1,1,0,1,1,0.30864349552000403,],[1,1,1,0,0,0.13801129107671986,],[1,1,1,0,1,0.5657705779744621,],[1,1,1,1,0,0.04118091309636647,],[1,1,1,1,1,0.5425572848625094,],])
    AG2_F31 = Factor('AG2_F31', [AG2_V31,AG2_V32,AG2_V33,AG2_V34,AG2_V35,])
    AG2_F31.add_values([[0,0,0,0,0,0.8668513051730359,],[0,0,0,0,1,0.08673146942612729,],[0,0,0,1,0,0.9694124840323549,],[0,0,0,1,1,0.7597501001051575,],[0,0,1,0,0,0.3101389283617364,],[0,0,1,0,1,0.2970513994968635,],[0,0,1,1,0,0.4836630329837213,],[0,0,1,1,1,0.9028881248000652,],[0,1,0,0,0,0.6624333225132286,],[0,1,0,0,1,0.15058503756131994,],[0,1,0,1,0,0.13715718735402066,],[0,1,0,1,1,0.4038661299800332,],[0,1,1,0,0,0.6614218341280176,],[0,1,1,0,1,0.06633498996062905,],[0,1,1,1,0,0.38667566868340475,],[0,1,1,1,1,0.0031235746735538863,],[1,0,0,0,0,0.19069269826289145,],[1,0,0,0,1,0.059536367244135316,],[1,0,0,1,0,0.8527867806128456,],[1,0,0,1,1,0.8330130185297665,],[1,0,1,0,0,0.44688071836114385,],[1,0,1,0,1,0.9568114118964339,],[1,0,1,1,0,0.2982538486424946,],[1,0,1,1,1,0.30750034712871976,],[1,1,0,0,0,0.09865325876098609,],[1,1,0,0,1,0.583064710088594,],[1,1,0,1,0,0.07734459101259812,],[1,1,0,1,1,0.4433463915332323,],[1,1,1,0,0,0.39874917273955673,],[1,1,1,0,1,0.7075005432607552,],[1,1,1,1,0,0.9182612340660511,],[1,1,1,1,1,0.25617178182617295,],])
    AG2_F32 = Factor('AG2_F32', [AG2_V32,AG2_V33,AG2_V34,AG2_V35,AG2_V36,])
    AG2_F32.add_values([[0,0,0,0,0,0.3974562767690737,],[0,0,0,0,1,0.10819961117455555,],[0,0,0,1,0,0.551360269386853,],[0,0,0,1,1,0.09154481515225836,],[0,0,1,0,0,0.32419133197263333,],[0,0,1,0,1,0.9723012889919934,],[0,0,1,1,0,0.4467890814258205,],[0,0,1,1,1,0.7412537196145262,],[0,1,0,0,0,0.6254246507519177,],[0,1,0,0,1,0.5283188732540056,],[0,1,0,1,0,0.5302336411716772,],[0,1,0,1,1,0.3379163157787189,],[0,1,1,0,0,0.5132858881243388,],[0,1,1,0,1,0.5341035145610501,],[0,1,1,1,0,0.5172994730488244,],[0,1,1,1,1,0.7445585009370144,],[1,0,0,0,0,0.5053976525333899,],[1,0,0,0,1,0.06213280598587558,],[1,0,0,1,0,0.5190693002124217,],[1,0,0,1,1,0.025291973707228424,],[1,0,1,0,0,0.3726755892415662,],[1,0,1,0,1,0.1518278240604356,],[1,0,1,1,0,0.3664906430397327,],[1,0,1,1,1,0.3206140933145942,],[1,1,0,0,0,0.32144915954570163,],[1,1,0,0,1,0.6935255158224448,],[1,1,0,1,0,0.49903323582920583,],[1,1,0,1,1,0.3299411269042102,],[1,1,1,0,0,0.8389092093735006,],[1,1,1,0,1,0.02508156022494064,],[1,1,1,1,0,0.11142414255676018,],[1,1,1,1,1,0.2783496546438059,],])
    AG2_F33 = Factor('AG2_F33', [AG2_V33,AG2_V34,AG2_V35,AG2_V36,AG2_V37,])
    AG2_F33.add_values([[0,0,0,0,0,0.35580085378056675,],[0,0,0,0,1,0.7175719947498059,],[0,0,0,1,0,0.23951679054106934,],[0,0,0,1,1,0.018326762563079815,],[0,0,1,0,0,0.9041994571413812,],[0,0,1,0,1,0.5367202456118795,],[0,0,1,1,0,0.6589817540329422,],[0,0,1,1,1,0.2953728605367493,],[0,1,0,0,0,0.7631663402750668,],[0,1,0,0,1,0.60048321460353,],[0,1,0,1,0,0.27638767887630666,],[0,1,0,1,1,0.9225466359884935,],[0,1,1,0,0,0.6365390625804213,],[0,1,1,0,1,0.0070958932818576004,],[0,1,1,1,0,0.42326728323262874,],[0,1,1,1,1,0.6030714713666566,],[1,0,0,0,0,0.11661727682025728,],[1,0,0,0,1,0.991327006452706,],[1,0,0,1,0,0.5462727436301974,],[1,0,0,1,1,0.7842759662144229,],[1,0,1,0,0,0.46152805062559954,],[1,0,1,0,1,0.6039265497785978,],[1,0,1,1,0,0.03510722705397895,],[1,0,1,1,1,0.30108392445350446,],[1,1,0,0,0,0.20027360548069292,],[1,1,0,0,1,0.4120104705592596,],[1,1,0,1,0,0.6668959586109015,],[1,1,0,1,1,0.6596606590405936,],[1,1,1,0,0,0.11267099718148456,],[1,1,1,0,1,0.04457956760928831,],[1,1,1,1,0,0.47522046095595266,],[1,1,1,1,1,0.6671941425246204,],])
    AG2_F34 = Factor('AG2_F34', [AG2_V34,AG2_V35,AG2_V36,AG2_V37,AG2_V38,])
    AG2_F34.add_values([[0,0,0,0,0,0.0111633875557825,],[0,0,0,0,1,0.6986304990273327,],[0,0,0,1,0,0.20658811568175284,],[0,0,0,1,1,0.7048240215325755,],[0,0,1,0,0,0.8248408272670895,],[0,0,1,0,1,0.556792278084589,],[0,0,1,1,0,0.3211717992031412,],[0,0,1,1,1,0.3712532645982581,],[0,1,0,0,0,0.0650812707773094,],[0,1,0,0,1,0.8465958463503075,],[0,1,0,1,0,0.3546904245530306,],[0,1,0,1,1,0.11835611979531345,],[0,1,1,0,0,0.611152946284693,],[0,1,1,0,1,0.26101752119541605,],[0,1,1,1,0,0.1794713316467877,],[0,1,1,1,1,0.3730375130325207,],[1,0,0,0,0,0.10956069614397808,],[1,0,0,0,1,0.03934510681297253,],[1,0,0,1,0,0.5083190239574505,],[1,0,0,1,1,0.6382801955004347,],[1,0,1,0,0,0.6491269522608151,],[1,0,1,0,1,0.931504738460951,],[1,0,1,1,0,0.43389169474001227,],[1,0,1,1,1,0.2920178154787128,],[1,1,0,0,0,0.28674554428956356,],[1,1,0,0,1,0.837493604930942,],[1,1,0,1,0,0.13934569299369917,],[1,1,0,1,1,0.180642855233725,],[1,1,1,0,0,0.2644778442876104,],[1,1,1,0,1,0.90564610173291,],[1,1,1,1,0,0.8984415277927623,],[1,1,1,1,1,0.6022230333877533,],])
    AG2_F35 = Factor('AG2_F35', [AG2_V35,AG2_V36,AG2_V37,AG2_V38,AG2_V39,])
    AG2_F35.add_values([[0,0,0,0,0,0.4893191225651244,],[0,0,0,0,1,0.08242365551204442,],[0,0,0,1,0,0.48438016709970505,],[0,0,0,1,1,0.42430098851818315,],[0,0,1,0,0,0.01822669247469946,],[0,0,1,0,1,0.7598788139126272,],[0,0,1,1,0,0.9108691011117656,],[0,0,1,1,1,0.696881303081404,],[0,1,0,0,0,0.25007696734841184,],[0,1,0,0,1,0.7676909277286815,],[0,1,0,1,0,0.357955728904973,],[0,1,0,1,1,0.8037341902063091,],[0,1,1,0,0,0.8951252579343215,],[0,1,1,0,1,0.2942265561316459,],[0,1,1,1,0,0.04240437036504954,],[0,1,1,1,1,0.19866533302695577,],[1,0,0,0,0,0.6937199081710822,],[1,0,0,0,1,0.9749495057990899,],[1,0,0,1,0,0.6765676917765261,],[1,0,0,1,1,0.8623775359515417,],[1,0,1,0,0,0.4617223027405391,],[1,0,1,0,1,0.7752858020461996,],[1,0,1,1,0,0.4305168062174221,],[1,0,1,1,1,0.5096904501806291,],[1,1,0,0,0,0.9499743130798021,],[1,1,0,0,1,0.3366873937080077,],[1,1,0,1,0,0.02218269584408895,],[1,1,0,1,1,0.441942611118663,],[1,1,1,0,0,0.9897719921150108,],[1,1,1,0,1,0.6520986306060303,],[1,1,1,1,0,0.8087382241051785,],[1,1,1,1,1,0.9640342324112072,],])
    AG2_F36 = Factor('AG2_F36', [AG2_V36,AG2_V37,AG2_V38,AG2_V39,AG2_V40,])
    AG2_F36.add_values([[0,0,0,0,0,0.5114943949895401,],[0,0,0,0,1,0.07412883077515563,],[0,0,0,1,0,0.24442490937054015,],[0,0,0,1,1,0.9301259121094076,],[0,0,1,0,0,0.5670443907842174,],[0,0,1,0,1,0.36742116474713366,],[0,0,1,1,0,0.27690304115478864,],[0,0,1,1,1,0.9257366436821409,],[0,1,0,0,0,0.0841949943399134,],[0,1,0,0,1,0.16952301117646543,],[0,1,0,1,0,0.7874279489648601,],[0,1,0,1,1,0.8141333229507002,],[0,1,1,0,0,0.7647700957459126,],[0,1,1,0,1,0.548895590514647,],[0,1,1,1,0,0.7322191254974775,],[0,1,1,1,1,0.6972437292400853,],[1,0,0,0,0,0.5309895166434423,],[1,0,0,0,1,0.2922550348326891,],[1,0,0,1,0,0.6959620259991742,],[1,0,0,1,1,0.0862525344162861,],[1,0,1,0,0,0.016676960964464783,],[1,0,1,0,1,0.6953518815223666,],[1,0,1,1,0,0.05686469301576538,],[1,0,1,1,1,0.23197113092614005,],[1,1,0,0,0,0.12651000339412705,],[1,1,0,0,1,0.4434101675994766,],[1,1,0,1,0,0.2478088996634058,],[1,1,0,1,1,0.03290166888742802,],[1,1,1,0,0,0.5004765115271925,],[1,1,1,0,1,0.8118720295688863,],[1,1,1,1,0,0.23377079458628194,],[1,1,1,1,1,0.06146536414565546,],])
    AG2_F37 = Factor('AG2_F37', [AG2_V37,AG2_V38,AG2_V39,AG2_V40,AG2_V41,])
    AG2_F37.add_values([[0,0,0,0,0,0.3252210786166127,],[0,0,0,0,1,0.35701517505627545,],[0,0,0,1,0,0.40501822152251515,],[0,0,0,1,1,0.8454094931560638,],[0,0,1,0,0,0.14056471818781355,],[0,0,1,0,1,0.003041622279595421,],[0,0,1,1,0,0.20838073118080325,],[0,0,1,1,1,0.8077629624302085,],[0,1,0,0,0,0.08977683273518725,],[0,1,0,0,1,0.565760610317714,],[0,1,0,1,0,0.43106749327160154,],[0,1,0,1,1,0.9391083139718399,],[0,1,1,0,0,0.46262739399499403,],[0,1,1,0,1,0.03316066959517158,],[0,1,1,1,0,0.44206556430732513,],[0,1,1,1,1,0.5594093602234183,],[1,0,0,0,0,0.33229717650083135,],[1,0,0,0,1,0.8510796523379994,],[1,0,0,1,0,0.6084687035165044,],[1,0,0,1,1,0.9604161640419511,],[1,0,1,0,0,0.8523209490878687,],[1,0,1,0,1,0.9845163133504309,],[1,0,1,1,0,0.6574804075006151,],[1,0,1,1,1,0.8878012591795733,],[1,1,0,0,0,0.49509154302859637,],[1,1,0,0,1,0.15951287748187723,],[1,1,0,1,0,0.6964311529722813,],[1,1,0,1,1,0.4571455301007678,],[1,1,1,0,0,0.12991119500417073,],[1,1,1,0,1,0.018797641539932932,],[1,1,1,1,0,0.36327890379633426,],[1,1,1,1,1,0.5906793797124535,],])
    AG2_F38 = Factor('AG2_F38', [AG2_V38,AG2_V39,AG2_V40,AG2_V41,AG2_V42,])
    AG2_F38.add_values([[0,0,0,0,0,0.69130957568117,],[0,0,0,0,1,0.059110028705799664,],[0,0,0,1,0,0.37557566764114975,],[0,0,0,1,1,0.1558285641228535,],[0,0,1,0,0,0.5896308762873378,],[0,0,1,0,1,0.484774776982547,],[0,0,1,1,0,0.05431474110093077,],[0,0,1,1,1,0.9669789882295042,],[0,1,0,0,0,0.19779393499189293,],[0,1,0,0,1,0.4985542499133902,],[0,1,0,1,0,0.5364976192803038,],[0,1,0,1,1,0.88817882386151,],[0,1,1,0,0,0.20642403906234216,],[0,1,1,0,1,0.9364684229902286,],[0,1,1,1,0,0.6245129663262499,],[0,1,1,1,1,0.045053168445345335,],[1,0,0,0,0,0.0411797549921237,],[1,0,0,0,1,0.13600587969279782,],[1,0,0,1,0,0.6397280598462322,],[1,0,0,1,1,0.5463175840008156,],[1,0,1,0,0,0.6518487673428526,],[1,0,1,0,1,0.7272502445044629,],[1,0,1,1,0,0.19215368955570303,],[1,0,1,1,1,0.423668547148002,],[1,1,0,0,0,0.9862371678007502,],[1,1,0,0,1,0.44395063613756086,],[1,1,0,1,0,0.5005222387038614,],[1,1,0,1,1,0.40415562291445756,],[1,1,1,0,0,0.12449137681966019,],[1,1,1,0,1,0.5269384845964031,],[1,1,1,1,0,0.1525254140421064,],[1,1,1,1,1,0.4068747923298835,],])
    AG2_F39 = Factor('AG2_F39', [AG2_V39,AG2_V40,AG2_V41,AG2_V42,AG2_V43,])
    AG2_F39.add_values([[0,0,0,0,0,0.8482481090909366,],[0,0,0,0,1,0.5711800075209138,],[0,0,0,1,0,0.0025807556042333497,],[0,0,0,1,1,0.830409580419426,],[0,0,1,0,0,0.06668249496900079,],[0,0,1,0,1,0.849275178109277,],[0,0,1,1,0,0.012595686192051005,],[0,0,1,1,1,0.14441140150408174,],[0,1,0,0,0,0.7796129030863915,],[0,1,0,0,1,0.2948871180144939,],[0,1,0,1,0,0.0860935403177353,],[0,1,0,1,1,0.98820818448405,],[0,1,1,0,0,0.06634572533499135,],[0,1,1,0,1,0.0986239017965022,],[0,1,1,1,0,0.8014160763097434,],[0,1,1,1,1,0.9657204955465104,],[1,0,0,0,0,0.04152734685085457,],[1,0,0,0,1,0.04056513280064341,],[1,0,0,1,0,0.09151713244857257,],[1,0,0,1,1,0.9972545973466351,],[1,0,1,0,0,0.6581515432297954,],[1,0,1,0,1,0.7773450766441454,],[1,0,1,1,0,0.8195641991068165,],[1,0,1,1,1,0.8384348714667066,],[1,1,0,0,0,0.628162039540196,],[1,1,0,0,1,0.09089570070351954,],[1,1,0,1,0,0.7102864355388785,],[1,1,0,1,1,0.5223349980072793,],[1,1,1,0,0,0.6311760976591946,],[1,1,1,0,1,0.23478476234942922,],[1,1,1,1,0,0.6747043350310099,],[1,1,1,1,1,0.020056826009470285,],])
    AG2_F40 = Factor('AG2_F40', [AG2_V40,AG2_V41,AG2_V42,AG2_V43,AG2_V44,])
    AG2_F40.add_values([[0,0,0,0,0,0.6271269195201903,],[0,0,0,0,1,0.737496835490672,],[0,0,0,1,0,0.06306842061875222,],[0,0,0,1,1,0.5467227820289079,],[0,0,1,0,0,0.5445389905503762,],[0,0,1,0,1,0.9398705437084508,],[0,0,1,1,0,0.10618948220239,],[0,0,1,1,1,0.36059048027702734,],[0,1,0,0,0,0.48444110226997295,],[0,1,0,0,1,0.45329175978041003,],[0,1,0,1,0,0.19377908854192183,],[0,1,0,1,1,0.4529960284443178,],[0,1,1,0,0,0.5793877533530466,],[0,1,1,0,1,0.3339178272577063,],[0,1,1,1,0,0.14830758139500663,],[0,1,1,1,1,0.13781131278862,],[1,0,0,0,0,0.3215007480978273,],[1,0,0,0,1,0.17756691753517598,],[1,0,0,1,0,0.9009273913266792,],[1,0,0,1,1,0.7716503659254568,],[1,0,1,0,0,0.7797954532238746,],[1,0,1,0,1,0.6515663152442267,],[1,0,1,1,0,0.5138915490571957,],[1,0,1,1,1,0.7233624191223538,],[1,1,0,0,0,0.22054726509346004,],[1,1,0,0,1,0.6627864835513998,],[1,1,0,1,0,0.2920180082195168,],[1,1,0,1,1,0.46267541957002134,],[1,1,1,0,0,0.9815712438939558,],[1,1,1,0,1,0.7129420075269932,],[1,1,1,1,0,0.8268866166320086,],[1,1,1,1,1,0.8736272767356221,],])
    AG2_F41 = Factor('AG2_F41', [AG2_V41,AG2_V42,AG2_V43,AG2_V44,AG2_V45,])
    AG2_F41.add_values([[0,0,0,0,0,0.15519580675021571,],[0,0,0,0,1,0.6334079598661937,],[0,0,0,1,0,0.18537359880750207,],[0,0,0,1,1,0.9886129165700109,],[0,0,1,0,0,0.46503512564215166,],[0,0,1,0,1,0.3811496427975047,],[0,0,1,1,0,0.49107892365376177,],[0,0,1,1,1,0.2154473590355637,],[0,1,0,0,0,0.9315969213179397,],[0,1,0,0,1,0.726061061379616,],[0,1,0,1,0,0.9964790617061439,],[0,1,0,1,1,0.5747996141487032,],[0,1,1,0,0,0.8333829845216479,],[0,1,1,0,1,0.7459680614613884,],[0,1,1,1,0,0.46248519047753023,],[0,1,1,1,1,0.39594019043863676,],[1,0,0,0,0,0.13435553124055527,],[1,0,0,0,1,0.7843848822108643,],[1,0,0,1,0,0.43623890146218364,],[1,0,0,1,1,0.9391909732644004,],[1,0,1,0,0,0.5791684670923545,],[1,0,1,0,1,0.4582942613919465,],[1,0,1,1,0,0.9042467262933017,],[1,0,1,1,1,0.47846482152772807,],[1,1,0,0,0,0.4324904477937072,],[1,1,0,0,1,0.9737243337470691,],[1,1,0,1,0,0.552229115250992,],[1,1,0,1,1,0.43506828838177064,],[1,1,1,0,0,0.4139843122301261,],[1,1,1,0,1,0.22382010747245693,],[1,1,1,1,0,0.9328940305566705,],[1,1,1,1,1,0.856157418530454,],])
    AG2_F42 = Factor('AG2_F42', [AG2_V42,AG2_V43,AG2_V44,AG2_V45,AG2_V46,])
    AG2_F42.add_values([[0,0,0,0,0,0.9196195507329681,],[0,0,0,0,1,0.11246938862871511,],[0,0,0,1,0,0.19529346899617542,],[0,0,0,1,1,0.7241611165438621,],[0,0,1,0,0,0.2889418426459605,],[0,0,1,0,1,0.16086009972108498,],[0,0,1,1,0,0.2908013418737933,],[0,0,1,1,1,0.7488576296151902,],[0,1,0,0,0,0.5215641563540659,],[0,1,0,0,1,0.6486455346281454,],[0,1,0,1,0,0.030393774564667325,],[0,1,0,1,1,0.6547821436670821,],[0,1,1,0,0,0.2317819328751233,],[0,1,1,0,1,0.7881011824101836,],[0,1,1,1,0,0.4134225712655483,],[0,1,1,1,1,0.8431212569666574,],[1,0,0,0,0,0.6525827221113829,],[1,0,0,0,1,0.9792472361423272,],[1,0,0,1,0,0.2813397802277437,],[1,0,0,1,1,0.7581173355346749,],[1,0,1,0,0,0.16121418987648303,],[1,0,1,0,1,0.43708313578099967,],[1,0,1,1,0,0.625606288839251,],[1,0,1,1,1,0.7014591323835293,],[1,1,0,0,0,0.43184132492577104,],[1,1,0,0,1,0.5087771875907722,],[1,1,0,1,0,0.820911822794598,],[1,1,0,1,1,0.4360435977856781,],[1,1,1,0,0,0.307443307409102,],[1,1,1,0,1,0.4544870145203171,],[1,1,1,1,0,0.008028670070411801,],[1,1,1,1,1,0.14535243417726196,],])
    AG2_F43 = Factor('AG2_F43', [AG2_V43,AG2_V44,AG2_V45,AG2_V46,AG2_V47,])
    AG2_F43.add_values([[0,0,0,0,0,0.9044141144469234,],[0,0,0,0,1,0.2351574666150564,],[0,0,0,1,0,0.6004977666795185,],[0,0,0,1,1,0.9290669904088973,],[0,0,1,0,0,0.7220636888673543,],[0,0,1,0,1,0.5514271605481689,],[0,0,1,1,0,0.7807684707172811,],[0,0,1,1,1,0.6254829800478731,],[0,1,0,0,0,0.5547721819753175,],[0,1,0,0,1,0.5601346382314695,],[0,1,0,1,0,0.0714632327176754,],[0,1,0,1,1,0.06201256925578076,],[0,1,1,0,0,0.36048855746480557,],[0,1,1,0,1,0.06279805010931563,],[0,1,1,1,0,0.5814834558902273,],[0,1,1,1,1,0.7814896543253873,],[1,0,0,0,0,0.49307246418993017,],[1,0,0,0,1,0.40970861798640845,],[1,0,0,1,0,0.4861248312334173,],[1,0,0,1,1,0.42144525942349476,],[1,0,1,0,0,0.5766449327043669,],[1,0,1,0,1,0.38218497791874667,],[1,0,1,1,0,0.6243956951836436,],[1,0,1,1,1,0.16921201967660313,],[1,1,0,0,0,0.8273901447291332,],[1,1,0,0,1,0.34751458322827433,],[1,1,0,1,0,0.8082467750767147,],[1,1,0,1,1,0.019478309892945588,],[1,1,1,0,0,0.5177736267066988,],[1,1,1,0,1,0.7382571202158303,],[1,1,1,1,0,0.5569788602267861,],[1,1,1,1,1,0.24174149689284227,],])
    AG2_F44 = Factor('AG2_F44', [AG2_V44,AG2_V45,AG2_V46,AG2_V47,AG2_V48,])
    AG2_F44.add_values([[0,0,0,0,0,0.672973192786953,],[0,0,0,0,1,0.5559705048316036,],[0,0,0,1,0,0.8480392167071384,],[0,0,0,1,1,0.7266473526715234,],[0,0,1,0,0,0.9087854978485943,],[0,0,1,0,1,0.11931810009706437,],[0,0,1,1,0,0.7192915528049828,],[0,0,1,1,1,0.7914879567633564,],[0,1,0,0,0,0.8031442390011455,],[0,1,0,0,1,0.9732545008833041,],[0,1,0,1,0,0.48558146923173967,],[0,1,0,1,1,0.7471712688763409,],[0,1,1,0,0,0.7031541113789279,],[0,1,1,0,1,0.946106941957816,],[0,1,1,1,0,0.9320914969744655,],[0,1,1,1,1,0.6246596262919318,],[1,0,0,0,0,0.991361722994947,],[1,0,0,0,1,0.559967608616995,],[1,0,0,1,0,0.49946636547937434,],[1,0,0,1,1,0.3097577938763404,],[1,0,1,0,0,0.06871295509458748,],[1,0,1,0,1,0.6223822793353169,],[1,0,1,1,0,0.03471097368211293,],[1,0,1,1,1,0.5212956464711421,],[1,1,0,0,0,0.22305496387175125,],[1,1,0,0,1,0.8808044975320254,],[1,1,0,1,0,0.6367858721847084,],[1,1,0,1,1,0.009016564661732144,],[1,1,1,0,0,0.7355231125503198,],[1,1,1,0,1,0.39051111777531594,],[1,1,1,1,0,0.6414290171261119,],[1,1,1,1,1,0.8812781810437655,],])
    AG2_F45 = Factor('AG2_F45', [AG2_V45,AG2_V46,AG2_V47,AG2_V48,AG2_V49,])
    AG2_F45.add_values([[0,0,0,0,0,0.06256582738854494,],[0,0,0,0,1,0.6813042488101871,],[0,0,0,1,0,0.8998955043897289,],[0,0,0,1,1,0.47287673498918537,],[0,0,1,0,0,0.5481578987915596,],[0,0,1,0,1,0.3490542527745045,],[0,0,1,1,0,0.24969152851783727,],[0,0,1,1,1,0.16417509276476486,],[0,1,0,0,0,0.472723883334835,],[0,1,0,0,1,0.5338840885400561,],[0,1,0,1,0,0.812578390332889,],[0,1,0,1,1,0.09649536259239123,],[0,1,1,0,0,0.15420487263487156,],[0,1,1,0,1,0.960638477328221,],[0,1,1,1,0,0.5741937360144591,],[0,1,1,1,1,0.7383688117020385,],[1,0,0,0,0,0.3143269566628119,],[1,0,0,0,1,0.9082180709407922,],[1,0,0,1,0,0.31849098664194064,],[1,0,0,1,1,0.54412589832269,],[1,0,1,0,0,0.01232824922890773,],[1,0,1,0,1,0.8155838434324034,],[1,0,1,1,0,0.29459161688862207,],[1,0,1,1,1,0.12589994509968896,],[1,1,0,0,0,0.9938574849476425,],[1,1,0,0,1,0.6461404930315585,],[1,1,0,1,0,0.03837302890151991,],[1,1,0,1,1,0.5987278278364214,],[1,1,1,0,0,0.6752524304355503,],[1,1,1,0,1,0.019780207982879768,],[1,1,1,1,0,0.20958927434888036,],[1,1,1,1,1,0.3521431597092592,],])
    AG2_F46 = Factor('AG2_F46', [AG2_V46,AG2_V47,AG2_V48,AG2_V49,AG2_V50,])
    AG2_F46.add_values([[0,0,0,0,0,0.8009202651216881,],[0,0,0,0,1,0.29255295426008954,],[0,0,0,1,0,0.663513617675208,],[0,0,0,1,1,0.47307681837891863,],[0,0,1,0,0,0.5094912507968066,],[0,0,1,0,1,0.07492091875680376,],[0,0,1,1,0,0.7998309663399469,],[0,0,1,1,1,0.32852690195581624,],[0,1,0,0,0,0.1432080484117844,],[0,1,0,0,1,0.8868530133368164,],[0,1,0,1,0,0.8060649238611705,],[0,1,0,1,1,0.44872461836643074,],[0,1,1,0,0,0.6745102856982584,],[0,1,1,0,1,0.06526353893762765,],[0,1,1,1,0,0.9725460625163038,],[0,1,1,1,1,0.5328891180703978,],[1,0,0,0,0,0.2249820249713645,],[1,0,0,0,1,0.7181600387103797,],[1,0,0,1,0,0.4928031604773209,],[1,0,0,1,1,0.5502921261807562,],[1,0,1,0,0,0.9927851498180736,],[1,0,1,0,1,0.23876812783126442,],[1,0,1,1,0,0.12985863246448426,],[1,0,1,1,1,0.6554971002472334,],[1,1,0,0,0,0.34791235231155404,],[1,1,0,0,1,0.1967636088837571,],[1,1,0,1,0,0.7978958140239202,],[1,1,0,1,1,0.20279319175084118,],[1,1,1,0,0,0.6814617916991548,],[1,1,1,0,1,0.7649959974222836,],[1,1,1,1,0,0.27585017737959217,],[1,1,1,1,1,0.9149582187671752,],])
    AG2_F47 = Factor('AG2_F47', [AG2_V47,AG2_V48,AG2_V49,AG2_V50,AG2_V51,])
    AG2_F47.add_values([[0,0,0,0,0,0.03678364239752211,],[0,0,0,0,1,0.1367445490010621,],[0,0,0,1,0,0.07857640047458192,],[0,0,0,1,1,0.7597470772421803,],[0,0,1,0,0,0.10725482724040326,],[0,0,1,0,1,0.9940118400031952,],[0,0,1,1,0,0.6391080834476165,],[0,0,1,1,1,0.16380845685064924,],[0,1,0,0,0,0.9836731898973619,],[0,1,0,0,1,0.30101554643934925,],[0,1,0,1,0,0.4332661203766485,],[0,1,0,1,1,0.6053463770801738,],[0,1,1,0,0,0.9806522163724666,],[0,1,1,0,1,0.5753931642708318,],[0,1,1,1,0,0.238030182878012,],[0,1,1,1,1,0.6554578157045525,],[1,0,0,0,0,0.7945304571404692,],[1,0,0,0,1,0.10542653880842649,],[1,0,0,1,0,0.3207196639864737,],[1,0,0,1,1,0.9548604467735838,],[1,0,1,0,0,0.4165414514581617,],[1,0,1,0,1,0.25109789203813926,],[1,0,1,1,0,0.9294115951389367,],[1,0,1,1,1,0.3732284900219967,],[1,1,0,0,0,0.37528528429357727,],[1,1,0,0,1,0.6413092818555045,],[1,1,0,1,0,0.2780853210043815,],[1,1,0,1,1,0.051583482696379794,],[1,1,1,0,0,0.24810225582434386,],[1,1,1,0,1,0.10821058168310337,],[1,1,1,1,0,0.20946135366422822,],[1,1,1,1,1,0.29472612419252014,],])
    AG2_F48 = Factor('AG2_F48', [AG2_V48,AG2_V49,AG2_V50,AG2_V51,AG2_V52,])
    AG2_F48.add_values([[0,0,0,0,0,0.7455325701963774,],[0,0,0,0,1,0.7702380318794254,],[0,0,0,1,0,0.27087590421425994,],[0,0,0,1,1,0.6442792396653201,],[0,0,1,0,0,0.7568128309224107,],[0,0,1,0,1,0.5690381578377122,],[0,0,1,1,0,0.8201987254922296,],[0,0,1,1,1,0.42786030610566633,],[0,1,0,0,0,0.8754949381704821,],[0,1,0,0,1,0.9506253659238971,],[0,1,0,1,0,0.0370870566009124,],[0,1,0,1,1,0.16448607862001768,],[0,1,1,0,0,0.7694800920715933,],[0,1,1,0,1,0.6819992812506788,],[0,1,1,1,0,0.2873895724022609,],[0,1,1,1,1,0.01291538788340753,],[1,0,0,0,0,0.8360796805411177,],[1,0,0,0,1,0.4399916667546708,],[1,0,0,1,0,0.773618456553472,],[1,0,0,1,1,0.9007635522997607,],[1,0,1,0,0,0.7821524527932066,],[1,0,1,0,1,0.9707322571962433,],[1,0,1,1,0,0.929282555991332,],[1,0,1,1,1,0.520008350139935,],[1,1,0,0,0,0.8484404854017692,],[1,1,0,0,1,0.5324887927740369,],[1,1,0,1,0,0.19836126888253983,],[1,1,0,1,1,0.6074518788325083,],[1,1,1,0,0,0.2667385290044675,],[1,1,1,0,1,0.5105059238324691,],[1,1,1,1,0,0.1524665504839317,],[1,1,1,1,1,0.6168310770588044,],])
    AG2_F49 = Factor('AG2_F49', [AG2_V49,AG2_V50,AG2_V51,AG2_V52,AG2_V53,])
    AG2_F49.add_values([[0,0,0,0,0,0.9562882275146741,],[0,0,0,0,1,0.2815340451138543,],[0,0,0,1,0,0.7041845530516259,],[0,0,0,1,1,0.41036913783313045,],[0,0,1,0,0,0.16302898517850387,],[0,0,1,0,1,0.5733055984146083,],[0,0,1,1,0,0.1478741594665057,],[0,0,1,1,1,0.42011462167979496,],[0,1,0,0,0,0.22444068227144173,],[0,1,0,0,1,0.7748457196509905,],[0,1,0,1,0,0.632482222547219,],[0,1,0,1,1,0.010115278429842884,],[0,1,1,0,0,0.34340640681775336,],[0,1,1,0,1,0.04085195222333347,],[0,1,1,1,0,0.5207693376903302,],[0,1,1,1,1,0.30176695103356943,],[1,0,0,0,0,0.1252005271792628,],[1,0,0,0,1,0.6837567218443934,],[1,0,0,1,0,0.3434398842830495,],[1,0,0,1,1,0.4818370911244575,],[1,0,1,0,0,0.7194620124906724,],[1,0,1,0,1,0.642667931261129,],[1,0,1,1,0,0.866525328411054,],[1,0,1,1,1,0.665935270079514,],[1,1,0,0,0,0.9188973463760639,],[1,1,0,0,1,0.9442333343548656,],[1,1,0,1,0,0.9110346895348338,],[1,1,0,1,1,0.5019368290989987,],[1,1,1,0,0,0.9836589518013166,],[1,1,1,0,1,0.2671667376510278,],[1,1,1,1,0,0.5731166766383411,],[1,1,1,1,1,0.15134185853709364,],])
    AG2_F50 = Factor('AG2_F50', [AG2_V50,AG2_V51,AG2_V52,AG2_V53,AG2_V54,])
    AG2_F50.add_values([[0,0,0,0,0,0.3476147076143985,],[0,0,0,0,1,0.12069668751838396,],[0,0,0,1,0,0.9017316927692213,],[0,0,0,1,1,0.1323649868208652,],[0,0,1,0,0,0.18916835615284194,],[0,0,1,0,1,0.9038521919297382,],[0,0,1,1,0,0.7470538568460107,],[0,0,1,1,1,0.3507709224327521,],[0,1,0,0,0,0.9399327546690472,],[0,1,0,0,1,0.2707168928213221,],[0,1,0,1,0,0.7797339108568514,],[0,1,0,1,1,0.9103698875268967,],[0,1,1,0,0,0.41071171146231505,],[0,1,1,0,1,0.7045093002828927,],[0,1,1,1,0,0.9274322797758289,],[0,1,1,1,1,0.06729835790902275,],[1,0,0,0,0,0.32987498140850774,],[1,0,0,0,1,0.5732463855325317,],[1,0,0,1,0,0.46789215782478677,],[1,0,0,1,1,0.9247941990525821,],[1,0,1,0,0,0.7167251529163335,],[1,0,1,0,1,0.4822681755093827,],[1,0,1,1,0,0.6094771512479745,],[1,0,1,1,1,0.013928103973215636,],[1,1,0,0,0,0.8840851537678841,],[1,1,0,0,1,0.2432173978567281,],[1,1,0,1,0,0.6646851600010563,],[1,1,0,1,1,0.0021835219252778343,],[1,1,1,0,0,0.5216605651420237,],[1,1,1,0,1,0.24008251339921144,],[1,1,1,1,0,0.03231175373119954,],[1,1,1,1,1,0.09866025416365486,],])
    AG2_F51 = Factor('AG2_F51', [AG2_V51,AG2_V52,AG2_V53,AG2_V54,AG2_V55,])
    AG2_F51.add_values([[0,0,0,0,0,0.07365300452140038,],[0,0,0,0,1,0.8388144934862277,],[0,0,0,1,0,0.10355121764248615,],[0,0,0,1,1,0.15714625027157136,],[0,0,1,0,0,0.4533927642364019,],[0,0,1,0,1,0.9106387226093471,],[0,0,1,1,0,0.7547087867881535,],[0,0,1,1,1,0.3334262065096447,],[0,1,0,0,0,0.45522619675257947,],[0,1,0,0,1,0.8797975310406118,],[0,1,0,1,0,0.0435961300011075,],[0,1,0,1,1,0.298856489249977,],[0,1,1,0,0,0.40210415814913825,],[0,1,1,0,1,0.9395056396380758,],[0,1,1,1,0,0.9673647398207842,],[0,1,1,1,1,0.4265020087817625,],[1,0,0,0,0,0.060393703487275185,],[1,0,0,0,1,0.09680306928579635,],[1,0,0,1,0,0.3011501047160025,],[1,0,0,1,1,0.27430052920559833,],[1,0,1,0,0,0.45579429210015376,],[1,0,1,0,1,0.18632749696924386,],[1,0,1,1,0,0.9970058036117588,],[1,0,1,1,1,0.2535904114900593,],[1,1,0,0,0,0.2408621553596332,],[1,1,0,0,1,0.5759712263557721,],[1,1,0,1,0,0.29855170934620706,],[1,1,0,1,1,0.7749726014731002,],[1,1,1,0,0,0.26187905349318075,],[1,1,1,0,1,0.9124550402249463,],[1,1,1,1,0,0.39674803816900445,],[1,1,1,1,1,0.521260266368778,],])
    AG2_F52 = Factor('AG2_F52', [AG2_V52,AG2_V53,AG2_V54,AG2_V55,AG2_V56,])
    AG2_F52.add_values([[0,0,0,0,0,0.8956878617543854,],[0,0,0,0,1,0.11671467794277804,],[0,0,0,1,0,0.5088028074893493,],[0,0,0,1,1,0.7422919498875858,],[0,0,1,0,0,0.5268460549647423,],[0,0,1,0,1,0.5793610474861968,],[0,0,1,1,0,0.6825142425120853,],[0,0,1,1,1,0.9143067737561592,],[0,1,0,0,0,0.7869169600762176,],[0,1,0,0,1,0.007750366088867778,],[0,1,0,1,0,0.8990514806573418,],[0,1,0,1,1,0.7167171735185357,],[0,1,1,0,0,0.22719894299239835,],[0,1,1,0,1,0.8754349440673228,],[0,1,1,1,0,0.5767840327974247,],[0,1,1,1,1,0.5773891691197844,],[1,0,0,0,0,0.7531311242929679,],[1,0,0,0,1,0.3336633035899633,],[1,0,0,1,0,0.09390387700925437,],[1,0,0,1,1,0.0912943493292353,],[1,0,1,0,0,0.46230400986118975,],[1,0,1,0,1,0.8380651964265685,],[1,0,1,1,0,0.9964621456824919,],[1,0,1,1,1,0.07680495274572771,],[1,1,0,0,0,0.9885862826453853,],[1,1,0,0,1,0.8290543360408258,],[1,1,0,1,0,0.26115105141614997,],[1,1,0,1,1,0.7710921984259245,],[1,1,1,0,0,0.47907865218985796,],[1,1,1,0,1,0.7973111339424443,],[1,1,1,1,0,0.43397081925001985,],[1,1,1,1,1,0.748508210512146,],])
    AG2_F53 = Factor('AG2_F53', [AG2_V53,AG2_V54,AG2_V55,AG2_V56,AG2_V57,])
    AG2_F53.add_values([[0,0,0,0,0,0.1510643560051119,],[0,0,0,0,1,0.20523182028268303,],[0,0,0,1,0,0.7584977173772836,],[0,0,0,1,1,0.5105611421211096,],[0,0,1,0,0,0.7986704846141658,],[0,0,1,0,1,0.9998682360410284,],[0,0,1,1,0,0.20043645011975084,],[0,0,1,1,1,0.2897761153642714,],[0,1,0,0,0,0.7503449129371537,],[0,1,0,0,1,0.4325327963053461,],[0,1,0,1,0,0.7251299220176138,],[0,1,0,1,1,0.4917238374204636,],[0,1,1,0,0,0.14718419816055958,],[0,1,1,0,1,0.2694482435325327,],[0,1,1,1,0,0.6236911493983559,],[0,1,1,1,1,0.7104697698766446,],[1,0,0,0,0,0.6576398480470917,],[1,0,0,0,1,0.4947365313682481,],[1,0,0,1,0,0.7370817508122801,],[1,0,0,1,1,0.26702278484401243,],[1,0,1,0,0,0.6942127291233783,],[1,0,1,0,1,0.4293270354282004,],[1,0,1,1,0,0.8827370742987954,],[1,0,1,1,1,0.9500051800360847,],[1,1,0,0,0,0.3548871125068888,],[1,1,0,0,1,0.8926991040380855,],[1,1,0,1,0,0.812496483953283,],[1,1,0,1,1,0.767870409342742,],[1,1,1,0,0,0.22789709764796312,],[1,1,1,0,1,0.6673273159171373,],[1,1,1,1,0,0.4763055635060065,],[1,1,1,1,1,0.6687207884864086,],])
    AG2_F54 = Factor('AG2_F54', [AG2_V54,AG2_V55,AG2_V56,AG2_V57,AG2_V58,])
    AG2_F54.add_values([[0,0,0,0,0,0.970770069203303,],[0,0,0,0,1,0.8428462998376879,],[0,0,0,1,0,0.7224924396184583,],[0,0,0,1,1,0.23961498811869975,],[0,0,1,0,0,0.8994786589694274,],[0,0,1,0,1,0.6674634586516421,],[0,0,1,1,0,0.3178980888553552,],[0,0,1,1,1,0.8675275121992649,],[0,1,0,0,0,0.9189836010707162,],[0,1,0,0,1,0.951309144579559,],[0,1,0,1,0,0.1823294459092379,],[0,1,0,1,1,0.060226856487815277,],[0,1,1,0,0,0.21253621095596198,],[0,1,1,0,1,0.5824437453964048,],[0,1,1,1,0,0.3125427596718643,],[0,1,1,1,1,0.4437557965242127,],[1,0,0,0,0,0.5713391281038335,],[1,0,0,0,1,0.7666302208465378,],[1,0,0,1,0,0.356159828928263,],[1,0,0,1,1,0.959175457205182,],[1,0,1,0,0,0.098521103087804,],[1,0,1,0,1,0.5079487465530009,],[1,0,1,1,0,0.5802197457272237,],[1,0,1,1,1,0.207759730947847,],[1,1,0,0,0,0.12648645415015916,],[1,1,0,0,1,0.7492197525626301,],[1,1,0,1,0,0.9117368783959643,],[1,1,0,1,1,0.5129774323709023,],[1,1,1,0,0,0.43895461608699204,],[1,1,1,0,1,0.7179240751148975,],[1,1,1,1,0,0.3236269672695766,],[1,1,1,1,1,0.5409739922242125,],])
    AG2_F55 = Factor('AG2_F55', [AG2_V55,AG2_V56,AG2_V57,AG2_V58,AG2_V59,])
    AG2_F55.add_values([[0,0,0,0,0,0.9084962894673981,],[0,0,0,0,1,0.9503197276115259,],[0,0,0,1,0,0.35169755142789605,],[0,0,0,1,1,0.07210298437622878,],[0,0,1,0,0,0.13779501808570793,],[0,0,1,0,1,0.904206233641579,],[0,0,1,1,0,0.6944494608121914,],[0,0,1,1,1,0.3603715412226673,],[0,1,0,0,0,0.9743010277482049,],[0,1,0,0,1,0.5879266132289976,],[0,1,0,1,0,0.5143879965844356,],[0,1,0,1,1,0.979555192582159,],[0,1,1,0,0,0.6969495533110222,],[0,1,1,0,1,0.24789919359424384,],[0,1,1,1,0,0.6927494903090011,],[0,1,1,1,1,0.4485236439975345,],[1,0,0,0,0,0.22356585827821643,],[1,0,0,0,1,0.992326468239239,],[1,0,0,1,0,0.8229748877804627,],[1,0,0,1,1,0.8867199136852985,],[1,0,1,0,0,0.23899443225321695,],[1,0,1,0,1,0.6433984086060591,],[1,0,1,1,0,0.7364057922584721,],[1,0,1,1,1,0.012182264330297699,],[1,1,0,0,0,0.6379087448518587,],[1,1,0,0,1,0.05580443752185321,],[1,1,0,1,0,0.569714376298021,],[1,1,0,1,1,0.7832810201388244,],[1,1,1,0,0,0.3631078450011754,],[1,1,1,0,1,0.2514520733433135,],[1,1,1,1,0,0.8435220898502754,],[1,1,1,1,1,0.2990002449153674,],])
    AG2_F56 = Factor('AG2_F56', [AG2_V56,AG2_V57,AG2_V58,AG2_V59,AG2_V60,])
    AG2_F56.add_values([[0,0,0,0,0,0.4970758067621832,],[0,0,0,0,1,0.00261318396287022,],[0,0,0,1,0,0.9374750896764681,],[0,0,0,1,1,0.17103651265768066,],[0,0,1,0,0,0.7743677145548782,],[0,0,1,0,1,0.020847124966988286,],[0,0,1,1,0,0.819605502272574,],[0,0,1,1,1,0.7770696653298705,],[0,1,0,0,0,0.22000020424471117,],[0,1,0,0,1,0.2612822543785632,],[0,1,0,1,0,0.10631184534553613,],[0,1,0,1,1,0.012053266481604857,],[0,1,1,0,0,0.8567036926494931,],[0,1,1,0,1,0.9607152665217826,],[0,1,1,1,0,0.19318190721831383,],[0,1,1,1,1,0.7537171106049837,],[1,0,0,0,0,0.255612305212012,],[1,0,0,0,1,0.19033854764492156,],[1,0,0,1,0,0.17803691153839174,],[1,0,0,1,1,0.445678929351764,],[1,0,1,0,0,0.6146025415343458,],[1,0,1,0,1,0.028922158015186678,],[1,0,1,1,0,0.5616233981183923,],[1,0,1,1,1,0.0779273017309943,],[1,1,0,0,0,0.5131118952916223,],[1,1,0,0,1,0.39526010344941637,],[1,1,0,1,0,0.47123272227568963,],[1,1,0,1,1,0.11684957612419054,],[1,1,1,0,0,0.32393829386069184,],[1,1,1,0,1,0.8146920336251581,],[1,1,1,1,0,0.863742465888231,],[1,1,1,1,1,0.863484719913308,],])
    AG2_F57 = Factor('AG2_F57', [AG2_V57,AG2_V58,AG2_V59,AG2_V60,AG2_V61,])
    AG2_F57.add_values([[0,0,0,0,0,0.11612144361709703,],[0,0,0,0,1,0.3378192274979823,],[0,0,0,1,0,0.2214560041910356,],[0,0,0,1,1,0.18747743212863585,],[0,0,1,0,0,0.5169872590803956,],[0,0,1,0,1,0.5082548893696146,],[0,0,1,1,0,0.6087660280650419,],[0,0,1,1,1,0.10670533885984383,],[0,1,0,0,0,0.07344285803008854,],[0,1,0,0,1,0.6465184891142586,],[0,1,0,1,0,0.036984040513467875,],[0,1,0,1,1,0.23396727877349566,],[0,1,1,0,0,0.44909609766156044,],[0,1,1,0,1,0.04214122991090604,],[0,1,1,1,0,0.4072525653766196,],[0,1,1,1,1,0.553755106925552,],[1,0,0,0,0,0.6925655226974495,],[1,0,0,0,1,0.041286817176133035,],[1,0,0,1,0,0.1699620583099212,],[1,0,0,1,1,0.8353740242661183,],[1,0,1,0,0,0.4227201089784073,],[1,0,1,0,1,0.08016187656426259,],[1,0,1,1,0,0.5353157311597397,],[1,0,1,1,1,0.6675929998419055,],[1,1,0,0,0,0.10873457793589188,],[1,1,0,0,1,0.40665044217812946,],[1,1,0,1,0,0.4756966749981904,],[1,1,0,1,1,0.07122294108544537,],[1,1,1,0,0,0.37181807568980757,],[1,1,1,0,1,0.8972151081779209,],[1,1,1,1,0,0.36561479443966427,],[1,1,1,1,1,0.345098488663278,],])
    AG2_F58 = Factor('AG2_F58', [AG2_V58,AG2_V59,AG2_V60,AG2_V61,AG2_V62,])
    AG2_F58.add_values([[0,0,0,0,0,0.9611714119446237,],[0,0,0,0,1,0.36890969338899643,],[0,0,0,1,0,0.7522036878801932,],[0,0,0,1,1,0.6323550395816442,],[0,0,1,0,0,0.02170239662225241,],[0,0,1,0,1,0.8490558431638622,],[0,0,1,1,0,0.1677873315503823,],[0,0,1,1,1,0.4433055954892994,],[0,1,0,0,0,0.8134227756123159,],[0,1,0,0,1,0.4648591997898289,],[0,1,0,1,0,0.41490421277986395,],[0,1,0,1,1,0.19588986456534568,],[0,1,1,0,0,0.5843714789015888,],[0,1,1,0,1,0.33342801168169145,],[0,1,1,1,0,0.9841252363691225,],[0,1,1,1,1,0.5929585981297439,],[1,0,0,0,0,0.004403967354976843,],[1,0,0,0,1,0.3852215328401256,],[1,0,0,1,0,0.31785655640878174,],[1,0,0,1,1,0.9134510276416282,],[1,0,1,0,0,0.8718822124304236,],[1,0,1,0,1,0.9082348259519049,],[1,0,1,1,0,0.9801695854440988,],[1,0,1,1,1,0.7584586847882079,],[1,1,0,0,0,0.08776693714862364,],[1,1,0,0,1,0.17706084322493132,],[1,1,0,1,0,0.9218679701050442,],[1,1,0,1,1,0.018115863025513806,],[1,1,1,0,0,0.14818461605402736,],[1,1,1,0,1,0.4684091125898367,],[1,1,1,1,0,0.13376986745121536,],[1,1,1,1,1,0.7429295040864444,],])
    AG2_F59 = Factor('AG2_F59', [AG2_V59,AG2_V60,AG2_V61,AG2_V62,AG2_V63,])
    AG2_F59.add_values([[0,0,0,0,0,0.5251978475455947,],[0,0,0,0,1,0.8460016904026122,],[0,0,0,1,0,0.9605889428507852,],[0,0,0,1,1,0.6786682574868559,],[0,0,1,0,0,0.731527958847082,],[0,0,1,0,1,0.7793878333381188,],[0,0,1,1,0,0.17300806070643146,],[0,0,1,1,1,0.37798905867735794,],[0,1,0,0,0,0.15526372408301437,],[0,1,0,0,1,0.4449136390162063,],[0,1,0,1,0,0.8362663008683544,],[0,1,0,1,1,0.43339874854785837,],[0,1,1,0,0,0.71982386260014,],[0,1,1,0,1,0.477259138855468,],[0,1,1,1,0,0.3681444151330082,],[0,1,1,1,1,0.955939048570865,],[1,0,0,0,0,0.5082878629780079,],[1,0,0,0,1,0.7492560651542834,],[1,0,0,1,0,0.5231869272064368,],[1,0,0,1,1,0.054900669072116014,],[1,0,1,0,0,0.09879378543649836,],[1,0,1,0,1,0.1734522701588763,],[1,0,1,1,0,0.41609095756007486,],[1,0,1,1,1,0.537718591659238,],[1,1,0,0,0,0.30405285800693016,],[1,1,0,0,1,0.7858797417073521,],[1,1,0,1,0,0.04452431386092549,],[1,1,0,1,1,0.3245116890342173,],[1,1,1,0,0,0.11124927623902087,],[1,1,1,0,1,0.9747275668528367,],[1,1,1,1,0,0.33966451151253574,],[1,1,1,1,1,0.4194487558322661,],])
    AG2_F60 = Factor('AG2_F60', [AG2_V60,AG2_V61,AG2_V62,AG2_V63,AG2_V64,])
    AG2_F60.add_values([[0,0,0,0,0,0.3188037488885879,],[0,0,0,0,1,0.9984261088949634,],[0,0,0,1,0,0.30543490975103493,],[0,0,0,1,1,0.6023842816447578,],[0,0,1,0,0,0.9259608046194091,],[0,0,1,0,1,0.8735497409138039,],[0,0,1,1,0,0.2923190982613037,],[0,0,1,1,1,0.3727755828505462,],[0,1,0,0,0,0.26732452755003466,],[0,1,0,0,1,0.11572582783500847,],[0,1,0,1,0,0.9236504413369911,],[0,1,0,1,1,0.10472608028133717,],[0,1,1,0,0,0.5426884445150085,],[0,1,1,0,1,0.8849505330631245,],[0,1,1,1,0,0.6342410201264009,],[0,1,1,1,1,0.8639994871137009,],[1,0,0,0,0,0.5390855719316388,],[1,0,0,0,1,0.6732737118101625,],[1,0,0,1,0,0.7151198649214224,],[1,0,0,1,1,0.5564534183058416,],[1,0,1,0,0,0.2509500591976875,],[1,0,1,0,1,0.26207670033022806,],[1,0,1,1,0,0.2568909966983628,],[1,0,1,1,1,0.805404444596042,],[1,1,0,0,0,0.862252191636796,],[1,1,0,0,1,0.2508646710210224,],[1,1,0,1,0,0.9239862407069109,],[1,1,0,1,1,0.7429645195137607,],[1,1,1,0,0,0.7723148801748769,],[1,1,1,0,1,0.5501627512539425,],[1,1,1,1,0,0.542874903691085,],[1,1,1,1,1,0.468522157650484,],])
    AG2_F61 = Factor('AG2_F61', [AG2_V61,AG2_V62,AG2_V63,AG2_V64,AG2_V65,])
    AG2_F61.add_values([[0,0,0,0,0,0.3489369281832818,],[0,0,0,0,1,0.9681754807622599,],[0,0,0,1,0,0.35764956948934373,],[0,0,0,1,1,0.9702710784347898,],[0,0,1,0,0,0.2704111115447567,],[0,0,1,0,1,0.2393384538148271,],[0,0,1,1,0,0.7721706876383262,],[0,0,1,1,1,0.23583165913988716,],[0,1,0,0,0,0.8076001208227793,],[0,1,0,0,1,0.455855708145728,],[0,1,0,1,0,0.006271612243757047,],[0,1,0,1,1,0.08698301820191194,],[0,1,1,0,0,0.11002987473463315,],[0,1,1,0,1,0.32713557469357213,],[0,1,1,1,0,0.7993898889296076,],[0,1,1,1,1,0.1937263169229625,],[1,0,0,0,0,0.5915610881900305,],[1,0,0,0,1,0.4307947410399801,],[1,0,0,1,0,0.3110901801446252,],[1,0,0,1,1,0.5276017651844265,],[1,0,1,0,0,0.5849677100267142,],[1,0,1,0,1,0.37444055895607326,],[1,0,1,1,0,0.8835048652096595,],[1,0,1,1,1,0.7539269307133216,],[1,1,0,0,0,0.1057546144802138,],[1,1,0,0,1,0.9518566912732447,],[1,1,0,1,0,0.867340437521174,],[1,1,0,1,1,0.15281811086715066,],[1,1,1,0,0,0.7044321366209351,],[1,1,1,0,1,0.9588439810921886,],[1,1,1,1,0,0.08205857668461743,],[1,1,1,1,1,0.725751988374002,],])
    AG2_F62 = Factor('AG2_F62', [AG2_V62,AG2_V63,AG2_V64,AG2_V65,AG2_V66,])
    AG2_F62.add_values([[0,0,0,0,0,0.30235994362516977,],[0,0,0,0,1,0.5677251565497837,],[0,0,0,1,0,0.6131633165634817,],[0,0,0,1,1,0.2064477777124202,],[0,0,1,0,0,0.9438063355233448,],[0,0,1,0,1,0.5772241436484542,],[0,0,1,1,0,0.7396851447045,],[0,0,1,1,1,0.12431762491806946,],[0,1,0,0,0,0.3461179814561559,],[0,1,0,0,1,0.12558452630957762,],[0,1,0,1,0,0.12319696063271471,],[0,1,0,1,1,0.42017285405718563,],[0,1,1,0,0,0.9431887921172438,],[0,1,1,0,1,0.0860212351293581,],[0,1,1,1,0,0.6574734456334022,],[0,1,1,1,1,0.36498383156902275,],[1,0,0,0,0,0.5292340334088754,],[1,0,0,0,1,0.31665912409363595,],[1,0,0,1,0,0.31688150055068637,],[1,0,0,1,1,0.214139578834368,],[1,0,1,0,0,0.9259701401292865,],[1,0,1,0,1,0.3435514254330311,],[1,0,1,1,0,0.5077991153525525,],[1,0,1,1,1,0.6714381416549702,],[1,1,0,0,0,0.1457176110625446,],[1,1,0,0,1,0.14857508698440808,],[1,1,0,1,0,0.6005894589752033,],[1,1,0,1,1,0.6915566764286164,],[1,1,1,0,0,0.5004138641090018,],[1,1,1,0,1,0.11024703713973119,],[1,1,1,1,0,0.34696759361028273,],[1,1,1,1,1,0.9962736586184372,],])
    AG2_F63 = Factor('AG2_F63', [AG2_V63,AG2_V64,AG2_V65,AG2_V66,AG2_V67,])
    AG2_F63.add_values([[0,0,0,0,0,0.8110989599367169,],[0,0,0,0,1,0.957467121422055,],[0,0,0,1,0,0.14269243922768401,],[0,0,0,1,1,0.49955325118259675,],[0,0,1,0,0,0.792486037255601,],[0,0,1,0,1,0.5128427606706343,],[0,0,1,1,0,0.3129174757178919,],[0,0,1,1,1,0.5082349810491873,],[0,1,0,0,0,0.28437622529461243,],[0,1,0,0,1,0.05417429213120303,],[0,1,0,1,0,0.4341743872354045,],[0,1,0,1,1,0.25579305452585027,],[0,1,1,0,0,0.47028129605485214,],[0,1,1,0,1,0.4874742696410363,],[0,1,1,1,0,0.10338414902144574,],[0,1,1,1,1,0.18515261673654884,],[1,0,0,0,0,0.6100953963381114,],[1,0,0,0,1,0.8055444814149412,],[1,0,0,1,0,0.8175678147602745,],[1,0,0,1,1,0.3618245526103043,],[1,0,1,0,0,0.5284051221361867,],[1,0,1,0,1,0.5322661503249124,],[1,0,1,1,0,0.5919671150221891,],[1,0,1,1,1,0.2849317005081484,],[1,1,0,0,0,0.9268165137028911,],[1,1,0,0,1,0.9791709207103056,],[1,1,0,1,0,0.5961665321729386,],[1,1,0,1,1,0.22774151423708322,],[1,1,1,0,0,0.3528895503647178,],[1,1,1,0,1,0.44892569212697325,],[1,1,1,1,0,0.36758055146653745,],[1,1,1,1,1,0.6741282968245986,],])
    AG2_F64 = Factor('AG2_F64', [AG2_V64,AG2_V65,AG2_V66,AG2_V67,AG2_V68,])
    AG2_F64.add_values([[0,0,0,0,0,0.7792107195457226,],[0,0,0,0,1,0.5426293744685782,],[0,0,0,1,0,0.40262512258541444,],[0,0,0,1,1,0.7409991157203999,],[0,0,1,0,0,0.5754351182383899,],[0,0,1,0,1,0.3175015901025914,],[0,0,1,1,0,0.11706551666508888,],[0,0,1,1,1,0.9210470132148504,],[0,1,0,0,0,0.7268937633099201,],[0,1,0,0,1,0.3528521192452804,],[0,1,0,1,0,0.4996997478333729,],[0,1,0,1,1,0.40307570596246894,],[0,1,1,0,0,0.7868949401172173,],[0,1,1,0,1,0.7003520118023776,],[0,1,1,1,0,0.047741594765804606,],[0,1,1,1,1,0.867285910301404,],[1,0,0,0,0,0.5209933602981222,],[1,0,0,0,1,0.2808071935098457,],[1,0,0,1,0,0.9283062011485456,],[1,0,0,1,1,0.8916512042009858,],[1,0,1,0,0,0.5440647939308878,],[1,0,1,0,1,0.2984124355516963,],[1,0,1,1,0,0.9754936545508508,],[1,0,1,1,1,0.47961236272970065,],[1,1,0,0,0,0.0995295064257317,],[1,1,0,0,1,0.9611196987653068,],[1,1,0,1,0,0.41676598269934734,],[1,1,0,1,1,0.06456593168442394,],[1,1,1,0,0,0.7348995851563785,],[1,1,1,0,1,0.48248325154991156,],[1,1,1,1,0,0.174484427622336,],[1,1,1,1,1,0.8617178639242035,],])
    AG2_F65 = Factor('AG2_F65', [AG2_V65,AG2_V66,AG2_V67,AG2_V68,AG2_V69,])
    AG2_F65.add_values([[0,0,0,0,0,0.3479974418262959,],[0,0,0,0,1,0.4185399240120532,],[0,0,0,1,0,0.9219794011037357,],[0,0,0,1,1,0.8702598654148475,],[0,0,1,0,0,0.4476711356761053,],[0,0,1,0,1,0.7931365461627524,],[0,0,1,1,0,0.6691541969123235,],[0,0,1,1,1,0.8671812381264663,],[0,1,0,0,0,0.43951599877553554,],[0,1,0,0,1,0.07129615692429137,],[0,1,0,1,0,0.9491036663977461,],[0,1,0,1,1,0.26527520394188625,],[0,1,1,0,0,0.05913946511564859,],[0,1,1,0,1,0.2784897224818554,],[0,1,1,1,0,0.07098209799089313,],[0,1,1,1,1,0.9216107471344681,],[1,0,0,0,0,0.6375243200352912,],[1,0,0,0,1,0.6648919080942894,],[1,0,0,1,0,0.07564176142799087,],[1,0,0,1,1,0.66599752446186,],[1,0,1,0,0,0.4801644272121866,],[1,0,1,0,1,0.9080314227423374,],[1,0,1,1,0,0.9005713150211723,],[1,0,1,1,1,0.6667310653188108,],[1,1,0,0,0,0.8201404809749455,],[1,1,0,0,1,0.31194801411829576,],[1,1,0,1,0,0.4102372243788843,],[1,1,0,1,1,0.7979057811755265,],[1,1,1,0,0,0.7446901482414284,],[1,1,1,0,1,0.7843202214605178,],[1,1,1,1,0,0.27200951116676164,],[1,1,1,1,1,0.8838558407255044,],])
    AG2_F66 = Factor('AG2_F66', [AG2_V66,AG2_V67,AG2_V68,AG2_V69,AG2_V70,])
    AG2_F66.add_values([[0,0,0,0,0,0.9615725225219163,],[0,0,0,0,1,0.8120804697825049,],[0,0,0,1,0,0.6590689404247856,],[0,0,0,1,1,0.8191127245155231,],[0,0,1,0,0,0.06091480918498891,],[0,0,1,0,1,0.03366439219693183,],[0,0,1,1,0,0.9589609996061321,],[0,0,1,1,1,0.23783284252916162,],[0,1,0,0,0,0.290070550356836,],[0,1,0,0,1,0.8904687649760464,],[0,1,0,1,0,0.8535948859925061,],[0,1,0,1,1,0.408141161576238,],[0,1,1,0,0,0.858360558813745,],[0,1,1,0,1,0.5613760192964283,],[0,1,1,1,0,0.9143405870865018,],[0,1,1,1,1,0.10994660992530857,],[1,0,0,0,0,0.7743951916838935,],[1,0,0,0,1,0.27438296942023527,],[1,0,0,1,0,0.25272034679963734,],[1,0,0,1,1,0.5003731922617938,],[1,0,1,0,0,0.7721967254104533,],[1,0,1,0,1,0.14496809935915592,],[1,0,1,1,0,0.7768074315354875,],[1,0,1,1,1,0.35990120094692984,],[1,1,0,0,0,0.49376552137647517,],[1,1,0,0,1,0.3945123601459292,],[1,1,0,1,0,0.4959560907704693,],[1,1,0,1,1,0.5211847210874394,],[1,1,1,0,0,0.004237524292119723,],[1,1,1,0,1,0.029543596463762714,],[1,1,1,1,0,0.45019479286981046,],[1,1,1,1,1,0.5514097213056858,],])
    AG2_F67 = Factor('AG2_F67', [AG2_V67,AG2_V68,AG2_V69,AG2_V70,AG2_V71,])
    AG2_F67.add_values([[0,0,0,0,0,0.9979292073790654,],[0,0,0,0,1,0.512686222123901,],[0,0,0,1,0,0.42134951188881614,],[0,0,0,1,1,0.6465639444193274,],[0,0,1,0,0,0.33294874562234505,],[0,0,1,0,1,0.6366762465169585,],[0,0,1,1,0,0.887672287894617,],[0,0,1,1,1,0.19783681862408528,],[0,1,0,0,0,0.677814287484236,],[0,1,0,0,1,0.34297752476800586,],[0,1,0,1,0,0.9927391994920381,],[0,1,0,1,1,0.010505625043178708,],[0,1,1,0,0,0.8648958774947999,],[0,1,1,0,1,0.9051410198940817,],[0,1,1,1,0,0.6699345679089369,],[0,1,1,1,1,0.49034991984909326,],[1,0,0,0,0,0.1691653605048183,],[1,0,0,0,1,0.060630407997003304,],[1,0,0,1,0,0.8076338625864815,],[1,0,0,1,1,0.4223152558835164,],[1,0,1,0,0,0.33137241347906865,],[1,0,1,0,1,0.6611862724079164,],[1,0,1,1,0,0.6680178247040883,],[1,0,1,1,1,0.43254273287629813,],[1,1,0,0,0,0.5685955408804022,],[1,1,0,0,1,0.8048928799942431,],[1,1,0,1,0,0.9296299705542078,],[1,1,0,1,1,0.23269463513990746,],[1,1,1,0,0,0.5974016486589355,],[1,1,1,0,1,0.551438695983992,],[1,1,1,1,0,0.2845044657857299,],[1,1,1,1,1,0.20421017089261126,],])
    AG2_F68 = Factor('AG2_F68', [AG2_V68,AG2_V69,AG2_V70,AG2_V71,AG2_V72,])
    AG2_F68.add_values([[0,0,0,0,0,0.9700116433147055,],[0,0,0,0,1,0.9500655801953114,],[0,0,0,1,0,0.4581548147818793,],[0,0,0,1,1,0.33878035913436777,],[0,0,1,0,0,0.22745080103214985,],[0,0,1,0,1,0.9897445078532345,],[0,0,1,1,0,0.548798676050156,],[0,0,1,1,1,0.8496890581914354,],[0,1,0,0,0,0.635643298214501,],[0,1,0,0,1,0.40941843746909845,],[0,1,0,1,0,0.7028882872872004,],[0,1,0,1,1,0.5800396690052927,],[0,1,1,0,0,0.15115817520248356,],[0,1,1,0,1,0.18636470248869658,],[0,1,1,1,0,0.5405460379347766,],[0,1,1,1,1,0.40492735189569373,],[1,0,0,0,0,0.41765716538468944,],[1,0,0,0,1,0.5382503439219886,],[1,0,0,1,0,0.6592523400003432,],[1,0,0,1,1,0.3225744111970699,],[1,0,1,0,0,0.9230538858614177,],[1,0,1,0,1,0.0070419662003753354,],[1,0,1,1,0,0.46250503950671545,],[1,0,1,1,1,0.4997007716242714,],[1,1,0,0,0,0.6097706237431227,],[1,1,0,0,1,0.66267733897971,],[1,1,0,1,0,0.14599994548359563,],[1,1,0,1,1,0.8460122592170366,],[1,1,1,0,0,0.43520807983333537,],[1,1,1,0,1,0.2679537003307328,],[1,1,1,1,0,0.2635125997902023,],[1,1,1,1,1,0.053857974257,],])
    AG2_F69 = Factor('AG2_F69', [AG2_V69,AG2_V70,AG2_V71,AG2_V72,AG2_V73,])
    AG2_F69.add_values([[0,0,0,0,0,0.5504817651458729,],[0,0,0,0,1,0.692167449094838,],[0,0,0,1,0,0.3822129327587795,],[0,0,0,1,1,0.5509189698473028,],[0,0,1,0,0,0.6573023115106386,],[0,0,1,0,1,0.5250233543466991,],[0,0,1,1,0,0.004493099406389999,],[0,0,1,1,1,0.5359425399246519,],[0,1,0,0,0,0.145213402780517,],[0,1,0,0,1,0.6800033041565001,],[0,1,0,1,0,0.5586833269947105,],[0,1,0,1,1,0.6370788068321732,],[0,1,1,0,0,0.31974810033540746,],[0,1,1,0,1,0.09206142586284068,],[0,1,1,1,0,0.7372248867485799,],[0,1,1,1,1,0.2512896811720448,],[1,0,0,0,0,0.26860441109547817,],[1,0,0,0,1,0.13931269116656117,],[1,0,0,1,0,0.8298932679559614,],[1,0,0,1,1,0.48640924805986235,],[1,0,1,0,0,0.5503952192092166,],[1,0,1,0,1,0.6940860341744913,],[1,0,1,1,0,0.4992800231461067,],[1,0,1,1,1,0.5753714300713364,],[1,1,0,0,0,0.2867016572823431,],[1,1,0,0,1,0.23346156711956356,],[1,1,0,1,0,0.1480510317489034,],[1,1,0,1,1,0.5723743903300323,],[1,1,1,0,0,0.5815020814111183,],[1,1,1,0,1,0.8436524955664129,],[1,1,1,1,0,0.6727440398679566,],[1,1,1,1,1,0.0935216058932397,],])
    AG2_F70 = Factor('AG2_F70', [AG2_V70,AG2_V71,AG2_V72,AG2_V73,AG2_V74,])
    AG2_F70.add_values([[0,0,0,0,0,0.6668942962552585,],[0,0,0,0,1,0.12332994790101955,],[0,0,0,1,0,0.4603879779097503,],[0,0,0,1,1,0.14213244566399252,],[0,0,1,0,0,0.5259020746411303,],[0,0,1,0,1,0.5927514978976924,],[0,0,1,1,0,0.889441607273969,],[0,0,1,1,1,0.08889809550114877,],[0,1,0,0,0,0.260056059518563,],[0,1,0,0,1,0.5298086753348057,],[0,1,0,1,0,0.9642286814687803,],[0,1,0,1,1,0.4280173264857942,],[0,1,1,0,0,0.6701918819094687,],[0,1,1,0,1,0.003178864567568915,],[0,1,1,1,0,0.693109010845096,],[0,1,1,1,1,0.29100213243157924,],[1,0,0,0,0,0.7446240284244622,],[1,0,0,0,1,0.19836253856439928,],[1,0,0,1,0,0.3963769276334347,],[1,0,0,1,1,0.9951415505335653,],[1,0,1,0,0,0.006085765462210146,],[1,0,1,0,1,0.5859739991768237,],[1,0,1,1,0,0.5846741408247147,],[1,0,1,1,1,0.8401125317724608,],[1,1,0,0,0,0.8851953484450493,],[1,1,0,0,1,0.043164397291400265,],[1,1,0,1,0,0.04956324340584939,],[1,1,0,1,1,0.9207682497708132,],[1,1,1,0,0,0.6605957136655443,],[1,1,1,0,1,0.21360593964970168,],[1,1,1,1,0,0.23602586790460284,],[1,1,1,1,1,0.2999267022404282,],])
    AG2_F71 = Factor('AG2_F71', [AG2_V71,AG2_V72,AG2_V73,AG2_V74,AG2_V75,])
    AG2_F71.add_values([[0,0,0,0,0,0.9533635643737669,],[0,0,0,0,1,0.4149953712062148,],[0,0,0,1,0,0.10236750414049402,],[0,0,0,1,1,0.05271141419026341,],[0,0,1,0,0,0.7627868800597047,],[0,0,1,0,1,0.544289027430153,],[0,0,1,1,0,0.19051304409239048,],[0,0,1,1,1,0.8767405460193767,],[0,1,0,0,0,0.6573698310785918,],[0,1,0,0,1,0.8167495288827172,],[0,1,0,1,0,0.4275405432730424,],[0,1,0,1,1,0.5562972889967406,],[0,1,1,0,0,0.7729040443357694,],[0,1,1,0,1,0.0809970701779762,],[0,1,1,1,0,0.1872537168882393,],[0,1,1,1,1,0.03423785231449075,],[1,0,0,0,0,0.4404594525001756,],[1,0,0,0,1,0.9829439013594495,],[1,0,0,1,0,0.2009281737732613,],[1,0,0,1,1,0.7950535394318105,],[1,0,1,0,0,0.6252870431275924,],[1,0,1,0,1,0.33385061924664433,],[1,0,1,1,0,0.43522001738817717,],[1,0,1,1,1,0.912964293881615,],[1,1,0,0,0,0.8901754293546866,],[1,1,0,0,1,0.23266964057843367,],[1,1,0,1,0,0.5141776499398015,],[1,1,0,1,1,0.6473169049370763,],[1,1,1,0,0,0.6146272446502211,],[1,1,1,0,1,0.8229537998544794,],[1,1,1,1,0,0.6978491697849267,],[1,1,1,1,1,0.35115150462196676,],])
    AG2_F72 = Factor('AG2_F72', [AG2_V72,AG2_V73,AG2_V74,AG2_V75,AG2_V76,])
    AG2_F72.add_values([[0,0,0,0,0,0.28395593004288344,],[0,0,0,0,1,0.8340217372103462,],[0,0,0,1,0,0.4947533033370738,],[0,0,0,1,1,0.707241778451082,],[0,0,1,0,0,0.2919069283371389,],[0,0,1,0,1,0.783486480795483,],[0,0,1,1,0,0.7022515373876118,],[0,0,1,1,1,0.681768928408566,],[0,1,0,0,0,0.14454256437557472,],[0,1,0,0,1,0.4030973427027188,],[0,1,0,1,0,0.4954876586298839,],[0,1,0,1,1,0.9464821276353671,],[0,1,1,0,0,0.2712557205876596,],[0,1,1,0,1,0.1769583434226124,],[0,1,1,1,0,0.6303558354014103,],[0,1,1,1,1,0.21142582364165607,],[1,0,0,0,0,0.4635313595222905,],[1,0,0,0,1,0.9378189909365192,],[1,0,0,1,0,0.6304789392524894,],[1,0,0,1,1,0.3206637039179387,],[1,0,1,0,0,0.8705957119793921,],[1,0,1,0,1,0.4472524927509364,],[1,0,1,1,0,0.19078066349239245,],[1,0,1,1,1,0.5898202658301743,],[1,1,0,0,0,0.22561607752916188,],[1,1,0,0,1,0.19022146023791928,],[1,1,0,1,0,0.18778383424335954,],[1,1,0,1,1,0.9398159547887488,],[1,1,1,0,0,0.606990524235967,],[1,1,1,0,1,0.9618442270714318,],[1,1,1,1,0,0.9180661742507649,],[1,1,1,1,1,0.4123608404635831,],])
    AG2_F73 = Factor('AG2_F73', [AG2_V73,AG2_V74,AG2_V75,AG2_V76,AG2_V77,])
    AG2_F73.add_values([[0,0,0,0,0,0.5184948490320449,],[0,0,0,0,1,0.6030221956569088,],[0,0,0,1,0,0.6528870636442667,],[0,0,0,1,1,0.9318779197640369,],[0,0,1,0,0,0.04473181118925974,],[0,0,1,0,1,0.4033974853891911,],[0,0,1,1,0,0.29145447109492567,],[0,0,1,1,1,0.12958960484717316,],[0,1,0,0,0,0.648119577671865,],[0,1,0,0,1,0.4164471450510656,],[0,1,0,1,0,0.18699833244894876,],[0,1,0,1,1,0.21901968700766541,],[0,1,1,0,0,0.40853633037033715,],[0,1,1,0,1,0.3163491670603541,],[0,1,1,1,0,0.6876846622431636,],[0,1,1,1,1,0.8155540711628345,],[1,0,0,0,0,0.15978133148768595,],[1,0,0,0,1,0.7398643970286175,],[1,0,0,1,0,0.26471512131633657,],[1,0,0,1,1,0.13878613370333448,],[1,0,1,0,0,0.6032738302490905,],[1,0,1,0,1,0.6825135604009099,],[1,0,1,1,0,0.3294947561838158,],[1,0,1,1,1,0.6505369947414489,],[1,1,0,0,0,0.15419545788917766,],[1,1,0,0,1,0.5897032196223361,],[1,1,0,1,0,0.4996815311446905,],[1,1,0,1,1,0.9577938585352279,],[1,1,1,0,0,0.6510149895312177,],[1,1,1,0,1,0.14459143559833412,],[1,1,1,1,0,0.1587634344721275,],[1,1,1,1,1,0.27154704067609664,],])
    AG2_F74 = Factor('AG2_F74', [AG2_V74,AG2_V75,AG2_V76,AG2_V77,AG2_V78,])
    AG2_F74.add_values([[0,0,0,0,0,0.2564840044322679,],[0,0,0,0,1,0.9968047693509914,],[0,0,0,1,0,0.9649901347019756,],[0,0,0,1,1,0.8079457770265215,],[0,0,1,0,0,0.9579931013991781,],[0,0,1,0,1,0.4324938960735138,],[0,0,1,1,0,0.23222761293133704,],[0,0,1,1,1,0.48488538808886206,],[0,1,0,0,0,0.29101044945338167,],[0,1,0,0,1,0.7173377727367982,],[0,1,0,1,0,0.0866126250428351,],[0,1,0,1,1,0.845449852508425,],[0,1,1,0,0,0.40822017802272786,],[0,1,1,0,1,0.26711054948293567,],[0,1,1,1,0,0.970261036401781,],[0,1,1,1,1,0.3649099312369114,],[1,0,0,0,0,0.2647095293768414,],[1,0,0,0,1,0.3844214078684991,],[1,0,0,1,0,0.09716527316556522,],[1,0,0,1,1,0.027958563245787414,],[1,0,1,0,0,0.1718995759871837,],[1,0,1,0,1,0.6559256915184563,],[1,0,1,1,0,0.21732395328949666,],[1,0,1,1,1,0.039736410865111954,],[1,1,0,0,0,0.14325382487197372,],[1,1,0,0,1,0.8608776733056706,],[1,1,0,1,0,0.7173292522131419,],[1,1,0,1,1,0.9811938399235506,],[1,1,1,0,0,0.6913981003854682,],[1,1,1,0,1,0.39884129514076105,],[1,1,1,1,0,0.8682113559241973,],[1,1,1,1,1,0.6563767048557767,],])
    AG2_F75 = Factor('AG2_F75', [AG2_V75,AG2_V76,AG2_V77,AG2_V78,AG2_V79,])
    AG2_F75.add_values([[0,0,0,0,0,0.4945608065953141,],[0,0,0,0,1,0.8453096460949397,],[0,0,0,1,0,0.2372171998651486,],[0,0,0,1,1,0.3453309192503358,],[0,0,1,0,0,0.2332694613578946,],[0,0,1,0,1,0.5277276962370967,],[0,0,1,1,0,0.01655483498741042,],[0,0,1,1,1,0.8697208922276681,],[0,1,0,0,0,0.6919804698866919,],[0,1,0,0,1,0.4050824267404147,],[0,1,0,1,0,0.7613581570775295,],[0,1,0,1,1,0.7351740701944458,],[0,1,1,0,0,0.393856307182889,],[0,1,1,0,1,0.8945839007718102,],[0,1,1,1,0,0.6599727697226725,],[0,1,1,1,1,0.9546168916901564,],[1,0,0,0,0,0.15049650989411686,],[1,0,0,0,1,0.23193610431185469,],[1,0,0,1,0,0.11266057730807415,],[1,0,0,1,1,0.7969567719477478,],[1,0,1,0,0,0.4741189197636761,],[1,0,1,0,1,0.2914230889843015,],[1,0,1,1,0,0.9690897871210599,],[1,0,1,1,1,0.4105317808563715,],[1,1,0,0,0,0.36382650608889017,],[1,1,0,0,1,0.5992693464465165,],[1,1,0,1,0,0.32371190278646894,],[1,1,0,1,1,0.5039035006865181,],[1,1,1,0,0,0.8893895262366575,],[1,1,1,0,1,0.5930493737664106,],[1,1,1,1,0,0.5911398231478856,],[1,1,1,1,1,0.7879187892744686,],])
    AG2_F76 = Factor('AG2_F76', [AG2_V76,AG2_V77,AG2_V78,AG2_V79,AG2_V80,])
    AG2_F76.add_values([[0,0,0,0,0,0.7684097234841712,],[0,0,0,0,1,0.14267088770627742,],[0,0,0,1,0,0.2828119566746656,],[0,0,0,1,1,0.7647890618126482,],[0,0,1,0,0,0.7582481589747417,],[0,0,1,0,1,0.5512626787287688,],[0,0,1,1,0,0.37638693967106523,],[0,0,1,1,1,0.4256867918260612,],[0,1,0,0,0,0.6204578487452713,],[0,1,0,0,1,0.3912016762829076,],[0,1,0,1,0,0.713307387696545,],[0,1,0,1,1,0.30787390291054817,],[0,1,1,0,0,0.06609772678151793,],[0,1,1,0,1,0.5260638587114796,],[0,1,1,1,0,0.8109567542993873,],[0,1,1,1,1,0.14584058230855068,],[1,0,0,0,0,0.31093987520781885,],[1,0,0,0,1,0.2552891721909572,],[1,0,0,1,0,0.15874628848698652,],[1,0,0,1,1,0.31126953771693655,],[1,0,1,0,0,0.05102336858041124,],[1,0,1,0,1,0.9404477759330844,],[1,0,1,1,0,0.7855980668039012,],[1,0,1,1,1,0.7288912680200927,],[1,1,0,0,0,0.8632753806240963,],[1,1,0,0,1,0.8444201123080983,],[1,1,0,1,0,0.17727813834175749,],[1,1,0,1,1,0.9390175828029629,],[1,1,1,0,0,0.8574349361972802,],[1,1,1,0,1,0.44222737670585116,],[1,1,1,1,0,0.04018912863885299,],[1,1,1,1,1,0.2705008848031598,],])
    AG2_F77 = Factor('AG2_F77', [AG2_V77,AG2_V78,AG2_V79,AG2_V80,AG2_V81,])
    AG2_F77.add_values([[0,0,0,0,0,0.15507923884528652,],[0,0,0,0,1,0.8821718237275077,],[0,0,0,1,0,0.26881463201352646,],[0,0,0,1,1,0.9359104992471814,],[0,0,1,0,0,0.737539210238461,],[0,0,1,0,1,0.9747117800449441,],[0,0,1,1,0,0.6352633731548704,],[0,0,1,1,1,0.43225163011739104,],[0,1,0,0,0,0.10988656333050423,],[0,1,0,0,1,0.2595542346734063,],[0,1,0,1,0,0.10390346717151623,],[0,1,0,1,1,0.3277439676642063,],[0,1,1,0,0,0.44414625378954836,],[0,1,1,0,1,0.1298745489279438,],[0,1,1,1,0,0.46981284432965514,],[0,1,1,1,1,0.41206723248830257,],[1,0,0,0,0,0.8480081408369138,],[1,0,0,0,1,0.7295110969782143,],[1,0,0,1,0,0.6433763691966382,],[1,0,0,1,1,0.6287180927900383,],[1,0,1,0,0,0.40724190228268164,],[1,0,1,0,1,0.24808601383402626,],[1,0,1,1,0,0.5433544887003388,],[1,0,1,1,1,0.8562143822884728,],[1,1,0,0,0,0.787542715463319,],[1,1,0,0,1,0.06293056159911403,],[1,1,0,1,0,0.7220820102795394,],[1,1,0,1,1,0.3715997611320786,],[1,1,1,0,0,0.9754164677771977,],[1,1,1,0,1,0.12988719482798777,],[1,1,1,1,0,0.7444522779064544,],[1,1,1,1,1,0.533082525995274,],])
    AG2_F78 = Factor('AG2_F78', [AG2_V78,AG2_V79,AG2_V80,AG2_V81,AG2_V82,])
    AG2_F78.add_values([[0,0,0,0,0,0.3432481109547382,],[0,0,0,0,1,0.2160614372680927,],[0,0,0,1,0,0.41036841478296204,],[0,0,0,1,1,0.46919080972976285,],[0,0,1,0,0,0.8168458545930776,],[0,0,1,0,1,0.613523340543269,],[0,0,1,1,0,0.12922107704061744,],[0,0,1,1,1,0.3966510442490138,],[0,1,0,0,0,0.9364390612471841,],[0,1,0,0,1,0.618910356904493,],[0,1,0,1,0,0.7948691806866559,],[0,1,0,1,1,0.7831836400112084,],[0,1,1,0,0,0.13838916541594432,],[0,1,1,0,1,0.05229459694236517,],[0,1,1,1,0,0.9119828106626976,],[0,1,1,1,1,0.7092094696021943,],[1,0,0,0,0,0.8466986179311655,],[1,0,0,0,1,0.519180285192832,],[1,0,0,1,0,0.11117829248829987,],[1,0,0,1,1,0.35286915753961495,],[1,0,1,0,0,0.893590390483273,],[1,0,1,0,1,0.23945032320452847,],[1,0,1,1,0,0.08568775945801578,],[1,0,1,1,1,0.6557060282323806,],[1,1,0,0,0,0.5118016639485655,],[1,1,0,0,1,0.7943099073373386,],[1,1,0,1,0,0.2358293363283591,],[1,1,0,1,1,0.883433485479315,],[1,1,1,0,0,0.9967486040587271,],[1,1,1,0,1,0.3535913200265612,],[1,1,1,1,0,0.6669907515454855,],[1,1,1,1,1,0.12315321362602508,],])
    AG2_F79 = Factor('AG2_F79', [AG2_V79,AG2_V80,AG2_V81,AG2_V82,AG2_V83,])
    AG2_F79.add_values([[0,0,0,0,0,0.7456946076245703,],[0,0,0,0,1,0.5578902637293883,],[0,0,0,1,0,0.8339375597033055,],[0,0,0,1,1,0.10371686510334953,],[0,0,1,0,0,0.535380328092872,],[0,0,1,0,1,0.7705427594639949,],[0,0,1,1,0,0.1573171515516301,],[0,0,1,1,1,0.23993062511675944,],[0,1,0,0,0,0.8917298997390741,],[0,1,0,0,1,0.457549627256947,],[0,1,0,1,0,0.37358101042698816,],[0,1,0,1,1,0.20844355968476225,],[0,1,1,0,0,0.5491227751775638,],[0,1,1,0,1,0.24462057063319123,],[0,1,1,1,0,0.2563137391220829,],[0,1,1,1,1,0.6646233309314057,],[1,0,0,0,0,0.14830123885055158,],[1,0,0,0,1,0.527716210533895,],[1,0,0,1,0,0.7188040527319989,],[1,0,0,1,1,0.2419765232571707,],[1,0,1,0,0,0.7696065757346553,],[1,0,1,0,1,0.41203545552821014,],[1,0,1,1,0,0.048540145472818805,],[1,0,1,1,1,0.9444335981588727,],[1,1,0,0,0,0.9810735386646164,],[1,1,0,0,1,0.21356373460531977,],[1,1,0,1,0,0.8874788144106119,],[1,1,0,1,1,0.9624102947294424,],[1,1,1,0,0,0.04142247710717592,],[1,1,1,0,1,0.2295606508907754,],[1,1,1,1,0,0.3804626811810297,],[1,1,1,1,1,0.20586398963661995,],])
    AG2_F80 = Factor('AG2_F80', [AG2_V80,AG2_V81,AG2_V82,AG2_V83,AG2_V84,])
    AG2_F80.add_values([[0,0,0,0,0,0.15688587865445497,],[0,0,0,0,1,0.4107032826846197,],[0,0,0,1,0,0.8489037158475006,],[0,0,0,1,1,0.4361678445886294,],[0,0,1,0,0,0.24123956900302168,],[0,0,1,0,1,0.6162919807845305,],[0,0,1,1,0,0.22162872977161976,],[0,0,1,1,1,0.9273939236446993,],[0,1,0,0,0,0.8179830704019223,],[0,1,0,0,1,0.2079407722336194,],[0,1,0,1,0,0.22170267232587157,],[0,1,0,1,1,0.7746286389762724,],[0,1,1,0,0,0.4446667532976077,],[0,1,1,0,1,0.1663623083063559,],[0,1,1,1,0,0.43000809768498405,],[0,1,1,1,1,0.3180806346679152,],[1,0,0,0,0,0.8373942660784974,],[1,0,0,0,1,0.15443872427843378,],[1,0,0,1,0,0.6711981838511414,],[1,0,0,1,1,0.9492573254871456,],[1,0,1,0,0,0.3826375176572765,],[1,0,1,0,1,0.12955932338147044,],[1,0,1,1,0,0.06627449400573852,],[1,0,1,1,1,0.45804974599794857,],[1,1,0,0,0,0.2031500385051404,],[1,1,0,0,1,0.16684840684347763,],[1,1,0,1,0,0.07892317541604688,],[1,1,0,1,1,0.2630152050617947,],[1,1,1,0,0,0.15920689590228415,],[1,1,1,0,1,0.7327666599574162,],[1,1,1,1,0,0.30121248835680225,],[1,1,1,1,1,0.25627578056432615,],])
    AG2_F81 = Factor('AG2_F81', [AG2_V81,AG2_V82,AG2_V83,AG2_V84,AG2_V85,])
    AG2_F81.add_values([[0,0,0,0,0,0.22191151507764414,],[0,0,0,0,1,0.06749990473571453,],[0,0,0,1,0,0.9434869870828805,],[0,0,0,1,1,0.026884322452424458,],[0,0,1,0,0,0.8737333867007874,],[0,0,1,0,1,0.21097975291968885,],[0,0,1,1,0,0.31567020735761697,],[0,0,1,1,1,0.995247104360315,],[0,1,0,0,0,0.8767313622880765,],[0,1,0,0,1,0.21528184627355365,],[0,1,0,1,0,0.8276121479645798,],[0,1,0,1,1,0.5938072988437132,],[0,1,1,0,0,0.8010911564683686,],[0,1,1,0,1,0.8537552837991816,],[0,1,1,1,0,0.6825624301281393,],[0,1,1,1,1,0.9067083041945421,],[1,0,0,0,0,0.5464244668744883,],[1,0,0,0,1,0.6745311267353443,],[1,0,0,1,0,0.8382185511894177,],[1,0,0,1,1,0.7773263793417081,],[1,0,1,0,0,0.48549239302312197,],[1,0,1,0,1,0.18302854200747806,],[1,0,1,1,0,0.72195487240837,],[1,0,1,1,1,0.8327365999760137,],[1,1,0,0,0,0.9759579719270436,],[1,1,0,0,1,0.925292182217131,],[1,1,0,1,0,0.590309736436551,],[1,1,0,1,1,0.04547352049186769,],[1,1,1,0,0,0.17897714950684565,],[1,1,1,0,1,0.7239861514406198,],[1,1,1,1,0,0.6731174116236178,],[1,1,1,1,1,0.7407811168933612,],])
    AG2_F82 = Factor('AG2_F82', [AG2_V82,AG2_V83,AG2_V84,AG2_V85,AG2_V86,])
    AG2_F82.add_values([[0,0,0,0,0,0.10151399154769505,],[0,0,0,0,1,0.22183292800359478,],[0,0,0,1,0,0.2832678804512996,],[0,0,0,1,1,0.24434630248445038,],[0,0,1,0,0,0.1295520391243509,],[0,0,1,0,1,0.7227807291221825,],[0,0,1,1,0,0.8744971090308475,],[0,0,1,1,1,0.6180064507201617,],[0,1,0,0,0,0.7985472719400851,],[0,1,0,0,1,0.05837015549834163,],[0,1,0,1,0,0.870507876553275,],[0,1,0,1,1,0.0397944020729199,],[0,1,1,0,0,0.44398761036172957,],[0,1,1,0,1,0.5226980018017048,],[0,1,1,1,0,0.589505985767165,],[0,1,1,1,1,0.8578968550378779,],[1,0,0,0,0,0.017776321620011835,],[1,0,0,0,1,0.7902429505936146,],[1,0,0,1,0,0.2987876355771602,],[1,0,0,1,1,0.7085302127304937,],[1,0,1,0,0,0.46309711414529325,],[1,0,1,0,1,0.47494513960973617,],[1,0,1,1,0,0.45940542397214124,],[1,0,1,1,1,0.8964868788042969,],[1,1,0,0,0,0.3015335219965852,],[1,1,0,0,1,0.8388137824736319,],[1,1,0,1,0,0.2524088175825727,],[1,1,0,1,1,0.32507371251828354,],[1,1,1,0,0,0.12273057788853071,],[1,1,1,0,1,0.5366405559978829,],[1,1,1,1,0,0.45521691094457706,],[1,1,1,1,1,0.37305778827643143,],])
    AG2_F83 = Factor('AG2_F83', [AG2_V83,AG2_V84,AG2_V85,AG2_V86,AG2_V87,])
    AG2_F83.add_values([[0,0,0,0,0,0.9483822229708931,],[0,0,0,0,1,0.6020791720355495,],[0,0,0,1,0,0.4549738728292092,],[0,0,0,1,1,0.21987218038306958,],[0,0,1,0,0,0.7502271928622899,],[0,0,1,0,1,0.8600441042736184,],[0,0,1,1,0,0.5970150900362782,],[0,0,1,1,1,0.7701866887884072,],[0,1,0,0,0,0.795229588338316,],[0,1,0,0,1,0.13431342165113722,],[0,1,0,1,0,0.7062422151311849,],[0,1,0,1,1,0.9127193711743424,],[0,1,1,0,0,0.3175388391564317,],[0,1,1,0,1,0.2424456846284005,],[0,1,1,1,0,0.5823016499508168,],[0,1,1,1,1,0.5704020420973022,],[1,0,0,0,0,0.12286214502399406,],[1,0,0,0,1,0.909828324004219,],[1,0,0,1,0,0.43915887115670815,],[1,0,0,1,1,0.04764578540056078,],[1,0,1,0,0,0.38576141713940093,],[1,0,1,0,1,0.23154113369915644,],[1,0,1,1,0,0.638022667119056,],[1,0,1,1,1,0.19501180850604652,],[1,1,0,0,0,0.8349631581884053,],[1,1,0,0,1,0.7007750917660767,],[1,1,0,1,0,0.8131610129111707,],[1,1,0,1,1,0.1479772820979458,],[1,1,1,0,0,0.2506396282873417,],[1,1,1,0,1,0.36560400186661296,],[1,1,1,1,0,0.19259788568749583,],[1,1,1,1,1,0.3169018040514442,],])
    AG2_F84 = Factor('AG2_F84', [AG2_V84,AG2_V85,AG2_V86,AG2_V87,AG2_V88,])
    AG2_F84.add_values([[0,0,0,0,0,0.43088982848114454,],[0,0,0,0,1,0.6773494524845037,],[0,0,0,1,0,0.7639543832666785,],[0,0,0,1,1,0.22567594782635086,],[0,0,1,0,0,0.21710581956842281,],[0,0,1,0,1,0.410579265016412,],[0,0,1,1,0,0.06123921181716481,],[0,0,1,1,1,0.9176945695516154,],[0,1,0,0,0,0.661813276198493,],[0,1,0,0,1,0.4210796906839919,],[0,1,0,1,0,0.25535251118202995,],[0,1,0,1,1,0.7290625030520549,],[0,1,1,0,0,0.23509472285062086,],[0,1,1,0,1,0.051834700404547525,],[0,1,1,1,0,0.7718288337389929,],[0,1,1,1,1,0.4691327710184467,],[1,0,0,0,0,0.7610542065485506,],[1,0,0,0,1,0.8490974607643393,],[1,0,0,1,0,0.5920707490932865,],[1,0,0,1,1,0.2743643522434034,],[1,0,1,0,0,0.6021673626044375,],[1,0,1,0,1,0.34312015110635524,],[1,0,1,1,0,0.30291727753468195,],[1,0,1,1,1,0.6805612637871084,],[1,1,0,0,0,0.7639739874680691,],[1,1,0,0,1,0.644748853352022,],[1,1,0,1,0,0.6466714717218476,],[1,1,0,1,1,0.8336965474806642,],[1,1,1,0,0,0.47435204891206084,],[1,1,1,0,1,0.9104804465912093,],[1,1,1,1,0,0.4906585056132018,],[1,1,1,1,1,0.8718691391156631,],])
    AG2_F85 = Factor('AG2_F85', [AG2_V85,AG2_V86,AG2_V87,AG2_V88,AG2_V89,])
    AG2_F85.add_values([[0,0,0,0,0,0.8087752573235941,],[0,0,0,0,1,0.5884999720780598,],[0,0,0,1,0,0.7767482324760667,],[0,0,0,1,1,0.11789072778284602,],[0,0,1,0,0,0.403717688600463,],[0,0,1,0,1,0.6931071001793582,],[0,0,1,1,0,0.9180493477747697,],[0,0,1,1,1,0.2598528291510863,],[0,1,0,0,0,0.3795158280550023,],[0,1,0,0,1,0.9315386355544211,],[0,1,0,1,0,0.6583278780247992,],[0,1,0,1,1,0.29468487057040244,],[0,1,1,0,0,0.4092936439624222,],[0,1,1,0,1,0.5575271628207329,],[0,1,1,1,0,0.5035814911694981,],[0,1,1,1,1,0.9212661401531663,],[1,0,0,0,0,0.13642903390263741,],[1,0,0,0,1,0.15964613767914176,],[1,0,0,1,0,0.715371837875635,],[1,0,0,1,1,0.07507106112602274,],[1,0,1,0,0,0.4186640541084684,],[1,0,1,0,1,0.6193038187368066,],[1,0,1,1,0,0.218208465506045,],[1,0,1,1,1,0.4030500397134186,],[1,1,0,0,0,0.9453817530707739,],[1,1,0,0,1,0.1726304827212056,],[1,1,0,1,0,0.9240709871851097,],[1,1,0,1,1,0.01955672258403329,],[1,1,1,0,0,0.5252282707039674,],[1,1,1,0,1,0.07440787385147286,],[1,1,1,1,0,0.5685357267892952,],[1,1,1,1,1,0.7847235170188106,],])
    AG2_F86 = Factor('AG2_F86', [AG2_V86,AG2_V87,AG2_V88,AG2_V89,AG2_V90,])
    AG2_F86.add_values([[0,0,0,0,0,0.3540659000062646,],[0,0,0,0,1,0.6675566725324352,],[0,0,0,1,0,0.26037354867644885,],[0,0,0,1,1,0.17194480422194602,],[0,0,1,0,0,0.45701189014925486,],[0,0,1,0,1,0.0045623010844498295,],[0,0,1,1,0,0.6954353490052188,],[0,0,1,1,1,0.5490144012674033,],[0,1,0,0,0,0.9850330273174085,],[0,1,0,0,1,0.40937598780042234,],[0,1,0,1,0,0.7149322598369144,],[0,1,0,1,1,0.9713882547233487,],[0,1,1,0,0,0.12969107849275174,],[0,1,1,0,1,0.1341245954733156,],[0,1,1,1,0,0.5637182946779866,],[0,1,1,1,1,0.9368960933315275,],[1,0,0,0,0,0.3762280541682649,],[1,0,0,0,1,0.4718208182565131,],[1,0,0,1,0,0.49214282677004484,],[1,0,0,1,1,0.9853607636397231,],[1,0,1,0,0,0.3438829052794938,],[1,0,1,0,1,0.880424306090303,],[1,0,1,1,0,0.7007944443999168,],[1,0,1,1,1,0.6840865530930758,],[1,1,0,0,0,0.844567457927326,],[1,1,0,0,1,0.1527135319153308,],[1,1,0,1,0,0.14920604869704115,],[1,1,0,1,1,0.6866848833393492,],[1,1,1,0,0,0.7142363968914582,],[1,1,1,0,1,0.6377851032213117,],[1,1,1,1,0,0.5161219142425993,],[1,1,1,1,1,0.145912563020558,],])
    AG2_F87 = Factor('AG2_F87', [AG2_V87,AG2_V88,AG2_V89,AG2_V90,AG2_V91,])
    AG2_F87.add_values([[0,0,0,0,0,0.4092741893972237,],[0,0,0,0,1,0.8529057848586333,],[0,0,0,1,0,0.16539974298774027,],[0,0,0,1,1,0.8426451686339257,],[0,0,1,0,0,0.12936651185217107,],[0,0,1,0,1,0.09562684185813397,],[0,0,1,1,0,0.7456137745968503,],[0,0,1,1,1,0.7848210973832057,],[0,1,0,0,0,0.19929566181423958,],[0,1,0,0,1,0.2627239618169567,],[0,1,0,1,0,0.9620303283169551,],[0,1,0,1,1,0.15625239864675816,],[0,1,1,0,0,0.2635542907611022,],[0,1,1,0,1,0.049820107862859356,],[0,1,1,1,0,0.7063611849842141,],[0,1,1,1,1,0.16592597870811854,],[1,0,0,0,0,0.6234926585984659,],[1,0,0,0,1,0.4217044879493665,],[1,0,0,1,0,0.8189147854746924,],[1,0,0,1,1,0.47181062937130624,],[1,0,1,0,0,0.12634852469485988,],[1,0,1,0,1,0.5795497859810231,],[1,0,1,1,0,0.8757606706210227,],[1,0,1,1,1,0.6197128396465755,],[1,1,0,0,0,0.5034069040646156,],[1,1,0,0,1,0.5520087435121482,],[1,1,0,1,0,0.46307639386296695,],[1,1,0,1,1,0.5490298496784173,],[1,1,1,0,0,0.8898879010949651,],[1,1,1,0,1,0.5576512169189002,],[1,1,1,1,0,0.6947424830148572,],[1,1,1,1,1,0.5910994823919141,],])
    AG2_F88 = Factor('AG2_F88', [AG2_V88,AG2_V89,AG2_V90,AG2_V91,AG2_V92,])
    AG2_F88.add_values([[0,0,0,0,0,0.8731464690911286,],[0,0,0,0,1,0.032356904627661005,],[0,0,0,1,0,0.17821135715808087,],[0,0,0,1,1,0.02043572743149173,],[0,0,1,0,0,0.6320057908386695,],[0,0,1,0,1,0.2964219529161301,],[0,0,1,1,0,0.5758270257386953,],[0,0,1,1,1,0.23970530865729522,],[0,1,0,0,0,0.7006699490637877,],[0,1,0,0,1,0.031729366594165434,],[0,1,0,1,0,0.3285096656019477,],[0,1,0,1,1,0.5935937688989854,],[0,1,1,0,0,0.5815100163700274,],[0,1,1,0,1,0.8142615035042886,],[0,1,1,1,0,0.12832978754177546,],[0,1,1,1,1,0.04038260588748036,],[1,0,0,0,0,0.941635323556359,],[1,0,0,0,1,0.41132970984053807,],[1,0,0,1,0,0.3192905149171876,],[1,0,0,1,1,0.05627472606698941,],[1,0,1,0,0,0.3622368771364853,],[1,0,1,0,1,0.15112674652323616,],[1,0,1,1,0,0.20873268040985407,],[1,0,1,1,1,0.42030204393798687,],[1,1,0,0,0,0.5446634124141417,],[1,1,0,0,1,0.5728499750341685,],[1,1,0,1,0,0.8033297487958415,],[1,1,0,1,1,0.6277757143866157,],[1,1,1,0,0,0.3285216844798856,],[1,1,1,0,1,0.8727185095657312,],[1,1,1,1,0,0.2566990618582888,],[1,1,1,1,1,0.13107910528418085,],])
    AG2_F89 = Factor('AG2_F89', [AG2_V89,AG2_V90,AG2_V91,AG2_V92,AG2_V93,])
    AG2_F89.add_values([[0,0,0,0,0,0.7631865785617743,],[0,0,0,0,1,0.5140461681366654,],[0,0,0,1,0,0.10538932894730733,],[0,0,0,1,1,0.6106744932705807,],[0,0,1,0,0,0.7750145281524206,],[0,0,1,0,1,0.6429806974878427,],[0,0,1,1,0,0.05041544330618413,],[0,0,1,1,1,0.44552232585680585,],[0,1,0,0,0,0.12234519615367091,],[0,1,0,0,1,0.8465478230311388,],[0,1,0,1,0,0.1144921626717198,],[0,1,0,1,1,0.703551106090211,],[0,1,1,0,0,0.6774079060237458,],[0,1,1,0,1,0.8516406650617816,],[0,1,1,1,0,0.399874507933805,],[0,1,1,1,1,0.9685446190529896,],[1,0,0,0,0,0.10253392614734558,],[1,0,0,0,1,0.6610928082152671,],[1,0,0,1,0,0.6555702797278462,],[1,0,0,1,1,0.3165490616771012,],[1,0,1,0,0,0.6185413897328499,],[1,0,1,0,1,0.2444501919990362,],[1,0,1,1,0,0.5538420535174357,],[1,0,1,1,1,0.2856876976749941,],[1,1,0,0,0,0.33456048159489415,],[1,1,0,0,1,0.6066689922298407,],[1,1,0,1,0,0.5146045502464128,],[1,1,0,1,1,0.6465911227897813,],[1,1,1,0,0,0.16613586876453784,],[1,1,1,0,1,0.4732574089603525,],[1,1,1,1,0,0.18264152893576777,],[1,1,1,1,1,0.23544571494168784,],])
    AG2_F90 = Factor('AG2_F90', [AG2_V90,AG2_V91,AG2_V92,AG2_V93,AG2_V94,])
    AG2_F90.add_values([[0,0,0,0,0,0.018442313681754332,],[0,0,0,0,1,0.903910962950423,],[0,0,0,1,0,0.5160007787258045,],[0,0,0,1,1,0.6526906323884739,],[0,0,1,0,0,0.08244948864723414,],[0,0,1,0,1,0.8864846511506395,],[0,0,1,1,0,0.8502083552748039,],[0,0,1,1,1,0.96963843780391,],[0,1,0,0,0,0.14519995285539236,],[0,1,0,0,1,0.25820089066424184,],[0,1,0,1,0,0.4173538879663358,],[0,1,0,1,1,0.26493023600236243,],[0,1,1,0,0,0.8645982958323534,],[0,1,1,0,1,0.8827151282023579,],[0,1,1,1,0,0.22183552672218143,],[0,1,1,1,1,0.5897433489588991,],[1,0,0,0,0,0.3514462706618091,],[1,0,0,0,1,0.9645011081080058,],[1,0,0,1,0,0.300743425187891,],[1,0,0,1,1,0.9387980951043472,],[1,0,1,0,0,0.8711062217712419,],[1,0,1,0,1,0.3846019943686613,],[1,0,1,1,0,0.9166684813257822,],[1,0,1,1,1,0.9546349728868977,],[1,1,0,0,0,0.39902679777567546,],[1,1,0,0,1,0.8571118962013651,],[1,1,0,1,0,0.2838516078117437,],[1,1,0,1,1,0.12283823047639095,],[1,1,1,0,0,0.7913963495287472,],[1,1,1,0,1,0.09168920180048702,],[1,1,1,1,0,0.36826124267454496,],[1,1,1,1,1,0.28896687339696275,],])
    AG2_F91 = Factor('AG2_F91', [AG2_V91,AG2_V92,AG2_V93,AG2_V94,AG2_V95,])
    AG2_F91.add_values([[0,0,0,0,0,0.9155961856735199,],[0,0,0,0,1,0.6402193307893176,],[0,0,0,1,0,0.5280324328335291,],[0,0,0,1,1,0.6836960097253809,],[0,0,1,0,0,0.34671161037821396,],[0,0,1,0,1,0.45376598256410927,],[0,0,1,1,0,0.3326453181155061,],[0,0,1,1,1,0.4299903642556275,],[0,1,0,0,0,0.8100933601506113,],[0,1,0,0,1,0.5967064933866604,],[0,1,0,1,0,0.7520477671670714,],[0,1,0,1,1,0.5583240769142875,],[0,1,1,0,0,0.13349680963214738,],[0,1,1,0,1,0.1529367176079705,],[0,1,1,1,0,0.09156734218173802,],[0,1,1,1,1,0.14977287107622572,],[1,0,0,0,0,0.344014619723868,],[1,0,0,0,1,0.2707746187623683,],[1,0,0,1,0,0.10992803804168332,],[1,0,0,1,1,0.7341550251874972,],[1,0,1,0,0,0.1964626209425088,],[1,0,1,0,1,0.9977576674894616,],[1,0,1,1,0,0.5120308210024409,],[1,0,1,1,1,0.8412737393671363,],[1,1,0,0,0,0.25051678322080745,],[1,1,0,0,1,0.4313361257386563,],[1,1,0,1,0,0.29790354476138786,],[1,1,0,1,1,0.998169692359941,],[1,1,1,0,0,0.31122145584683164,],[1,1,1,0,1,0.047256416759575544,],[1,1,1,1,0,0.8417624344219523,],[1,1,1,1,1,0.6091998895420334,],])
    AG2_F92 = Factor('AG2_F92', [AG2_V92,AG2_V93,AG2_V94,AG2_V95,AG2_V96,])
    AG2_F92.add_values([[0,0,0,0,0,0.9588703602223497,],[0,0,0,0,1,0.5530045451435659,],[0,0,0,1,0,0.37924639089147394,],[0,0,0,1,1,0.879210100583145,],[0,0,1,0,0,0.8371998060643739,],[0,0,1,0,1,0.6414458931536279,],[0,0,1,1,0,0.33711212666480417,],[0,0,1,1,1,0.7505250165962692,],[0,1,0,0,0,0.008059544421409328,],[0,1,0,0,1,0.08371608434745192,],[0,1,0,1,0,0.8264356744704487,],[0,1,0,1,1,0.9314859599443535,],[0,1,1,0,0,0.1360728113074021,],[0,1,1,0,1,0.8540905062453847,],[0,1,1,1,0,0.38343920163495365,],[0,1,1,1,1,0.17815492575980374,],[1,0,0,0,0,0.840519575020431,],[1,0,0,0,1,0.016790243582079215,],[1,0,0,1,0,0.34318483852715315,],[1,0,0,1,1,0.40555379481251774,],[1,0,1,0,0,0.4361032134032552,],[1,0,1,0,1,0.3920184305040128,],[1,0,1,1,0,0.2902704446884804,],[1,0,1,1,1,0.5757915479863537,],[1,1,0,0,0,0.6943149150678726,],[1,1,0,0,1,0.5268094083042388,],[1,1,0,1,0,0.1918833564052864,],[1,1,0,1,1,0.442239005578064,],[1,1,1,0,0,0.9142251536755649,],[1,1,1,0,1,0.21530573294138075,],[1,1,1,1,0,0.1651040429694965,],[1,1,1,1,1,0.4510757840042946,],])
    AG2_F93 = Factor('AG2_F93', [AG2_V93,AG2_V94,AG2_V95,AG2_V96,AG2_V97,])
    AG2_F93.add_values([[0,0,0,0,0,0.6426395966430618,],[0,0,0,0,1,0.64742140002854,],[0,0,0,1,0,0.2390467706400542,],[0,0,0,1,1,0.04929427253742407,],[0,0,1,0,0,0.767136300306485,],[0,0,1,0,1,0.6579711221025253,],[0,0,1,1,0,0.26279440572879204,],[0,0,1,1,1,0.10261566337085283,],[0,1,0,0,0,0.818103425455755,],[0,1,0,0,1,0.8530472473713899,],[0,1,0,1,0,0.9689930351134131,],[0,1,0,1,1,0.04648608192796204,],[0,1,1,0,0,0.418784185827551,],[0,1,1,0,1,0.3135626383861584,],[0,1,1,1,0,0.13486007857916402,],[0,1,1,1,1,0.24484493890648173,],[1,0,0,0,0,0.48137752069601475,],[1,0,0,0,1,0.05924577694084263,],[1,0,0,1,0,0.9928062586016494,],[1,0,0,1,1,0.8978174093883591,],[1,0,1,0,0,0.2271136183869604,],[1,0,1,0,1,0.043612477506748425,],[1,0,1,1,0,0.8638486351322543,],[1,0,1,1,1,0.29677756929185384,],[1,1,0,0,0,0.77980096172553,],[1,1,0,0,1,0.9350142181144079,],[1,1,0,1,0,0.5604726267527838,],[1,1,0,1,1,0.9353776722848455,],[1,1,1,0,0,0.8965261787297922,],[1,1,1,0,1,0.21590545146645304,],[1,1,1,1,0,0.2894358712728006,],[1,1,1,1,1,0.23460895792913203,],])
    AG2_F94 = Factor('AG2_F94', [AG2_V94,AG2_V95,AG2_V96,AG2_V97,AG2_V98,])
    AG2_F94.add_values([[0,0,0,0,0,0.9163438408463851,],[0,0,0,0,1,0.06358914674293736,],[0,0,0,1,0,0.16388228159888232,],[0,0,0,1,1,0.535806618735609,],[0,0,1,0,0,0.3427836819267733,],[0,0,1,0,1,0.38795954067319655,],[0,0,1,1,0,0.3672115834223923,],[0,0,1,1,1,0.5812147423066049,],[0,1,0,0,0,0.44409483408376743,],[0,1,0,0,1,0.37113138715068755,],[0,1,0,1,0,0.9992887195044813,],[0,1,0,1,1,0.9141339113353155,],[0,1,1,0,0,0.30915378119037323,],[0,1,1,0,1,0.2656027607299457,],[0,1,1,1,0,0.8750526624771731,],[0,1,1,1,1,0.06537825571466648,],[1,0,0,0,0,0.7972348991907651,],[1,0,0,0,1,0.5735841287943069,],[1,0,0,1,0,0.527345789688418,],[1,0,0,1,1,0.2798568247766558,],[1,0,1,0,0,0.524231636278023,],[1,0,1,0,1,0.9802556776694725,],[1,0,1,1,0,0.04888408772848689,],[1,0,1,1,1,0.366438649036601,],[1,1,0,0,0,0.7110696705536476,],[1,1,0,0,1,0.10568840194356106,],[1,1,0,1,0,0.5647086571479577,],[1,1,0,1,1,0.22764794521086176,],[1,1,1,0,0,0.17449412999113376,],[1,1,1,0,1,0.501822825470839,],[1,1,1,1,0,0.8925578263780426,],[1,1,1,1,1,0.9005411980501707,],])
    AG2_F95 = Factor('AG2_F95', [AG2_V95,AG2_V96,AG2_V97,AG2_V98,AG2_V99,])
    AG2_F95.add_values([[0,0,0,0,0,0.5417703766030662,],[0,0,0,0,1,0.4702186470790281,],[0,0,0,1,0,0.08839373798775188,],[0,0,0,1,1,0.430698128083238,],[0,0,1,0,0,0.42360559334637765,],[0,0,1,0,1,0.31690000753053477,],[0,0,1,1,0,0.45659360833399504,],[0,0,1,1,1,0.5124990475650134,],[0,1,0,0,0,0.10919503862892098,],[0,1,0,0,1,0.3363793039354642,],[0,1,0,1,0,0.8152950714712156,],[0,1,0,1,1,0.5095023451493181,],[0,1,1,0,0,0.5121957332841366,],[0,1,1,0,1,0.8231529276790004,],[0,1,1,1,0,0.953668954944528,],[0,1,1,1,1,0.741194101371035,],[1,0,0,0,0,0.5249081735153894,],[1,0,0,0,1,0.28921577484298366,],[1,0,0,1,0,0.30904939057436176,],[1,0,0,1,1,0.10179824144332562,],[1,0,1,0,0,0.5857671442871177,],[1,0,1,0,1,0.6635256571184489,],[1,0,1,1,0,0.5250645259933368,],[1,0,1,1,1,0.9725433888467854,],[1,1,0,0,0,0.1597733725090914,],[1,1,0,0,1,0.6372135629382343,],[1,1,0,1,0,0.263220937131411,],[1,1,0,1,1,0.06308479197370015,],[1,1,1,0,0,0.4507250770745805,],[1,1,1,0,1,0.2893505169621444,],[1,1,1,1,0,0.710065000917473,],[1,1,1,1,1,0.06044848153739737,],])
    AG2_bayesnet = BayesianNetwork('Randomly generated net 2',[AG2_V0,AG2_V5,AG2_V10,AG2_V15,AG2_V20,AG2_V25,AG2_V30,AG2_V35,AG2_V40,AG2_V45,AG2_V50,AG2_V55,AG2_V60,AG2_V65,AG2_V70,AG2_V75,AG2_V80,AG2_V85,AG2_V90,AG2_V95,AG2_V1,AG2_V2,AG2_V3,AG2_V4,AG2_V6,AG2_V7,AG2_V8,AG2_V9,AG2_V11,AG2_V12,AG2_V13,AG2_V14,AG2_V16,AG2_V17,AG2_V18,AG2_V19,AG2_V21,AG2_V22,AG2_V23,AG2_V24,AG2_V26,AG2_V27,AG2_V28,AG2_V29,AG2_V31,AG2_V32,AG2_V33,AG2_V34,AG2_V36,AG2_V37,AG2_V38,AG2_V39,AG2_V41,AG2_V42,AG2_V43,AG2_V44,AG2_V46,AG2_V47,AG2_V48,AG2_V49,AG2_V51,AG2_V52,AG2_V53,AG2_V54,AG2_V56,AG2_V57,AG2_V58,AG2_V59,AG2_V61,AG2_V62,AG2_V63,AG2_V64,AG2_V66,AG2_V67,AG2_V68,AG2_V69,AG2_V71,AG2_V72,AG2_V73,AG2_V74,AG2_V76,AG2_V77,AG2_V78,AG2_V79,AG2_V81,AG2_V82,AG2_V83,AG2_V84,AG2_V86,AG2_V87,AG2_V88,AG2_V89,AG2_V91,AG2_V92,AG2_V93,AG2_V94,AG2_V96,AG2_V97,AG2_V98,AG2_V99,],[AG2_F0,AG2_F1,AG2_F2,AG2_F3,AG2_F4,AG2_F5,AG2_F6,AG2_F7,AG2_F8,AG2_F9,AG2_F10,AG2_F11,AG2_F12,AG2_F13,AG2_F14,AG2_F15,AG2_F16,AG2_F17,AG2_F18,AG2_F19,AG2_F20,AG2_F21,AG2_F22,AG2_F23,AG2_F24,AG2_F25,AG2_F26,AG2_F27,AG2_F28,AG2_F29,AG2_F30,AG2_F31,AG2_F32,AG2_F33,AG2_F34,AG2_F35,AG2_F36,AG2_F37,AG2_F38,AG2_F39,AG2_F40,AG2_F41,AG2_F42,AG2_F43,AG2_F44,AG2_F45,AG2_F46,AG2_F47,AG2_F48,AG2_F49,AG2_F50,AG2_F51,AG2_F52,AG2_F53,AG2_F54,AG2_F55,AG2_F56,AG2_F57,AG2_F58,AG2_F59,AG2_F60,AG2_F61,AG2_F62,AG2_F63,AG2_F64,AG2_F65,AG2_F66,AG2_F67,AG2_F68,AG2_F69,AG2_F70,AG2_F71,AG2_F72,AG2_F73,AG2_F74,AG2_F75,AG2_F76,AG2_F77,AG2_F78,AG2_F79,AG2_F80,AG2_F81,AG2_F82,AG2_F83,AG2_F84,AG2_F85,AG2_F86,AG2_F87,AG2_F88,AG2_F89,AG2_F90,AG2_F91,AG2_F92,AG2_F93,AG2_F94,AG2_F95,])
    AG2_test = VETest(AG2_bayesnet,[],AG2_V99,[[0.5301289139648628, 0.4698710860351371]],'Variable Elimination Test (Generated Bayes Net 2)')

    AG3_V0 = Variable('AG3_V0',[0,1])
    AG3_V1 = Variable('AG3_V1',[0,1])
    AG3_V2 = Variable('AG3_V2',[0,1])
    AG3_V3 = Variable('AG3_V3',[0,1])
    AG3_V4 = Variable('AG3_V4',[0,1])
    AG3_V5 = Variable('AG3_V5',[0,1])
    AG3_V6 = Variable('AG3_V6',[0,1])
    AG3_V7 = Variable('AG3_V7',[0,1])
    AG3_V8 = Variable('AG3_V8',[0,1])
    AG3_V9 = Variable('AG3_V9',[0,1])
    AG3_V10 = Variable('AG3_V10',[0,1])
    AG3_V11 = Variable('AG3_V11',[0,1])
    AG3_V12 = Variable('AG3_V12',[0,1])
    AG3_V13 = Variable('AG3_V13',[0,1])
    AG3_V14 = Variable('AG3_V14',[0,1])
    AG3_V15 = Variable('AG3_V15',[0,1])
    AG3_V16 = Variable('AG3_V16',[0,1])
    AG3_V17 = Variable('AG3_V17',[0,1])
    AG3_V18 = Variable('AG3_V18',[0,1])
    AG3_V19 = Variable('AG3_V19',[0,1])
    AG3_F0 = Factor('AG3_F0', [AG3_V3,AG3_V11,AG3_V12,AG3_V14,AG3_V19,])
    AG3_F0.add_values([[0,0,0,0,0,0.15618706858748685,],[0,0,0,0,1,0.8157335647001853,],[0,0,0,1,0,0.8001207155022907,],[0,0,0,1,1,0.17263886942564033,],[0,0,1,0,0,0.14295637999657312,],[0,0,1,0,1,0.5852810699916174,],[0,0,1,1,0,0.6941859653089665,],[0,0,1,1,1,0.6276040163976063,],[0,1,0,0,0,0.5044641379932717,],[0,1,0,0,1,0.8778312825074255,],[0,1,0,1,0,0.7378137931763299,],[0,1,0,1,1,0.5344596208677126,],[0,1,1,0,0,0.10732856699163552,],[0,1,1,0,1,0.055733842280025675,],[0,1,1,1,0,0.46430007458987244,],[0,1,1,1,1,0.34214476747341016,],[1,0,0,0,0,0.26715324430452253,],[1,0,0,0,1,0.527719182054026,],[1,0,0,1,0,0.4322948223521605,],[1,0,0,1,1,0.8054816215472166,],[1,0,1,0,0,0.6708644996780755,],[1,0,1,0,1,0.5521231680015685,],[1,0,1,1,0,0.4344868660646973,],[1,0,1,1,1,0.25200603724732196,],[1,1,0,0,0,0.4020660055536742,],[1,1,0,0,1,0.12051815885787495,],[1,1,0,1,0,0.27638736830929533,],[1,1,0,1,1,0.31019965683801193,],[1,1,1,0,0,0.362612830403326,],[1,1,1,0,1,0.557948465190287,],[1,1,1,1,0,0.053723531652023905,],[1,1,1,1,1,0.6705342439963432,],])
    AG3_F1 = Factor('AG3_F1', [AG3_V4,AG3_V7,AG3_V12,AG3_V15,AG3_V17,AG3_V19,])
    AG3_F1.add_values([[0,0,0,0,0,0,0.5086758909910333,],[0,0,0,0,0,1,0.44173508664895733,],[0,0,0,0,1,0,0.7213043437359774,],[0,0,0,0,1,1,0.8355026374934187,],[0,0,0,1,0,0,0.7502259696834233,],[0,0,0,1,0,1,0.5907860901914687,],[0,0,0,1,1,0,0.520157332735876,],[0,0,0,1,1,1,0.8645782627765877,],[0,0,1,0,0,0,0.7088494632284699,],[0,0,1,0,0,1,0.41969620895672144,],[0,0,1,0,1,0,0.08441621387219368,],[0,0,1,0,1,1,0.5731184883562062,],[0,0,1,1,0,0,0.12580119168025458,],[0,0,1,1,0,1,0.3983672467129382,],[0,0,1,1,1,0,0.9488601835481564,],[0,0,1,1,1,1,0.41334093804441907,],[0,1,0,0,0,0,0.8164996592938478,],[0,1,0,0,0,1,0.20792287307713664,],[0,1,0,0,1,0,0.15967495515536095,],[0,1,0,0,1,1,0.32608974064907975,],[0,1,0,1,0,0,0.9025024370332089,],[0,1,0,1,0,1,0.28705077138384455,],[0,1,0,1,1,0,0.6796143141395152,],[0,1,0,1,1,1,0.6168309820475123,],[0,1,1,0,0,0,0.794583057907475,],[0,1,1,0,0,1,0.25866171693367745,],[0,1,1,0,1,0,0.7509677860675232,],[0,1,1,0,1,1,0.1912512520578007,],[0,1,1,1,0,0,0.20542197749181276,],[0,1,1,1,0,1,0.12420833312957513,],[0,1,1,1,1,0,0.3582230383372722,],[0,1,1,1,1,1,0.7102692138546342,],[1,0,0,0,0,0,0.21973679252679756,],[1,0,0,0,0,1,0.12075238915707966,],[1,0,0,0,1,0,0.728633995481601,],[1,0,0,0,1,1,0.633869606274765,],[1,0,0,1,0,0,0.6177988273608588,],[1,0,0,1,0,1,0.6739910760122028,],[1,0,0,1,1,0,0.4391721119866671,],[1,0,0,1,1,1,0.366999718685686,],[1,0,1,0,0,0,0.5920656409611024,],[1,0,1,0,0,1,0.283302848896838,],[1,0,1,0,1,0,0.8621477314269782,],[1,0,1,0,1,1,0.6658462386873815,],[1,0,1,1,0,0,0.2963091491828492,],[1,0,1,1,0,1,0.37561802623216944,],[1,0,1,1,1,0,0.25272731835350826,],[1,0,1,1,1,1,0.6560312483244884,],[1,1,0,0,0,0,0.009919959119822123,],[1,1,0,0,0,1,0.26644815237030217,],[1,1,0,0,1,0,0.39614802326084586,],[1,1,0,0,1,1,0.8234618847304609,],[1,1,0,1,0,0,0.6487259551808146,],[1,1,0,1,0,1,0.9644235619698993,],[1,1,0,1,1,0,0.024029103843958288,],[1,1,0,1,1,1,0.2511129608621647,],[1,1,1,0,0,0,0.7390924429994238,],[1,1,1,0,0,1,0.5958323191553342,],[1,1,1,0,1,0,0.9472991784098354,],[1,1,1,0,1,1,0.40145135056366327,],[1,1,1,1,0,0,0.3968789552187271,],[1,1,1,1,0,1,0.11488531693171229,],[1,1,1,1,1,0,0.9127145249795185,],[1,1,1,1,1,1,0.38506322960518324,],])
    AG3_F2 = Factor('AG3_F2', [AG3_V17,AG3_V18,])
    AG3_F2.add_values([[0,0,0.41263707106701586,],[0,1,0.38690162579163917,],[1,0,0.6432250145887994,],[1,1,0.5994890251136502,],])
    AG3_F3 = Factor('AG3_F3', [AG3_V1,AG3_V14,])
    AG3_F3.add_values([[0,0,0.8319179791602006,],[0,1,0.3864368536176408,],[1,0,0.08031766953140343,],[1,1,0.11874913711556155,],])
    AG3_F4 = Factor('AG3_F4', [AG3_V1,AG3_V2,AG3_V17,])
    AG3_F4.add_values([[0,0,0,0.5610179010325689,],[0,0,1,0.3865735014248762,],[0,1,0,0.8644131452259775,],[0,1,1,0.8064629876613102,],[1,0,0,0.8533167975509943,],[1,0,1,0.9244321069276931,],[1,1,0,0.7306750405972263,],[1,1,1,0.9899433531394928,],])
    AG3_F5 = Factor('AG3_F5', [AG3_V6,AG3_V7,AG3_V9,AG3_V13,AG3_V17,])
    AG3_F5.add_values([[0,0,0,0,0,0.0916677219923888,],[0,0,0,0,1,0.597021049845587,],[0,0,0,1,0,0.6848232343015082,],[0,0,0,1,1,0.15806119166380198,],[0,0,1,0,0,0.7985061852267913,],[0,0,1,0,1,0.40975920656141146,],[0,0,1,1,0,0.8438489052150596,],[0,0,1,1,1,0.9169119798782804,],[0,1,0,0,0,0.8800578892174292,],[0,1,0,0,1,0.12832669039236227,],[0,1,0,1,0,0.05868733403944142,],[0,1,0,1,1,0.1552179576129688,],[0,1,1,0,0,0.4815428233793061,],[0,1,1,0,1,0.1285747775300347,],[0,1,1,1,0,0.3445139263845011,],[0,1,1,1,1,0.2069065424795375,],[1,0,0,0,0,0.30549356627255314,],[1,0,0,0,1,0.8397550530388213,],[1,0,0,1,0,0.657694208349627,],[1,0,0,1,1,0.24295200877433723,],[1,0,1,0,0,0.3592170100130447,],[1,0,1,0,1,0.29865769573360773,],[1,0,1,1,0,0.2580547658148038,],[1,0,1,1,1,0.5205682591203475,],[1,1,0,0,0,0.1759698079662516,],[1,1,0,0,1,0.8045686499123306,],[1,1,0,1,0,0.6423238804853415,],[1,1,0,1,1,0.35086264634168096,],[1,1,1,0,0,0.3717583275277116,],[1,1,1,0,1,0.32819011136783194,],[1,1,1,1,0,0.3493527856890108,],[1,1,1,1,1,0.38834578164297245,],])
    AG3_F6 = Factor('AG3_F6', [AG3_V0,AG3_V9,AG3_V10,AG3_V15,AG3_V18,])
    AG3_F6.add_values([[0,0,0,0,0,0.44589652805260904,],[0,0,0,0,1,0.6061964048901338,],[0,0,0,1,0,0.28004026811256616,],[0,0,0,1,1,0.6293251871785605,],[0,0,1,0,0,0.43627177321208477,],[0,0,1,0,1,0.7816445583784497,],[0,0,1,1,0,0.6957867208229216,],[0,0,1,1,1,0.8322045120085089,],[0,1,0,0,0,0.8903374580435093,],[0,1,0,0,1,0.053882740352730316,],[0,1,0,1,0,0.9237686608230614,],[0,1,0,1,1,0.08589414919340782,],[0,1,1,0,0,0.329562688176264,],[0,1,1,0,1,0.10900570375162397,],[0,1,1,1,0,0.3464453323559653,],[0,1,1,1,1,0.395179858868545,],[1,0,0,0,0,0.63856992023857,],[1,0,0,0,1,0.9685510659985876,],[1,0,0,1,0,0.09945946153199761,],[1,0,0,1,1,0.05643894108257252,],[1,0,1,0,0,0.4458407394864652,],[1,0,1,0,1,0.19921436138153942,],[1,0,1,1,0,0.9791481375571818,],[1,0,1,1,1,0.015971342747714657,],[1,1,0,0,0,0.2953544891533688,],[1,1,0,0,1,0.098169648266663,],[1,1,0,1,0,0.8750957190212157,],[1,1,0,1,1,0.10673405224934636,],[1,1,1,0,0,0.7181917148592265,],[1,1,1,0,1,0.23895884658100253,],[1,1,1,1,0,0.6122994941148845,],[1,1,1,1,1,0.9581033429399328,],])
    AG3_F7 = Factor('AG3_F7', [AG3_V4,AG3_V5,AG3_V9,AG3_V11,AG3_V14,AG3_V16,])
    AG3_F7.add_values([[0,0,0,0,0,0,0.5229143083434482,],[0,0,0,0,0,1,0.9807022841524805,],[0,0,0,0,1,0,0.6322002240818119,],[0,0,0,0,1,1,0.47472310161583064,],[0,0,0,1,0,0,0.8383624562582107,],[0,0,0,1,0,1,0.1379933669541083,],[0,0,0,1,1,0,0.763686738052948,],[0,0,0,1,1,1,0.6059061713626644,],[0,0,1,0,0,0,0.7831743066647027,],[0,0,1,0,0,1,0.3641631645961789,],[0,0,1,0,1,0,0.845073234357135,],[0,0,1,0,1,1,0.22417536752253883,],[0,0,1,1,0,0,0.9497209813584927,],[0,0,1,1,0,1,0.006890481150926783,],[0,0,1,1,1,0,0.47381624572972714,],[0,0,1,1,1,1,0.9345668343005696,],[0,1,0,0,0,0,0.5046576026550822,],[0,1,0,0,0,1,0.5633476563948293,],[0,1,0,0,1,0,0.3587112776606737,],[0,1,0,0,1,1,0.15557802681400987,],[0,1,0,1,0,0,0.6303178956129288,],[0,1,0,1,0,1,0.34304816619093537,],[0,1,0,1,1,0,0.3995714140262039,],[0,1,0,1,1,1,0.06375255680001649,],[0,1,1,0,0,0,0.5002989153456376,],[0,1,1,0,0,1,0.7701974053243518,],[0,1,1,0,1,0,0.21499932745474087,],[0,1,1,0,1,1,0.25294357456380134,],[0,1,1,1,0,0,0.868438278340633,],[0,1,1,1,0,1,0.34262322744373264,],[0,1,1,1,1,0,0.32172925128832197,],[0,1,1,1,1,1,0.533295622000662,],[1,0,0,0,0,0,0.8513212043539281,],[1,0,0,0,0,1,0.33737743391641645,],[1,0,0,0,1,0,0.7560341361464664,],[1,0,0,0,1,1,0.36140210723151084,],[1,0,0,1,0,0,0.5732516860608563,],[1,0,0,1,0,1,0.9728581869726283,],[1,0,0,1,1,0,0.5743821746003795,],[1,0,0,1,1,1,0.7854873856549286,],[1,0,1,0,0,0,0.9263694833811992,],[1,0,1,0,0,1,0.25912542327694754,],[1,0,1,0,1,0,0.5025769469956047,],[1,0,1,0,1,1,0.2832556148917341,],[1,0,1,1,0,0,0.8800207339233657,],[1,0,1,1,0,1,0.8465419662071175,],[1,0,1,1,1,0,0.3518732232981314,],[1,0,1,1,1,1,0.5427291313329771,],[1,1,0,0,0,0,0.9810585161300058,],[1,1,0,0,0,1,0.34634094285042205,],[1,1,0,0,1,0,0.20393183258943026,],[1,1,0,0,1,1,0.6642009630784633,],[1,1,0,1,0,0,0.8753382671661508,],[1,1,0,1,0,1,0.012933927909996241,],[1,1,0,1,1,0,0.25595446926897175,],[1,1,0,1,1,1,0.5463377743017486,],[1,1,1,0,0,0,0.14673530045456853,],[1,1,1,0,0,1,0.06659346724976604,],[1,1,1,0,1,0,0.7360522898444803,],[1,1,1,0,1,1,0.6277039760245703,],[1,1,1,1,0,0,0.6036837815620231,],[1,1,1,1,0,1,0.39141548262153114,],[1,1,1,1,1,0,0.36884883945260355,],[1,1,1,1,1,1,0.12895563854735742,],])
    AG3_F8 = Factor('AG3_F8', [AG3_V3,AG3_V9,AG3_V12,AG3_V14,])
    AG3_F8.add_values([[0,0,0,0,0.25953916865421417,],[0,0,0,1,0.990742666202685,],[0,0,1,0,0.5459566923541277,],[0,0,1,1,0.3000819380834831,],[0,1,0,0,0.9987983984083837,],[0,1,0,1,0.7135277241613377,],[0,1,1,0,0.2773492221282209,],[0,1,1,1,0.8684296627241135,],[1,0,0,0,0.9770564426479468,],[1,0,0,1,0.8735810183867113,],[1,0,1,0,0.7017996725096918,],[1,0,1,1,0.8364445656542714,],[1,1,0,0,0.19358287321504095,],[1,1,0,1,0.6423981948980874,],[1,1,1,0,0.3769889567342375,],[1,1,1,1,0.7006823799370517,],])
    AG3_F9 = Factor('AG3_F9', [AG3_V1,AG3_V2,AG3_V3,])
    AG3_F9.add_values([[0,0,0,0.24429069360539707,],[0,0,1,0.15747844186591675,],[0,1,0,0.06319871862774476,],[0,1,1,0.8652007308240887,],[1,0,0,0.980056581684394,],[1,0,1,0.6484175589670058,],[1,1,0,0.09712348119853426,],[1,1,1,0.3380985193206385,],])
    AG3_F10 = Factor('AG3_F10', [AG3_V0,AG3_V4,AG3_V14,])
    AG3_F10.add_values([[0,0,0,0.3712838759033828,],[0,0,1,0.802078562603669,],[0,1,0,0.177192567012488,],[0,1,1,0.9630687310231014,],[1,0,0,0.9552226724557844,],[1,0,1,0.8111798616800214,],[1,1,0,0.44753053955109456,],[1,1,1,0.9027594374203565,],])
    AG3_F11 = Factor('AG3_F11', [AG3_V4,AG3_V8,AG3_V9,AG3_V11,AG3_V15,])
    AG3_F11.add_values([[0,0,0,0,0,0.24640491123290623,],[0,0,0,0,1,0.32428469691065076,],[0,0,0,1,0,0.23082664714610884,],[0,0,0,1,1,0.0972067586705743,],[0,0,1,0,0,0.4278897703466411,],[0,0,1,0,1,0.18559845550284892,],[0,0,1,1,0,0.8968844523673299,],[0,0,1,1,1,0.8736083541816236,],[0,1,0,0,0,0.9853013165007541,],[0,1,0,0,1,0.9105224382714829,],[0,1,0,1,0,0.9363498543473103,],[0,1,0,1,1,0.16035043303668606,],[0,1,1,0,0,0.47532538099692584,],[0,1,1,0,1,0.8701931358247402,],[0,1,1,1,0,0.8950549581386781,],[0,1,1,1,1,0.6858887636656243,],[1,0,0,0,0,0.9391072720480841,],[1,0,0,0,1,0.12507067980173714,],[1,0,0,1,0,0.692849307332882,],[1,0,0,1,1,0.35016799357610745,],[1,0,1,0,0,0.05598210479021454,],[1,0,1,0,1,0.9082954950231441,],[1,0,1,1,0,0.28294529803508495,],[1,0,1,1,1,0.7973081126476225,],[1,1,0,0,0,0.178481908641968,],[1,1,0,0,1,0.18343198012309214,],[1,1,0,1,0,0.26977412496042824,],[1,1,0,1,1,0.5890774192542243,],[1,1,1,0,0,0.04818315111534028,],[1,1,1,0,1,0.9706220096661415,],[1,1,1,1,0,0.8596782541545176,],[1,1,1,1,1,0.7606650293786371,],])
    AG3_F12 = Factor('AG3_F12', [AG3_V3,AG3_V6,AG3_V8,AG3_V10,AG3_V12,AG3_V16,])
    AG3_F12.add_values([[0,0,0,0,0,0,0.6968491561866254,],[0,0,0,0,0,1,0.8902571531719161,],[0,0,0,0,1,0,0.3697627111433236,],[0,0,0,0,1,1,0.30993715653146037,],[0,0,0,1,0,0,0.7327261264295659,],[0,0,0,1,0,1,0.29803218605575926,],[0,0,0,1,1,0,0.1699862792764665,],[0,0,0,1,1,1,0.24056341295998157,],[0,0,1,0,0,0,0.4092070625146417,],[0,0,1,0,0,1,0.23419526889977108,],[0,0,1,0,1,0,0.8962294673010769,],[0,0,1,0,1,1,0.44002479403304506,],[0,0,1,1,0,0,0.052608826325030576,],[0,0,1,1,0,1,0.45427592255191135,],[0,0,1,1,1,0,0.6343048495521316,],[0,0,1,1,1,1,0.1516438225006927,],[0,1,0,0,0,0,0.5091086320094843,],[0,1,0,0,0,1,0.2654988100050216,],[0,1,0,0,1,0,0.7017177147903644,],[0,1,0,0,1,1,0.42440626794347264,],[0,1,0,1,0,0,0.3160726242132348,],[0,1,0,1,0,1,0.618828201798214,],[0,1,0,1,1,0,0.6091448962915317,],[0,1,0,1,1,1,0.10182451220777186,],[0,1,1,0,0,0,0.5059276419933492,],[0,1,1,0,0,1,0.40050604840663484,],[0,1,1,0,1,0,0.0994651244480943,],[0,1,1,0,1,1,0.17928471078832176,],[0,1,1,1,0,0,0.9353003439413025,],[0,1,1,1,0,1,0.9072183029484221,],[0,1,1,1,1,0,0.2914183321758573,],[0,1,1,1,1,1,0.04249433362779719,],[1,0,0,0,0,0,0.7009128134720175,],[1,0,0,0,0,1,0.29505392985236895,],[1,0,0,0,1,0,0.07685493168550722,],[1,0,0,0,1,1,0.5830627516155734,],[1,0,0,1,0,0,0.9890049677096083,],[1,0,0,1,0,1,0.4311495623868122,],[1,0,0,1,1,0,0.27951435550378606,],[1,0,0,1,1,1,0.37143949023930445,],[1,0,1,0,0,0,0.482363074340469,],[1,0,1,0,0,1,0.8865076820984027,],[1,0,1,0,1,0,0.2302619565399319,],[1,0,1,0,1,1,0.09624399292269423,],[1,0,1,1,0,0,0.7826149021436855,],[1,0,1,1,0,1,0.25131480849842036,],[1,0,1,1,1,0,0.4938385920264578,],[1,0,1,1,1,1,0.7863381617137091,],[1,1,0,0,0,0,0.8371786240283603,],[1,1,0,0,0,1,0.02309186038609826,],[1,1,0,0,1,0,0.4632558065476492,],[1,1,0,0,1,1,0.045747529747936604,],[1,1,0,1,0,0,0.005395458819823671,],[1,1,0,1,0,1,0.7828584334199502,],[1,1,0,1,1,0,0.6088284095397707,],[1,1,0,1,1,1,0.34197708980844116,],[1,1,1,0,0,0,0.70800405413137,],[1,1,1,0,0,1,0.9023989750228577,],[1,1,1,0,1,0,0.4544227226845722,],[1,1,1,0,1,1,0.27344749223166653,],[1,1,1,1,0,0,0.868427710447671,],[1,1,1,1,0,1,0.5030062832193193,],[1,1,1,1,1,0,0.5015062689760228,],[1,1,1,1,1,1,0.4225691412527372,],])
    AG3_F13 = Factor('AG3_F13', [AG3_V5,AG3_V10,])
    AG3_F13.add_values([[0,0,0.3856115328044098,],[0,1,0.6236339812486856,],[1,0,0.13936662224027602,],[1,1,0.2995674017936685,],])
    AG3_F14 = Factor('AG3_F14', [AG3_V4,AG3_V8,AG3_V12,AG3_V17,])
    AG3_F14.add_values([[0,0,0,0,0.48573448218029996,],[0,0,0,1,0.7575285222754625,],[0,0,1,0,0.10745732554531573,],[0,0,1,1,0.4418451854033669,],[0,1,0,0,0.9103301801129936,],[0,1,0,1,0.43813130928787886,],[0,1,1,0,0.31448939876870574,],[0,1,1,1,0.4896336716803431,],[1,0,0,0,0.31166997336286395,],[1,0,0,1,0.4888067318145096,],[1,0,1,0,0.3730455433862781,],[1,0,1,1,0.7969162458998091,],[1,1,0,0,0.6913945759990696,],[1,1,0,1,0.8241939438682597,],[1,1,1,0,0.14107626317586772,],[1,1,1,1,0.4786101926884602,],])
    AG3_F15 = Factor('AG3_F15', [AG3_V7,AG3_V17,AG3_V19,])
    AG3_F15.add_values([[0,0,0,0.0004993931083813629,],[0,0,1,0.33404319048150877,],[0,1,0,0.8262175358375055,],[0,1,1,0.17973114454525435,],[1,0,0,0.8898410926685318,],[1,0,1,0.9440858129748824,],[1,1,0,0.32119481088041674,],[1,1,1,0.5748297416083077,],])
    AG3_F16 = Factor('AG3_F16', [AG3_V8,AG3_V18,])
    AG3_F16.add_values([[0,0,0.4883837867709023,],[0,1,0.7611789739137813,],[1,0,0.23046311379786377,],[1,1,0.9013948138826341,],])
    AG3_F17 = Factor('AG3_F17', [AG3_V3,AG3_V6,AG3_V15,AG3_V16,AG3_V18,])
    AG3_F17.add_values([[0,0,0,0,0,0.213657865597672,],[0,0,0,0,1,0.6159706877826142,],[0,0,0,1,0,0.4791906629378543,],[0,0,0,1,1,0.40356238563691504,],[0,0,1,0,0,0.041189351752717755,],[0,0,1,0,1,0.8784567303847028,],[0,0,1,1,0,0.7830150460308186,],[0,0,1,1,1,0.6251381335103942,],[0,1,0,0,0,0.002793539322297404,],[0,1,0,0,1,0.6190698399532645,],[0,1,0,1,0,0.3268224555702021,],[0,1,0,1,1,0.1050591171025611,],[0,1,1,0,0,0.22763370023677632,],[0,1,1,0,1,0.1264751640505528,],[0,1,1,1,0,0.30929572210559075,],[0,1,1,1,1,0.9276322267648062,],[1,0,0,0,0,0.2999370032039293,],[1,0,0,0,1,0.5575952930991629,],[1,0,0,1,0,0.9419259534027385,],[1,0,0,1,1,0.4336104008290044,],[1,0,1,0,0,0.024224941042035996,],[1,0,1,0,1,0.10377357512141192,],[1,0,1,1,0,0.20459354304803057,],[1,0,1,1,1,0.6079372643910902,],[1,1,0,0,0,0.48366781313313206,],[1,1,0,0,1,0.06389094578856,],[1,1,0,1,0,0.9930759598926913,],[1,1,0,1,1,0.16854065321956363,],[1,1,1,0,0,0.097701252461685,],[1,1,1,0,1,0.21031879246918628,],[1,1,1,1,0,0.17107695812775656,],[1,1,1,1,1,0.7174444675422545,],])
    AG3_F18 = Factor('AG3_F18', [AG3_V6,AG3_V7,AG3_V10,AG3_V11,])
    AG3_F18.add_values([[0,0,0,0,0.6265623005996375,],[0,0,0,1,0.23109204919903586,],[0,0,1,0,0.6213895290565089,],[0,0,1,1,0.005144965824643726,],[0,1,0,0,0.04118840681333675,],[0,1,0,1,0.11065783503148596,],[0,1,1,0,0.048298165036848986,],[0,1,1,1,0.52496806941373,],[1,0,0,0,0.05037943481338625,],[1,0,0,1,0.08214460900870868,],[1,0,1,0,0.3886316318511111,],[1,0,1,1,0.01937073107003876,],[1,1,0,0,0.8283498587587714,],[1,1,0,1,0.4665672571178727,],[1,1,1,0,0.757276988077624,],[1,1,1,1,0.7480682104226007,],])
    AG3_F19 = Factor('AG3_F19', [AG3_V9,AG3_V14,AG3_V16,AG3_V17,])
    AG3_F19.add_values([[0,0,0,0,0.40324733600048934,],[0,0,0,1,0.9378012736322108,],[0,0,1,0,0.7317573218987294,],[0,0,1,1,0.036351205387303694,],[0,1,0,0,0.13981219856477456,],[0,1,0,1,0.4853520596453343,],[0,1,1,0,0.9138022862125355,],[0,1,1,1,0.14274760194305827,],[1,0,0,0,0.5212228994491346,],[1,0,0,1,0.6482140918267127,],[1,0,1,0,0.05816519713653071,],[1,0,1,1,0.10956224551939206,],[1,1,0,0,0.5120363160435575,],[1,1,0,1,0.26112969560425175,],[1,1,1,0,0.4754886860781171,],[1,1,1,1,0.17727382293454158,],])
    AG3_F20 = Factor('AG3_F20', [AG3_V0,AG3_V13,AG3_V14,AG3_V15,AG3_V16,])
    AG3_F20.add_values([[0,0,0,0,0,0.8323753452958619,],[0,0,0,0,1,0.8443917693451308,],[0,0,0,1,0,0.893213217263589,],[0,0,0,1,1,0.8683706537659748,],[0,0,1,0,0,0.6903660264330013,],[0,0,1,0,1,0.24335203634391817,],[0,0,1,1,0,0.28900073856031433,],[0,0,1,1,1,0.302661203440993,],[0,1,0,0,0,0.8372077946871871,],[0,1,0,0,1,0.6465418310084816,],[0,1,0,1,0,0.7115098572403449,],[0,1,0,1,1,0.237619796111736,],[0,1,1,0,0,0.08142050572148693,],[0,1,1,0,1,0.6432188844610619,],[0,1,1,1,0,0.9596869773490595,],[0,1,1,1,1,0.7978726480662247,],[1,0,0,0,0,0.680536359072989,],[1,0,0,0,1,0.3171976151431721,],[1,0,0,1,0,0.1606435964080549,],[1,0,0,1,1,0.7003894426786894,],[1,0,1,0,0,0.08853046934961392,],[1,0,1,0,1,0.3028781525273613,],[1,0,1,1,0,0.8098272397633098,],[1,0,1,1,1,0.7284197451468413,],[1,1,0,0,0,0.979962324027145,],[1,1,0,0,1,0.5236670186429493,],[1,1,0,1,0,0.8639062010580575,],[1,1,0,1,1,0.41281731505663516,],[1,1,1,0,0,0.1826814619993525,],[1,1,1,0,1,0.9144422736808155,],[1,1,1,1,0,0.1767423669815766,],[1,1,1,1,1,0.1446877887136553,],])
    AG3_F21 = Factor('AG3_F21', [AG3_V5,AG3_V17,AG3_V18,])
    AG3_F21.add_values([[0,0,0,0.5764774356186924,],[0,0,1,0.3608545059255544,],[0,1,0,0.4648776144319554,],[0,1,1,0.097323665573267,],[1,0,0,0.6158283663978968,],[1,0,1,0.8233972028125837,],[1,1,0,0.7418227077728771,],[1,1,1,0.8019993140099272,],])
    AG3_F22 = Factor('AG3_F22', [AG3_V11,AG3_V19,])
    AG3_F22.add_values([[0,0,0.47782026675543227,],[0,1,0.669345216869325,],[1,0,0.13257038388189543,],[1,1,0.2596404652546633,],])
    AG3_F23 = Factor('AG3_F23', [AG3_V0,AG3_V3,AG3_V5,AG3_V9,AG3_V13,])
    AG3_F23.add_values([[0,0,0,0,0,0.14669137030600068,],[0,0,0,0,1,0.7577405856185123,],[0,0,0,1,0,0.011281373019102824,],[0,0,0,1,1,0.5069405137299701,],[0,0,1,0,0,0.31688546712826343,],[0,0,1,0,1,0.48633486779932855,],[0,0,1,1,0,0.5195257713720566,],[0,0,1,1,1,0.9597198363584952,],[0,1,0,0,0,0.25097363316759475,],[0,1,0,0,1,0.9916381661717135,],[0,1,0,1,0,0.8157445298870111,],[0,1,0,1,1,0.19020966996905975,],[0,1,1,0,0,0.14252411450459238,],[0,1,1,0,1,0.8745575662345707,],[0,1,1,1,0,0.0416786586068582,],[0,1,1,1,1,0.26835894629333545,],[1,0,0,0,0,0.07538289173932895,],[1,0,0,0,1,0.3971111056808401,],[1,0,0,1,0,0.1138722188057738,],[1,0,0,1,1,0.5753673703445239,],[1,0,1,0,0,0.9976051024957746,],[1,0,1,0,1,0.6821212300367414,],[1,0,1,1,0,0.6552934454232665,],[1,0,1,1,1,0.22730391094587266,],[1,1,0,0,0,0.1105865631596776,],[1,1,0,0,1,0.6215011957019603,],[1,1,0,1,0,0.3146241614231693,],[1,1,0,1,1,0.7845427848099038,],[1,1,1,0,0,0.4600621093555143,],[1,1,1,0,1,0.8362886079118246,],[1,1,1,1,0,0.2031088400069433,],[1,1,1,1,1,0.33813488128920316,],])
    AG3_F24 = Factor('AG3_F24', [AG3_V2,AG3_V5,AG3_V9,AG3_V17,AG3_V18,])
    AG3_F24.add_values([[0,0,0,0,0,0.09544750207235861,],[0,0,0,0,1,0.27010217926038615,],[0,0,0,1,0,0.9406493324756547,],[0,0,0,1,1,0.6976244379693263,],[0,0,1,0,0,0.2558183182709971,],[0,0,1,0,1,0.5274428765915924,],[0,0,1,1,0,0.8369769400349322,],[0,0,1,1,1,0.6753647443496767,],[0,1,0,0,0,0.17266050212994655,],[0,1,0,0,1,0.9739014920524182,],[0,1,0,1,0,0.020344603404861626,],[0,1,0,1,1,0.11559658722872775,],[0,1,1,0,0,0.6587384629949423,],[0,1,1,0,1,0.5148914762206329,],[0,1,1,1,0,0.8144636402915606,],[0,1,1,1,1,0.8606854587888346,],[1,0,0,0,0,0.3814097263258822,],[1,0,0,0,1,0.1292884025173699,],[1,0,0,1,0,0.5851506617934727,],[1,0,0,1,1,0.34014341265105574,],[1,0,1,0,0,0.388534430927131,],[1,0,1,0,1,0.756218906503372,],[1,0,1,1,0,0.9346181974298438,],[1,0,1,1,1,0.1160996566341764,],[1,1,0,0,0,0.7533212671202008,],[1,1,0,0,1,0.035844777029884645,],[1,1,0,1,0,0.5609024641002641,],[1,1,0,1,1,0.3244228504963639,],[1,1,1,0,0,0.039551518561607824,],[1,1,1,0,1,0.9726292071268311,],[1,1,1,1,0,0.04719725576048549,],[1,1,1,1,1,0.6948704785723062,],])
    AG3_F25 = Factor('AG3_F25', [AG3_V1,AG3_V10,AG3_V11,AG3_V19,])
    AG3_F25.add_values([[0,0,0,0,0.6014074569725633,],[0,0,0,1,0.5436578673678516,],[0,0,1,0,0.1781241952167736,],[0,0,1,1,0.6245614170488035,],[0,1,0,0,0.8184719489727241,],[0,1,0,1,0.20706383940198803,],[0,1,1,0,0.22644074552825375,],[0,1,1,1,0.5835494673461763,],[1,0,0,0,0.39216990637167415,],[1,0,0,1,0.7458001091076333,],[1,0,1,0,0.5440204135523513,],[1,0,1,1,0.7606686083375221,],[1,1,0,0,0.8419558411681176,],[1,1,0,1,0.8303266007791265,],[1,1,1,0,0.22798045733279615,],[1,1,1,1,0.48048245377467036,],])
    AG3_F26 = Factor('AG3_F26', [AG3_V1,AG3_V6,AG3_V7,AG3_V12,AG3_V15,AG3_V17,])
    AG3_F26.add_values([[0,0,0,0,0,0,0.43983127569354613,],[0,0,0,0,0,1,0.6058411428999081,],[0,0,0,0,1,0,0.10895348757175152,],[0,0,0,0,1,1,0.6967165147474835,],[0,0,0,1,0,0,0.18494438589505632,],[0,0,0,1,0,1,0.4404202361253759,],[0,0,0,1,1,0,0.1714522449162964,],[0,0,0,1,1,1,0.18091906427469476,],[0,0,1,0,0,0,0.5077298754152472,],[0,0,1,0,0,1,0.8410847960230199,],[0,0,1,0,1,0,0.4997117547605379,],[0,0,1,0,1,1,0.45122926320985957,],[0,0,1,1,0,0,0.5243111114526247,],[0,0,1,1,0,1,0.6533771402223348,],[0,0,1,1,1,0,0.21727068343688333,],[0,0,1,1,1,1,0.7816621831726474,],[0,1,0,0,0,0,0.299326329944624,],[0,1,0,0,0,1,0.6233011273327814,],[0,1,0,0,1,0,0.5567541840818939,],[0,1,0,0,1,1,0.04378008145817657,],[0,1,0,1,0,0,0.09269371610875965,],[0,1,0,1,0,1,0.6556944139054195,],[0,1,0,1,1,0,0.15383378568880482,],[0,1,0,1,1,1,0.6651622222758987,],[0,1,1,0,0,0,0.8047595617242856,],[0,1,1,0,0,1,0.3768198637952649,],[0,1,1,0,1,0,0.28510555085804373,],[0,1,1,0,1,1,0.3929228750748476,],[0,1,1,1,0,0,0.8625611376066086,],[0,1,1,1,0,1,0.8809863258234628,],[0,1,1,1,1,0,0.35682926461336373,],[0,1,1,1,1,1,0.1962749334676874,],[1,0,0,0,0,0,0.915008547746157,],[1,0,0,0,0,1,0.4098200115602587,],[1,0,0,0,1,0,0.6469255480254389,],[1,0,0,0,1,1,0.2969015335146831,],[1,0,0,1,0,0,0.8626320799661192,],[1,0,0,1,0,1,0.556087480311011,],[1,0,0,1,1,0,0.5753572187026985,],[1,0,0,1,1,1,0.26086682309571885,],[1,0,1,0,0,0,0.8745930067458404,],[1,0,1,0,0,1,0.7793955540325584,],[1,0,1,0,1,0,0.41603760269307316,],[1,0,1,0,1,1,0.6998656247426553,],[1,0,1,1,0,0,0.2800161931435794,],[1,0,1,1,0,1,0.011880761954560549,],[1,0,1,1,1,0,0.08877937793153633,],[1,0,1,1,1,1,0.12498718847343565,],[1,1,0,0,0,0,0.8542224260378777,],[1,1,0,0,0,1,0.4859754682192499,],[1,1,0,0,1,0,0.321309094342229,],[1,1,0,0,1,1,0.032786905768955696,],[1,1,0,1,0,0,0.13121861868682616,],[1,1,0,1,0,1,0.26274152975355697,],[1,1,0,1,1,0,0.5934903557456918,],[1,1,0,1,1,1,0.46847054608053557,],[1,1,1,0,0,0,0.7158828430569442,],[1,1,1,0,0,1,0.034272852082199524,],[1,1,1,0,1,0,0.7279656629795116,],[1,1,1,0,1,1,0.24063516133539642,],[1,1,1,1,0,0,0.9734359649155256,],[1,1,1,1,0,1,0.11188998365338407,],[1,1,1,1,1,0,0.6359742496167493,],[1,1,1,1,1,1,0.8134178132830773,],])
    AG3_F27 = Factor('AG3_F27', [AG3_V1,AG3_V5,AG3_V15,AG3_V17,])
    AG3_F27.add_values([[0,0,0,0,0.6623583642809693,],[0,0,0,1,0.613743462984614,],[0,0,1,0,0.5111906084197477,],[0,0,1,1,0.9140792693918212,],[0,1,0,0,0.40275209736025636,],[0,1,0,1,0.8832005147393914,],[0,1,1,0,0.03860467704193639,],[0,1,1,1,0.3785549215399321,],[1,0,0,0,0.8927342457378871,],[1,0,0,1,0.5687158145943807,],[1,0,1,0,0.8529903291051063,],[1,0,1,1,0.7410145849999262,],[1,1,0,0,0.7044969588112155,],[1,1,0,1,0.2690198180289393,],[1,1,1,0,0.4349181271155801,],[1,1,1,1,0.4577296227257387,],])
    AG3_F28 = Factor('AG3_F28', [AG3_V2,AG3_V3,AG3_V12,AG3_V17,AG3_V18,])
    AG3_F28.add_values([[0,0,0,0,0,0.2953186370542793,],[0,0,0,0,1,0.767938977658579,],[0,0,0,1,0,0.4969972813080395,],[0,0,0,1,1,0.5677218507868145,],[0,0,1,0,0,0.6810294446201098,],[0,0,1,0,1,0.8157452429594003,],[0,0,1,1,0,0.4734519516729623,],[0,0,1,1,1,0.49004483640040314,],[0,1,0,0,0,0.09356223700248889,],[0,1,0,0,1,0.6985558979400168,],[0,1,0,1,0,0.3785717164751971,],[0,1,0,1,1,0.3826652492264629,],[0,1,1,0,0,0.11095606410348118,],[0,1,1,0,1,0.21985599290362995,],[0,1,1,1,0,0.6651363522043164,],[0,1,1,1,1,0.18838353126616508,],[1,0,0,0,0,0.9304039113365087,],[1,0,0,0,1,0.9614640221896064,],[1,0,0,1,0,0.6640909187506188,],[1,0,0,1,1,0.9501849205808781,],[1,0,1,0,0,0.5635007345993783,],[1,0,1,0,1,0.5079885765762819,],[1,0,1,1,0,0.16134697550184657,],[1,0,1,1,1,0.7839485600292206,],[1,1,0,0,0,0.7863530659414836,],[1,1,0,0,1,0.4408806809566942,],[1,1,0,1,0,0.00788031381530646,],[1,1,0,1,1,0.00011720260120082076,],[1,1,1,0,0,0.35972411551500416,],[1,1,1,0,1,0.9478747095620947,],[1,1,1,1,0,0.5953987686416842,],[1,1,1,1,1,0.8992661190403619,],])
    AG3_F29 = Factor('AG3_F29', [AG3_V3,AG3_V4,AG3_V15,AG3_V16,])
    AG3_F29.add_values([[0,0,0,0,0.671785583093295,],[0,0,0,1,0.3230227713358874,],[0,0,1,0,0.6564859711747356,],[0,0,1,1,0.5875252193102481,],[0,1,0,0,0.4314328124733669,],[0,1,0,1,0.6313977309065721,],[0,1,1,0,0.5962465164862515,],[0,1,1,1,0.781879413149538,],[1,0,0,0,0.3976092352778057,],[1,0,0,1,0.8832186434247973,],[1,0,1,0,0.06861408031947698,],[1,0,1,1,0.5688389023490688,],[1,1,0,0,0.5807069093628165,],[1,1,0,1,0.26993127212828777,],[1,1,1,0,0.2988487105278733,],[1,1,1,1,0.5668399201350721,],])
    AG3_F30 = Factor('AG3_F30', [AG3_V3,AG3_V4,])
    AG3_F30.add_values([[0,0,0.7987172813714508,],[0,1,0.6959399314000033,],[1,0,0.7312477140128676,],[1,1,0.2912685673482646,],])
    AG3_F31 = Factor('AG3_F31', [AG3_V1,AG3_V2,AG3_V9,])
    AG3_F31.add_values([[0,0,0,0.8131925790336401,],[0,0,1,0.15833979323237296,],[0,1,0,0.6118846614469649,],[0,1,1,0.37012653512150956,],[1,0,0,0.9573204264054374,],[1,0,1,0.380756674949478,],[1,1,0,0.3748556335170944,],[1,1,1,0.5426638314374042,],])
    AG3_F32 = Factor('AG3_F32', [AG3_V4,AG3_V5,AG3_V15,])
    AG3_F32.add_values([[0,0,0,0.33004178797137557,],[0,0,1,0.04888029861903228,],[0,1,0,0.9006265557796593,],[0,1,1,0.12416640400867386,],[1,0,0,0.6025103268568468,],[1,0,1,0.7738005660581281,],[1,1,0,0.3291881832959192,],[1,1,1,0.7436087430330796,],])
    AG3_F33 = Factor('AG3_F33', [AG3_V3,AG3_V5,AG3_V8,])
    AG3_F33.add_values([[0,0,0,0.6304615706085398,],[0,0,1,0.6621651871086411,],[0,1,0,0.7943367476881235,],[0,1,1,0.7221573991117836,],[1,0,0,0.09845419993928296,],[1,0,1,0.23182082975996834,],[1,1,0,0.8204217669661769,],[1,1,1,0.28362015958031384,],])
    AG3_F34 = Factor('AG3_F34', [AG3_V0,AG3_V4,AG3_V8,AG3_V9,AG3_V10,AG3_V12,])
    AG3_F34.add_values([[0,0,0,0,0,0,0.694686968990156,],[0,0,0,0,0,1,0.803594269445681,],[0,0,0,0,1,0,0.3088860002082987,],[0,0,0,0,1,1,0.6972357106416088,],[0,0,0,1,0,0,0.45148379910899383,],[0,0,0,1,0,1,0.9101447157999822,],[0,0,0,1,1,0,0.7626664973508462,],[0,0,0,1,1,1,0.9053331135214806,],[0,0,1,0,0,0,0.8179724882010957,],[0,0,1,0,0,1,0.629302969054441,],[0,0,1,0,1,0,0.3440455450520389,],[0,0,1,0,1,1,0.913601884907785,],[0,0,1,1,0,0,0.5177828369118658,],[0,0,1,1,0,1,0.567144024105325,],[0,0,1,1,1,0,0.35645191866375137,],[0,0,1,1,1,1,0.5613653330553585,],[0,1,0,0,0,0,0.4167956092681657,],[0,1,0,0,0,1,0.5749180712241116,],[0,1,0,0,1,0,0.35676896317405377,],[0,1,0,0,1,1,0.6969651616710709,],[0,1,0,1,0,0,0.4797134011833888,],[0,1,0,1,0,1,0.9103494842018884,],[0,1,0,1,1,0,0.47979964103317857,],[0,1,0,1,1,1,0.44526119044174256,],[0,1,1,0,0,0,0.8273998966350713,],[0,1,1,0,0,1,0.9223429316822334,],[0,1,1,0,1,0,0.541267737040701,],[0,1,1,0,1,1,0.8793561544380611,],[0,1,1,1,0,0,0.8538972489069951,],[0,1,1,1,0,1,0.5262463457732507,],[0,1,1,1,1,0,0.47846873718423577,],[0,1,1,1,1,1,0.5746398163565474,],[1,0,0,0,0,0,0.2921397316738257,],[1,0,0,0,0,1,0.4144234642138387,],[1,0,0,0,1,0,0.3101125171449372,],[1,0,0,0,1,1,0.12122329021842679,],[1,0,0,1,0,0,0.6339521257039131,],[1,0,0,1,0,1,0.029325937815574243,],[1,0,0,1,1,0,0.37588260109970945,],[1,0,0,1,1,1,0.11981451512383848,],[1,0,1,0,0,0,0.7752028090376384,],[1,0,1,0,0,1,0.6643057998787435,],[1,0,1,0,1,0,0.4100781979812314,],[1,0,1,0,1,1,0.7424463492701456,],[1,0,1,1,0,0,0.6426096353390955,],[1,0,1,1,0,1,0.973879463047461,],[1,0,1,1,1,0,0.08528054125981273,],[1,0,1,1,1,1,0.5002093482351763,],[1,1,0,0,0,0,0.1125491395673005,],[1,1,0,0,0,1,0.7256336046927594,],[1,1,0,0,1,0,0.46893822516244704,],[1,1,0,0,1,1,0.08041527164986596,],[1,1,0,1,0,0,0.9358139039044574,],[1,1,0,1,0,1,0.4030698341811933,],[1,1,0,1,1,0,0.715591114889219,],[1,1,0,1,1,1,0.8112425678467278,],[1,1,1,0,0,0,0.1013981122555333,],[1,1,1,0,0,1,0.25334550687503116,],[1,1,1,0,1,0,0.8330540317519374,],[1,1,1,0,1,1,0.3918698965104293,],[1,1,1,1,0,0,0.6249371760944162,],[1,1,1,1,0,1,0.0005756625562374751,],[1,1,1,1,1,0,0.3670062393590319,],[1,1,1,1,1,1,0.2921950841885545,],])
    AG3_F35 = Factor('AG3_F35', [AG3_V3,AG3_V4,AG3_V6,AG3_V8,AG3_V14,])
    AG3_F35.add_values([[0,0,0,0,0,0.22681543473907917,],[0,0,0,0,1,0.6661581983360718,],[0,0,0,1,0,0.0041545862773760475,],[0,0,0,1,1,0.13533655157226865,],[0,0,1,0,0,0.3311935790648547,],[0,0,1,0,1,0.19583205452137753,],[0,0,1,1,0,0.3438418157972612,],[0,0,1,1,1,0.2451627282119818,],[0,1,0,0,0,0.361853946319148,],[0,1,0,0,1,0.5636520602828884,],[0,1,0,1,0,0.3537694513438478,],[0,1,0,1,1,0.5741966256707749,],[0,1,1,0,0,0.4760991574742299,],[0,1,1,0,1,0.8033539907766276,],[0,1,1,1,0,0.12037255020634349,],[0,1,1,1,1,0.8638159741738372,],[1,0,0,0,0,0.7107497653169446,],[1,0,0,0,1,0.8928513736743534,],[1,0,0,1,0,0.9781598043947453,],[1,0,0,1,1,0.8207380827486457,],[1,0,1,0,0,0.05584005433041993,],[1,0,1,0,1,0.40351329864949914,],[1,0,1,1,0,0.2769423215986153,],[1,0,1,1,1,0.535811723420609,],[1,1,0,0,0,0.41270466339914924,],[1,1,0,0,1,0.4098271779911095,],[1,1,0,1,0,0.28817454822470684,],[1,1,0,1,1,0.9805493140330087,],[1,1,1,0,0,0.1582131678237082,],[1,1,1,0,1,0.11713380551959457,],[1,1,1,1,0,0.3000167659434779,],[1,1,1,1,1,0.15615666794933003,],])
    AG3_F36 = Factor('AG3_F36', [AG3_V9,AG3_V10,])
    AG3_F36.add_values([[0,0,0.7939237491587431,],[0,1,0.21603304708113283,],[1,0,0.7428875784706807,],[1,1,0.4826332738837594,],])
    AG3_F37 = Factor('AG3_F37', [AG3_V0,AG3_V6,AG3_V8,AG3_V9,AG3_V12,AG3_V17,])
    AG3_F37.add_values([[0,0,0,0,0,0,0.7864356810601489,],[0,0,0,0,0,1,0.8818154454272277,],[0,0,0,0,1,0,0.5875209769684859,],[0,0,0,0,1,1,0.8003315125876994,],[0,0,0,1,0,0,0.5621873924052511,],[0,0,0,1,0,1,0.032348453003711614,],[0,0,0,1,1,0,0.965152807546647,],[0,0,0,1,1,1,0.5026919401024618,],[0,0,1,0,0,0,0.6158817406599629,],[0,0,1,0,0,1,0.3746832080178977,],[0,0,1,0,1,0,0.9031941206560161,],[0,0,1,0,1,1,0.7635943267050382,],[0,0,1,1,0,0,0.7951761259230027,],[0,0,1,1,0,1,0.12276917610090242,],[0,0,1,1,1,0,0.9436286944557215,],[0,0,1,1,1,1,0.15691422266311458,],[0,1,0,0,0,0,0.352985470941552,],[0,1,0,0,0,1,0.6746077335410966,],[0,1,0,0,1,0,0.2719143145646261,],[0,1,0,0,1,1,0.32272595267014453,],[0,1,0,1,0,0,0.7674221548235794,],[0,1,0,1,0,1,0.395241025526705,],[0,1,0,1,1,0,0.7607590921632668,],[0,1,0,1,1,1,0.014669362496961972,],[0,1,1,0,0,0,0.7384074138402714,],[0,1,1,0,0,1,0.7170474620972945,],[0,1,1,0,1,0,0.8433696725571265,],[0,1,1,0,1,1,0.01966780872168902,],[0,1,1,1,0,0,0.7543062512558951,],[0,1,1,1,0,1,0.5599977995288421,],[0,1,1,1,1,0,0.8876801538963611,],[0,1,1,1,1,1,0.5538413562732692,],[1,0,0,0,0,0,0.8339647346234306,],[1,0,0,0,0,1,0.8536596746030669,],[1,0,0,0,1,0,0.6785454741778322,],[1,0,0,0,1,1,0.9237313481208483,],[1,0,0,1,0,0,0.8914494296781756,],[1,0,0,1,0,1,0.8760920617380289,],[1,0,0,1,1,0,0.5223074901459679,],[1,0,0,1,1,1,0.6887200727228787,],[1,0,1,0,0,0,0.8346863145971264,],[1,0,1,0,0,1,0.5270409791782682,],[1,0,1,0,1,0,0.5768406426271795,],[1,0,1,0,1,1,0.9792268253093287,],[1,0,1,1,0,0,0.9599561061854807,],[1,0,1,1,0,1,0.6686623493162018,],[1,0,1,1,1,0,0.23319480890505453,],[1,0,1,1,1,1,0.4162581374961393,],[1,1,0,0,0,0,0.4376120938626837,],[1,1,0,0,0,1,0.7265137906139555,],[1,1,0,0,1,0,0.9796246190276525,],[1,1,0,0,1,1,0.0814696228398934,],[1,1,0,1,0,0,0.5945973593618853,],[1,1,0,1,0,1,0.6797142051442151,],[1,1,0,1,1,0,0.8723924312088803,],[1,1,0,1,1,1,0.7426381695264348,],[1,1,1,0,0,0,0.2877551115754714,],[1,1,1,0,0,1,0.6309493768120487,],[1,1,1,0,1,0,0.8284153465764509,],[1,1,1,0,1,1,0.8826641621877893,],[1,1,1,1,0,0,0.8736907868546216,],[1,1,1,1,0,1,0.7690996320872006,],[1,1,1,1,1,0,0.6535634398946821,],[1,1,1,1,1,1,0.9413795333869627,],])
    AG3_F38 = Factor('AG3_F38', [AG3_V0,AG3_V15,])
    AG3_F38.add_values([[0,0,0.5129710679964193,],[0,1,0.7911244131473908,],[1,0,0.015411028949082594,],[1,1,0.3666226344523303,],])
    AG3_F39 = Factor('AG3_F39', [AG3_V1,AG3_V11,])
    AG3_F39.add_values([[0,0,0.8444398270390463,],[0,1,0.26300656755601026,],[1,0,0.312414151777759,],[1,1,0.1436858078765524,],])
    AG3_F40 = Factor('AG3_F40', [AG3_V1,AG3_V2,AG3_V6,AG3_V12,AG3_V13,AG3_V19,])
    AG3_F40.add_values([[0,0,0,0,0,0,0.7797733098702861,],[0,0,0,0,0,1,0.659203436062476,],[0,0,0,0,1,0,0.21099576161545117,],[0,0,0,0,1,1,0.8863332418049574,],[0,0,0,1,0,0,0.9075984660178077,],[0,0,0,1,0,1,0.6829383597630572,],[0,0,0,1,1,0,0.05648267415796883,],[0,0,0,1,1,1,0.02771135661594739,],[0,0,1,0,0,0,0.6253820460828433,],[0,0,1,0,0,1,0.5660524734102684,],[0,0,1,0,1,0,0.6124737613684362,],[0,0,1,0,1,1,0.0800996302240511,],[0,0,1,1,0,0,0.05775468718411038,],[0,0,1,1,0,1,0.9640666293361837,],[0,0,1,1,1,0,0.6073183317844442,],[0,0,1,1,1,1,0.2683487408678886,],[0,1,0,0,0,0,0.35508469051066593,],[0,1,0,0,0,1,0.474017606505607,],[0,1,0,0,1,0,0.2464113908289971,],[0,1,0,0,1,1,0.026872090846647868,],[0,1,0,1,0,0,0.7637473743857645,],[0,1,0,1,0,1,0.058859004183120824,],[0,1,0,1,1,0,0.45439976532825893,],[0,1,0,1,1,1,0.4994337785481603,],[0,1,1,0,0,0,0.12358869048912026,],[0,1,1,0,0,1,0.030228375033753276,],[0,1,1,0,1,0,0.34176787691835586,],[0,1,1,0,1,1,0.10518092651361773,],[0,1,1,1,0,0,0.9710329681064532,],[0,1,1,1,0,1,0.9705995586331453,],[0,1,1,1,1,0,0.8193325311640586,],[0,1,1,1,1,1,0.36348519094811504,],[1,0,0,0,0,0,0.11903595022623842,],[1,0,0,0,0,1,0.35870954988504516,],[1,0,0,0,1,0,0.37538721680438386,],[1,0,0,0,1,1,0.9890489997474555,],[1,0,0,1,0,0,0.21482815018064383,],[1,0,0,1,0,1,0.40854404450426235,],[1,0,0,1,1,0,0.44654786972183863,],[1,0,0,1,1,1,0.09814150927358288,],[1,0,1,0,0,0,0.520869969997498,],[1,0,1,0,0,1,0.2827405824449995,],[1,0,1,0,1,0,0.998844691214863,],[1,0,1,0,1,1,0.8456637889202328,],[1,0,1,1,0,0,0.7728340598720711,],[1,0,1,1,0,1,0.5640039423743506,],[1,0,1,1,1,0,0.9766105326956303,],[1,0,1,1,1,1,0.6596128926795349,],[1,1,0,0,0,0,0.4242258294722749,],[1,1,0,0,0,1,0.257785439172392,],[1,1,0,0,1,0,0.5612191166709345,],[1,1,0,0,1,1,0.9703968773391768,],[1,1,0,1,0,0,0.9078011656180208,],[1,1,0,1,0,1,0.4999710286790205,],[1,1,0,1,1,0,0.24039844890801365,],[1,1,0,1,1,1,0.9332736332930468,],[1,1,1,0,0,0,0.27960486879228635,],[1,1,1,0,0,1,0.9834636147353291,],[1,1,1,0,1,0,0.3273841166061344,],[1,1,1,0,1,1,0.6654382395183454,],[1,1,1,1,0,0,0.9398727745475838,],[1,1,1,1,0,1,0.036969462295442006,],[1,1,1,1,1,0,0.8403876364157647,],[1,1,1,1,1,1,0.30472797343797464,],])
    AG3_F41 = Factor('AG3_F41', [AG3_V17,AG3_V19,])
    AG3_F41.add_values([[0,0,0.4792108724770306,],[0,1,0.8665137189576142,],[1,0,0.6365597718763969,],[1,1,0.03030405856424508,],])
    AG3_F42 = Factor('AG3_F42', [AG3_V3,AG3_V5,AG3_V9,AG3_V11,AG3_V13,AG3_V17,])
    AG3_F42.add_values([[0,0,0,0,0,0,0.102902193340044,],[0,0,0,0,0,1,0.44409014733187724,],[0,0,0,0,1,0,0.32419110370471216,],[0,0,0,0,1,1,0.08163666022773476,],[0,0,0,1,0,0,0.9512916776719623,],[0,0,0,1,0,1,0.8172308572663923,],[0,0,0,1,1,0,0.785358654156239,],[0,0,0,1,1,1,0.2556367644372257,],[0,0,1,0,0,0,0.37455641524013145,],[0,0,1,0,0,1,0.8071263657315195,],[0,0,1,0,1,0,0.05245973111377971,],[0,0,1,0,1,1,0.7395777181398575,],[0,0,1,1,0,0,0.7015768403864101,],[0,0,1,1,0,1,0.5565439596605691,],[0,0,1,1,1,0,0.186002907323788,],[0,0,1,1,1,1,0.9713349784065556,],[0,1,0,0,0,0,0.6835015404147979,],[0,1,0,0,0,1,0.5293076580553483,],[0,1,0,0,1,0,0.6551858348486566,],[0,1,0,0,1,1,0.6401303652260946,],[0,1,0,1,0,0,0.1616818365020348,],[0,1,0,1,0,1,0.1178359004715027,],[0,1,0,1,1,0,0.7696325756511307,],[0,1,0,1,1,1,0.56794050975947,],[0,1,1,0,0,0,0.4255847709822928,],[0,1,1,0,0,1,0.42183696033851575,],[0,1,1,0,1,0,0.5823674785786928,],[0,1,1,0,1,1,0.22935289585105137,],[0,1,1,1,0,0,0.27376683320499406,],[0,1,1,1,0,1,0.08326215360396703,],[0,1,1,1,1,0,0.8338995246806213,],[0,1,1,1,1,1,0.7120857292084273,],[1,0,0,0,0,0,0.21822023239724683,],[1,0,0,0,0,1,0.2899695942579196,],[1,0,0,0,1,0,0.08431396195160984,],[1,0,0,0,1,1,0.5843983199215466,],[1,0,0,1,0,0,0.4630719777256559,],[1,0,0,1,0,1,0.8733892930408265,],[1,0,0,1,1,0,0.5285151157405075,],[1,0,0,1,1,1,0.147068866589354,],[1,0,1,0,0,0,0.19353388158985893,],[1,0,1,0,0,1,0.11974831926004197,],[1,0,1,0,1,0,0.16466444890261248,],[1,0,1,0,1,1,0.0034352111055384322,],[1,0,1,1,0,0,0.8616183991235125,],[1,0,1,1,0,1,0.23470238322444248,],[1,0,1,1,1,0,0.007116701976780645,],[1,0,1,1,1,1,0.722680190674485,],[1,1,0,0,0,0,0.633148170985249,],[1,1,0,0,0,1,0.7068373624058933,],[1,1,0,0,1,0,0.24964403123525064,],[1,1,0,0,1,1,0.15401319521584678,],[1,1,0,1,0,0,0.4671279075992621,],[1,1,0,1,0,1,0.7999875767980711,],[1,1,0,1,1,0,0.21143804890415901,],[1,1,0,1,1,1,0.8239928518063463,],[1,1,1,0,0,0,0.8643107209849025,],[1,1,1,0,0,1,0.6322953065723366,],[1,1,1,0,1,0,0.08157337146827975,],[1,1,1,0,1,1,0.2876851025302491,],[1,1,1,1,0,0,0.13212427001596105,],[1,1,1,1,0,1,0.21236407429681553,],[1,1,1,1,1,0,0.940828562434342,],[1,1,1,1,1,1,0.18637270614026746,],])
    AG3_F43 = Factor('AG3_F43', [AG3_V0,AG3_V4,AG3_V5,AG3_V13,])
    AG3_F43.add_values([[0,0,0,0,0.316805176910284,],[0,0,0,1,0.7475330427361327,],[0,0,1,0,0.5377932600202826,],[0,0,1,1,0.969905872074003,],[0,1,0,0,0.6905325155520018,],[0,1,0,1,0.15309495141711338,],[0,1,1,0,0.8900747190266469,],[0,1,1,1,0.8363713237645718,],[1,0,0,0,0.6947625575666132,],[1,0,0,1,0.9180449571659041,],[1,0,1,0,0.7433274369701156,],[1,0,1,1,0.4611749640324039,],[1,1,0,0,0.32647709360205335,],[1,1,0,1,0.6517525156441861,],[1,1,1,0,0.036857175176902644,],[1,1,1,1,0.6419583830570799,],])
    AG3_F44 = Factor('AG3_F44', [AG3_V0,AG3_V8,AG3_V17,])
    AG3_F44.add_values([[0,0,0,0.05222698651971025,],[0,0,1,0.4312058465971395,],[0,1,0,0.004702027590216459,],[0,1,1,0.19062171458321664,],[1,0,0,0.8954868360145901,],[1,0,1,0.7586200225789763,],[1,1,0,0.14062084953729195,],[1,1,1,0.3328581253793774,],])
    AG3_F45 = Factor('AG3_F45', [AG3_V0,AG3_V8,AG3_V12,AG3_V15,AG3_V17,AG3_V19,])
    AG3_F45.add_values([[0,0,0,0,0,0,0.5822189020835908,],[0,0,0,0,0,1,0.43727389468738936,],[0,0,0,0,1,0,0.09786978525146592,],[0,0,0,0,1,1,0.957212599491854,],[0,0,0,1,0,0,0.012461736214395159,],[0,0,0,1,0,1,0.7561182207843647,],[0,0,0,1,1,0,0.6416834491167972,],[0,0,0,1,1,1,0.9512488873072119,],[0,0,1,0,0,0,0.9170072422243849,],[0,0,1,0,0,1,0.16749798632083607,],[0,0,1,0,1,0,0.7832793107434199,],[0,0,1,0,1,1,0.9887588581925407,],[0,0,1,1,0,0,0.7530446361007536,],[0,0,1,1,0,1,0.2597682680292373,],[0,0,1,1,1,0,0.3690687555814093,],[0,0,1,1,1,1,0.8963271176721068,],[0,1,0,0,0,0,0.41411133884149287,],[0,1,0,0,0,1,0.049148370683835804,],[0,1,0,0,1,0,0.8491946781709807,],[0,1,0,0,1,1,0.634893260984133,],[0,1,0,1,0,0,0.22568524214994648,],[0,1,0,1,0,1,0.531762129516275,],[0,1,0,1,1,0,0.3288440509173488,],[0,1,0,1,1,1,0.02713741103659581,],[0,1,1,0,0,0,0.6134117400846326,],[0,1,1,0,0,1,0.4868405571096239,],[0,1,1,0,1,0,0.9188283288200236,],[0,1,1,0,1,1,0.14931433204413375,],[0,1,1,1,0,0,0.34959543364432477,],[0,1,1,1,0,1,0.22693943331359456,],[0,1,1,1,1,0,0.1942129695357207,],[0,1,1,1,1,1,0.6085695964656255,],[1,0,0,0,0,0,0.1488526964502396,],[1,0,0,0,0,1,0.9563412219245199,],[1,0,0,0,1,0,0.039790289028386716,],[1,0,0,0,1,1,0.04488697383211907,],[1,0,0,1,0,0,0.7743023987050259,],[1,0,0,1,0,1,0.15726784425470508,],[1,0,0,1,1,0,0.43991247135488326,],[1,0,0,1,1,1,0.6426154915156207,],[1,0,1,0,0,0,0.445596144993491,],[1,0,1,0,0,1,0.12223894909692411,],[1,0,1,0,1,0,0.8621237703112237,],[1,0,1,0,1,1,0.6352471946570234,],[1,0,1,1,0,0,0.6019705645603196,],[1,0,1,1,0,1,0.9723115233082166,],[1,0,1,1,1,0,0.39081627980223405,],[1,0,1,1,1,1,0.7490407170359099,],[1,1,0,0,0,0,0.29862003118253183,],[1,1,0,0,0,1,0.7355837999030163,],[1,1,0,0,1,0,0.4392482122027886,],[1,1,0,0,1,1,0.3254900947923701,],[1,1,0,1,0,0,0.42768709910824837,],[1,1,0,1,0,1,0.9253239851303594,],[1,1,0,1,1,0,0.9155300898193421,],[1,1,0,1,1,1,0.5102898669059097,],[1,1,1,0,0,0,0.6827994787818439,],[1,1,1,0,0,1,0.5825907895262533,],[1,1,1,0,1,0,0.026858744310152845,],[1,1,1,0,1,1,0.30428620429192155,],[1,1,1,1,0,0,0.9070076923510337,],[1,1,1,1,0,1,0.15542374007947768,],[1,1,1,1,1,0,0.02302282033784602,],[1,1,1,1,1,1,0.19356212990543717,],])
    AG3_F46 = Factor('AG3_F46', [AG3_V2,AG3_V9,AG3_V16,])
    AG3_F46.add_values([[0,0,0,0.9884506037717968,],[0,0,1,0.10011061997888218,],[0,1,0,0.562995959322264,],[0,1,1,0.13531653389407716,],[1,0,0,0.08096056009336577,],[1,0,1,0.37618201503091003,],[1,1,0,0.03856608404572713,],[1,1,1,0.2279442085589058,],])
    AG3_F47 = Factor('AG3_F47', [AG3_V1,AG3_V2,AG3_V15,AG3_V18,])
    AG3_F47.add_values([[0,0,0,0,0.5488584260639309,],[0,0,0,1,0.8514126743580284,],[0,0,1,0,0.7688396135183161,],[0,0,1,1,0.9357557191190239,],[0,1,0,0,0.8783791645375119,],[0,1,0,1,0.6779704576603323,],[0,1,1,0,0.5073956955730652,],[0,1,1,1,0.027449743062542,],[1,0,0,0,0.2580328549046574,],[1,0,0,1,0.20975119481836957,],[1,0,1,0,0.2080894879798188,],[1,0,1,1,0.3713586970797811,],[1,1,0,0,0.7823936157415512,],[1,1,0,1,0.7784243100304387,],[1,1,1,0,0.23656255898807682,],[1,1,1,1,0.2303100800792491,],])
    AG3_F48 = Factor('AG3_F48', [AG3_V11,AG3_V17,])
    AG3_F48.add_values([[0,0,0.6405176305612831,],[0,1,0.7697104260790855,],[1,0,0.48892015347933976,],[1,1,0.02258279892329972,],])
    AG3_F49 = Factor('AG3_F49', [AG3_V0,AG3_V1,AG3_V8,])
    AG3_F49.add_values([[0,0,0,0.056989889139569365,],[0,0,1,0.06738057995689392,],[0,1,0,0.6575775918502739,],[0,1,1,0.30573771998554106,],[1,0,0,0.31536603471243674,],[1,0,1,0.7299451013542527,],[1,1,0,0.35329527137011507,],[1,1,1,0.3906609357969277,],])
    AG3_bayesnet = BayesianNetwork('Randomly generated net 3',[ AG3_V0, AG3_V1, AG3_V2, AG3_V3, AG3_V4, AG3_V5, AG3_V6, AG3_V7, AG3_V8, AG3_V9, AG3_V10, AG3_V11, AG3_V12, AG3_V13, AG3_V14, AG3_V15, AG3_V16, AG3_V17, AG3_V18, AG3_V19,],[AG3_F0,AG3_F1,AG3_F2,AG3_F3,AG3_F4,AG3_F5,AG3_F6,AG3_F7,AG3_F8,AG3_F9,AG3_F10,AG3_F11,AG3_F12,AG3_F13,AG3_F14,AG3_F15,AG3_F16,AG3_F17,AG3_F18,AG3_F19,AG3_F20,AG3_F21,AG3_F22,AG3_F23,AG3_F24,AG3_F25,AG3_F26,AG3_F27,AG3_F28,AG3_F29,AG3_F30,AG3_F31,AG3_F32,AG3_F33,AG3_F34,AG3_F35,AG3_F36,AG3_F37,AG3_F38,AG3_F39,AG3_F40,AG3_F41,AG3_F42,AG3_F43,AG3_F44,AG3_F45,AG3_F46,AG3_F47,AG3_F48,AG3_F49,])
    AG3_test = VETest(AG3_bayesnet,[],AG3_V19,[[0.5866499280692985, 0.41335007193070156]],'Variable Elimination Test (Generated Bayes Net 3, Large)')

    

    t1.test()
    t2.test()
    t3.test()

    t14.test()

    t4.test()
    t5.test()
    t6.test()
    t7.test()
    t8.test()
    t9.test()
    t10.test()
    t11.test()
    t12.test()
    t13.test()
    

    #The following tests are on larger, randomly generated bayes nets
    #Try these only after having passed the above tests
    
    #AG_t1.test()
    #AG2_test.test()
    #AG3_test.test()
    
