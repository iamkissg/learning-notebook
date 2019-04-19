# Practical NLP for the Real World

> In theory, there is no difference between theory and pratice; but in practice, there is.

## Toolbox

### Vectorize

- My kingdom for a vector
	- How to feed model data
- Vectorize words
- Vectorize sentences

### Visualization

> Have vectors captured any meaning?

- Bag of words (PCA)
- TF-IDF (PCA)
- Word2Vec (PAC)

### Validation

- Inspect the model
	- Simple models = Meaningful coefficients
- Inspect the data
	- Use vectorization
- Inspect the errors

### Deep Dive

- UMAP plot of labels
  - Finding outliers
  - Duplicated data?
  - Wrong label?
- Clean data, easy ML
- The metrics are as good as the data
  - How to find out about the quality of data?
    - Easy way: inspect the data
    - Hard way: Deploy to production and hope
- Complex models
  - Some models can build sentence vectors allowing them to preserve order
  - The can leverage knowledge from an outside corpus
  - This makes them harder to debug and validate
  - CNN
    - Shallow network
    - Leverages word order
    - Fast and simple
  - Language models
    - Pre-trained versions avaliable
    - Slow inference
    - Even slower fine-tuning
  - Transfer Learning Works
    - Transfer learning with BERT vs. Training custom word vectors with FastText
- How to debug end-to-end models
  - Validation - [LIME](https://github.com/marcotcr/lime)
    - Individual example
    - Aggregate
      - Finding common explainers
- Error analysis
  - Visualize the topology of errors
  - Examining errors
  - Labeling conflicts
    - Solution -> Relabel those examples
  - Duplicates (+conflicts)
  - Data gaps
    - Solution -> get more data to disambiguate jokes from  disasters
  - Clear priorities
    1. Solve data duplicates and conflicting data
    2. Fix inaccurate labels
    3. ...
    4. We could benefit from knowledge about context, using pre-trained LMs

### Miscellaneous

- A better dataset solves more problems than any model
- Testing
  - Test distributions
    - Data inputs
    - Model outputs
  - Test model state (Tensorboard)
- Many flavors
  - Learning Context (word2vec) + Learning Frequency => Glove + Learning syntax => Cove
- Make it supervised
  - Richard Socher: Rather than spending a month figuring out an unsupervised machine learning problem, just label some data for a week and train a classifier.