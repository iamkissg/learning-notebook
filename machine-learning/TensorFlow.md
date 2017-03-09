# TensorFlow

## About TensorFlow

- TensorFlow 是使用数据流图 (data flow graphs) 的数值计算库.
- Nodes in the graph represent mathematical operations, while the graph edges represent the multidimensional data arrays (tensors) communicated between them.

## Basic Usage

- how TensorFlow:
    - 以 `graphs` 表示计算
    - 在 `Session` 的上下文执行图
    - 用 `Tensors` 表示数据
    - 用 `Variables` 维持状态
    - 用**反馈(feed)** 和**抓取(fetch)**以从操作获得数据或输入操作
- `nodes` in the graph are called `ops`, an op takes zero or more `Tensors`, performs some computation, and produces zero or more `Tensors`
- `Tensor` 是一个多维数组
- TensorFlow 的基本过程: 用 `graph` 描述计算, `graph`  需要加载入到 `Session` 执行, `Session` 将 `ops` 置于 `Devices` 之上 (CPUs or GPUs) 并提供方法执行, 方法以 numpy 的 `ndarray` 对象返回 `Tensors` (Python) or `tensorflow::Tensor` 实例 (C 和 C++)
- TensorFlow 程序通常由 2 部分组成:
    - 构造阶段 - 组装 graph
    - 执行阶段 - 使用 Session 执行 graph 中的 ops
- The ops constructors in the Python library return objects that stand for the output of the constructed ops, it can also be passed to other ops constructors to use as inputs.
- `Session` should be closed to release resources, 可用 `with` 语句
- 可用 `with ... Device` 语句指定 CPU 或 GPU 单元进行运算. `Device` 用字符串表示, 如 `/gpu:0`
- 分布式计算, 实例化 Session 时, 传递机器的网络位置: `with tf.Session("/grpc://example.org:2222") as sess:`
- `with tf.device("/job:ps/task:0"):` 直接指定执行计算的 worker
- TensorFLow 程序使用 tensor 数据结构表示所有的数据, 只有 tensor 在 computation graph 的操作间传递.
- tensor 是有静态类型, 级别 (rank), 形状的,


