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

- IDE 的标准功能：自动保存，全屏，字体大小，配色方案
- 对外提供 API：
 - `initialize(context)` - 初始化状态或其他 bookkeeping。之在算法开始前调用一次。`context` 是增强的 Python 字典(可使用点标记法），用于在回测或实时交易阶段保持状态。在算法中，应该使用 `context` 而不是全局变量
 - `handle_data(context, data)` - 可选方法，每分钟调用，使用 `data` 获得个人价格或价格窗。该方法应该少用，most algorithm functions should be run in scheduled functions.
 - `before_trading_start(context, data)` - 可选。每天在开市之前调用一次。算法可通过管道（Pipeline）选择证券进行交易，或做其他日计算。
- `data` 对象：
 - `data` 为算法提供指定的 OHLCV（open/high/low/close/volume）值，以及历史窗口的 OHLCV 值，检查资产是否可交易，价格是否过时
 - `data` 对象知道算法的当前时间，并使用当前时间进行计算
 - `data` 对象的所有方法可接收单个资产或一个资产的列表，价格获取方法还接收一个 OHLCV 字段或者列表。The more that your algorithm can batch up queries by passing multiple assets or multiple fields, the faster we can get that data to your algorithm.
- 调度函数（`schedule_function`）:
 - 当算法不需要每分钟都执行时，会更快。`schedule_function` 方法用于指定算法执行的时间，使用日期或时间规则。所有的调度需要在 `initialize` 方法中完成。

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
 - 被调度的函数不是异步的，两个被调度函数只能按被创建的顺序执行
 - 同一分钟，`handle_data` 函数在其他任何被调度函数之前执行。被调度函数拥有与 `handle_data` 相同的超时限制。`handle_data` 与任何被调度函数花费的总时间不能超过 50 s。
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

- 算法最经常的动作之一是**取证券的价格和交易量信息**，可以特定分钟获取数据，or data for a window of minutes
- 使用 `data.current` 获取特定分钟的数据，可向其传递一个或多个证券，也可以是一个或多个字段。返回的数据将作为交易值
 - 通过参数 `last_traded`，`data.current` 也可以用于查找最近一分钟内交易的资产
- 使用 `data.history` 获取 data for a window of time，可传递一个或多个资产，一个或多个字段，`1m (minute)` 或 `1d` 指定数据的粒度，以及 the number of bars。返回的数据将被调整，为当前仿真时间进行拆分，兼并，股利
- `bar_count` 字段指定了 `history` 函数返回的 DataFrame 数据的天或分钟数
- `price` 是 forward-filled 的。若价格存在，返回最近的价格。否则，返回 `NaN`
- 若证券没有被交易或在给定时间不存在，`volume`返回 0，`open`，`high`，`low`，`close` 返回 `NaN`
- 不要将某天的 `data.history` 结果保存到下一天。当天的调用获得的是当天的价格，是调整过的（今天有今天的价格，明天有明天的价格）
- 当算法调用 `history` 时，the returned data is adjusted for splits, mergers, and dividends as of the current simulation date. 换言之，当算法请求一个历史窗口价格时，将以窗口中心进行分离，得到的前半部分将被调整？
- `history` 的参数与对应的返回值：
 - 单个证券和单个字段 - pandas Series，以日期为索引
 - 多个证券和单个字段 - pandas DataFrame，以日期为索引，以资产为列
 - 单个证券和多个字段 - pandas DataFrame，以日期为索引，以字段为列
 - 多个资产和多个字段 - pandas Panel，以字段为索引，日期为主轴，证券为次轴
 - 所有的价格都是分流，并根据仿真当天日期股息 (dividend-adjusted) 调整过的。`data.history` 返回的价格数据不应该被保存或被传递
 - **"price" is always forward-filled. The other fields ("open", "high", "low", "close", "volume") are never forward-filled.**

#### History and Backtest Start

###### 常规应用：当前价格与昨日收盘价

```python
def initialize(context):
    # AAPL, MSFT, and SPY
    context.securities = [sid(24), sid(5061), sid(8554)]

def handle_data(context, data):
    price_history = data.history(context.securities, "price", bar_count=2, frequency="1d")
    for s in context.securities:
        prev_bar = price_history[s][-2]  # 昨日收盘价
        curr_bar = price_history[s][-1]  # 当前价
        if curr_bar > prev_bar:
            order(s, 20)
```

###### 常规应用：回看 X 轴

- 计算对定历史时间的百分比变化

```python
def initialize(context):
    # AAPL, MSFT, and SPY
    context.securities = [sid(24), sid(5061), sid(8554)]

def handle_data(context, data):
    prices = data.history(context.securities, "price", bar_count=10, frequency="1d")
    pct_change = (prices.ix[-1] - prices.ix[0]) / prices.ix[0]  # 取 x 维度?
    log.info(pct_change)
```

- pandas DataFrame 的函数 `iloc` 将两个值以一对的方式返回： `rice_history.iloc[[0, -1]]`。因此上述策略可以改写为：

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

    vwap_15 = vwap(hist["price"][-15:], hist["volume"][-15:])
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
    Computes regression coefficients (slope and intercept)
    计算回归系数（斜率与截距）
    OLS - Ordianry Least Squares（普通最小二乘法）
    via Ordinary Least Squares between two securities.
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

```python
# Python TA-Lib wrapper
# https://github.com/mrjbq7/ta-lib
# EMA(exp moving average) 计算举例
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
- 使用 `data.can_trade` 来检查股票在算法当前点是否可交易。
- 
