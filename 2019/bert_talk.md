# BERT Talk

## Pre-trained word embeddings

- Problem: word embeddings are applied in a context free manner
- Solution: train contextual representations on text corpus

## History of Contextual Representations

- Semi-supervised Sequence Learning
  - Train LSTM language model
  - Fine-tune on classification task
- ELMo
  - Train separate left-to-right and right-to-left LMs
  - Apply as "pre-trained embeddings"
- Improving Language Understanding by Generative Pre-Training
  - Train deep transformer LM
  - Fine-tune on classification task

## Problems with Previous Methods

- Problem: Language models only use left context or right context, but language understanding is bidirectional
- Why are LMs unidirectional?
- Reason 1: directionality is needed to generate a well-formed probability distribution. (???)
- Reason 2: Words can "see themselves" in a bidirectional encoder. (see themselves ???)
- Unidirectional context build representation *incrementally*; bidirectional context words can *"see themselves"*

## Masked LM

> Mask out k% of the input words, and then predict the masked words

- Problem 1: Too little masking: too expensive to train ; too much masking: not enough context
- Problem 2: mask token never seen at fine-tuning
- Solution 2: 15% of the words to predict, but don't replace with `[MASK]` 100% of the time. Instead:
  - 80% of the time, replace with `[MASK]`
  - 10% of the time, replace random word
  - 10% of the time, keep same

## Next Sentence Prediction

- To learn relationships between sentences, predict whether Sentence B is actual sentence that proceeds Sentence A, or a random sentence

## Input Representation

- `WordPiece` vocabulary
- Each token is sum of `token embedding`, `segment embedding`, and `position embedding`
- Single sequence is much more efficient???

## Model Architecture

- Transformer encoder
  - Multi-head self attention
    - Models context
  - Feed-forward layers
    - Computes non-linear hierarchical features
  - Layer norm and residuals
    - Makes training deep networks healthy (???)
  - Positional embeddings
    - Allows model to learning relative positioning
- Empirical advantages of Transformer vs. LSTM:
  - Self-attention == no locality bias
    - Long-distance context has "equal opportunity"
  - Single multiplication per layer == efficiency on TPU
    - Effective batch size is number of words, not sequences (???)

## Effect of Modules

- Effect of pre-training task
  - `Masked LM` is very important on some tasks, `Next Sentence Prediction` is important on other tasks.
  - Left-to-right model does very poorly on word-level task (SQuAD ???).
- Effect of directionality and training time
  - Masked LM takes slightly longer to converge. But absolute results are much better almost immediately.

## Common questions

- ELMo-style shallow bi-directionality
  - Advantage: slightly faster training time
  - Disadvantages:
    - Will need to add non-pre-trained bidirectional model on top
    - right-to-left SQuAD model does not see question
    - Need to train two models
    - Off-by-one: LTR predict next word, RTL predicts previous word
    - Not trivial to add arbitrary pre-training tasks
- Why wasn't contextual pre-training popular before 2018 with ELMo?
  - Good results on pre-training is > 1,000x to 100,000x expensive than supervised training
    - E.g., 10x-100x bigger model trained for 100x-1,000x as many steps
  - The model mush be learning more than "contextual embeddings" OR predicting missing words requires learning many types of language understanding features
    - syntax, semantics, pragmatics, coreference, etc.
  - Implication: pre-trained model is much bigger than it needs to be to solve specific task
  - Task-specific model distillation words very well
- Is modeling "solved" in NLP OR is is there a reason to come up with novel model architectures?
  - Examples of NLP models that are not "solved":
    - Models that minimize total training cost vs. accuracy on modern hardware
    - Models that are very parameter efficient (e.g., for mobile deployment)
    - Models that represent knowledge/context in latent space
    - Models that represent structured data (e.g., knowledge graph)
    - Models that jointly represent vision and language
- Personal belief: near-term improvements in NLP will be mostly about making clever use of "free" data.
  - Unsupervised vs. semi-supervised vs. synthetic supervised is somewhat arbitrary
  - "Data I can get a lot of without paying anyone" vs. "Data I have to pay people to create" is more pragmatic (实用主义的) distinction.
- No less "prestigious" (有名望的) than modeling paper
  - Phrase-based & Neural unsupervised machine translation
- Empirical results from BERT are great, but biggest impact on the field is:
  - With pre-training, bigger == better, without clear limits
  - Unclear if adding things on top of BERT really helps by very much