import tensorflow as tf
import numpy as np

# Create the MLP variables for TF graph
# _X : The input matrix
# _W : The weight matrix
# _B : The bias vectors
# _AF : The activation function

def _CreateMLP(_X,_W,_B,_AF):
    n=len(_W)
    for i in range (n-1):
        _X = _AF(tf.matmul(_X,_W[i])+ _B[i])
    return tf.matmul(_X,_W[n-1])+ _B[n-1]


# Add L2 regularizers for the weight and bias matrices
# _W : weight matrices
# _B : bias matrices
# return : tensorflow variable representing L2 regularization cost
def _Create2Reg(_W,_B):
    n=len(_W)
    regularizers = tf.nn.l2_loss(_W[0])+ tf.nn.l2_loss(_B[0])
    for i in range(1,n):
        regularizers += tf.nn.l2_loss(_W[i])+ tf.nn.l2_loss(_B[i])
    return regularizers


# Create weight and bias vectors for an MLP
# layers : The number of neurons in each layer( including input and output)
# return : a tuple of lists of the weight and bias matrices respectivily
def _CreateVars(layers):
    weigth=[]
    bias =[]
    n = len(layers)
    for i in range(n-1):
        lyrstd = np.sqrt(1.0/layers[i])
        curW = tf.Variable(tf.random_normal([layers[i],layers[i+1]], stddev=lyrstd))
        weigth.append(curW)
        curB = tf.Variable(tf.random_normal([layers[i+1]],stddev=lyrstd))
        bias.append(curB)
    return(weigth,bias)
        # Fan in for layer; used as standard dev


# Helper function for selecting an activation function
# name : The name of the activation function
# return :  A handle for the tensorflow activation function
def _GetActiveFn(name):
    if name == 'tanh':
        return tf.tanh
    elif name=='sig':
        return tf.sigmoid
    elif name == 'relu':
        return tf.nn.relu
    elif name =='relu6':
        return tf.nn.relu6
    elif name =='elu':
        return tf.nn.elu
    elif name=="softplus":
        return tf.nn.softplus
    elif name=='softsign':
        return tf.nn.softsign
    return None


# Gives the next batch of samples of size self.batSz or the remaining
# samples if there are not that many
# A : samples to choose from
# y : targets to choose from
# cur : next sample to use
# batSz : size of the batch
# return : A tuple of the new samples and targets
def _NextBatch(A,y,cur,batsZ):
    m=len(A)
    nxt = cur + batsZ
    if(nxt>m):
        nxt=m
    return (A[cur:nxt],y[cur:nxt])

# Multi layer perceptron for regression
class MLPR :
    # Predicte outputs
    pred= None
    # loss function
    loss = None
    # the optimization method
    optmzr = None
    # Max number of iterations
    mItr= None
    # error tolerance
    tol = None
    # Tensorflow session
    sess = None
    # input placeholder
    x = None
    # output placeholder
    y=None
    # boolean for toggling verbose output
    vrbse = None
    # batch size
    batSz = None

    # The constructor
    # param layers : A list of layer sizes
    # param actvFn: the activation function to use
    # param learnRate : The learning rate parameter
    # param decay : the decay paramater
    # param maxItr : maximum number of interations
    # param tol : Maximum error toleratod
    # param batchSize : Size of training batches to use (use all if none)
    # param verbose : Print training information
    # param reg: Regularization weight

    def __init__(self,layers,actvFn='tanh', learnRate=0.001, decay=0.9, maxItr = 2000
            ,tol = 1e-2, batchSize= None, verbose = False,reg=0.001):
        self.tol = tol
        self.mItr = maxItr
        self.vrbse = verbose
        self.batSz = batchSize

        # input size
        self.x = tf.placeholder("float",[None,layers[0]])
        # Output Size
        self.y = tf.placeholder("float",[None,layers[-1]])
        # Setup weight and bias variables
        weight,bias = _CreateVars(layers)
        # Creat the tensorflow MLP model
        self.pred = _CreateMLP(self.x, weight,bias,_GetActiveFn(actvFn))
        # use L2 as the cost function
        self.loss = tf.reduce_sum(tf.nn.l2_loss(self.pred-self.y))
        # use regularization to prevent over fitting
        if(reg is not None):
            self.loss += _Create2Reg(weight,bias)*reg
        # use ADAM method to minimize the loss function
        self.optmzr = tf.train.AdamOptimizer(learning_rate=learnRate).minimize(self.loss)
        self.sess = tf.Session()
        init = tf.initialize_all_variables()
        self.sess.run(init)
    # Fit the MLP to the data
    # param A : numpy matrix where each row is a sample
    # param y : numpy matrix of target values

    def fit(self,A,y):
        m=len(A)
#         Begin training
        for i in range(self.mItr):
            if(self.batSz is None):
                self.sess.run(self.optmzr, feed_dict={self.x:A,self.y:y})
            else:
                for j in range(0,m,self.batSz):
                    batA, batY = _NextBatch(A,y,j,self.batSz)
                    self.sess.run(self.optmzr,feed_dict={self.x:A,self.y:y})
            err = np.sqrt(self.sess.run(self.loss,feed_dict={self.x:A,self.y:y}))
            if(self.vrbse):
                print("Iter {:5d}\t{:.8f}".format(i+1,err))
            if(err<self.tol):
                break


#     Predict the output of the given input( only run after calling fit)
#     Param a : input values for which to predict outputs
# return  the predicted output values
    def predict(self,A):
        if(self.sess==None):
            print("Error: MLP has not yet been fitted")
            return None
        res = self.sess.run(self.pred, feed_dict={self.x:A})
        return res




