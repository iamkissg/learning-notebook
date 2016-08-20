# Note on Zipline

- zipline是一个python交易算法库, 是一个事件驱动系统, 同时支持回溯测试与实时交易
- 特点:
 - 易用: 使程序员能专注于算法部署
 - Zipline comes “batteries included” as many common statistics like moving average and linear regression can be readily accessed from within a user-written algorithm.(包括常用统计方法, 如移动平均和线性回归)
 - Input of historical data and output of performance statistics are based on Pandas DataFrames to integrate nicely into the existing PyData eco-system.(与现有python生态圈能很好融合)
 - Statistic and machine learning libraries like matplotlib, scipy, statsmodels, and sklearn support development, analysis, and visualization of state-of-the-art trading systems.(统计和机器学习库, 如matplotlib, scipy, statsmodels, 和sklearn, 支持支持交易系统的开发, 数据分析和可视化)

---

## Beginner Tutorial

- 每个`zipline`算法都由2部分组成: `initialize(context)`和`handle_data(context, data)`
- 在启动算法之前, `zipline`调用`initialize()`函数, 传入`context`变量. `context`是一个持久化的命名空间, 可用于存储从上一个算法迭代得到的变量, 并传给下一个算法.
- 算法完成初始化之后, 每个事件发生时, `zipline`调用一次`handle_data()`. 每次调用, 传入相同的`context`变量, 和称为`data`的事件框架, 包括当前交易的OHLC和所属空间中每支股票的成交价(volume for stock).
- 所有算法中重用函数都可以在`zipline.api`中找到
- `order()`函数接收2个参数: 一个证券对象(security object), 以及一个表示欲订购股票数目的值
- `record()`函数允许在每次迭代的过程中保存变量的值(跟踪). 使用关键字函数`varname=var`. 算法结束之后, 就可以访问`record()`跟踪的变量值.
- `zipline`提供了3个接口: 一个命令行接口, `IPython Notebook`, 以及`run_algorithm()`

### 命令行接口

- `-f FILENAME`或`--algofile FILENAME` - 指定包含算法的文件
- `-t TEXT`或`--algotext TEXT` - 指定要运行的算法脚本
- `-D TEXT`或`--define TEXT` - 执行算法之前, 定义一个名称, 绑定到命令空间
- `--data-frequency [daily|minute]` - 指定模拟的数据频率
- `--capital-base FLOAT` - 指定模拟的初始资本
- `-b BUNDLE-NAME`或`--BUNDLE BUNDLE-NAME` - 指定模拟所需的数据捆绑(默认: quantopian-quandl)
- `--bundle-timestamp TIMESTAMP` - 指定查询数据的日期
- `-s DATE`或`--start DATE` - 模拟开始日期
- `-e DATE`或`--end DATE` - 模拟结束日期
- `-o FILENAME`或`--output FILENAME` - 指定数据输出的位置. 若指定为`-`, 则数据将被输出到标准输出(屏幕)
- `--print-algo / --no-print-algo` - 打印算法到标准输出
- 可以用以上参数定义一个配置文件, 之后就可以简单地用`-c`选项来运行算法了.

### IPython Notebook

- 使用之前, 需要先在单元内编写算法, 并告诉zipline去执行该算法. 通过`%%zipline`

### history

- `history()` 维持一个数据的滚动窗口
- 在 zipline 中, 需要用 `add_history()` 方法注册 history container

---

## 数据绑定

- 一个数据绑定(data bundle)是价格数据, 调整数据 (adjustment) 和资产数据库的集合. 它允许预加载回测所需的所有数据, 并存储数据以便之后使用
- `zipline bundles` 命令查看现有的数据绑定.同时返回对数据绑定进行内容撷取的时间(使用).
- 使用数据绑定的第一步是对其进行内容撷取. 内容撷取进程会调用自定义的绑定命令, 并将撷取的数据写到 zipline 访问的标准位置, 默认的位置是`$ZIPLINE_ROOT/data/<bundle>`, 而默认的, `ZIPLINE_ROOT=~/.zipline`. 用`zipline ingest [-b <bundle>]`命令进行内容撷取

- 当`ingest`命令完成, 它将新的数据写入到`$ZIPLINE_ROOT/data/<bundle>`目录下以当前数据命名的子目录下.
- 采用默认的保存所有数据的方式, 数据目录可能会变得非常大. 使用`zipline clean`命令可基于时间约束(--before, --after<date>, 或--keep-last <int>)清除数据绑定.
- 用`run`命令进行回溯测试, `--bundle`选项指定要使用的数据绑定
- `--bundle-date`选项指定日期, 以查询绑定数据. 设置了`--bundle-date`将在运行时使用最近的绑定撷取, 所谓最近就是小于或等于`bundle-date`

### 默认数据绑定

- 默认的, zipline使用quandl的wiki集作为默认数据绑定`quandl`, 它包括了每日价格数据, 现金股利, split和财富元数据. 要从`quandl`中撷取数据, 建议在`quandl.com`网上注册一个账户, 利用APIkey来获得每日更多的API请求. 获得APIkey之后, 可运行形如`QUANDL_API_KEY=<api-key> zipline ingest quandl`的命令, 以匿名用户运行`ingest`命令
- 可设置环境变量`QUANDL_DOWNLOAD_ATTEMPTS`来设定从quandl服务器的尝试下载次数, 默认是5.
- `QUANDL_DOWNLOAD_ATTEMPTS`不是允许的失败总数, 而每次请求允许的失败次数.quandl加载器会每100股发送一次请求.
- quantopian提供了quandl wiki数据集的镜像, 其数据是zipline期望的格式.
- zipline提供了工厂函数`yahoo_equities()`, 用于从yahoo阶段性创建数据绑定.

```python
from zipline.data.bundles import register, yahoo_equities

# these are the tickers you would like data for
equities = {
    'AAPL',
    'MSFT',
    'GOOD',
}
register(
    'my-yahoo-equities-bundle',  # name this whatever you like
    yahoo_equities(equities),
)
```

- 以上代码添加到`~/zipline/extensions.py`, 就创建了一个新的数据绑定.

### 编写新的绑定

- 数据绑定的存在使得通过zipline使用不同数据源更容易. 要添加一个新的绑定, 必须实现`ingest`函数
- `ingest`函数用于加载数据到内存, 并将其传递给一系列zipline提供的writer对象, 以将数据转换成zipline的内部格式. ingest函数可能从远端下载数据也可能从本地主机加载文件. 该函数提供的writers根据事务, 将数据写到恰当的位置.

```python
ingest(environ,
       asset_db_writer,
       minute_bar_writer,
       daily_bar_writer,
       adjustment_writer,
       calendar,
       cache,
       show_progress,
       output_dir)
```

- `environ` - 代表使用的环境变量的映射.
- `asset_db_writer` - `AssetDBWriter`的实例.
- `minute_bar_writer` - `BcolzMinuteBarWriter`的实例, 用于将数据转换成zipline的内部bcolz格式, 以供`BcolzMinuteBarReader`读取.
- `dail_bar_writer` - `BcolzDailyBarWriter`的实例, 同上.
- `adjustment_writer` - `SQLiteAdjustmentWriter`, 用于存储splits, mergers, dividends, stock dividends.
- `calendar` - `pandas.DatetimeIndex`对象, 保存所有的交易天数可, 用于加载绑定的数据加载
- `cache` - `dataframe_cache`的实例, 从字符串到数据帧的映射
- `show_progress` - 布尔值
- `output_dir` - 字符串, 表示数据输出的位置.

---

## API

- 算法必须实现一个 `initialize` 方法。`handle_data` 和 `before_trading_start` 是可选的
- `initialize(context)`
 - 回测的最开始调用一次，算法可用该方法设置 bookkeeping
 - context - 初始化好的空的Python字典，可用点标记法的扩展字典
- `handle_data(context, data)`
 - 每分钟调用
 - context - 就是`initialize`中修改的 context，保存用户定义的状态，以及 portfolio 对象。
 - data - 提供了下列方法的对象，获得价格与卷数据，检查 security(证券) 是否存在，检查证券交易的最新时间
- `before_trading_start(context, data)`
 - 每天开市之前调用。在该方法中，不能放置 orders。该方法的目的是使用管道创建证券集，以便算法需要。
