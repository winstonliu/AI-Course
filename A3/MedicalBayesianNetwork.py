from BayesianNetwork import *

'''
The patient class defines a series of known observations for an individual

name: The patients name, not necessarily unique
evidenceVariables: The variables which have known values
evidenceValues: The value of the corresponding variable
'''
class Patient:

    def __init__(self, name, evidenceVars, evidenceVals):
        self.name = name
        self.evidenceVars = evidenceVars
        self.evidenceVals = evidenceVals

    def evidenceVariables(self):
        '''return a list of the evidence variables that can be modified'''
        return list(self.evidenceVars)

    def evidenceValues(self):
        '''return a list of the evidence values that can be modified'''
        return list(self.evidenceVals)
    
        
'''
The MedicalBayesianNetwork represents a Bayesian network with some variables
having special status:

BayesNet : the underlying Bayesian Network (A BayesianNetwork object)
treatmentVars : a list of variables in Bayesnet representing possible treatments
outcomeVars: a list of variables in Bayesnet representing possible patient 
             outcomes

Note that the treatment and outcome variables must be variables of the Bayes net

Treament and Outcome variables should be mutually exclusive

'''
class MedicalBayesianNetwork:
    def __init__(self, BayesNet, treatmentVars, outcomeVars):
        self.name = BayesNet.name
        self.net = BayesNet
        self.treatmentVars = treatmentVars
        self.outcomeVars = outcomeVars
    
    def set_evidence_by_patient(self, patient):
        '''Sets the evidence variables in the associated Bayes net to match
        the evidence displayed by the patient'''
        
        for i in range(0,len(patient.evidenceVars)):            
            patient.evidenceVars[i].set_evidence(patient.evidenceVals[i])
            

    def getTreatmentVars(self):
        '''return a list of the treatment variables that can be modified'''
        return list(self.treatmentVars)

    def getOutcomeVars(self):
        '''return a list of the outcome variables that can be modified'''
        return list(self.outcomeVars)

        
        
        
