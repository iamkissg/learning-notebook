# Multi-Task Learning

## Deep Multi-Task Learning - 3 Lessons Learned

* `Hard parameter sharing`: 即 MT-DNN 的做法, 有一个共享的子神经网络, 多个 task-specific 头.

### Lesson 1 Combining Lossens

* 简单地将不同任务对应的 loss 相加是不对的. 不同任务的 losses' scale (规模) 不同, 有一些任务会占据主导地位, 从而使得其他任务对应的 losses 对共享的神经网络的更新太有限; (如果不同任务的重要性不同, 我估计在同一规模的基础上, 得强调这些任务)
* 最简单的策略是, 用加权和代替求和, 但是多了一个超参数: 不同任务的权;
* [Multi-Task Learning Using Uncertainty to Weigh Losses for Scene Geometry and Semantics](https://arxiv.org/abs/1705.07115) 提供了另一种思路: 用不确定性来为不同 losses 赋权. The way it is done, is by learning another noise parameter that is integrated in the loss function for each task. 字面上来看, 是在 loss function 中增加了一个参数.

### Lesson 2 Tuning Learning Rates

* 为不同头和共享子网络分配不同的学习率, Optimizer, Scheduler 等; (PyTorch 已经实现了)

### Lesson 3 Using estimates as features

* 用一个任务的输出作为另一个任务的特征;
* 为防止任务 B 上的误差通过任务 A 的头反向传播, 要截断, 即将来自任务 A 的特征作为常量特征.
