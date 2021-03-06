import numpy as np
Pi=np.pi

#In these type of files (that end with the word "Model") we specify all the details needed for a model to be used by the program. In this file we are giving the details for a sixth degree polynomial of the form: F(q) = a6*q^6 + a5*q^5 + a4*q^4 + a3*q^3 + a2*q^2 + a1*q + a0

ModelName=["10DegreePoly"]

#Number of Parameters:
Pz=7

#Seed for the parameters:
ParS0=[1,-0.116,0.0083,0,0,0,0]

#Seed for parameters when fitting the optimal parameters
OptParS0=[0,0,0,0,0]

#These are the first part of the optimal parameters which in our case are fixed to give a radius of 0.84
FirstOptParam=[1,-0.1176]


##Function F(variable; parameters adjustable by data):
##Par is = [a0,a1,a2,a3,a4,a5,a6]
def F(q,Fpar):
    return Fpar[0]+q*Fpar[1]+Fpar[2]*q**2+Fpar[3]*q**3+Fpar[4]*q**4+Fpar[5]*q**5+Fpar[6]*q**6


#I am adding this version of the function to use the python function fitter because I was having problems with minimizing \chi2 with the scipy minimizer. The function fitter likes the function to have the structure F(x, parameter 1, parameter 2, .... )
def FNoList(q,a0,a1,a2,a3,a4,a5,a6):
    return F(q,[a0,a1,a2,a3,a4,a5,a6])

##These are the optimal parameters, those that have zero bias on the radius. In this case they are NOT given and they should be fitted by the data, so the line is disabled
#OptParams=[N.A.]


#This version of the function has its a0 and a1 fixed at 1 and -0.1176 so it can fit the other parameters. Together they will be the optimal parameters for a given dataset: those with minimum bias
def FOpt(q,a2,a3,a4,a5,a6):
    return F(q,[1,-0.1176,a2,a3,a4,a5,a6])


#Function F(variable[LIST]; parameters adjustable by data). This function returns the data as a list
def FList(qlistF,Fpar):
    Fvalin=np.array([])
    for j in range(len(qlistF)):
        Fvalin=np.append(Fvalin,F(qlistF[j],Fpar))
    return Fvalin

#The gradient of the function that is modeling the form factor. The third argument is the parameter index (if we are taking the derivative with respect to the first parameter for example)
def GradF(q,Fpar,iIndex):

    if iIndex==0:
        return 1

    
    else:
        return q**(iIndex)

    
#GradFList gives back a list of the gradients of the model evaluated at the different datapoints    
def GradFList(qvals,Fpar):
    gradlistFinj=np.array([])
    for iG in range(len(Fpar)):
        gradlistFinj=np.append(gradlistFinj,GradF(qvals[0],Fpar,iG))
    gradlistFin=gradlistFinj
    for jG in range(1,len(qvals)):
        gradlistFinj=np.array([])
        for iG in range(len(Fpar)):
            gradlistFinj=np.append(gradlistFinj,GradF(qvals[jG],Fpar,iG))
        gradlistFin=np.vstack((gradlistFin,gradlistFinj))
    return gradlistFin


#Hessian Matrix of the MODEL (not \chi2). This is used to calculate the Hessian of \chi2 since there is a term there proportional to second derivatives of F. 
def HessF(q,Fpar, iIndex, kIndex):
    return 0



#The radius as a function of the parameters
def ModelRadius(Fpar):
    return np.sqrt(-6*Fpar[1]/Fpar[0])

#The gradient of the radius as a function of the parameters. The second argument is the parameter index (if we are taking the derivative with respect to the first parameter for example)
def GradRadius(Fpar,index):
    if index==0:
        return  (np.sqrt(1.5))*(Fpar[1]*((((-Fpar[1])/Fpar[0])**-0.5)*(Fpar[0]**-2.)))
    if index==1:
        return -np.sqrt(3/(-2*Fpar[1]*Fpar[0]))
    if index>1:
        return 0






