# 20180107

## Autograd mechanics


* 在一个操作中, 有一个输入需要梯度, 那么输出也需要梯度; 反之, 只有所有输入都不需要梯度, 输出才不需要梯度, 此时 BP 才不会在对应子图传播. 因此 freeze NN's parameters 的办法可以是设置 `requires_grad=False`.

```python
model = torchvision.models.resnet18(pretrained=True)
for param in model.parameters():
    param.requires_grad = False
# Replace the last fully-connected layer
# Parameters of newly constructed modules have requires_grad=True by default
model.fc = nn.Linear(512, 100)

# Optimize only the classifier
optimizer = optim.SGD(model.fc.parameters(), lr=1e-2, momentum=0.9)
```

* `volatile` for pytorch.autograd.Variable, 推荐在纯推理模式下使用, 即确定不会调用 `.backward()` 的情况下. 此时将使用最小的内存消耗. 一个操作中有至少一个 volatile, 输出也将变成 volatile, 因此 volatile 在计算图中传播得比 `requires_grad=False` 还要快得多. (前者只需要一个 volatile 节点, 后者需要设置所有节点 requires_grad=False 才能使得 NN 最后的输出不带梯度)
* `autograd` 通过记录一张`有向非循环计算图, directed acyclic graph`, 来记录创建了数据的所有操作. 图的叶节点是输入, 根节点是输出. 梯度从根节点依据 chain rule 传播到叶节点的过程就是 BP 的过程.
* autograd 用 a graph of `Fucntion` object, 来表示上述计算图. 前向传播时, autograd 执行计算的同时, 还会构建 `Function` graph 以便 BP 时计算梯度. (计算得到的 Variable 类型数据都会有一个 `.grad_fn`, 作为计算图的入口, 直观点可以理解成该属性记录了数据是由哪些变量通过何种操作得到的).
* PyTorch 提供的是动态计算图机制, 每次都会重建计算图, 也意味着可以按需修改计算图. `What you run is what you differentiate`
* 官方不建议在 autograd 中使用 in-place 操作. autograd 缓冲的释放与复用是高效的, in-place 操作实际上不能显著地减少内存使用量. 限制 in-place 操作适用性的两大原因:
    * Overwriting values required to compute gradients. (This is why variables don’t support `log_`. Its gradient formula requires the original input, and while it is possible to recreate it by computing the inverse operation, it is numerically unstable, and requires additional work that often defeats the purpose of using these functions)
    * in-place 操作实际上都需要 rewrite 计算图. Out-of-place 操作会分配新的对象, 并保持对旧图的索引; in-place 操作则需要修改所有输入的 creator. in-place 操作使得计算变得诡异, 尤其是多个 Variable 指向同一块存储区域时. in-place 会抛出错误, 如果一个 modified inputs 的存储被其他 Variable 再次引用.
        * **in-place correctness checks**: Every variable keeps a version counter, that is incremented every time it’s marked dirty in any operation. When a Function saves any tensors for backward, a version counter of their containing Variable is saved as well. Once you access `self.saved_tensors` it is checked, and if it’s greater than the saved value an error is raised.
