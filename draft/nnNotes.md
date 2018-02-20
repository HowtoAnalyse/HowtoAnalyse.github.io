1. What does a neuron compute?

A neuron computes a linearity (Wx + b) and then an activation g (sigmoid, tanh, ReLU, ...).


2. Suppose img is a (32,32,3) array, representing a 32x32 image with 3 color channels red, green and blue. How do you reshape this into a column vector?

x = img.reshape((32*32*3,1))

> "np.dot(a,b)" performs a matrix multiplication on a and b, whereas "a*b" performs an element-wise multiplication.

The tanh activation usually works better than sigmoid activation function for hidden units because the mean of its output is closer to zero, and so it centers the data better for the next layer. True


6. Suppose you have built a neural network. You decide to initialize the weights and biases to be zero. Which of the following statements is true?


Each neuron in the first hidden layer will perform the same computation. So even after multiple iterations of gradient descent each neuron in the layer will be computing the same thing as other neurons.

7. Logistic regression’s weights w should be initialized randomly rather than to all zeros, because if you initialize to all zeros, then logistic regression will fail to learn a useful decision boundary because it will fail to “break symmetry” False

Logistic Regression doesn't have a hidden layer. If you initialize the weights to zeros, the first example x fed in the logistic regression will output zero but the derivatives of the Logistic Regression depend on the input x (because there's no hidden layer) which is not zero. So at the second iteration, the weights values follow x's distribution and are different from each other if x is not a constant vector.

8. You have built a network using the tanh activation for all the hidden units. You initialize the weights to relative large values, using np.random.randn(..,..)*1000. What will happen?

when the inputs of a tanh is far from zero, its gradient is very close to zero (because of flat edges of tanh).

Z[1]
and A[1]
are quantities computed over a batch of training examples, not only 1.

1. Question 1
What is the "cache" used for in our implementation of forward propagation and backward propagation?

We use it to pass variables computed during forward propagation to the corresponding backward propagation step. It contains useful values for backward propagation to compute derivatives.

3. The deeper layers of a neural network are typically computing more complex features of the input than the earlier layers.


4. Vectorization allows you to compute forward propagation in an L
-layer neural network without an explicit for-loop (or any other explicit iterative loop) over the layers l=1, 2, …,L. False

Because in a deeper network, we cannot avoid a for loop iterating over the layers

7.During forward propagation, in the forward function for a layer l
you need to know what is the activation function in a layer (Sigmoid, tanh, ReLU, etc.). During backpropagation, the corresponding backward function also needs to know what is the activation function for layer l
, since the gradient depends on it. True

