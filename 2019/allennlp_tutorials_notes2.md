# An In-Depth Tutorial to AllenNLP (From Basics to ELMo and BERT)

- The basic AllenNLP pipeline is composed of:
  - DatasetReader: Extracts necessary information from data into a list of Instance objects
  - Model: The model to be trained 
  - Iterator: Batches the data
  - Trainer: Handles training and metric recording
  - (Predictor: Generates predictions from raw strings)
- Elements in AllenNLP are loosely coupled (松耦合的), meaning it is easy to swap different models and DatasetReaders in without having to change other parts.
- `DatasetReader`
  - Responsible for
    - Reading the data from disk
    - Extracting relevant information from the data
    - Converting the data into a list of Instances
  - Not a collection of data itself, but a **schema** for converting data on disk into lists of instances.
  - All we need to custom are
    - `__init__()`
    - `_read()`
    - `text_to_instance`
      - Take the data for a single example and pack into an `Instance` object.
- `Field`
  - Corresponds to inputs to a model.
  - Each field handles converting the data into tensors.
  - `TextField`
    - Converts a sequence of tokens into integers.
    - Takes an additional argument `TokenIndexer`.
  - `MetadataField`: takes data that is not supposed to be tensorized.
  - `ArrayField`: converts numpy arrays into tensors
- `Vocabulary`
  - built when iterating instances.
- `Iterator`
  - A few things have to be considered:
    - Sequences of different lengths need to be padded
    - To minimize padding, sequences of similar lengths can be put in the same batch
    - Tensors need to be sent to the GPU if using the GPU
    - Data needs to be shuffled at the end of each epoch during training, but we don't want to shuffle in the midst of an epoch in order to cover all examples evenly
  - `BucketIterator`
    - To prevent the batches from becoming deterministic, a small amount of noise is added to the lengths.
    - Responsible for numericalizing the text fields.
    - We pass the vocabulary so that the Iterator knows how to map the words to integers.
    - `iterator.index_with(vocab)`
    - A `schema` for how to convert lists of Instances into mini batches of tensors. (In Pytorch, iterators are direct sources of batches)
- `Model`
  - Returns a dictionary
  - Computes loss within the forward method during training
  - AllenNLP has a whole host of convenient tools for constructing models for NLP:
    - A token embedder
    - An encoder
    - (For seq2seq models) A decoder
  - `Embedder`
    - Maps a sequence of token ids (or character ids) into a sequence of tensors
  - `Encoder`
    - AllenNLP provides a handy wrapper called `PytorchSeq2VecEncoder` that wraps the LSTM so that it takes a sequence as input and returns the final hidden state, converting it into a Seq2VecEncoder
- `Trainer`
  - AllenNLP provies a Trainer class that removes the necessity of boilerplate code and gives us all sorts of functionality including access to TensorBoard.
- `Predictor`

## Practical Example

- Writing the pipeline so that we can iterate over multiple configurations, swap components in and out, and implement crazy architectures without making codebase exploded.
- To incorporate ELMo, we need to change two things:
  1. The token indexer
     * ELMo uses character-level features (`ELMoTokenCharacterIndexer`)
  2. The embedder

## Torchtext vs AllenNLP

- `Torchtext` is a lightweight framework that is completely agnostic to how the model is defined or trained. All it handles is the conversion of text files into batches of data that can be fed into models.
- AllenNLP is more of an all-or-nothing framework: either use all the features or use non of them.