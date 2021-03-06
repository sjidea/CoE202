# -*- coding: utf-8 -*-
"""note07e_ACTIVITY_NeuralNetwork_deeper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/100PSrvBSngYPea3P09LX4UWDDNPLSmmK

# [CoE202] note 07e. Neural Network (Numpy, 2 hidden layers)

- Class Date : 21.04.29.
- Office Hour : -----------
- If you have any questions, ask via KLMS Q&A board or come to TA office hour to get our help.
"""

# this is just an annotation
import numpy as np # this is for importing numpy library (and we will use abbreviation np for that)
import matplotlib.pyplot as plt # this is for importing matplotlib.pyplot (library for graph plot)
import scipy.io

# load data file from Google drive
from google.colab import drive
drive.mount("/content/drive")

mat = scipy.io.loadmat('/content/drive/My Drive/CoE202/note 6/data_nonlinear_classification2.mat')

data = mat['data']
label = mat['label']

# define our nonlinear classifier
class nonlinear_classifier():

    # set initial weights
    def __init__(self, W1_init, W2_init, W3_init, W4_init):
        super(nonlinear_classifier, self).__init__()
        self.W1 = W1_init
        self.W2 = W2_init
        self.W3 = W3_init
        self.W4 = W4_init
            
    # forward pass
    def forward(self, x):

        # xk : input, zk: Wxk+b, yk = h(zk) (h is the activation function) @ kth layer

        #################################################################################
        # ACTIVITY  : fill in this part 
        # layer by layer forward pass by calling self.forward_single_layer
        self.x1 = x  # input of the 1st layer = input of the network
        self.y1, self.z1 = self.forward_single_layer(self.W1, self.x1) 
        self.x2 = self.y1 # input of the 2nd layer is the output of the first layer
        self.y2, self.z2 = self.forward_single_layer(self.W2, self.x2)
        self.x3 = self.y2 # input of the 2nd layer is the output of the first layer
        self.y3, self.z3 = self.forward_single_layer(self.W3, self.x3)
        self.x4 = self.y3 # input of the 2nd layer is the output of the first layer
        self.y4, self.z4 = self.forward_single_layer(self.W4, self.x4)
        y = self.y4 # output of the network = output of the 2nd layer
        #################################################################################
        
        return y # return network output

    def backward(self, label):

        y = self.y4
        
        # calculate loss and accuracy 
        loss = cross_entropy(y, label)
        loss_avg = np.mean(loss)        
        prediction_threshold = (y>0.5)
        accuracy = np.mean(prediction_threshold==label)
        n_sample = label.shape[1]

        #################################################################################    
        # ACTIVITY  : fill in this part 
        # back-propagation
        # layer by layer backward pass by calling self.backward_single_layer
        dLdy = (y-label)/(y*(1-y))
        dLdy, dLdw4 = self.backward_single_layer(self.W4, self.x4, self.y4, dLdy)
        dLdy, dLdw3 = self.backward_single_layer(self.W3, self.x3, self.y3, dLdy)
        dLdy, dLdw2 = self.backward_single_layer(self.W2, self.x2, self.y2, dLdy)
        dLdy, dLdw1 = self.backward_single_layer(self.W1, self.x1, self.y1, dLdy)
        #################################################################################  

        return loss_avg, accuracy, dLdw1, dLdw2, dLdw3, dLdw4

    def forward_single_layer(self, W, x):

        # x : input, z: Wx+b, y = h(z) (h is the activation function)
     
        x_pad = np.concatenate( (x, np.ones((1, x.shape[1]))), axis=0) # x_pad = [x; 1]
        z = np.matmul(W,x_pad) # z = [W b] X x_pad
        y = 1/(1 + np.exp(-z)) # y = sigmoid(z)

        return y, z
    
    def backward_single_layer(self, W, x, y, dLdy):
        
        n_data = x.shape[1]

        dLdz = dLdy*y*(1-y) # backprop sigmoid
        x_pad = np.concatenate( (x, np.ones((1, x.shape[1]))), axis=0) # add ones (for bias term)
        dzdw = x_pad.T     # take transpose
        dzdx = W[:,:-1].T  # exclude bias part then transpose 

        dLdw = np.matmul(dLdz,dzdw)/n_data # divide by the number of data points (average)
        dLdx = np.matmul(dzdx,dLdz)
        
        return dLdx, dLdw    

    # update parameters
    def update(self, dW1, dW2, dW3, dW4):

        self.W1 = self.W1 + dW1
        self.W2 = self.W2 + dW2   
        self.W3 = self.W3 + dW3   
        self.W4 = self.W4 + dW4   


# define cross entropy loss
def cross_entropy(prediction, label):
    epsilon = 1e-10
    prediction = np.clip(prediction, epsilon, 1. - epsilon)
    ce = -( np.log(prediction) *label + np.log(1-prediction)*(1-label))
    return ce

# define a function to plot data
def show_data_binary_class(data, label):
    fig, ax = plt.subplots()
    ind = 0
    for color in ['tab:blue', 'tab:orange']:
        current_ind = np.where(label==ind)[1]
        x = data[0,current_ind]
        y = data[1,current_ind]
        ax.scatter(x, y, c=color, edgecolors='none')
        ind +=1

# initialize my classifier
W1_init = np.random.rand(4,2+1)
W2_init = np.random.rand(4,4+1)
W3_init = np.random.rand(4,4+1)
W4_init = np.random.rand(1,4+1)

my_classifier = nonlinear_classifier(W1_init, W2_init, W3_init, W4_init)

# show ground truth classification
print('ground truth')
show_data_binary_class(data, label)

# test our initial (untrained) classifier
prediction = my_classifier.forward(data)
prediction_threshold = (prediction>0.5)

# show the performance of untrained classifier
print('current classification')
show_data_binary_class(data, prediction_threshold)

# train nonlinear classifier
n_iter = 100000
learning_rate = 0.02
loss_iter = np.zeros(n_iter, dtype=float)
accuracy_iter = np.zeros(n_iter, dtype=float)
dW1, dW2, dW3, dW4 = 0, 0, 0, 0
beta = 0.9
useMomentum  = True
for iter in range(n_iter):

    prediction =  my_classifier.forward(data)
    [loss, accuracy, dLdw1, dLdw2, dLdw3, dLdw4] =  my_classifier.backward(label)
    if useMomentum:
        dW1 = dW1*beta -learning_rate*dLdw1
        dW2 = dW2*beta -learning_rate*dLdw2
        dW3 = dW3*beta -learning_rate*dLdw3
        dW4 = dW4*beta -learning_rate*dLdw4
    else:
        dW1 = -learning_rate*dLdw1
        dW2 = -learning_rate*dLdw2
        dW3 = -learning_rate*dLdw3
        dW4 = -learning_rate*dLdw4

    my_classifier.update(dW1, dW2, dW3, dW4)
    loss_iter[iter] = loss

    prediction_threshold = (prediction>0.5)
    accuracy_iter[iter] = accuracy

    if iter % 5000 == 0:
        print(loss)

# show loss during training
plt.plot( range(1,n_iter+1), loss_iter)  
plt.ylim((0, 2))

# show accuracy during training
plt.plot(  range(1,n_iter+1), 100*accuracy_iter)  
plt.ylim((0, 100))

# test our trained classifier
prediction = my_classifier.forward(data)
prediction_threshold = (prediction>0.5)

# show result from trained classifier
print('current classification')
show_data_binary_class(data, prediction_threshold)

Xtest = np.mgrid[-1:1:0.01, -1:1:0.01].reshape(2,-1)

prediction = my_classifier.forward(Xtest)
prediction_img = np.rot90(prediction.reshape(200, 200), k=1, axes=(0, 1))
plt.imshow(prediction_img)
