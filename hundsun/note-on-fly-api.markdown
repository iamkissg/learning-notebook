### 恒生投研平台API
- zipline.api.symbol(self, symbol_str) - 对指定的股票代码进行序列化, 返回股票代码序列
- zipline.api.order(self, asset, amount, limit_price=None, stop_price=None, style=None) - 买卖股票下单
 - asset - 股票代码
 - amount - 数量
 - 调用成功, 订单创建成功， 返回Order对象，否则None
- order_target(sid, amount, style=None) - 买卖股票, 使指定的股票最终数量达到指定的amount
- order_value(sid, value, style=None) - 买卖指定价格为value的股票. value为负，卖出；为正，买入
- order_target_value(sid, value, style=None) - 调整股票仓位到value价值
- cancel_order(order) - 取消订单, 参数为order对象或order_id
- get_open_orders() - 获得当天的所有未完成的订, 返回一个dict, key是order_id, value是Order对象
- get_orders() - 获取当天的所有订单
- initialize(context) - 初始化方法，用于初始一些全局变量
 - context: UserContext对象, 存放有当前的账户/股票持仓信息
- handle_data(context, data) - 该函数每个单位时间会调用一次, 如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次
 - context: UserContext对象, 存放有当前的账户/股票持仓信息
 - data: 一个字典(dict), **key是股票代码编号, value是当时的SecurityUnitData对象**. 存放前一个单位时间(按天回测, 是前一天) 的数据.
- before_trading_start(context) - 该函数会在每天开始交易前被调用,此处添加每天都要初始化的信息.
 - context: UserContext对象, 存放有当前的账户/股票持仓信息
- history(count, frequency='1d', field='low', ffill=True, security_list=None) - 查看历史的行情数据.
 - 参数:
  - count: 数量, 返回的结果集的行数
  - frequency: 单位时间长度, 几天或者几分钟, 格式支持’Xd’,’Xm’, X是一个正整数, 分别表示X天和X分钟(不论是按天还是按分钟回测都能拿到这两种单位的数据),注意, 当X > 1时, field只支持[‘open’, ‘close’, ‘high’, ‘low’, ‘volume’, ‘money’]这几个标准字段.目前只支持‘1d’.
  - field: 要获取的数据类型, 支持[‘open’, ‘close’, ‘high’, ‘low’, ‘volume’, ‘money’].
  - security_list: 要获取数据的股票列表, None表示universe中选中的所有股票
 - 返回: pandas.DataFrame对象, 行索引是datetime.datetime对象, 列索引是股票代号的编号.
- get_index_stocks(index_code) - 获取一个指数在平台可交易的成分股列表, 返回股票代码的list
 - index_code, 指数代码，尾缀必须是.XBHS 如沪深300：000300.XBHS
- get_industry_stocks(industry_code) - 获取一个行业的所有股票, 返回股票代码的list
 - industry_code: 行业编码, 尾缀必须是.XBHS 如农业股：A01000.XBHS
- get_price(security,start_date='20150101',end_date='20151231',frequency='daily', fields=None) - 获取一支或者多只股票的行情数据, 按天或者按分钟
 - 参数:
  - security: 一支股票代码或者一个股票代码的list
  - start_date: 字符串, 开始时间, 默认是’20150101’
  - end_date: 格式同上, 结束时间, 默认是’20151231’
  - frequency: 单位时间长度, 几天或者几分钟, 格式支持’Xd’,’Xm’, X是一个正整数, 分别表示X天和X分钟(不论是按天还是按分钟回测都能拿到这两种单位的数据),注意, 当X > 1时, field只支持[‘open’, ‘close’, ‘high’, ‘low’, ‘volume’, ‘money’]这几个标准字段.目前只支持‘1d’.
  - field: 要获取的数据类型, 支持[‘open’, ‘close’, ‘high’, ‘low’, ‘volume’, ‘money’].支持SecurityUnitData里面的所有基本属性.
 - 返回:
  - 如果是一支股票, 则返回pandas.DataFrame对象, 行索引是datetime.datetime对象, 列索引是行情字段名字,
  - 如果是多支股票, 则返回pandas.Panel对象, 里面是很多pandas.DataFrame对象, 索引是股票代码编号, 每个pandas.DataFrame的行索引是datetime.datetime对象, 列索引是行情字段
- set_universe(security_list) - 设置要操作的股票池.
 - security_list: 股票列表,支持单支或者多支股票
- record(**kwargs) - 跟踪记录
- log - 打印日志.
 - log.error(content1)
 - log.warn(content2)
 - log.info(content3)
 - log.debug(content4)
- g - 全局对象g，用来存储用户的各类可被不同函数（包括自定义函数）调用的全局数

```python
g.security = None #股票池
g.start = None  #开始时间
g.end = None  #结束时间
g.frequency = None  #单位时间长度, 几天或者几分钟, 格式支持’Xd’,’Xm’，目前只支持’1d’
g.start_fund = None #起始资金
g.daycount = None  #累计天数
```

- UserContext - TradingAlgorithm对象

```python
capital_base 起始资金
sim_params SimulationParameters对象
period_start：开始时间
period_end：结束时间
capital_base：起始资金
data_frequency：周期设置
emission_rate：执行速率
first_open：开市时间
last_close：停市时间
initialized：是否执行初始化
slippage VolumeShareSlippage对象
volume_limit：容积限制
price_impact：价格影响力
commission：佣金费用
blotter Blotter对象（记录）
transact_partial VolumeShareSlippage对象
volume_limit：容积限制
price_impact：价格影响力
commission：佣金费用
open_orders：未完成交易订单
orders：交易订单总和
new_orders：新生成的交易订单
current_dt：当前单位时间的开始时间, datetime.datetime对象,
recorded_vars：收益曲线值
```

- SecurityUnitData - 一个单位时间内的股票的数据, 是一个字典，根据sid获取BarData对象数据

```python
# 基础属性
open 时间段开始时价格
close 时间段结束时价格
price结束时价格
low 最低价
high 最高价
volume 成交的股票数量
money 成交的金额
is_open 值为0或1, 判断股票是否停牌,0：停牌，1：正常。停牌时open/close/low/high/ price依然有值,所有属性都等于停牌前的收盘价, volume=money=0

# 额外属性和方法
sid 股票代码编号
returns 股票在这个单位时间的相对收益比例, 等于 (close-pre_close)/pre_close
mavg(days, field=price) 过去days天的每天收盘价的平均值, 把field设成’high’,则为每天最高价的平均价, field可以是基本属性中任意一种
vwap(days) 过去days天的每天均价的加权平均值
stddev(days) 过去days天的每天收盘价的标准差
```

- Portfolio - 当前的资金,股票信息

```python
cash 当前持有的剩余资金
positions 当前持有的股票(包含不可卖出的股票), 一个dict, key是股票代码, value是Position对象
starting_cash 初始资金
portfolio_value 当前持有的股票和现金的总价值
positions_value 当前持有的股票的总价值
capital_used 已使用的现金
returns 当前的收益比例, 相对于初始资金
```

- Position - 持有的某个股票的信息

```python
amount 总持有股票数量
last_sale_price  最新的卖出价格
cost_basis 每只股票的持仓成本
sid 股票代码编号
```

- Order对象 - 买卖订单信息

```python
status: 状态, 一个OrderStatus值
created: 订单生成时间, datetime.datetime对象
amount: 下单数量, 不管是买还是卖, 都是正数
filled : 已经成交的股票数量, 正数
symbol: 股票代码
id:  订单ID
commission: 佣金费用
```
