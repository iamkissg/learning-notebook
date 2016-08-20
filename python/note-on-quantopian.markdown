# Note on Quantopian

- The Quantopian Research platform is an IPython notebook environment that is used for research and data analysis during algorithm creation. (研究与数据分析)
- It is also used for analyzing the past performance of algorithms. (分析算法性能)
- historical data & live data
- 算法仿真期间，使用仿真交易的价格
- 当算法调用历史价格或交易量数据时，将会对当前仿真日期进行拆分（splits），兼并（mergers），分红（dividends）进行调整。
- 研究环境是自定义的 IPython server。
- 研究环境还能分析回测与实时交易算法的性能
- 当**回测**完成后，可进行模拟交易（paper trading）

## Developing in the IDE

#### Overview

- IDE 的标准功能：自动保存，全屏，字体大小，配色方案
- 对外提供 API：
 - `initialize(context)` - 初始化状态或其他 bookkeeping。**只在算法开始前调用一次。**`context` 是增强的 Python 字典(可使用点标记法），用于在回测或实时交易阶段保持状态。在算法中，应该使用 `context` 共享数据, 而不是全局变量
 - `handle_data(context, data)` - 可选方法，**每分钟调用**，使用 `data` 获得个人价格 (individual prices) 或价格窗 (windows of prices) 。该方法应该少用，most algorithm functions should be run in scheduled functions.
 - `before_trading_start(context, data)` - 可选。**每天在开市之前调用一次**。算法可通过管道（Pipeline）选择证券进行交易，或做其他日计算。


#### data 对象：
 - `data` 为算法提供指定的 OHLCV（open/high/low/close/volume）值，以及历史窗口的 OHLCV 值，检查资产是否可交易，价格是否过时
 - `data` 对象知道算法的当前时间，并使用当前时间进行计算
 - `data` 对象的所有方法可接收单个资产 (assets) 或一个资产的列表，价格获取方法还接收一个 OHLCV 字段或者列表。The more that your algorithm can batch up queries by passing multiple assets or multiple fields, the faster we can get that data to your algorithm.
- 调度函数（`schedule_function`）:

#### Scheduling Functions
 - **当算法不需要每分钟都执行时，会更快。**`schedule_function` 方法用于指定算法执行的时间，使用日期或时间规则。所有的调度需要在 `initialize` 方法中完成。定义:

```txt
Signature: zipline.api.schedule_function(self, func, date_rule=None, time_rule=None, half_days=True)
Docstring: Schedules a function to be called according to some timed rules.

Parameters
----------
func : callable[(context, data) -> None]
    The function to execute when the rule is triggered.
date_rule : EventRule, optional
    The rule for the dates to execute this function.
time_rule : EventRule, optional
    The rule for the times to execute this function.
half_days : bool, optional
    Should this rule fire on half days?
```

- schedule\_function() 函数的使用:
```python
def initialize(context):
  schedule_function(
    func=myfunc,
    date_rule=date_rules.every_day(),
    time_rule=time_rules.market_close(minutes=1),
    half_days=True
  )
```
 - 月模式（`month_start`，`month_end`）接受 `days_offset` 参数用于设置日期偏移。在设置时间内才进行计算
 - 周模式同月模式
 - 调用多次 `schedule_funtion` 函数，实现更灵活的调度
 - **被调度的函数不是异步的，两个被调度函数只能按被创建的顺序执行**
 - 同一分钟，`handle_data` 函数在其他任何被调度函数**之前**执行。被调度函数拥有与 `handle_data` 相同的超时限制。每分钟, `handle_data` 与任何被调度函数花费的总时间不能超过 50 s。
 - `date_rules` - every\_day(), week\_start(), week\_end(), month\_start(), month\_end()
 - `time_rules` - market\_open, market\_close
 - 多 `schedule_function` 的应用

```python
def initialize(context):
  # execute on the second trading day of the month
  schedule_function(
    myfunc,
    date_rules.month_start(days_offset=1)
  )

  # execute on the 10th trading day of the month
  schedule_function(
    myfunc,
    date_rules.month_start(days_offset=9)
  )

def myfunc(context,data):
  pass
```

 - 自定义调度时间

```python
def initialize(context):
  # For every minute available (max is 6 hours and 30 minutes)
  total_minutes = 6*60 + 30

  for i in range(1, total_minutes):
    # Every 30 minutes run schedule
    if i % 30 == 0:
      # This will start at 9:31AM and will run every 30 minutes
      schedule_function(
      myfunc,
        date_rules.every_day(),
        time_rules.market_open(minutes=i),
        True
      )

def myfunc(context,data):
  pass
```

#### Getting price data for securites

- 算法最经常的动作之一是**取价格和成交价信息**，可以特定分钟获取数据，或一段时间的价格 (a window of minutes)
- 使用 `data.current` 获取**特定分钟的数据**，传入一个或多个**证券 (securities)**，可以有一个或多个字段。返回的数据将作为交易值 (as-traded values)
 - 通过参数 `'last_traded'`，`data.current` 也可以用于查找最近一分钟内交易的资产
- 使用 `data.history` **获取一段时间的数据 (get data for a window of time)**，**传入一个或多个资产 (assets)**，同样可以有一个或多个字段，`1m (minute)` 或 `1d` 指定数据的粒度和 the number of bars。返回的数据将被调整，为当前仿真时间进行拆分，兼并，股利 (The data returned will be adjusted for splits, mergers, and dividends as of the current simulation time.)
须知:
 - `price` 是预填充的 (forward-filled)。若价格存在，返回最近的价格。否则，返回 `NaN`
 - 若证券没有被交易或在给定分钟不存在，`volume`返回 0，`open`，`high`，`low`，`close` 返回 `NaN`
- `bar_count` 字段指定了 `history` 函数返回的 DataFrame 数据的天或分钟数
- **不要将某天的 `data.history` 结果保存到下一天。当天的调用获得的是当天的价格，是调整过的（今天有今天的价格，明天有明天的价格）**

#### History

- 当算法调用 `history` 时，**the returned data is adjusted** for splits, mergers, and dividends **as of the current simulation date.** 当算法请求历史窗口价格时, there is a split in the middle of that window, the first part of that window will be adjusted for the split. This adjustment is done so that your algorithm can do meaningful calculations using the values in the window.
- `data.history(assets, fields, bar_count, frequency)` - bar\_count 参数用于指定函数返回的 DataFrame 包含的天数或分钟数, frequency 参数通常传 `1d` 或 `1m`, 或用 pandas 的 [resample](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.resample.html) 指定频率.
- Examples:
 - Daily History
  - `history(context.assets, "price", 1, "1d")` - 返回当前价格
  - `history(context.assets, "volume", 1, "1d")` - 返回当天开盘以来的成交价, 即使只是部分的
  - `history(context.assets, "price", 2, "1d")` - 返回昨天的收盘价以及当前价
  - `history(context.assets, "price", 6, "1d")` - 返回前 5 天的价格和当前价
 - Minute History:
  - `history(context.assets, "price", 1, "1m")` - 返回当前价格
  - `history(context.assets, "price", 2, "1m")` - 返回前一分钟的收盘价和当前价
  - `history(context.assets, "volume", 60, "1m")` - 返回前 60 分钟的成交价
- `history` 的参数与对应的返回值：
 - 单个证券和单个字段 - pandas Series，以日期为索引
 - 多个证券和单个字段 - pandas DataFrame，以日期为索引，以资产为列
 - 单个证券和多个字段 - pandas DataFrame，以日期为索引，以字段为列
 - 多个资产和多个字段 - pandas Panel，以字段为索引，日期为主轴，证券为次轴
 - 所有的价格都是分流 (split)，并根据仿真当天日期股息 (dividend-adjusted) 调整过的。`data.history` 返回的价格数据不应该被保存或被传递
 - **"price" is always forward-filled. The other fields ("open", "high", "low", "close", "volume") are never forward-filled.**

###### 常规应用：当前价格与昨日收盘价

```python
def initialize(context):
    # AAPL, MSFT, and SPY
    context.securities = [sid(24), sid(5061), sid(8554)]

def handle_data(context, data):
    price_history = data.history(context.securities, "price", bar_count=2, frequency="1d")
    # 对单支股票.
    # 多证券单字段, 返回以日期为索引, 字段为列的 DataFrame
    for s in context.securities:
        prev_bar = price_history[s][-2]  # 昨日收盘价
        curr_bar = price_history[s][-1]  # 当前价
        if curr_bar > prev_bar:          # 当前价高于昨日收盘价, 买入 20
            order(s, 20)
```

###### 常规应用：回看 X 轴

- 计算给定历史时间的百分比变化, 只需开始点和结束点的价格, 而不需中间价

```python
def initialize(context):
    # AAPL, MSFT, and SPY
    context.securities = [sid(24), sid(5061), sid(8554)]

def handle_data(context, data):
    prices = data.history(context.securities, "price", bar_count=10, frequency="1d")
    pct_change = (prices.ix[-1] - prices.ix[0]) / prices.ix[0]  # 取 x 维度?
    log.info(pct_change)
```

- pandas DataFrame 的函数 `iloc` 返回数字索引的行： `price_history.iloc[[0, -1]]`。因此上述策略可以改写为：

```python
def initialize(context):
    # AAPL, MSFT, and SPY
    context.securities = [sid(24), sid(5061), sid(8554)]

def handle_data(context, data):
    price_history = data.history(context.securities, "price", bar_count=10, frequency="1d")
    pct_change = price_history.iloc[[0, -1]].pct_change()  # 最后的 ptc_change() 可以直接对一对值计算百分比变化？
    log.info(pct_change)
```

- 查看不同的值

```python
def initialize(context):
    # AAPL, MSFT, and SPY
    context.securities = [sid(24), sid(5061), sid(8554)]

def handle_data(context, data):
    price_history = data.history(context.securities, "price", bar_count=10, frequency="1d")
    diff = price_history.iloc[[0, -1]].diff()
    log.info(diff)
```

###### 常规使用：滚动变换

- 通过 pandas 提供的方法进行滚动变换计算：
 - mavg(moving average, 移动平均线) -> DataFrame.mean
 - stddev(standard deviation, 标准差) -> DataFrame.std
 - vwap(volume weighted average price, 成交量加权平均价) -> DataFrame.sum

```python
# moving average
def initialize(context):
    # AAPL, MSFT, and SPY
    context.securities = [sid(24), sid(5061), sid(8554)]

def handle_data(context, data):
    price_history = data.history(context.securities, "price", bar_count=5, frequency="1d")
    log.info(price_history.mean())
```

```python
# standard deviation
def initialize(context):
    # AAPL, MSFT, and SPY
    context.securities = [sid(24), sid(5061), sid(8554)]

def handle_data(context, data):
    price_history = data.history(context.securities, "price", bar_count=5, frequency="1d")
    log.info(price_history.std())
```

```python
# volume weighted average price
def initialize(context):
    # AAPL, MSFT, and SPY
    context.securities = [sid(24), sid(5061), sid(8554)]

def vwap(prices, volumes):
    return (prices * volumes).sum() / volumes.sum()

def handle_data(context, data):
    hist = data.history(context.securities, ["price", "volume"], 30, '1d')

    # 最近 15 天的
    vwap_15 = vwap(hist["price"][-15:], hist["volume"][-15:])
    # 最近 30 天的
    vwap_30 = vwap(hist["price"], hist["volume"])

    for s in context.securities:
        if vwap_15[s] > vwap_30[s]:
            order(s, 50)
```

###### 常规使用：使用外部库

- `history` 返回 pandas DataFrame，因此其值可以传给能对 numpy 和 pandas 数据结构进行操作的库

```python
# 使用 OLS 策略
import statsmodels.api as sm

def ols_transform(prices, sec1, sec2):
    """
    计算回归系数（斜率与截距）
    OLS - Ordianry Least Squares（普通最小二乘法）
    """
    p0 = prices[sec1]
    p1 = sm.add_constant(prices[sec2], prepend=True)
    return sm.OLS(p0, p1).fit().params

def initialize(context):
    # KO
    context.sec1 = sid(4283)
    # PEP
    context.sec2 = sid(5885)

def handle_data(context, data):
    price_history = data.history([context.sec1, context.sec2], "price", bar_count=30, frequency="1d")
    intercept, slope = ols_transform(price_history, context.sec1, context.sec2)
```

###### 常规使用：使用 TA-Lib

- `history` 可以返回 pandas Series 对象，其可以传递给 TA-Lib
- EMA(exp moving average, 指数移动平均)

```python
# Python TA-Lib wrapper
# https://github.com/mrjbq7/ta-lib
import talib

def initialize(context):
    # AAPL
    context.my_stock = sid(24)

def handle_data(context, data):
    my_stock_series = data.history(context.my_stock, "price", bar_count=30, frequency="1d")
    ema_result = talib.EMA(my_stock_series, timeperiod=12)
    record(ema=ema_result[-1])
```

## Ordering

- 调用 `order(security, amount)` 模拟简单的市场订购。`security` 是期望交易的**证券**。`amount` 为正则买入，为负则卖出。返回 order id，以便跟踪交易状态。
- 订购摘牌的证券是错误的，在 IPO 之前进行订购也是错误的
- 使用 `data.can_trade()` 来检查股票在算法当前点是否可交易, 当证券是可交易, 且至少被交易了一次, 才返回 True
- Quantopian 是预填充 (forward-fill) 价格的, 因此证券价格可能是老旧的. 用 `data.is_stale` 方法检查, 当资产可用, 最新的价格是上一分钟的价格时, 返回 True
- Quantopian 支持 4 中类型的下单:
 - market order: `order(security, amount)`
 - limit order: `order(security, amount, style=LimitOrder(price))` - 只有价格达到或高于指定的价格, 才会执行
 - stop order: `order(security, amount, style=StopOrder(price))` - 又称为止损 (stop-loss) 下单, 当达到指定价格后, 该下单转为 market order
 - stop-limit order: `order(security, amount, style=StopLimitOrder(limit_price, stop_price))` - 当达到指定的 stop price, 该下单转为 limit order
- 所有未结订单 (open orders) 在交易日的最后都会被取消
- `get_order(order)` - 查看指定订单的状态
- `stop_reached` - 查看 stop order 的指定价位
- `get_open_orders()` - 获取未结订单的列表. 传入股票代码, 可查看指定股票的未结订单
- `cancel_order(order)` - 取消订单

## Viewing Portfolio State

- 当前的投资组合 (portfolio) 状态可在 `handle_data` 函数中通过 `context` 对象获得: `context.portfolio.xxx`
- 个人财务状况 (individual position) 可通过 `context.portfolio.positions` 字典查看

## Pipeline:

- 许多交易算法就以下结构是不同的:
 1. 对于一个已知的 (大) 域 (universe) 中的每个资产, 基于数据的尾随窗口 (a trailing window of data) 计算 N 标量值 (?)
 2. 基于第 1 步的计算结果, 选择一个更小的资产的"可交易域"
 3. 在第 2 步选出的交易域中, 计算期望的投资组合比重
 4. 下单, 将算法当前的投资组合配额调整成第 3 步中计算出的期望比重
- **Pipeline API**模块提供了实现上述方案的框架
- 用户通过创建和注册表示计算管道 (computational pipeline) 阶段的对象与管道进行交互. Quantopian 的内部机制将这些对象编译进一个 Directed Acyclic Graph, 并输入到一个最佳的计算引擎, 以实现高效的处理

#### 基础使用

- 算法可分为 5 部分:
 - 初始化管道
 - 导入数据集
 - 创建计算
 - 添加计算到管道
 - 使用结果

```python
from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline
...
def initialize(context):
    pipe = Pipeline()
    attach_pipeline(pipe, name='my_pipeline')
```

- `Pipeline` 是一个表示计算的对象, 我们希望该计算每日都被执行. 新建的管道是空的, 这意味着它本身并不知道如何计算和计算什么, 也不会产生任何输出.
- `attach_pipeline()` - 1. 告诉算法使用管道对象, 2. 命名管道
- equity - (扣除一切费用后)抵押资产的净值
- 在创建计算让管道去执行之前, 需要指定计算的输入, 即导入数据集.
- 有关数据集的最重要的点: **数据集不持有实际的数据**. 数据集是告诉管道 API 从何以及如何取得计算输入的对象的集合. 这些对象经常对应于数据库的列
- `Factor` (计算因子) - 在管道 API 中, 是表示数据尾随窗口缩减 (reductions on trailing windows of data) 的对象. 每一个 Factor保存 4 个状态:
 1. `input` - `BoundColumn` 对象的列表, 描述了 Factor 的输入
 2. `window_length` - int, 描述 Factor 每天需要多少行历史数据
 3. `dtype` - Numpy 的 `dtype` 对象, 表示 Factor 计算得的值的类型. 大多数是 `float64`
 4. 一个对 `input` 和 `window_length` 描述的数据进行操作的 `compute` 函数
- 当对数据库中的 `N` 个资产计算一天的 `Factor` 时, 底层的管道 API 引擎将向 `compute` 函数提供大小为 `(window_length * N)` 的二维数组, 是 `inputs` 的列表的集合. `compute` 函数产生长度为 `N` 的数组作为输出
- `Filter` - 同 `Factor`一样, 表示数据集定义的输入数据的缩减. 不同之处在于, `Filter` 输出布尔值, `Factor` 输出 数字或时间值.
- `(sma_10 < 5)` 表达式使用了操作符重载来构造 Filter 实例
- 管道支持两大类操作: **添加新列** 和 **筛选不想要的行**
- `add(Filter/Factor, name)` - 向管道添加新列
- `set_screen(Filter)` - 告诉管道扔掉不需要的行, 即经 Filter 筛选, 结果为 False 的行
- `pipeline_output` - 获取管道的输出, 是一个 `pandas.DataFrame` 对象, 包含 `Pipeline.add()` 添加的列, 和筛选后的行.
- 大多数的算法会保存输出到 `context`, 以在 `before_trading_start` 之后的函数中复用. `context.pipeline_results = results`

```python
from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.factors import SimpleMovingAverage

def initialize(context):

    # 创建管道, 并连接到其上
    pipe = Pipeline()
    pipe = attach_pipeline(pipe, name='my_pipeline')

    # 构造 Factor,
    # inputs 用于导入数据集
    sma_10 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10)
    sma_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30)

    # 构造 Filter
    prices_under_5 = (sma_10 < 5)

    # 注册输出?
    pipe.add(sma_10, 'sma_10')
    pipe.add(sma_30, 'sma_30')

    # 过滤掉 Filter 返回为 False 的行
    pipe.set_screen(prices_under_5)

def before_trading_start(context, data):
    # 用管道名对输出进行访问
    results = pipeline_output('my_pipeline')
    print results.head(5)

    # 保存结果以复用
    context.pipeline_results = results
```

- 自定义 Factor, 最简单的方式是创建 `quantopian.pipeline.CustomFactor` 的子类, 并实现 `compute` 方法. 其声明是这样的: `def compute(self, today, assets, out, *inputs):`
 - `*inputs` 是一个 `window_length * N` 的 numpy 数组, N 是请求时数据库中资产数
 - `out` - 长度为 N 的空数组, `compute` 的职责就是向 out 中输出值
 - `asset_ids` - 长度为 N 的整型数组, 包含证券 id
 - `today` - 一个表示哪些天需要调用计算的 `datetime64[ns]`
- 一些 Factor 会同时提供 `inputs` 和 `window_length` 两个参数. 然而许多 Factor, 只需要对指定数据集或指定窗口大小进行操作, 比如 `VWAP` 应该以 `inputs=[USEquityPricing.close, USEquityPricing.volume]` 进行调用, `RSI` 会对一个 14 天的窗口进行标准计算. 因此, 根据需要, 可适当地使用默认值, 或使用类级属性.
- 有时候我们只对特定的股票集感兴趣, 这时可以向 `CustomFactor` 传递一个 `Filter` 作为 `mask` 参数. 之后 CustomFactor 将只对 FIlter 返回 True 的股票进行值的计算. 所有 Filter 返回为 False 的将被填充 missing value
- 使用切片, 可以从 Factor 的计算结果中取出单一的资产. `Slice` 对象作为自定义 Factor 的一个输入, 返回一个 N * 1 的列向量. 比如, 下述代码通过创建一个 `Returns` factor, 来解析出 AAPL 的列:

```python
from quantopian.pipeline import CustomFactor
from quantopian.pipeline.factors import Returns

returns = Returns(window_length=30)
returns_aapl = returns[sid(24)]

class MyFactor(CustomFactor):
    inputs = [returns_aapl]
    window_length = 5

    def compute(self, today, assets, out, returns_aapl):
        # `returns_aapl` is a 5 x 1 numpy array of the last 5 days of
        # returns values for AAPL. For example, it might look like:
        # [[ .01],
        #  [ .02],
        #  [-.01],
        #  [ .03],
        #  [ .01]]
        pass
```

- 只有特定 Factor 的切片可以作为 `Inputs`, 包括 `Returns, `rank`, `zscore`. 原因在于, 这些 Factor 产生标准值, 因此它们作为其他 Factor 的输入是 安全的
- `Slice` 对象不能作为列添加到管道. 每天, 一个切分计算一个单一资产的值, 而普通 Factor 为每个资产都计算结果
- 在算法中使用 Factor 的输出之前, 通常需要对其进行**标准化**.
- 标准化的一种思路是, 对值的重新缩放. 而缩放的一种实现是, 对比不同 factors 的结果
- 基础的 `Factor` 类提供了一些标准化输出的方法: `damean()` 方法通过计算每一行的平均值并减去这个平均值来转化输出; ``zscore()` 方法减去每行的平均值, 再除以每行的标准差
- 普通标准化方法的一个缺陷是, 异常值敏感, 比如上述的 `demean()` 方法, 若有一个极大或极小值, 将使平均值变大或变小, 而导致标准化异常. 一个惯用的方法是忽略极值
- 所有 Factor 标准化方法都有一个可选的关键字参数 `mask`, 接收 `Filter`. 这可以用于过滤异常值, 但由于 Filter 返回的是布尔值, 异常输出标准化后, 将得到 `NaN`
- 标准化的一个重要应用是, 基于组或分类资产调整 factor 的输出.
- `groupby` 参数允许用户指定在行的子集上进行标准化, 而不是整行
- `Classfier` 参数用于划分行以进行标准化. 其是一个类似于 Factor 和 Filter 的表达式, 不同点在于它产生整型数, 而不是浮点数或布尔值.
- 未完待续...

## Fetcher - Load any csv file

- Fetcher provides your algorithm with access to external times series data, Fetcher 提供了外部数据的访问
- 在 `initialize` 方法中调用 `fetcg_csv(url)`, 下载 csv 文件, 解析成 pandas dataframe 对象. 在模拟期间, `handle_data` 和其他函数按行 (rows) 读取 csv/dataframe 作为参数
- Fetcher data 具有与 Quantopian 其他数据相同的数据特征:
 - 使用 `record` 绘制时间线
 - 使用 `history` 创建尾随窗口 (trailing window), 使用统计模型
 - data will be streamed to algorithm without look-ahead bias. 这意味着, 若回测的时间点在 2013-10-01, 而 Fetcher data 开始于 2013-10-02, 那么直到 2013-10-02, 策略才能访问数据.
- Fetcher 支持 2 种时间线:
 - 证券信息 (security information)
 - 信号: 单独的数据, 比如消费者价格索引 (Consumer price index)
- 对于证券信息, csv 文件必须有一个 `symbol` 列. Quantopian 内部会映射 symbol 到 security id (sid). 在一个 csv 文件中, 可以有多个证券

```python
def initialize(context):
    # fetch data from a CSV file somewhere on the web.
    # Note that one of the columns must be named 'symbol' for
    # the data to be matched to the stock symbol
    fetch_csv('https://dl.dropboxusercontent.com/u/169032081/fetcher_sample_file.csv',
               date_column = 'Settlement Date',  # 指明时间列
               date_format = '%m/%d/%y')         # 指明时间格式
    context.stock = symbol('NFLX')               # 感兴趣的代码

def handle_data(context, data):
    record(Short_Interest = data.current(context.stock, 'Days To Cover'))
```

- 对于信号, csv 文件不需要 `symbol` 列, 但需要提供 symbol 参数:

```python
def initialize(context):
    fetch_csv('http://yourserver.com/cpi.csv', symbol='cpi')

def handle_data(context, data):
    # get the cpi for this date
    current_cpi = data.current('cpi','value')

    # plot it
    record(cpi=current_cpi)
```

- 从 Dropbox 导入文件: 将文件放到 Public folder, 再使用 "Public URL", 是 `https://dl.dropboxusercontent.com/u/1234567/filename.csv` 这样的格式, 而不是 `https://www.dropbox.com/s/abcdefg/filename.csv` 的格式
- 从 Google Drive 导入 csv 文件:
 1. Click on File > Publish to the web.
 2. Change the 'web page' option to 'comma-separated values (.csv)'.
 3. Click the Publish button.
 4. Copy and paste the URL into your Fetcher query.

#### Data Manipulation with Fetcher

- Fetcher 提供了 2 种修改 csv 文件的方式:
 - `pre_func` - 预处理函数, specifies the method you want to run on the pandas dataframe containing the CSV immediately after it was fetched from the remote server.(有些话, 真的是英文表达更贴切, 好吧, 是懒癌). 指定的方法可以重命名列, 重新格式化日期, 选择数据或对数据进行切片. 唯一的要求是, 返回 dataframe
 - `post_func` - 后处理函数, called after Fetcher has sorted the data based on given date column, 该函数用于对整个数据集进行时间线计算, 比如时间位移 (time shifting), 计算滚动统计, 添加派生列到 dataframe. 唯一的要求同 `pre_func`, 接收 dataframe, 返回 dataframe

## Validation (代码检查)

- 确保算法是合格的 Python 代码, 使用了 规定的 API, 没有明显的运行时错误
- 编译运行策略与回测是不同的, 编译是为了检查代码合法性, 粗糙地确保算法没错
- 一旦算法能无差地跑一遍, 才取分钟数据进行完整的回测

## Module Import

- 白名单: bisect, blaze, brokers, cmath, collections, copy, cvxopt, datetime, functools, heapq, itertools, math, numpy, odo, operator, pandas, pykalman, pytz, quantopian, Queue, re, scipy, sklearn, sqlalchemy, statsmodels, talib, time, zipline, zlib
