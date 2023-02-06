import pyomo.environ as pyo
from pyomo.opt import SolverFactory

import matplotlib.pyplot as plt
import numpy as np

import shutil
import sys
import os.path

#Declare model
model = pyo.ConcreteModel()
#Declare parameters Guess value
model.l = pyo.Param(initialize=250)
model.mina1=pyo.Param(initialize=0)
model.mina2=pyo.Param(initialize=0)
model.mina3=pyo.Param(initialize=0)
model.maxa1=pyo.Param(initialize=100)
model.maxa2=pyo.Param(initialize=100)
model.maxa3=pyo.Param(initialize=100)

#Creating variables that we want to optimize
model.a1 = pyo.Var(within=pyo.NonNegativeReals)
model.a2 = pyo.Var(within=pyo.NonNegativeReals)
model.a3 = pyo.Var(within=pyo.NonNegativeReals)

#Declare the Objective
def Objective(model):
    return(50*model.a1+40*model.a2+30*model.a3)


model.OBJ=pyo.Objective(rule=Objective, sense=pyo.minimize)

#Create constraints
#Load and generation balance:
def Constraint_SysBalance(model):
    return(model.a1+model.a2+model.a3-model.l==0)


model.C0=pyo.Constraint(rule=Constraint_SysBalance) #legge til dette på alle

#Low limit generation
def Constraint_a1LowGenLimit(model):
    return(model.mina1-model.a1<=0)


model.C1min=pyo.Constraint(rule=Constraint_a1LowGenLimit)

def Constraint_a2LowGenLimit(model):
    return(model.mina2-model.a2<=0)


model.C2min=pyo.Constraint(rule=Constraint_a2LowGenLimit)

def Constraint_a3LowGenLimit(model):
    return(model.mina3-model.a3<=0)


model.C3min=pyo.Constraint(rule=Constraint_a3LowGenLimit)

#Max limit generation
def Constraint_a1MaxGenLimit(model):
    return(model.a1-model.maxa1<=0)


model.C1max=pyo.Constraint(rule=Constraint_a1MaxGenLimit)


def Constraint_a2MaxGenLimit(model):
    return(model.a2-model.maxa2<=0)


model.C2max=pyo.Constraint(rule=Constraint_a2MaxGenLimit)

def Constraint_a3MaxGenLimit(model):
    return(model.a3-model.maxa3<=0)


model.C3max=pyo.Constraint(rule=Constraint_a3MaxGenLimit)

opt = SolverFactory("gurobi_persistent")
#opt.options['NonCovex'] = 2
#model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
opt.set_instance(model)
results = opt.solve()
model.display()
#model.dual.display()