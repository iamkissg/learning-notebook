# How to solve 90% of NLP problems: a step-by-step guide

1. Gather your data
2. Clean your data
   * Your model will only ever be as good as your data
   * A clean dataset will allow a model to learn meaningful features and not overfit on irrelevant noise
   * A example checklist for cleaning data:
     1. Remove all irrelevant characters such as any non alphanumeric characters
     2. Tokenize text by separating it into individual words
     3. Remove words that are not relevant, such as "@" twitter metions or urls
     4. Convert all characters to lowercase
     5. Consider combining misspelled or alternately spelled words to a single representation
     6. Consider lemmatization (reduce words such as "am", "are", "is" to a common form such as "be")
3. Find a good data representation
   * Visualizing the embeddings
4. Classification
   * Start with the simplest tool that could solve the job
   * We should never ship a model without trying to understand it
5. Inspection
   * Toolbox:
     * Confusion Matrix: if the priority is to react to every potential event, we would want to lower false negatives
   * Explaining and interpreting model
     * Plotting word importance: It's important to look at which words it is using to make decisions
6. Accounting for vocabulary structure
   * TF-IDF
7. Leveraging `semantics`
   * Word vectors
   * Sentence level representation
   * Cons: losing explainability
   * Toolbox
     * LIME - a black box explainer that allows users to explain the decision of any classifier on one particular example by perturbing (扰乱) the input and seeing how the prediction changes
8. Leveraging `syntax` using end-to-end approaches

## In general

- Start with a quick and simple model
- Explain its predictions
- Understand the kind of mistakes it is making
- Use that knowledge to inform your next step, whether that is working on your data, or a more complex model

