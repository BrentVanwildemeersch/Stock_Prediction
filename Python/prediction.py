import numpy as np
import matplotlib.pyplot as mpl
from sklearn.preprocessing import scale
from TFMLP import MLPR
#MLP imports
import tensorflow as tf


pth = '../apple_stock.csv'
A= np.loadtxt(pth,delimiter=",",skiprows=1,usecols=(1,4))
A=scale(A)

#y is the dependent variable
y=A[:,1].reshape(-1,1)
#A contains the independent variable
A = A[:,0].reshape(-1,1)


#Plot the high value of the stock price
mpl.plot(A[:,0],y[:,0])
mpl.ylabel("Stock Value")
mpl.xlabel("Date")
# mpl.show()


# number of neurons in the input layer
i=1
# number of neurons in the output layer
o = 1
# number of neurons in the hidden layer
h = 32
# the list of layer sizes
layers = [i,h,h,h,h,h,h,h,h,h,o]
mlpr = MLPR(layers, maxItr=1000, tol=0.4 , reg=0.001, verbose=True)


# length of the holdout period
nDays = 500
n = len(A)
# Learn the data
mlpr.fit(A[0:(n-nDays)],y[0:(n-nDays)])

# Begin prediction
yHat = mlpr.predict(A)
# Plot the results
mpl.plot(A,y,c="#f44242")
mpl.plot(A,yHat,c='#084c40')
mpl.show()





