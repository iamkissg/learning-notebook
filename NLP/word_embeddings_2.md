## Word Embeddings in 2017

### Subword-level embeddings

* `Subword-level information` 对 word embeddings 很有帮助. (但不适用于中文) 大多利用了 subword-level information 的模型, 以 CNN 或 BiLSTM 作为输入层, input the characters of a word, 再输出 a character-based word representation.
* 要将 character information 注入 pre-trained embeddings, 使用 character n-grams features 比 composition over individual characters 效果更好. FB 的 fastText classifier 正是基于此的.
* Sennrich et al 2016 的研究表明, 用于 Subword units based on byte-pair encoding 替换普通的 inputs units, `Machine Translation, MT` 的结果特别好.
* 使用 Subwords 的另一个好处是, 对于训练集中未出现, 或拼写错误的单词, 也能做出较好的分类.
* 使用集成 character information 的 pre-trained embeddings 的一种方法是, 使用在大量`相关领域, in-domain`的语料上训练好的 state-of-the-art `Language Model, LM`.
* LM is useful for different tasks as auxiliary objective (居然不知道何从翻起), `pre-trained LM embeddings` 能用于增强 word embeddings. 当我们对如何进行预训练和初始化模型有了更好的理解, pre-trained LM embeddings 被证明是更好的, 甚至可能取代 word2vec 作为 word embeddings 的首先.

### OOV handing

* 使用 pre-trained word embeddings 的一个主要问题是, 无法处理 `out-of-vocabulary, OOV` words. 过去的做法是, 所有 OOV 单词都用 UNK (unknown) 表示, 因此被 encode 成相同的向量. 当语料中存在大量 OOV 单词时, 这种做法是有害的. Subword-level embeddings 能减缓这个问题.
* Herbelot & Baroni (2017) 通过将 OOV 单词的 embeddings 初始化为 context words 的向量和, 然后使用高学习率快速修正这个 embeddings 来处理 OOV 问题. 该方法对于明确需要对`杜撰词, nonce word`建模的数据集特别有效, 能否可靠地应用于更多 NLP 问题还不清楚.
* Pinter et al (2017) 提出的方法是, 训练一个 character-based model to explicity re-create pre-trained embeddings, 以此来生成 OOV word embeddings. 该方法在资源有限, 无法使用大型语料, 只能使用 pre-trained embeddings 的情况下特别有效.

### Evaluation

* Evaluation of pre-trained embeddings 一直备受争议. 因为 wod embeddings 在 word similarity 或 analogy (两个常用的评估指标) 性能, 被证明与 downstream performance 间只有很弱的联系. (Tsvetkov et al. 2015)
* The RepEval Workshop at ACL 2016 讨论了 evaluate pre-trained embeddings 更好的方式. 结果是, pre-trained embeddings 能在 intrinsic task (intrinsic 是固有的意思, 其实就是原任务) 上 evaluate, 但最好的方式是在 downstream tasks 上进行 extrinsic evaluatoin.

### Multi-sense embeddings

* Word embeddings 的另一个问题是, 不能捕获多义词的多个意思. A tutorial at ACL 2016 指出, 近年来的研究都专注于在不同场景下, 为同一个单词学习不同的 embeddings. 但是, 大多数方法都只在 word similiarity 层面上进行了 evaluation.
* Pilehvar et al (2017) 首次将 topic categorization 作为 downstreamtask. 实验中, multi-sense embeddings 的性能比随机初始化 word embeddings 要好, 但不如 pre-trained word embeddings.
* 最近的研究表明, 目前的 word embedding 模型具有足够的表达能力, 能依据上下文信息消除歧义, 而不必依赖 multi-sense embeddings 或者 dedicated disambiguation pipeline.

### Beyond words as points

* 将单词 reduce 成向量空间的一个点是过分简化的做法, 会丢失一些有用的细节. 基于这个思想, Vilnis & McCallum (2015) 提出了将每个单词建模为一个概率分布的方法, 这样就能为每一维分配`概率质量, probability mass`和`不确定性, uncertainty`.
* Athiwaratkun & Wilson (2017) 将以上方法扩展到 multimodal distribution, 这就能处理`一词多义, polysemy`, entailment, uncertainty 等问题, 并提高`可解释性, interpretability`.
* 不同于以上方法, Nickel & Kiela (2017) embed word in a `双曲空间, hyperbolic space`, 来学习`分层表示, hierarchical representations`.
* A compelling research direction 是寻找其他的 word representations, 符合`语言学假设, linguistic assumptions`, 或能更好地处理 downstream tasks.

### Phrases and Multi-word expressions

* 除了无法处理一词多义问题外, word embeddings 不能 capture `词组的意思, meanings of phrases` and `短语的表达, multi-word expressions`. Multi-word expressions 可能是组成它的各个词的意思的组合函数, 也可能具有全新的意思.
* Mikolov et al. (2013) 在 word2vec 的论文中就提出了 Phrase embeddings 的方法, 简单地说就是用一个 token 来表示 phrase, 其他与 word embeddings 无异. 之后又有研究旨在学习更好的 compositional 和 non-compositional phrase embeddings.
* 然而, explicitly modelling phrases 对于 downstream tasks 没有显著的提升效果.

### Bias

* `偏见, bias`在 word embedding models 中正成为越来越严峻的问题. 在 Google News 的文章上训练的 word embeddings 展现了男女性别的刻板印象, 甚至到了恼人的程度. (Bolubasi et al. 2016)
* 理解其他 word embeddings 习得的偏见, 并找到更好的方式去除这些偏见是开发 fair algorithms for NLP 的关键.

### Temporal Dimension

* 文字是时代精神的镜子, 它们的意义是不断不变化的. 目前的文字表现形式可能与过去和未来的使用有很大不同.
* 因此在 NLP 中有一个研究方向是, 考虑`时间维度, temporal dimensioni`以及`文字的历时性, diachronic nature of words`. 这揭示了`语义, semantic`变化的规律, 对单词在时间维度上的类比及相关性进行了建模, 捕获了语义联系的动态变化.

### Lack of theoretical understanding

* 在 NLp 研究领域, 很少有研究能提供对 word embeddings sapce 及其属性 (比如, 类比关系) 的理论理解.
* Arora et al (2016) 提出了用于 word embeddings 的新型 generative model, 其将语料的生成视作在 discourse vector 间的随机漫步, 由此建立了针对 word analogy 的一些理论动机.
* Gittens et al. (2017) 为 additive compositonality 提供了更加彻底的理论依据, 证明了 skip-gram word vector 从信息论的视角来看是最优的.
* Mimno & Thomson (2017) 更彻底地揭示了 word emddings 与 the embeddings of context words 间的联系: word embeddings 不是均匀地散布在向量空间的, 而是处在与 context word embeddings 截然相反的狭小空间中.

### Task and domain-specific embeddings

* 使用 pre-trained embeddings 的一个主要不足是, 常用的新闻语料训练所得的 embeddings 不太适用于其他领域.
* Lu & Zheng (2017) 提出了 regularized skip-gram model, 用于学习`cross-domain, 跨领域`的 embeddings.
* 因此一个研究方向是, 以更好的方式对 pre-trained embeddings 进行调整, 使其适应新领域或将多个相关领域的知识联系起来.
* 另一种适应新领域的方法是, 使用`语义词典, semantic lexicons`中的现有知识中与任务相关的信息去增强 pre-trained embeddings. 一个有效的方法是 retro-fitting (文中没有更多描述了). retro-fitting 还被扩展到其他领域, 如 ConceptNet, intelligent selection of positive and negative samples.
* 将先验知识注入 word embeddings 是一个重要的研究方向, 将使得模型更鲁棒, 先验知识包括 monotonicity(You et al. 2017), word similarity(Niebler et al. 2017), logical relations, task-related grading or intensity 等等
* 除了在 NLP 中应用广泛之外, word embeddings 还被应用于 information retrieval, recommendation, link prediction in knowledge bases 等. Wu et al (2017) StarSpace: Embed All The Things! 提出了一个通用模型, 并且在这些应用中都取得了很好的效果.

### Embeddings for multiple languages

* 一个研究方向是, 使用尽可能少的`并行数据, parallel data`学习`跨语言, cross-lingual`的表示. 这样就能在语料很少的语言上学习 word representation.

### Embeddings based on other contexts

* word embeddigns 最典型的学习方法是, 基于 the window of surrounding context words.
* Levy & Goldberg (2014) 表明 `依赖结构, dependency structure` 可用作 context 去捕获更多的词义联系.
* Köhn (2015) 发现 dependency-based embeddings 在特定的多语言评估方法中表现最优, 这样的评估方法根据不同词义特征对 embeddigns 进行聚类.
* Melamud et al. (2016) 观察到不同的 context types 在不同的 downstream task 都有较好的效果, 从不同 context types 中习得的 word embeddings 简单`级联, concatenation`后, 能获得性能提升.
* 除了选择不同的 context words, additional context 还可以用于: 将 词典中的 co-occurrence information 整合进 negative sampling process, 以使得关联的单词相互更靠近, 防止它们被用作 negative samples.
