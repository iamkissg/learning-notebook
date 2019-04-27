# A Recipe for Training Neural Networks

## Neural Net Training is a leaky abstraction

- Neural nets are not "off-the-shelf" technology the second you deviate slightly from training an ImageNet classifier. (旨在说明神经网络技术不是现成的, 即取即用的)

> Backprop + SGD does not magically make your network work. Batch norm does not magically make it converge faster. RNNs don’t magically let you “plug in” text. And just because you can formulate your problem as RL doesn’t mean you should. If you insist on using the technology without understanding how it works you are likely to fail (要懂背后的机理, 才能用好)

## Neural Negs Training Fails Silently

- Everything could be correct syntactically, but the whole thing isn't arranged properly, and it's really hard to tell. (看起来一切都是好的, 结果就怎么都不好, 还莫名其妙的)
- The "possible error surface"  is large, logical (as opposed to syntactic), and very tricky to unit test.
- Most of time it will train but silently work a bit worse. (不及预期)
- The qualities that in my experience correlate most strongly to success in deep learning are **patience** and **attention to detail**.

## The Recipe

- In general, build neural nets **from simple to complex**, and at every step of the way we make concrete hypotheses about what will happen, and then either validate them with an experiment or investigate until we find some issues.
- What we try to prevent very hard is the introduction of a lot of *"unverified" complexity (无法验证的复杂性)* at once, which is bound to introduce bugs / misconfigurations that will take forever to find (if ever).
- If writing neural net code was like training one (???), you'd want to use a very small learning rate and guess and then evaluate the full test set after every iteration.

### Become one with the data (从数据出发)

- Begin by thoroughly inspecting your data (先看数据):
  - Scanning through thousands of examples
  - Understanding their distribution
  - Looking for pattern
  - Looking for imbalance and biases
  - Paying attention to MY own process for classifying the data, which hints at the kinds of architectures we'll eventually explore.
- Look at network (mis)predictions and understand where they might be coming from. (检查预测结果)
  - If the network is giving some predictions that doesn't seem consistent with what you've seen in the data, something is off.
- Write some simple code to search / filter / sort by whatever you can think of, and visualize their distributions and outliers along any axis.
  - Outliers especially almost always uncover (揭示) some bugs in data quality or preprocessing.

### Setup the end-to-end training/validation skeleton + get dumb baselines (建立 pipeline, 模型的训练那都是后话)

- After understanding data, next step is to set up **a full training + evaluation skeleton (骨架) and gain trust in its correctness via a series of experiments**. (关键还是建立好一套流程, pipeline)

- It is best to pick some simple model that you couldn't possibly have screwed up somehow (以某种方式搞砸).

- **Train** the model, **visualize** the losses, any other metrics, model predictions, and perform a series of **ablation experiments** with explicit hypotheses along the way.

- Tips and tricks

  - Fix random seed (固定随机种子). This removes a factor of variation and will help keep you sane (明智的).
  - Simplify. Make sure to disable any unnecessary fanciness (花式). (简化, 不要花招)
    - As an example, definitely turn off any data augmentation at this stage, Data augmentation is a regularization   strategy that we may incorporate later, but for now it just another opportunity to introduce some dumb bug.
  - Add significant digits to your eval. When plotting the test loss run the evaluation over the entire (large) test set. Do not just plot test losses over batches and then rely on smoothing them in Tensorboard. We are in pursuit of correctness and are very willing to give up time for staying sane. (不是太懂这一条)
  - Verify loss @ init. Verify that your loss starts at the correct loss value.
    - E.g., if you initialize final layer correctly, you should measure `-log(1/n_class)` on a softmax at initialization. (如果初始化没问题, 一开始的预测就像随机选择, 可以通过统计来确认模型是否有问题)
    - The same default values can be derived for L2 regression, Huber losses, etc.
  - Init well. Initialize the final layer weights correctly. (初始化好最后一层的参数, 此处有经验可言)
    - E.g., if you are regressing some values that have a mean of 50, then initialize the final bias to 50.
    - If you have an imbalanced dataset of a ratio 1:10 of positives:negatives, set the bias on logits such that the network predicts probability of 0.1 at initialization.
    - Setting these correctly will speed up convergence and eliminate "hockey stick" (曲棍球棒) loss curves, where in the first few iteration the net is basically just learning the bias. (更快地收敛, 避免了刚开始的迭代只是在学习 bias)
  - Human baseline. Monitor metrics other than loss that are human interpretable and checkable (e.g. accuracy).
    - Whenever possible evaluate your own (human) accuracy and compare to it.
    - Alternatively, annotate the test data twice and for each example, treat one annotation as prediction and the second as ground truth. (不懂 ???)
  - Input-independent baseline (e.g., easiest is to just set all you inputs to zero) (不太懂)
    - This should perform worse than when you actually plug in your data without zeroing it out.
    - Does the model learn to extract any information out of the input at all?
  - Overfit one batch. To do so we increase the capacity of the model and verify that we can reach the lowest achievable loss. (过拟合, 确保模型的能力是足够的)
    - Visualize in the same plot both the label and the prediction, and ensure that they end up aligning perfectly once we reach the minimum loss.
  - Verify deceasing training loss. (确保训练损失有在下降)
    - At this stage you will hopefully be underfitting on your dataset because you're working with a toy model.
    - Try to increase its capacity just a bit. Does the training loss go down as it should?
  - Visualize prediction dynamics. (可视化预测结果的动态变化, 了解模型是如何一步步走到最后的)
    - The "dynamics" of how these predictions move will give you incredibly good intuition for how the training progresses.
    - Very low or very high learning rates are also easily noticeable in the amount of jitter (抖动).
  - Use backprop to chart (绘制) dependencies. 
    - When you use `view` instead of `transpose/permute` somewhere, you inadvertently (不经意间) mix information across the batch dimension. (`view` 是视图而已, 避免一个 batch 中的不同信息混起来)
    - One way to debug this (and other related problems) is to **set the loss for some example i to be 1.0, run the backward pass all the way to the input, and ensure that you get a non-zero gradient only on the i-th example.** (检查反向传播是否正常, 同一个批量内, 信息不要串起来)
    - More generally, gradients give you information about what depends on what in your network, which can be useful for debugging.
  - Generalize a special case.
    - Write a very specific function to what I'm doing right now, get that to work, and then generalize it later making sure that I get the same result. (不是太明白)

### Overfit

> At this stage, we should have a good understanding of the dataset and we have the full training + evaluation pipeline working. For any given model we can (reproducibly) compute a metric that we trust. We are also armed with our performance for an input-independent baseline, the performance of a few dumb baselines (we better beat these), and we have a rough sense of the performance of a human (we hope to reach this). The stage is now set for iterating on a good model. (基础工作已经完成, 地基已经打好)

1. Get a model large enough that it can overfit (i.e. focus on training loss)
2. Regularize it appropriately (give up some training loss to improve the validation loss)

> If we are not able to reach a low error rate with any model at all that may again indicate some issues, bugs, or misconfiguration.

- Pick the model.
  - Choose an appropriate **architecture** for the data.
    - Don't be a hero. Simply find the most related paper and copy paste their simplest architecture that achieves good performance. (老实点, 不要耍花招)
    - You're allowed to do something more custom later and beat this. (内功深厚了之后, 可以杂耍起来了)
  - Adam is safe. (Adam 为先)
    - Adam is much more forgiving to hyperparameters, including a bad learning rate.
    - For ConvNet, a well-tuned SGD will almost always slightly outperform Adam, but the optimal learning rate region is much more narrow and problem-specific.
    - **At the initial stage of your project, don't be a hero and follow whatever the most related papers do.**
  - Complexify only one at a time. (控制变量)
  - Do not trust learning rate decay defaults. (慎重对待学习率衰退, 是利器, 其实更要慎重)
    - If you are re-purposing (再利用) code from some other domain always be very careful with learning rate decay. Not only would you want to use different decay schedules for different problems, but even worse, in a typical implementation the schedule will be based current epoch number, which can be vary widely simply depending on the size of your dataset.
    - In my own work I always disable learning rate decays entirely (constant learning rate) and tune this all the way at the very end.

### Regularize

> Ideally, we are now at a place where we have a large model that is fitting at least the training set.

- Get more data.
  - It is a very common mistake to spend a lot engineering cycles trying to squeeze juice out of a small dataset when you could instead be collecting more data. (除非研究就是基于有限数据的算法, 否则, 数据就像韩信将兵, 多多益善)
  - As far as I am aware adding more data is pretty much the only guaranteed way to monotonically improve the performance of a well-configured neural network almost indefinitely (无限期). The other would be ensembles, but that tops out after ~5 models.
- Data augment.
  - The next best thing is to real data is half-fake data - try out more aggressive data augmentation. (前半句略懂, 后半句不懂)
- Creative augmentation.
  - Examples:
    - [Domain randomization](https://openai.com/blog/learning-dexterity/)
    - Use of [Simulation](http://vladlen.info/publications/playing-data-ground-truth-computer-games/)
    - Clever [Hybrids](https://arxiv.org/abs/1708.01642) such as inserting (potentially simulated) data into scenes, or even GANs.
- Pretrain
- Stick with supervised learning.
  - Do not get over-excited about unsupervised pretraining. (不要盲目相信无监督学习)
  - NLP seems to be doing pretty well with BERT and friends, quite likely owing to the more deliberate nature of text, and a higher signal to noise ratio. (**NLP,真是"读书百遍, 其意自现"**)
- Smaller input dimensionality.
  - Remove features that may contain spurious (伪) signal.
  - Any added spurious input is just another opportunity to overfit if your dataset is small.
  - If low-level details don't matter much try to input s smaller image.
- Smaller model size. (看似和最后一条矛盾, 但此处强调运用领域知识来减小模型, 应为去掉不必要部分)
  - In many cases you can use domain knowledge constraints on the network to decrease its size.
- Decrease the batch size
  - Due to the normalization inside batch norm, smaller batch sizes somewhat correspond to stronger regularization. This is because the batch empirical mean/std are more approximate versions of the full mean/std so the scale & offset "wiggles" (晃) your batch around more. (使用 BN, 更小的 batch 能提供更强的正则化效果)
- Drop
  - Use this sparingly (保守地) / carefully because dropout [does not seem to play nice](https://arxiv.org/abs/1801.05134) with batch normalization. (Dropout 与 BN 的相爱相杀)
- Weight decay.
  - Increase the weight decay penalty.
- Early stopping
- Try a larger model.
  - I've found a few times in the past that larger models will of course overfit much more eventually, but their "early stopped" performance can often be much better than that of smaller models

> - Visualize the network's first-layer weight and ensure you get nice edges that make sense. If the first layer filters look like noise then something could be off. (CV)
> - Activations inside the net can sometimes display odd artifacts and hint at problems.

### Tune

> You should now be "in the loop" with your dataset exploring a wide space for architectures that achieve low validation loss.

- Random over grid search. (随机搜索代替网格搜索)
  - It is [best to use random search instead](http://jmlr.csail.mit.edu/papers/volume13/bergstra12a/bergstra12a.pdf) of grid search for simultaneously tuning multiple hyperparameters.
  - Intuitively, this is because neural nets are often much more sensitive to some parameters than others.
- Hyper-parameter optimization. (不知道算不算 AutoML 之流, [参考列表](https://medium.com/@mikkokotila/a-comprehensive-list-of-hyperparameter-optimization-tuning-solutions-88e067f19d9))
  - Bayesian hyper-parameter optimization toolboxes.

### Squeeze out the juice

> Once you find the best types of architectures and hyper-parameters you can still use a few more tricks to squeeze out the last pieces of juice out of the system.

- Ensembles.
  - If you can't afford the computation at test time look into distilling your ensemble into a network using [dark knowledge](https://arxiv.org/abs/1503.02531). (笑死我了, 就是 Model distillation)
- Leave it training.