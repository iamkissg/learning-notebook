# Checklist for debugging neural networks

* Start simple
  * Build a simpler model first
    * Build a small network with a single hidden layer and verify that everything is working correctly
    * Gradually  add model complexity
  * Train model on a single data point
    * Use one or two training data points to confirm whether the model is able to overfit
    * Try again for a single (or a few) epochs before progressing
* Confirm loss
  * Make sure that
    * Loss is appropriate for the task
    * Loss functions are being measured on the correct scale, especially when using more than one type of losses, make sure all losses are scaled properly
  * Pay attention to initial loss, check to see if that initial loss is close to expected loss if model started by guessing randomly
* Check intermediate outputs and connections
  * You may be running errrors around:
    * Incorrect expression for gradient updates
    * Weight updates not being applied
    * Vanishing or exploding gradients
  * If gradients values are zeros, it could mean that the learning rate might be too small or expressions for gradient updates are incorrect
  * Make sure to monitor the magnitudes of activations, weights, and updates of each layer match
    * the magnitude of the updates to the parameters should be ~1e-3.
  * Use gradient checking to check for these errors by approximating the gradient using a numerical approach.
  * Visualizing neural network:
    * Preliminary methods: show the overall structure of a trained model, including printing out shapes or filters of individual layers and parameters in each layer
    * Activation based methods: decipher the activation of the individual neurons or a group of neurons
    * Gradient based methods: manipulate the gradients that are from a forward and backward pass while training
    * (Tools: ConX, Tensorboard)
* Diagnose parameters
  * Batch size: large enough to have accurate estimates of error gradient but small enough that SGD can regularize the model.
    * ([On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima](https://arxiv.org/abs/1609.04836): when using a larger batch there is a degradation in quality of model. Large batch methods tend to converge to sharp minimizers of the training and testing functions, thus poor generalization)
  * Learning rate: consider incorporating learning rate scheduling to decrease learning rate as training progresses.
  * Gradient clipping: clip parameters' gradients during back propagation by a maximum value or maximum norm. Useful for addressing any exploding gradients.
  * Batch normalization: normalize the inputs of each layer in order to fight the  internal covariate shift problem
  * SGD: a recommended starting point is Adam or plain SGD with Nesterov momentum.
  * Regularization: significantly reduces the variance of the model without substantial increase in bias
  * Dropout: if using dropout and batch normalization together, be cautious  of the order of these operations.
    * Dropout is meant to block information from certain neurons completely to
      make sure the neurons do not co-adapt. So, the batch normalization has 
      to be after dropout otherwise you are passing information through 
      normalization statistics. (https://stackoverflow.com/questions/39691902/ordering-of-batch-normalization-and-dropout)
    * Theoretically, we find that Dropout would shift the variance of a 
      specific neural unit when we transfer the state of that network from 
      train to test. However, BN would maintain its statistical variance, 
      which is accumulated from the entire learning procedure, in the test 
      phase. The inconsistency of that variance (we name this scheme as 
      “variance shift”) causes the unstable numerical behavior in inference 
      that leads to more erroneous predictions finally, when applying Dropout 
      before BN.  ([Understanding the Disharmony between Dropout and Batch Normalization by Variance Shift](https://arxiv.org/abs/1801.05134))
* Tracking work
  * Tools like comet.ml can help automatically track datasets, code changes, experimentation history and production models
  * Tracking your work is the first step you can take to begin standardizing your environment and modeling workflow.