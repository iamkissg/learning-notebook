# Python 的时间处理

## time vs. datetime vs. calendar

- `time` 模块提供了时间相关的函数
- `time` - `Low-level` time related functions. Time access and conversions.
- `datetime` 提供了多种日期/时间相关的类
- `datetime` - `Object-oriented interface` to dates and times with similar functionality to the time module.
- `calendar` 允许用户像 Unix `cal` 程序一样打印日历，并提供了额外的日历相关的函数
- `calendar` - General calendar related functions.
-   

## time

- `time` 模块的部分函数是平台依赖的

## datetime

- `datetime` 和 `time` 对象有可选的时区属性 `tzinfo`

### 包含的类型

- `class datetime.date`
- `class datetime.time`
- `class datetime.datetime`
- `class datetime.timedelta`
- `class datetime.tzinfo`

#### date

- `str(d)` - `date` 对象有 `__str__()`
- 直接 `print dt`, 会以 IOS 时间格式打印输出
