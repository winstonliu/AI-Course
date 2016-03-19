#Updated March 14, 2016 

from MedicalBayesianNetwork import *
from DecisionSupport import *
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


                       


class MedTest:


    #net is the bayes net, 
    def __init__(self, mednet, patient, answer, name="Decision support test"):
        self.name = name
        self.mednet = mednet
        self.patient = patient        
        self.answer = answer

                         
    def test(self):
        #answer[0] : The scope of the factor, as a list of names
        #answer[1] : The "values" entry of the factor



        print("\nRunning Test : {}".format(self.name))

        
        try:            

            result = DecisionSupport(self.mednet,self.patient)
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
                    #uncomment the following line to print the table produced
                    #result2.print_table()
                else:
                    print("\t[!] Factor values mismatch the expected result in {} place{}:\n".format(tabletest[0], "" if (tabletest[0] == 1) else "s"))
                    print(tabletest[1])                            
                    
            
        except:

            print("\t[!] Execution error:\n*****")
            traceback.print_exc()        



if __name__ == '__main__':



    PatientAge = Variable('Age range' ,['0-30','31-65','65+'])
    CTScanResult = Variable('CT scan indication', ['Ischemic Stroke','Hemmorraghic Stroke'])
    MRIScanResult = Variable('MRI scan indication', ['Ischemic Stroke','Hemmorraghic Stroke'])

    StrokeType = Variable('Patient condition', ['Ischemic Stroke','Hemmorraghic Stroke', 'Stroke Mimic'])
    Anticoagulants = Variable('Anticoagulant status', ['Used','Not used'])
    PrimaryTreatment = Variable('Primary treatment', ['Thromblysis','Neurosurgical evaluation','None'])

    Mortality = Variable('Short term survival',[True, False])
    Disability = Variable ('Degree of long term disability', ['Negligible', 'Moderate', 'Severe'])


    

    
    F1 = Factor("F1", [PatientAge])
    F1.add_values(
        [
            ['0-30', 0.10],
            ['31-65', 0.30],
            ['65+', 0.60]
        ])
    
    F2 = Factor("F2", [CTScanResult])
    F2.add_values(
        [
            ['Ischemic Stroke',0.7],
            [ 'Hemmorraghic Stroke',0.3]
        ])
    F3 = Factor("F3", [MRIScanResult])
    F3.add_values(
        [
            ['Ischemic Stroke',0.7],
            [ 'Hemmorraghic Stroke',0.3]
        ])


    F5 = Factor("F5", [CTScanResult, StrokeType])
    F5.add_values(
        [
            ['Ischemic Stroke','Ischemic Stroke',0.16],
            ['Ischemic Stroke','Hemmorraghic Stroke',0],
            ['Ischemic Stroke','Stroke Mimic',0.84],            
            [ 'Hemmorraghic Stroke','Ischemic Stroke',0.04],
            [ 'Hemmorraghic Stroke','Hemmorraghic Stroke',0.89],            
            [ 'Hemmorraghic Stroke','Stroke Mimic',0.07]
        ])
    F6 = Factor("F6", [MRIScanResult, StrokeType])
    F6.add_values(
        [
            ['Ischemic Stroke','Ischemic Stroke',0.83],
            ['Ischemic Stroke','Hemmorraghic Stroke',0],
            ['Ischemic Stroke','Stroke Mimic',0.17],            
            [ 'Hemmorraghic Stroke','Ischemic Stroke',0.02],
            [ 'Hemmorraghic Stroke','Hemmorraghic Stroke',0.81],            
            [ 'Hemmorraghic Stroke','Stroke Mimic',0.17]
        ])
    F8 = Factor("F8", [Mortality, StrokeType, Anticoagulants])
    F8.add_values(
        [
            [False,'Ischemic Stroke', 'Used', 0.28],
            [False,'Hemmorraghic Stroke', 'Used', 0.99],
            [False,'Stroke Mimic', 'Used', 0.1],
            [False,'Ischemic Stroke','Not used', 0.56],
            [False,'Hemmorraghic Stroke', 'Not used', 0.58],
            [False,'Stroke Mimic', 'Not used', 0.05],
            [True,'Ischemic Stroke',  'Used' ,0.72],
            [True,'Hemmorraghic Stroke', 'Used', 0.01],
            [True,'Stroke Mimic', 'Used', 0.9],
            [True,'Ischemic Stroke',  'Not used' ,0.44],
            [True,'Hemmorraghic Stroke', 'Not used', 0.42],
            [True,'Stroke Mimic', 'Not used', 0.95],
        ])

    F9 = Factor("F9", [Mortality, StrokeType, PrimaryTreatment])
    F9.add_values(
        [
            [False,'Ischemic Stroke',     'None', 0.6],
            [False,'Hemmorraghic Stroke', 'None', 0.7],
            [False,'Stroke Mimic',        'None', 0.05],
            [False,'Ischemic Stroke',     'Neurosurgical evaluation', 0.6],
            [False,'Hemmorraghic Stroke', 'Neurosurgical evaluation', 0.3],
            [False,'Stroke Mimic',        'Neurosurgical evaluation', 0.1],
            [False,'Ischemic Stroke',     'Thromblysis', 0.25],
            [False,'Hemmorraghic Stroke', 'Thromblysis', 0.95],
            [False,'Stroke Mimic',        'Thromblysis', 0.2],


            [True,'Ischemic Stroke',     'None', 0.4],
            [True,'Hemmorraghic Stroke', 'None', 0.3],
            [True,'Stroke Mimic',        'None', 0.95],
            [True,'Ischemic Stroke',     'Neurosurgical evaluation', 0.4],
            [True,'Hemmorraghic Stroke', 'Neurosurgical evaluation', 0.7],
            [True,'Stroke Mimic',        'Neurosurgical evaluation', 0.9],
            [True,'Ischemic Stroke',     'Thromblysis', 0.72],
            [True,'Hemmorraghic Stroke', 'Thromblysis', 0.05],
            [True,'Stroke Mimic',        'Thromblysis', 0.8],
        ])


    F10= Factor("F10", [Mortality, StrokeType, PatientAge])
    F10.add_values(
        [
            [False,'Ischemic Stroke',     '0-30', .10],
            [False,'Hemmorraghic Stroke', '0-30', .20],
            [False,'Stroke Mimic',        '0-30', .05],
            [False,'Ischemic Stroke',     '31-65', .20],
            [False,'Hemmorraghic Stroke', '31-65', .30],
            [False,'Stroke Mimic',        '31-65', .1],
            [False,'Ischemic Stroke',     '65+'  , .60],
            [False,'Hemmorraghic Stroke', '65+'  , .80],
            [False,'Stroke Mimic',        '65+'  , .2],


            [True,'Ischemic Stroke',     '0-30' ,0.9],
            [True,'Hemmorraghic Stroke', '0-30' ,0.8],
            [True,'Stroke Mimic',        '0-30' ,0.95],
            [True,'Ischemic Stroke',     '31-65',0.8],
            [True,'Hemmorraghic Stroke', '31-65',0.7],
            [True,'Stroke Mimic',        '31-65',0.9],
            [True,'Ischemic Stroke',     '65+'  ,0.4],
            [True,'Hemmorraghic Stroke', '65+'  ,0.0],
            [True,'Stroke Mimic',        '65+'  ,0.8],
        ])



    F11 = Factor("F11", [Disability, StrokeType, PrimaryTreatment])
    F11.add_values(
        [
            ['Negligible','Ischemic Stroke',     'None'                    ,0.28],
            ['Negligible','Hemmorraghic Stroke', 'None'                    ,0.1],
            ['Negligible','Stroke Mimic',        'None'                    ,0.9],
            ['Negligible','Ischemic Stroke',     'Neurosurgical evaluation',0.3],
            ['Negligible','Hemmorraghic Stroke', 'Neurosurgical evaluation',0.55],
            ['Negligible','Stroke Mimic',        'Neurosurgical evaluation',0.88],
            ['Negligible','Ischemic Stroke',     'Thromblysis'             ,0.5],
            ['Negligible','Hemmorraghic Stroke', 'Thromblysis'             ,0.01],
            ['Negligible','Stroke Mimic',        'Thromblysis'             ,0.1],


            ['Moderate','Ischemic Stroke',     'None'                      ,0.3],
            ['Moderate','Hemmorraghic Stroke', 'None'                      ,0.4],
            ['Moderate','Stroke Mimic',        'None'                      ,0.05],
            ['Moderate','Ischemic Stroke',     'Neurosurgical evaluation'  ,0.3],
            ['Moderate','Hemmorraghic Stroke', 'Neurosurgical evaluation'  ,0.25],
            ['Moderate','Stroke Mimic',        'Neurosurgical evaluation'  ,0.06],
            ['Moderate','Ischemic Stroke',     'Thromblysis'               ,0.25],
            ['Moderate','Hemmorraghic Stroke', 'Thromblysis'               ,0.35],
            ['Moderate','Stroke Mimic',        'Thromblysis'               ,0.5],

            
            ['Severe','Ischemic Stroke',     'None'                        ,0.42],
            ['Severe','Hemmorraghic Stroke', 'None'                        ,0.5],
            ['Severe','Stroke Mimic',        'None'                        ,0.05],
            ['Severe','Ischemic Stroke',     'Neurosurgical evaluation'    ,0.4],
            ['Severe','Hemmorraghic Stroke', 'Neurosurgical evaluation'    ,0.06],
            ['Severe','Stroke Mimic',        'Neurosurgical evaluation'    ,0.2],
            ['Severe','Ischemic Stroke',     'Thromblysis'                 ,0.25],
            ['Severe','Hemmorraghic Stroke', 'Thromblysis'                 ,0.64],
            ['Severe','Stroke Mimic',        'Thromblysis'                 ,0.45],
        ])


    F12 = Factor("F12", [Disability, StrokeType, Anticoagulants])
    F12.add_values(
        [
            ['Negligible','Ischemic Stroke',     'Not used'                    ,0.4],
            ['Negligible','Hemmorraghic Stroke', 'Not used'                    ,0.5],
            ['Negligible','Stroke Mimic',        'Not used'                    ,0.95],
            ['Negligible','Ischemic Stroke',     'Used'                        ,0.5],
            ['Negligible','Hemmorraghic Stroke', 'Used'                        ,0.01],
            ['Negligible','Stroke Mimic',        'Used'                        ,0.9],
            

            ['Moderate','Ischemic Stroke',     'Not used'                      ,0.4],
            ['Moderate','Hemmorraghic Stroke', 'Not used'                      ,0.25],
            ['Moderate','Stroke Mimic',        'Not used'                      ,0.03],
            ['Moderate','Ischemic Stroke',     'Used'                          ,0.25],
            ['Moderate','Hemmorraghic Stroke', 'Used'                          ,0.05],
            ['Moderate','Stroke Mimic',        'Used'                          ,0.03],
                        
            ['Severe','Ischemic Stroke',     'Not used'                        ,0.3],
            ['Severe','Hemmorraghic Stroke', 'Not used'                        ,0.25],
            ['Severe','Stroke Mimic',        'Not used'                        ,0.02],
            ['Severe','Ischemic Stroke',     'Used'                            ,0.25],
            ['Severe','Hemmorraghic Stroke', 'Used'                            ,0.94],
            ['Severe','Stroke Mimic',        'Used'                            ,0.02],
        ])
    
    
    
    tempNet = BayesianNetwork("Stroke Diagnosis",
                             [PatientAge, CTScanResult,MRIScanResult, StrokeType, Anticoagulants, PrimaryTreatment, Mortality, Disability],
                             [F1,F2,F3,F5,F6,F8,F9,F10,F11,F12])


    
    mednet = MedicalBayesianNetwork(tempNet, [PrimaryTreatment, Anticoagulants],[Mortality, Disability])
    p1 = Patient("Alice",[PatientAge, CTScanResult],['31-65','Ischemic Stroke'])
    p2 = Patient("Bob",[PatientAge, MRIScanResult],['65+','Hemmorraghic Stroke'])
    p3 = Patient("Charles",[PatientAge, CTScanResult,MRIScanResult],['65+', 'Hemmorraghic Stroke', 'Ischemic Stroke'])
    p4 = Patient("Dave",[PatientAge],['0-30'])


    medtest1 = MedTest(mednet,p1, [['Short term survival', 'Degree of long term disability', 'Primary treatment', 'Anticoagulant status'], [0.7034664820507913, 0.6514166576979357, 0.9393782170904493, 0.9383164490107097, 0.9461559821430544, 0.945220840790866, 0.14884243752766246, 0.17842051487401636, 0.01984473172552662, 0.01791945446375387, 0.01837872029828077, 0.016536175764129978, 0.12722309113963418, 0.12361853749570796, 0.028285494667296567, 0.02034677811276286, 0.02448759947142746, 0.01673666359506375, 0.01380102106933662, 0.025032549580379385, 0.006428715243794653, 0.008203946221075068, 0.005136374313462832, 0.0069249407951749685, 0.0033668472951581202, 0.012300941728822803, 0.002597287146150142, 0.007605897491674838, 0.00243422132791459, 0.007112961867424855, 0.0033001209174172924, 0.009210798623137856, 0.003465554126782623, 0.007607474700023772, 0.0034071024458600446, 0.0074684171873404875]])
    medtest2 = MedTest(mednet,p2, [['Short term survival', 'Degree of long term disability', 'Primary treatment', 'Anticoagulant status'], [0.05096290020968793, 0.19012811172604246, 0.921839978134501, 0.8393887214456079, 0.4920122286550456, 0.7637943527911647, 0.008593168958099914, 0.030696776140913668, 0.002464855907487279, 0.002103609055841918, 0.0010941659098123227, 0.001589891058964649, 0.005275124082642258, 0.018566385817231655, 0.005147276707333676, 0.0043117452908664755, 0.0008641331109699882, 0.0011558798582578418, 0.0007380102054532811, 0.016927360982233044, 0.008392352786051055, 0.11941791406257446, 0.0020465493109746388, 0.04315981198846171, 0.026525361835106998, 0.2632100336648703, 0.01146652157413314, 0.027521369877459723, 0.02071693791651767, 0.08464176235295509, 0.9079054347090095, 0.48047133166870903, 0.050689014890493676, 0.007256640267649475, 0.48326598509667956, 0.10565830195019602]])
    medtest3 = MedTest(mednet,p3, [['Short term survival', 'Degree of long term disability', 'Primary treatment', 'Anticoagulant status'], [0.6008141112618725, 0.438382523940544, 0.785845996699689, 0.7006096692546444, 0.7993522449890056, 0.7173445366445693, 0.13699272233871962, 0.15176230219210646, 0.035373029361570135, 0.02918307903427715, 0.03353459291365594, 0.027661362242553535, 0.12642407795732083, 0.10915356789020685, 0.0486152820467339, 0.030953803678828596, 0.045944428874908044, 0.02857860540446981, 0.09068397681016405, 0.16058939834283692, 0.06126284357704404, 0.08040469829914963, 0.053617846465769274, 0.0711630734953485, 0.022579252497841366, 0.08007289338267448, 0.029527872501521175, 0.07942308047719002, 0.02814681441444967, 0.07573304624708033, 0.022505859134081655, 0.060039314251631275, 0.03937497581344173, 0.07942566925591013, 0.03940407234221168, 0.07951937596597851]])
    medtest4 = MedTest(mednet,p4, [['Short term survival', 'Degree of long term disability', 'Primary treatment', 'Anticoagulant status'], [0.5199945320249683, 0.5879541345064931, 0.9359158099626791, 0.9251906713900818, 0.8926381505150814, 0.9186370272939989, 0.11143358587086093, 0.1719345404344452, 0.022187628690116035, 0.030343432589181634, 0.01948179280881587, 0.0257263045153011, 0.09709918751571599, 0.12553953388785302, 0.0315979663947823, 0.02376127329735926, 0.02697582467395033, 0.02795791353480176, 0.004825047979504012, 0.012768606213207466, 0.0034868465259917775, 0.011412664622127335, 0.00253770494083496, 0.006499393681317674, 0.008640267993348714, 0.038038103216455184, 0.001987171037799769, 0.005299451023306869, 0.0034264438985598983, 0.009722284573331845, 0.25800737861560197, 0.06376508174154602, 0.004824577388631062, 0.003992507077943142, 0.05494008316275756, 0.011457076401248772]])
    
    medtest1.test()    
    medtest2.test()    
    medtest3.test()
    medtest4.test()
    
