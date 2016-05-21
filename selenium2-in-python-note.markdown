#Selenium 2 自动化测试实战--基于Python语言

- 初学者困局: 花了很多精力和时间, 但最终发现一切都是徒劳; 做了很多功课, 但真正该做的事情却未曾开始.

##Chapter1 自动化测试基础

###1.1

- 根据项目流程阶段划分软件测试:
 - 单元测试: 都程序中的单个子程序或具有独立功能的代码段进行测试
 - 集成测试: 在单元测试基础上, 通过单元模块组装成系统或子系统, 再对其进行测试. **重点是检查模块之间的接口是否正确**
 - 系统测试: 针对整个产品系统地进行测试, 验证系统是否满足需求规格的定义, 以及软件系统的正确性和性能等是否满足其需求规格的要求
 - 验收测试: 部署软件之前的最后一个测试阶段. 目的是确保软件准备就绪.
- 黑白灰盒测试
 - 黑盒测试: 着眼于程序外部结构, 不考虑内部逻辑结构, 主要针对软件界面和软件功能
 - 白盒测试: 关注程序内部结构
 - 灰盒测试: 介于前2者之间.
- 功能测试与性能测试
 - 功能测试: 检查实际功能是否符合用户需求. 又分: 逻辑功能测试, 界面测试, 易用性测试, 安装测试, 兼容性测试等
 - 性能测试: 通过自动化的测试工具模拟多种正常, 峰值以及异常负载条件来对系统的各项性能进行测试.
  - 软件性能主要分为**空间性能**和**时间性能**:
  - 时间性能: 软件的具体响应时间.
  - 空间性能: 软件运行时消耗的系统资源
- 手工与自动测试
 - 自动测试又分为功能自动化测试和性能自动化测试
 - 功能自动化测试: 通过编写脚本等方式对软件功能进行测试, 并验证测试结果是否正确.
 - 性能自动化测试: 通过性能工具来模拟用户向系统发起请求, 验证系统的处理能力.
- 冒烟测试, 回归测试, 随机测试, 探索测试, 安全测试
 - 冒烟测: 在对新版本进行大规模测试前, 先验证软件的基本功能是否实现, 是否具备可测性.
 - 回归测试: 指修改了代码之后, 重新测试以确认修改后没有引入新的错误或导致其他代码产生错误
 - 随机测试: 测试中所有数据都随机生产, 目的是模拟用户真实操作, 并发现一些边缘性错误
 - 探索性测试: 测试思维, 强调测试人员的主观能动性, 抛弃繁杂的测试计划和测试用例设计过程, 强调在碰到问题时及时改变测试策略
 - 安全测试: 对产品进行检验以验证产品符合安全需求定义和产品质量标准定义

###1.2 ~ 1.4

- 传统自动化测试, 可理解为基于产品UI层的自动化测试, 将黑盒功能测试转化为由程序或工具执行的自动化测试
- 分层自动化测试, 倡导从黑盒单层到黑白盒多层的自动化测试体系, 从全面黑盒自动化测试到对系统的不同层次进行自动化测试
- 单元自动化测试: 对软件中的最小可测试单元进行检查和验证. 目前几乎所有主流语言都有相应的单元测试框架, 如python的unittest
- 针对python的code review工具: review board
- 接口自动化测试
 - 模块接口测试: 测试模块间的调用与返回, 主要强调对一个类方法或函数的调用, 并对返回结果验证
 - web接口测试
  - 服务器接口测试: 测试浏览器与服务器的接口. 用户操作在前端页面上, 需要后端提供服务器接口, 前端通过调用这些接口获得需要的数据.
  - 外部接口测试: 由第三方提供的调用接口. 典型的例子是第三方登录
 - UI自动化测试
- google对产品测试类型的划分小测试(70%), 中测试(20%), 大测试(10%), 大体对应unit层, service层, ui层的测试

###1.5

- selenium RC(Remote Control)分为Client Libraries和Selenium Server.
 - Client Libraries库主要用于编写测试脚本, 控制Selenium Server的库
 - Selenium Server负责控制浏览器行为, 又分为Launcher, Http Proxy, Core.
  - Core被嵌入到浏览器页面中, 实际是一堆 JavaScript 函数的集合. 正是通过这些 JavaScript 函数实现对浏览器的控制操作
  - Launcher用于启动浏览器, 将Core加载到浏览器页面中, 并将浏览器的代理设置为Http Proxy
- Selenium`RC 在浏览器中运行 JavaScript 应用, 使浏览器内置的 JavaScript 翻译器来翻译和执行 selenese 命令(Selenium命令集合)
- WebDriver则通过原生浏览器支持来直接控制浏览器, 支持创建更高级的测试, 避免了 JavaScript 安全模型导致的限制. 还能利用操作系统级的调用模拟用户输入

###1.6

- html 不是编程语言, 是标记语言, 但可以在html标签中嵌入前端脚本
 - <html> </html> 之间的文本用于描述网页
 - <head> </head> 之间的文本用于定义文档头, 是所有头部元素的容器
 - <body> </body> 之间的文本是可见的页面内容
- JavaScript 被设计用来向html页面添加交互行为.
- xml vs html:
 - xml 扩展标记语言, 被设计为传输和存储数据, 关注数据内容
 - html 超文本标记语言, 被设计用来显示数据, 关注数据的外观
- xml 允许自定义标签

###Chapter3 Python拾遗

- 为了加快模块加载速度, 每个模块都在`__pycache__`目录中放置了该模块的预编译模块, 命名为`modul.version.pyc`, `version`是模块的预编译版本编码, 通常会包含python的版本号
- `import`语句的执行过程:
 1. 创建新的module对象
 2. 将该module对象插入sys.module中
 3. 装载module的代码. 搜索module程序所在位置的顺序如下所示. 由于搜索有先后顺序, 因此存在覆盖问题
  1. 当前路径
  2. PYTHONPATH指定的路径
  3. Python安装时设置的相关默认路径
 4. 执行新的module中对应代码

##Chapter4 WebDriver API

###4.1 定位元素
- webdriver 属于 selenium 体系中设计出来操作浏览器的一套 api. 站在webdriver的角度, 它针对多种编程语言都实现了一遍这套 api, 所以支持多语言; 站在编程语言角度, 是用于实现 web 自动化的第三方库.
- 查找元素的方法:
 1. 通过元素本身的属性, 如 id, name等
 2. 通过位置属性, xpath与css就提供了以标签名为层级关系的定位方式
 3. 通过相关元素
- id 定位 - `find_element_by_id` - 在html中, id 具有唯一性
- name 定位 - `find_element_by_name` - 不一定唯一
- class 定位 - `find_element_by_class_name`
- tag 定位 - `find_element_by_tag_name` - html的本质就是通过tag来定义实现不同的功能, 每个元素本质上也是一个tag
- link 定位 - `find_element_by_link_text` - 专门用来定位文本链接. 通过元素标签对之间的文本信息来定位元素
- partial link 定位 - `find_element_by_partial_link_text` - 对link定位的补充. 对于长文本链接, 可取部分信息来定位, 只要能唯一地标识该链接即可
- xpath 定位 - `find_element_by_xpath` - xpath 是 xml 中定位元素的语言.
 - 绝对路径定位 - 用标签名的层级关系来定位元素的绝对路径, 根路径为`/html`. 如果同层有多个相同标签名, 按从上往下的顺序指明, 从1开始, 如`div[2]`
 - 元素属性定位 - `find_element_by_xpath("//input[@id='stb']")`, `//`表示当前文档的某层, `input`表示定位元素的标签名, `[@id='stb']`表示元素的id属性值为stb. 更一般的形式为:\\
`find_element_by_xpath("//tagName[@attrName=attrValue]")`\\
可使用通配符`*`
 - 层级与属性结合 - 通过属性定位找到元素的父元素, 再通过层级关系定位到指定元素, 如\\
`find_element_by_xpath("//span[@class='xxx']/input")
 - 使用逻辑运算符定位 - 如果一个属性不能唯一地区分一个元素, 可通过使用逻辑运算符连接多个属性来定位它, 如\\
`find_element_by_xpath("//input[@id='kw' and @class='su']/span/input")
- css 定位 - `find_element_by_css_selector` - css 用于描述 html 或 xml 文档的表现形式. css使用选择器来为页面元素绑定属性, 这为元素定位提供了便利. css 可以选择控件的任意属性, 一般情况下比xpath定位要快.
 - 通过css选择器的class属性定位: `find_element_by_css_selector(".bg_btn")`
 - 通过css选择器的id属性定位: `find_element_by_css_selector("#su")`
 - 通过css选择器的标签名定位: `find_element_by_css_selector("input")`
 - 通过css选择器的父子关系定位: `find_element_by_css_selector("span>input")` - 将查找父标签下所有的子标签
 - 通过css选择器的属性定位: `find_element_by_css_selector("[name='kw']")` - 属性值可加引号, 也可不加
 - css选择器组合定位: `find_element_by_css_selector("form.fm>span>input.s_ipt") -
 - css选择器常见语法:

```text
.class            .intro           class 选择器,选择 class="intro"的所有元素
#id               #firstname       id 选择器,选择所有 id= " firstname " 所有元素
*                 *                选择所有元素
element           p                元素所有<p>元素
element > element div > input      选择父元素为 <div> 元素的所有 <input> 元素
element + element div + input      选择紧接在 <div> 元素之后的所有 <p> 元素。
[attribute=value] [target=_blank]  选择 target="_blank" 的所有元素
```

- 用 By 定位元素, 此时统一使用`find_element`方法, 第一个参数定位`By.XXX`, 用于指定定位的类型, 第二个参数与上一样, 指定定位的具体方式. 底层的代码实现是一样的, 但`find_element_by_xxx`的表达更清晰.

###4.2 控制浏览器

- `set_window_size()` - 设置窗口大小
- `maxmize_window()` - 浏览器窗口最大化
- `back()` - 后退
- `forward()` - 前进
- `refresh()` - 刷新页面

###4.3 简单元素操作

- `clear()` - 清楚文本
- `send_keys(*value)` - 模拟按键输入
- `click()` - 单击
- 文本输入框中可能有引导用户输入的提示信息, 因此在输入内容之前最好先调用`clear()`方法清楚内容.
- `submit()` - 提交表单, 功能与单击按钮类似:

```python
In [11]: driver.find_element_by_id("query").send_keys("机器学习")

In [12]: driver.find_element_by_id("query").submit()
```

- `size` - 返回元素中大小
- `location` - 返回元素的座标
- text` - 获取文本信息
- `get_attribute(name)` - 获得属性值
- `is_displayed()` - 判断是否可见

###4.4 鼠标事件

- `ActionChains`链中定义了一系列的鼠标操作, 该类的构造方法以`webdriver`为参数
- 除了`click`, `send_keys`等已经封装进`WebElement`的方法, 其他的鼠标事件都是基于元素的, 即使用元素或元素的属性作为参数, 而不能简单地使用点标记法
- `perform()` - 执行所有ActionChains中存储的行为
- `context_click(elm)` - 右击
- `double_click(elm)` - 双击
- `drag_and_drop(source, target)` - 拖动
- `move_to_element()` - 鼠标悬停

###4.5 键盘事件

- `Keys`提供了键盘上提供的几乎所有按键的方法. 多参数方式调用`send_keys`方法可输入组合键.

###4.6 获得验证信息

- 在编写功能测试用例时,一般会有预期结果,在执行用例的过程中将得到的实际结果与预期结果进行比较, 从而判断用户的通过与失败。
- 自动化测试用例由机器执行, 在完成之后, 通过获取一些信息来验证成功或失败, 而不必人工地检测. 常用的验证信息包括`title`, `URL`, `text`.
- `title` - 返回网页的标题
- `current_url` - 返回当前页面的url

###4.7 设置元素等待

- 大多数web应用都使用`AJAX`技术, 当浏览器加载页面时, 并不同时加载所有的页面元素, 这为元素定位增加了难度.
- `显式等待` - 等待某个条件成立时继续执行, 否则在达到最大时长时抛出超时异常

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.get("http://www.sogou.com")
# presence_of_all_elements_located(object) - 返回WebElement, 一旦它被加载
# until(method, message='') - 调用driver提供的方法, 直到返回值为True
element = WebDriverWait(driver,5,0.5).until(
              EC.presence_of_element_located((By.ID,"query")))  # 通过By定位
element.send_keys("selenium")
```

- `WebDriverWait(driver, timeout, poll_frequency=0.5, ignored_exceptions=None)` - 等待方法, 一般与`until`或`until_not`连用
- `until(method, message='')`
- `until_not(method, message='')`
- `expected_conditions`类提供的预期条件判断的方法:

```text
title_is                                   用于判断标题是否存在
title_contains                             用于判断标题是否包含预期信息。
presence_of_element_located                判断元素是否被加载DOM树里, 并不代表元素一定可见
visibility_of_element_located              元素是否可见
visibility_of                              同上, 用法略有不同
presence_of_all_elements_located           判断一组元素的是否存在
text_to_be_present_in_element              判断元素的text是否包含预期的字符串
text_to_be_present_in_element_value        判断元素的value属性是否包含预期的字符串
frame_to_be_available_and_switch_to_it     表单是否可用,若可用则切换到该表单。
invisibility_of_element_located            判断元素是否隐藏
element_to_be_clickable                    判断元素是否可见并可点击
staleness_of                               等到一个元素不再是依附于 DOM。
element_to_be_selected                     被选中的元素
element_located_to_be_selected             期望找到元素并选中ta
element_selection_state_to_be              判断某个元素的选中状态是否符合预期
element_located_selection_state_to_be      期望找到一个元素并检查是否选择状态
alert_is_present                           预期一个警告信息
```

- 也可以用`is_displayed()`来判断元素是否可见:

```python
from selenium import webdriver
from time import sleep, ctime

driver = webdriver.Firefox()
driver.get("http://www.baidu.com")
print(ctime())
for i in range(10):
    try:
        el = driver.find_element_by_id("kw22")
        if el.is_displayed():
            break
    except:
        sleep(1)
    else:
        print("time out")
    driver.close()
    print(ctime())

```
