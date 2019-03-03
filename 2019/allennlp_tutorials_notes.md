# AllenNLP Tutorials Notes

## DatasetReader

* [docs](https://github.com/allenai/allennlp/blob/master/tutorials/getting_started/laziness.md)
* DatasetReader 的基类提供了 `lazy` 接口, 用于实现 yield up instances as needed rather than all at onece.
* 创建子类的时候, 除了指定 `tokenizer` 和 `token_indexers` (stoi), 最好勿忘 `lazy`
* 自定义 DatasetReader 时, 要覆盖 `_read` 方法, 该方法被 `read` 方法调用以读取数据. 可以返回 `list`, 但强烈建议返回 `generator`, 前者不支持 lazy 模式.

```python
    def _read(self, file_path: str) -> Iterable[Instance]:
        """Do write your _read function this way"""
        # logic to iterate over file
            # some kind of for loop
            # instance = ...
            yield instance
```

* `read` 方法能根据 `lazy` 的属性值, 返回不同类型的值. lazy 模式就调用一些 generator 读取一条数据; 否则就转为 list.
* 当使用 json 作为配置文件时, 设置 `dataset_reader` 的 `lazy` 属性为 `true` 即可.

## DataIterator

```python
    def __init__(self,
                 batch_size: int = 32,
                 instances_per_epoch: int = None,
                 max_instances_in_memory: int = None) -> None:
        self._batch_size = batch_size
        self._instances_per_epoch = instances_per_epoch
        self._max_instances_in_memory = max_instances_in_memory
```

* AllenNLP 用 `DataIterator` 来对数据集进行迭代, 包括处理 batching, shuffling 等等.
* 以上是 BasicIterator, 默认情况下, 如果是 lazy dataset (应该就是指上面使用了 lazy 的 DatasetReader), 它会"惰性地"一次只读取 32 条数据, 打包成一个 `Batch`. 此时如果使用了 `shuflle=True`, 只会在每个 batch 内进行洗牌, 但是 batches 由于没有洗过牌, 总是按序被迭代.
* `max_instances_in_memory` 可以解决上述问题, 比如设置为 3200, iterator 将一次性加载 3200 条数据进存储器, 然后在 3200 中进行洗牌, 再生成 100 个 batches.
* `instance_per_epoch` 可用于指定一个 epoch 迭代的数据量, 即不必对整个数据集进行迭代了.

## Training a Model

```json
  "trainer": {
    "optimizer": "adam",
    "num_epochs": 40,
    "patience": 10,    // early stopping
    "cuda_device": -1  // CPU
  }
```

* AllenNLP 的设计原则之一是: 使用 [Jsonnet](https://jsonnet.org/) 格式文件来配置实验, 以上是一个例子.
* 它还提供了从命令行直接训练的方式: `allennlp train path/to/config.json --serialization-dir /tmp/tutorials/getting_started`
* `serialization-dir` 就是模型训练过程中生成文件被保存的地方, 比如 vocab, checkpointed weightes 等.
* `accuracy3`, 是 top3 的准确率.
* `training_state_epoch_XX.th` 保存的是 trainer 的状态, `model_state_epoch_XX.th` 保存的则是模型的参数, 还会自动保存 `best.th`. 此外, 所有的文件都会被打包进`model.tar.gz`.
* Evaluate a model: `allennlp evaluate path/to/model.tar.gz path/to/testset(can be a url) --cuda-device`
* Make predictions: `allennlp predict path/to/model.tar.gz inputs.txt`

## Configuring Experiments

```python
@DatasetReader.register("snli")
class SnliReader(DatasetReader):
    pass

@Model.register("esim")
class ESIM(Model):
    pass
```

* AllenNLP 的类大多继承了 `Registrable` 基类. 这意味着, 可以用这些类作为装饰器来自定义子类, 如上所示, 于是自定义类就也有了名称.
* 以上做法带来的一个好处是, 可以用 `Model.by_name('custom')` 类恢复类.
* `Registrable` 继承了 `FromParams`, 后者有一个 `from_params` 类方法, 于是允许从 `Params` 对象进行模型等等的实例化, 而 `Params` 可以看作参数的 dict.
* 以上, 使得 AllenNLP 能够从配置文件实例化对象.

```python
# Grab the part of the `config` that defines the model
model_params = config.pop("model")     # 从配置文件中提取模型参数

# Find out which model subclass we want
model_name = model_params.pop("type")  # 提取模型名称

# Instantiate that subclass with the remaining model params
model = Model.by_name(model_name).from_params(model_params)
```

* Because a class doesn't get registered until it's loaded, any code that uses `BaseClass.by_name('subclass_name')` must have already imported the code for the subclass. In particular, this means that once you start creating your own named models and helper classes, the `allennlp` command will not be aware of them unless you specify them with `--include-package`. You can also create your own script that imports your custom classes and then calls `allennlp.commands.main()`.
* 一个 `Dataset` 是一个 `Instance` 的集合, 一个 `Instance` 由多个 `Field` 组成, 每一个 `Field` 将 `Instance` 的部分(比如 Text 和 Label) 表示成`数组`.
* `DatasetReader` 负责将数据集转化成 `Dataset`. 以下是一个例子:

```json
  "dataset_reader": {
    "type": "sequence_tagging",  // 使用 SequenceTaggingDatasetReader
    "word_tag_delimiter": "/",   // 指定 word_tag_delimiter, 默认的 token_delimiter 就是空格, 不必特意指定
    "token_indexers": {
      "tokens": {
        "type": "single_id",
        "lowercase_tokens": true
      },
      "token_characters": {      // 这意味着每个 token 还有一个额外的编码 (总共 2 个)
        "type": "characters"     // TokenCharactersIndexer, 将每个 token 表示成 int-encoded 的 character list
      }
    }
  },
```

* 数据集的路径, 可以是本地的, 也可以是 URL. 对于后一种情况, AllenNLP 会在本地备份, 目录是 `~/.allennlp/datasets`
* 看起来, AllenNLP 会将配置文件中的 `aa_bb_cc` 转成驼峰式的名称: `AaBbCc`.
* 采用了模块化的设计, 将`TextFieldEmbedder`, `Seq2SeqEncoder` 等分开配置, 如下.
* 与 DatasetReader 的设置相对应, 设置了 `tokens` 和 `token_characters` (这些称为 `TokenEmbedder`), 而 `TextFieldEmbedder` 的输出是所有 embeddings 的 concatenation.
* 下面例子中对 `token_characters` 的处理相比 `tokens` 稍微更复杂, 由两部分组成: `TokenCharactersEncoder` 和 `CnnEncoder`. 后者就是一个简易的 CNN 了.
* 联合上面 DatasetReader 的配置, `TextFields` 和 `TextFieldEmbedder` 都可配置, 可以方便地在不同 word representations 之间进行切换.

```json
// 从配置文件中截取的, 缩进可能会不同

  // TextFieldEmbedder
  "text_field_embedder": {
    "tokens": {
      "type": "embedding",
      "embedding_dim": 50
    },
    "token_characters": {
      "type": "character_encoding",  // TokenCharactersEncoder
      "embedding": {
        "embedding_dim": 8
      },
      "encoder": {                   // CnnEncoder
        "type": "cnn",
        "embedding_dim": 8,
        "num_filters": 50,
        "ngram_filter_sizes": [
          5
        ]
      },
      "dropout": 0.2
    }
  },

    // Seq2SeqEncoder
    "encoder": {
      "type": "lstm",
      "input_size": 100,
      "hidden_size": 100,
      "num_layers": 2,
      "dropout": 0.5,
      "bidirectional": true
    }

  "iterator": {"type": "basic", "batch_size": 32},

  "trainer": {
    "optimizer": "adam",
    "num_epochs": 40,
    "patience": 10,
    "cuda_device": -1
  }
}
```

* 配置文件总是会保存到每一次实验的 archive 中.

## Creating Your Own Models

* 基本上, 实现一个新的模型, 在 `Model` 之外, 还需要自定义一个 `DatasetReader`, 除非后者已经存在了
* 以下是自定义 CRF Module 的一个例子, 输入是 `[seq_len, num_tags]`, 输出则是 `[seq_len,]`.

```python
    def __init__(self,
                 num_tags: int,
                 constraints: List[Tuple[int, int]] = None) -> None:
        super().__init__()
        self.num_tags = num_tags

        # transitions[i, j] is the logit for transitioning from state i to state j.
        # 转移矩阵
        self.transitions = torch.nn.Parameter(torch.Tensor(num_tags, num_tags))

        # _constraint_mask indicates valid transitions (based on supplied constraints).
        # 用 Mask 来设置可转移状态
        if constraints is None:
            self._constraint_mask = None
        else:
            constraint_mask = torch.Tensor(num_tags, num_tags).fill_(0.)
            for i, j in constraints:
                constraint_mask[i, j] = 1.

            # 作为参数, 但不更新
            self._constraint_mask = torch.nn.Parameter(constraint_mask, requires_grad=False)

        # Also need logits for transitioning from "start" state and to "end" state.
        self.start_transitions = torch.nn.Parameter(torch.Tensor(num_tags))
        self.end_transitions = torch.nn.Parameter(torch.Tensor(num_tags))

    def forward(self, *input):
        ...
```

* 将 `SimpleTagger` 替换成 `CrfTagger` 的步骤:
    * 为模型添加 `crf` 属性, 用于初始化 `ConditionalRandomField`
    * 将 Softmax 的类概率替换为 Viterbi 算法生成的最可能 Tag.
    * 将 Softmax+Cross-Entropy 的损失函数替换为负对数自然函数.
* (可用于但不限于 NER) AllenNLP 使用 `itertools.groupby` 来对输入块进行分组, 比如分成句子 (CoNLL 的数据, 句子间由空行隔开)
* 配置文件的修改 (相对于 SimpleTagger 的配置文件而言):
    * 修改 `model.type`
    * 修改 `dataset_reader.type`
    * 增加 `dataset_reader.tag_label`
* 当在 allennlp 的仓库之外创建模型, 需要加载自定义的模块. 使用 `--include-packages` 来指定额外的 package 们. 否则 AllenNLP 将无法为它们进行注册, 也就无从实例化了.

## Using AllenNLP as a Library - Datasets and Models

* AllenNLP 的好习惯, 在写任何代码之前, 为 `DatasetReader` 写测试 (在极少量的固定样本上).
* 测试类继承自 `allennlp.common.testing.AllenNlpTestCase`, 它包含了日志, 清理临时文件等有用的功能
* `DatasetReader` 最基础的 API 就是实例化和读取数据, 所以测试如下

```python
from allennlp.common.testing import AllenNlpTestCase
from allennlp.common.util import ensure_list

from my_library.dataset_readers import SemanticScholarDatasetReader

class TestSemanticScholarDatasetReader(AllenNlpTestCase):
    def test_read_from_file(self):
        reader = SemanticScholarDatasetReader()
        instances = ensure_list(reader.read('tests/fixtures/s2_papers.jsonl'))

        # 以下根据自定义的数据集而定, 是我们关于读取数据的预期
        assert len(instances) == 10
        fields = instances[0].fields
        assert [t.text for t in fields["title"].tokens] == instance1["title"]
        assert [t.text for t in fields["abstract"].tokens[:5]] == instance1["abstract"]
        assert fields["label"].label == instance1["venue"]
        fields = instances[1].fields
        assert [t.text for t in fields["title"].tokens] == instance2["title"]
        assert [t.text for t in fields["abstract"].tokens[:5]] == instance2["abstract"]
        assert fields["label"].label == instance2["venue"]
        fields = instances[2].fields
        assert [t.text for t in fields["title"].tokens] == instance3["title"]
        assert [t.text for t in fields["abstract"].tokens[:5]] == instance3["abstract"]
        assert fields["label"].label == instance3["venue"]
```

* 有了测试用例之后, 再来编写 `DatasetReader._read` 方法, 使输出符合预期. 下面例子中的 `cached_path` 要注意一下, 它大概是检查以 URL 形式输入的 `file_path` 是否在本地有备份了 (没有则下载), 最后返回本地路径.
* 根据教程的说法, 使用 `text_to_instance` 的一个原因是, 提供`hook` (钩子). (是我的话, 可能就不会另写一个方法了)
* 注意, `_token_indexers` 比看起来要复杂, 是一个 dict. 它可以从 token 中提取出不同的信息, 比如 word id, characters, POS 等等. 这提供了另一种灵活性.

```python
@DatasetReader.register("s2_papers")  # 将 SemanticsScholarDatasetReader 注册成一个 DatasetReader, 以便从配置文件中初始化
class SemanticScholarDatasetReader(DatasetReader):
    def __init__(self,
                 tokenizer: Tokenizer = None,
                 token_indexers: Dict[str, TokenIndexer] = None) -> None:
        self._tokenizer = tokenizer or WordTokenizer()
        self._token_indexers = token_indexers or {"tokens": SingleIdTokenIndexer()}

    def _read(self, file_path):
        with open(cached_path(file_path), "r") as data_file:
            logger.info("Reading instances from lines in file at: %s", file_path)
            for line_num, line in enumerate(Tqdm.tqdm(data_file.readlines())):
                line = line.strip("\n")
                if not line:
                    continue
                paper_json = json.loads(line)
                title = paper_json['title']
                abstract = paper_json['paperAbstract']
                venue = paper_json['venue']
                yield self.text_to_instance(title, abstract, venue)  # yield, yield, yield

    def text_to_instance(self, title: str, abstract: str, venue: str = None) -> Instance:
        tokenized_title = self._tokenizer.tokenize(title)
        tokenized_abstract = self._tokenizer.tokenize(abstract)
        title_field = TextField(tokenized_title, self._token_indexers)  # 指定使用的 Field
        abstract_field = TextField(tokenized_abstract, self._token_indexers)
        fields = {'title': title_field, 'abstract': abstract_field}
        if venue is not None:
            fields['label'] = LabelField(venue)
        return Instance(fields)  # fields 是一个 dict, Instance 接收一个 dict.
```

* 同样地, AllenNLP 的好习惯- -., 开始写 Model 之前, 来一个测试用例. 从 `allennlp.common.testing.ModelTestCase` 继承.
* Model 的基本要求 如下, `ModelTestCase` 都能满足:
    * 能成功训练
    * 可保存和加载, 并且重新加载的预测结果不变
    * 预测结果是一致的, 无论使用的 batch 多大
* AllenNLP 苦口婆心地教导: 强烈建议写测试, 在固定的小样上能更容易更快发现问题.
* 测试的额外准备: 用于测试的配置文件和 tiny 测试集.

```python
from allennlp.common.testing import ModelTestCase

class AcademicPaperClassifierTest(ModelTestCase):
    def setUp(self):
        super(AcademicPaperClassifierTest, self).setUp()
        self.set_up_model('tests/fixtures/academic_paper_classifier.json',
                          'tests/fixtures/s2_papers.jsonl')

    def test_model_can_train_save_and_load(self):
        self.ensure_model_can_train_save_and_load(self.param_file)
```

* `AllenNLP` 将 `Vocabulary` 作为参数传入 Model 的 Constructor. 而不是有些地方用的 `vocab_size` 和 `emb_dim` 组合. Vocabulary 负责将 strings 转为 integers.
* 考虑到有多种映射, `Vocabulary` 为它们分配了不同的命名空间, 比如 token vocabulary 和 label vocabulary.
* 使用 `Seq2VecEncoder`, 其 input size 为 `[batch_size, seq_len, emb_dim]`, output size `[batch_size, emb_dim]`.
* `InitialzerApplicator` 和 `RegularizerApplicator` 分别包含了从参数名到初始化方法和正则化方法的 mappings, 其实就是规定了不同参数如何初始化, 如何正则化.
* 有意思的是, 损失函数和 Metric 也定义在了 Model 中.
* `forward` 的参数命需要和 `DatasetReader` 中的 `Instance` 保持一致 (但是顺序?). `DatasetReader` 所做的就是将 `Instance` 分组成 batch, 将 `Fields` pad 成相同的 shape, 为每一个 `Field` 生成 batched array.
* `label` 也是 forward 的参数. AllenNLP 的思路是, 在每一个 training loop 中, `Model.forward` 为自己计算 loss. 结果作为 dict 的一项返回.
* `TextFields` 对应于 `DatasetReader` 的 `_token_indexers` 的结果, 是一个 dict, 交给 `TextFieldEmbedder` 处理, 对模型是透明的.
* Encoder 的输入比较神奇, 接收 embedding sequence 和 mask 作为参数. 也对, 求 padding 对应的结果不对.
* `get_metrics` 方法用于告诉 training code 要计算的 metrics.
* `decode`方法接收 forward 的输出, 并做必要的推断或解码, 比如将 label id 转成 label.

```python
@Model.register("paper_classifier")
class AcademicPaperClassifier(Model):
    def __init__(self,
                 vocab: Vocabulary,
                 text_field_embedder: TextFieldEmbedder,
                 title_encoder: Seq2VecEncoder,
                 abstract_encoder: Seq2VecEncoder,
                 classifier_feedforward: FeedForward,
                 initializer: InitializerApplicator = InitializerApplicator(),
                 regularizer: Optional[RegularizerApplicator] = None) -> None:
        super(AcademicPaperClassifier, self).__init__(vocab, regularizer)

        self.text_field_embedder = text_field_embedder
        self.num_classes = self.vocab.get_vocab_size("labels")
        self.title_encoder = title_encoder
        self.abstract_encoder = abstract_encoder
        self.classifier_feedforward = classifier_feedforward
        self.metrics = {
                "accuracy": CategoricalAccuracy(),
                "accuracy3": CategoricalAccuracy(top_k=3)
        }
        self.loss = torch.nn.CrossEntropyLoss()
        initializer(self)

    def forward(self,
                title: Dict[str, torch.LongTensor],
                abstract: Dict[str, torch.LongTensor],
                label: torch.LongTensor = None) -> Dict[str, torch.Tensor]:
        embedded_title = self.text_field_embedder(title)
        title_mask = util.get_text_field_mask(title)
        encoded_title = self.title_encoder(embedded_title, title_mask)

        embedded_abstract = self.text_field_embedder(abstract)
        abstract_mask = util.get_text_field_mask(abstract)
        encoded_abstract = self.abstract_encoder(embedded_abstract, abstract_mask)

        logits = self.classifier_feedforward(torch.cat([encoded_title, encoded_abstract], dim=-1))
        class_probabilities = F.softmax(logits)

        output_dict = {"class_probabilities": class_probabilities}

        if label is not None:
            loss = self.loss(logits, label.squeeze(-1))
            for metric in self.metrics.values():
                metric(logits, label.squeeze(-1))
            output_dict["loss"] = loss

        return output_dict

    def get_metrics(self, reset: bool = False) -> Dict[str, float]:
        return {metric_name: metric.get_metric(reset) for metric_name, metric in self.metrics.items()}

    def decode(self, output_dict: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        predictions = output_dict['class_probabilities'].cpu().data.numpy()
        argmax_indices = numpy.argmax(predictions, axis=-1)
        labels = [self.vocab.get_token_from_index(x, namespace="labels")
                  for x in argmax_indices]
        output_dict['label'] = labels
        return output_dict
```

* 模型完成之后, 执行测试, 验证模型的功能.
* 再然后就是写配置文件, `iterator` 用于指定如何对 DatasetReader 进行迭代, 如上所述.

```json
  "dataset_reader": {
    "type": "s2_papers"
  },

  // 数据集直接由 URL 给定, 所以 DatasetReader 必须使用 cached_path
  "train_data_path": "https://s3-us-west-2.amazonaws.com/allennlp/datasets/academic-papers-example/train.jsonl",
  "validation_data_path": "https://s3-us-west-2.amazonaws.com/allennlp/datasets/academic-papers-example/dev.jsonl",
  "iterator": {
    "type": "bucket",
    "sorting_keys": [["abstract", "num_tokens"], ["title", "num_tokens"]],
    "batch_size": 64
  },
  "trainer": {
    "num_epochs": 40,
    "patience": 10,
    "cuda_device": 0,
    "grad_clipping": 5.0,
    "validation_metric": "+accuracy",
    "optimizer": {
      "type": "adagrad"
    }
  }
  "model": {
    "type": "paper_classifier",
    "text_field_embedder": {
      "tokens": {
        "type": "embedding",
        "pretrained_file": "https://s3-us-west-2.amazonaws.com/allennlp/datasets/glove/glove.6B.100d.txt.gz",
        "embedding_dim": 100,
        "trainable": false
      }
    },
    "title_encoder": {
      "type": "lstm",
      "bidirectional": true,
      "input_size": 100,
      "hidden_size": 100,
      "num_layers": 1,
      "dropout": 0.2
    },
    "abstract_encoder": {
      "type": "lstm",
      "bidirectional": true,
      "input_size": 100,
      "hidden_size": 100,
      "num_layers": 1,
      "dropout": 0.2
    },
    "classifier_feedforward": {
      "input_dim": 400,
      "num_layers": 2,
      "hidden_dims": [200, 3],
      "activations": ["relu", "linear"],
      "dropout": [0.2, 0.0]
    }
   },
```

* 假设自定义的模型和 DatasetReader 存在于另一个目录, 务必使用 `--include-package` 指明路径.

## Using AllenNLP as a Library - Predictions and Demos

* 模型训练完毕, AllenNLP 提供了 `Predictor` 用于模型的使用. `Predictor.predict_json` 用于指定如何将 JSON 格式的输入转成 `Instance`, 并使用 `predict_instance` 将 `Instance` 序列化为 JSON
* `predict_json` 的返回是一个 JSON dict. 教程中说第二个元素还是一个 dict, `Model.forward_on_instance` 会加入其中. (但下面的代码只是返回了 list; 如果不需要, 可以使用一个 empty dict)

```python
@Predictor.register('paper-classifier')
class PaperClassifierPredictor(Predictor):
    """Predictor wrapper for the AcademicPaperClassifier"""
    @overrides
    def predict_json(self, json_dict: JsonDict) -> JsonDict:
        # 读数据, 转换成 Instance
        title = json_dict['title']
        abstract = json_dict['paperAbstract']
        instance = self._dataset_reader.text_to_instance(title=title, abstract=abstract)

        # label_dict will be like {0: "ACL", 1: "AI", ...}
        label_dict = self._model.vocab.get_index_to_token_vocabulary('labels')
        # Convert it to list ["ACL", "AI", ...]
        all_labels = [label_dict[i] for i in range(len(label_dict))]

        # 预测并返回, 返回 'all_labels' 用于可视化
        return {"instance": self.predict_instance(instance), "all_labels": all_labels}
```

* 预测的测试:

```python
class TestPaperClassifierPredictor(TestCase):
    def test_uses_named_inputs(self):
        inputs = {
            "title": "Interferring Discourse Relations in Context",
            "paperAbstract": (
                    "We investigate various contextual effects on text "
                    "interpretation, and account for them by providing "
                    "contextual constraints in a logical theory of text "
                    "interpretation. On the basis of the way these constraints "
                    "interact with the other knowledge sources, we draw some "
                    "general conclusions about the role of domain-specific "
                    "information, top-down and bottom-up discourse information "
                    "flow, and the usefulness of formalisation in discourse theory."
            )
        }

        archive = load_archive('tests/fixtures/model.tar.gz')
        predictor = Predictor.from_archive(archive, 'paper-classifier')

        result = predictor.predict_json(inputs)

        label = result.get("all_labels")
        assert label in ['AI', 'ML', 'ACL']

        class_probabilities = result.get("class_probabilities")
        assert class_probabilities is not None
        assert all(cp > 0 for cp in class_probabilities)
        assert sum(class_probabilities) == approx(1.0)
```

* 预测的命令行必需 model archive 和输入文件, 不知道为什么, `--predictor` 居然是可选的, 当然 `--include_package` 相当于是必需的, `--output-file` 输出文件.
* 有了 model 和 predictor, AllenNLP 提供了 web demo 的工具, 牛逼炸了

```bash
$ python -m allennlp.service.server_simple --help

usage: server_simple.py [-h] [--archive-path ARCHIVE_PATH]
                        [--predictor PREDICTOR] [--static-dir STATIC_DIR]
                        [--title TITLE] [--field-name FIELD_NAME]
                        [--include-package INCLUDE_PACKAGE]
```

* 更牛逼的是, 提供了自定义 demo, 使用 `npm`, `React`, `HTML` 和 `JS` 实现体验更好的交互. (暂且跳过)
