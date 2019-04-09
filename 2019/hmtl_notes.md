# HMTL Notes

## Beating the state-of-the-art in NLP with HMTL (Official)

* MTL 的优势:
    * single model, single forward pass 带来的计算量上的优势
    * 不同任务间的信息共享 (一个动机就是, 相关的任务可以从彼此之间获益, 得到更丰富的表示)
    * 归纳能力的迁移: 通过将相关任务间的领域信息作为归纳性偏见, 提高模型泛化能力. (并行学习, 共享表示)
    * 更多的数据量
* (Latent Multi-task Architecture Learning: 让模型自己决定共享参数或神经网络层)
* MTL 的面临的问题:
    * How should we train the network?
    * In which order should we tackle the various tasks?
    * Should we switch task periodically?
    * Should all the tasks be trained for same number of epochs?
* 本文提出的基本训练流程
    * Select a *task* (whatever your selection algorithm is).
    * Select a *batch* in the *dataset* for the chosen task (randomly sampling a batch is usually a safe choice).
    * Perform a forward pass.
    * Propagate the loss (backward pass) through the network.
* 以下是示例代码. 启发我的几点是:
    * `get_metrics` 直接定义在 Model 中;
    * `forward` 吃 task;

```python
import torch

from allennlp.models.model import Model
from allennlp.data.iterators import DataIterator

class Task():
    """
    A class to encapsulate the necessary informations (and datasets)
    about each task.
    Parameters
    ----------
    name : ``str``, required
        The name of the task.
    validation_metric_name : ``str``, required
        The name of the validation metric to use to monitor training
        to select the best epoch and to stop the training based on exit condition.
    validation_metric_decreases : ``bool``, required
        Whether or not the validation metric should decrease for improvement.
    evaluate_on_test : ``bool`, optional (default = False)
        Whether or not the task should be evaluated on the test set at the end of the training.
    """
    def __init__(self,
                name: str,
                validation_metric_name: str,
                validation_metric_decreases: bool,
                evaluate_on_test: bool = False) -> None:
        self._name = name

        self._train_data = None
        self._validation_data = None
        self._test_data = None
        self._evaluate_on_test = evaluate_on_test

        self._val_metric = validation_metric_name
        self._val_metric_decreases = validation_metric_decreases

        self._data_iterator = None

    def load_data(self,
                dataset_path: str,
                dataset_type: str):
        """
        Load a dataset from a file and store it.
        Parameters
        ----------
        dataset_path: ``str``, required
            The path to the dataset.
        dataset_type: ``str``, required
            The type of the dataset (train, validation, test)
        """
        assert dataset_type in ["train", "validation", "test"]

        dataset = read(dataset_path) # Replace with whatever loading you want.
        setattr(self, "_%s_data" % dataset_type, dataset)
    
    def set_data_iterator(self,
                         data_iterator: DataIterator):
self._data_iterator = data_iterator


class MyMTLModel(Model):
    def __init__(self):
        """
        Whatever you need to initialize your MTL model/architecture.
        """
  
    def forward(self,
                task_name: str,
                tensor_batch: torch.Tensor):
        """
        Defines the forward pass of the model. This function is designed
        to compute a loss function defined by the user.
        It should return 
        
        Parameters
        ----------
        task_name: ``str``, required
            The name of the task for which to compute the forward pass.
        tensor_batch: ``torch.Tensor``, required
            An embedding representation of the input to pass through the model.
            
        Returns
        -------
        output_dict: ``Dict[str, torch.Tensor]``
            An output dictionary containing at least the computed loss for the task of interest.
        """
        raise NotImplementedError
  
    def get_metrics(self, 
                    task_name: str):
        """
        Compute and update the metrics for the current task of interest.
        
        Parameters
        ----------
        task_name: ``str``, required
            The name of the current task of interest.
        Returns
        -------
        A dictionary of metrics.
        """
        raise NotImplementedError 
```

* 下面这段简短的代码就演示了论文中提到的 *proportional sampling*, 按数据集的大小来成比例地采样, 别其他特别的.

```python
from typing import List
import numpy as np

from allennlp.data.iterators import DataIterator

### Set the Data Iterator for each task ###
# The data iterator is responsible for yield batches over the specified dataset.
for task in task_list:
    task_name = task._name
    task.set_data_iterator(DataIterator()) # Set whatever DataIterator you like.
    
    
### Create the sampling probability distribution over the tasks ###
sampling_prob = [task._data_iterator.get_num_batches(task._train_data) for task in task_list]
sampling_prob = sampling_prob / np.sum(sampling_prob)


def choose_task(sampling_prob):
    """
    Randomly choose one task to train.
    """
    return np.argmax(np.random.multinomial(1, sampling_prob)) 
```

* 好像比较好的库都使用 Trainer / Learner 的概念, 将 train 之类的方法封装在其中. 像把 train, eval 等写在最外面的, 就好像小孩子的写法

```python
from allennlp.training.optimizers import Optimizer


class MultiTaskTrainer():
    def __init__(self,
                model: Model,
                task_list: List[Task])
        self._model = model
        self._task_list = task_list
        
        self._optimizers = {}
        for task in self._task_list:
            self._optimizers[task._name] = Optimizer() # Set the Optimizer you like.
            # Each task can have its own optimizer and own learning rate scheduler.
        
        
    def train(self,
             n_epochs: int = 50):
        
        ### Instantiate the training generators ###
        self._tr_generators = {}
        for task in self._task_list:
            data_iterator = task._data_iterator
            tr_generator = data_iterator(task._train_data,
                                        num_epochs = None)
            self._tr_generators[task._name] = tr_generator
        
        ### Begin Training ###
        self._model.train() # Set the model to train mode.
        for i in range(n_epochs):
            for _ in range(total_nb_training_batches):
                task_idx = choose_task()
                task = self._task_list[task_idx]
                task_name = task._name
                
                next_batch = next(self._tr_generators[task._name]) # Sample the next batch for the current task of interest.
                
                optimizer = self._optimizers[task._name] # Get the task-specific optimizer for the current task of interest.            
                optimizer.zero_grad()
                
                output_dict = self._model.forward(task_name = task_name, 
                                                  tensor_batch = batch) #Forward Pass
                
                loss = output_dict["loss"]
                loss.backward() # Backward Pass
```

* early_stopping 总是好的, 本文的做法(应该也是 AllenNLP 的), 用Task 类中定义的`_val_metric`和`_val_metric_decreases`来检验是否达到停止条件.
* Successive regularization: 防止 catastrophic forgetting 的手段之一, 防止按顺序进行学习的 MTL 的参数变得太厉害添加了 L2 惩罚.
* Multi-task as QA: 把任务都转化为问答.
* HMTL: 还不如论文中讲得多呢!
