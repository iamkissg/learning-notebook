# Choosing the right Machine Learning Algorithm

* Understand your data
  * (Naive Bayes works well with categorical input but is not at all sensitive to missing data)
  * Know your data
    * Look at Summary statistics and visualizations
      * Percentiles can help identify the range for most of the data
      * Averages and medians can describe central tendency
      * Correlations can indicate strong relationships
    * Visualize the data
      * Box plots can identify outliers
      * Density plots and histograms show the spread of data
      * Scatter plots can describe bivariate relationships
  * Clean your data
    * Deal with missing value. Missing data affects some models more than others. Even for models that handle missing data, they can be sensitive to it 
    * Choose what to do with outliers
      * Outliers can be very common in multidimensional data
      * Some models are less sensitive to outliers than others. Usually tree models are less sensitive to the presence of outliers. However, regression models, or any model that tries to use equations, could definitely be effected by outliers.
      * Outliers can be the result of bad data collection, or they can be legitimate (合法的) extreme values.
    * Does the data needs to be aggregated
  * Augment your data
    * Feature engineering is the process of going from raw data to data that is ready for modeling
      * Make the models easier to interpret
      * Capture more complex relationships
      * Reduce data redundancy and dimensionality
      * Rescale variables
    * Different models may have different feature engineering requirements. Some have built in feature engineering.
* Categorize the problem
  * Categorize by input:
    * If you have labeled data, it's a supervised learning problem
    * If you have unlabeled data and want to find feature structure, it's an unsupervised learning problem
    * If you want to optimize an objective function by interacting with an environment, it's a reinforcement learning problem
  * Categorize by output
    * If the output of model is a number, it's a regression problem
    * If the output of model is a class, it's a classification problem
    * If the output of model is a set of input groups, it's a clustering problem
    * Do you want to detect an anomaly (异常)?
* Understand your constraints
  * What is the data storage capacity?
  * Does the prediction have to be fast?
  * Does the learning have to be fast?
* Find the available algorithms
  * Some of the factors affecting the choice of a model:
    * Whether the model meets the business goals
    * How much pre-processing the model needs
    * How accurate the model is
    * How explainable the model is
    * How fast the model is: How long does it take to build a model, and how long does the model take to make predictions
    * How scalable the model is
  * An important criteria affecting choice of algorithm is model complexity. A model is more complex is:
    * It relies on more features to learn and predict
    * It relies on more complex feature engineering
    * It has more computational overhead
    * The same algorithm can be made more complex based on the number of parameters or the  choice of some hyperparameters:
      * A regression model can have more features, or polynomial terms and interaction terms
      * A decision tree can have more or less depth
      * ...
* Commonly used machine learning algorithms
  * Linear Regression
    * This kind of model is unstable in case features are redundant
    * Can be used to:
      * Time to go from one location to another
      * Predicting sales of particular product next month
      * Impact of blood alcohol content on coordination
      * Predict monthly gift card sales and improve yearly revenue projections
  * Logistic Regression
    * Provide a nice probabilistic interpretation
    * Can be used to:
      * Predicting the Customer Churn (客户流失)
      * Credit Scoring & Fraud Detection
      * Measuring the effectiveness of marketing campaigns
  * Decision trees
    * Decision trees easily handle feature interactions and they are non-parametric so we do not have to worry about outliers or whether the data is linearly separable.
    * But they do not support online learning. Every time we have to rebuild trees when new examples come on.
    * Also they easily overfit.
    * They take a lot of memory (the more features you have, the deeper and larger the decision trees are)
    * Can be used to:
      * Investment decisions
      * Customer churn
      * Banks loan (贷款) defaulters (违约者)
      * Build vs Buy decisions
      * Sales lead qualifications
    * K-means
      * The biggest disadvantage is the choice of K
    * Principal component analysis (PCA)
      * Sometimes you have a wide range of features, probably highly correlated between each other, and models can be easily overfit on a huge amount of data.
      * In addition to the low-dimensional sample representations, PCA provides a synchronized (同步的) low-dimensional representations of the variables #???
    * Support Vector Machine
      * Widely used when data has exactly two classes.
      * Especially popular in text classification problems where very high-dimensional spaces re the norm.
      * Advantages: high accuracy, nice theoretical guarantees regarding overfitting, work well even the data is not linearly separable in the base feature space
      * Disadvantages: memory-intensive, hard to interpret, difficult to tune
      * Can be used to:
        * Detecting persons with common diseases such as diabetes
        * Hand-written character recognition
        * Text categorization
        * Stock market price prediction
    * Naive Bayes
      * Easy to build and particularly useful for very large datasets
      * Good choice when CPU and memory resources are a limiting factor
      * If the NB conditional independence assumption holds, a NB classifier will converge quicker than discriminative models
      * Even if the NB assumption does not hold, a NB classifier still often does a great job in practice
      * The main disadvantage is that it cannot learn interactions between features.
      * Can be used to:
        * Sentiment analysis and text classification
        * Recommendation systems like Netflix, Amazon
        * To mark an email as spam or not
        * Face recognition
    * Random Forest
      * It helps identify most significant variables from input
      * Highly scalable to any number of dimensions and has generally quite acceptable performances
      * There are genetic algorithms, which scale admirably well to any dimension and any data with minimal knowledge of the data itself, with the most minimal and simplest implementation being the microbial genetic algorithm
      * Can be used to:
        * Predict patients for high risks
        * Predict parts failures in manufacturing
        * Predict loan defaulters
    * Neural Networks