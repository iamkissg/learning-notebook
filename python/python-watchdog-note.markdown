```python
# official demo
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # 若指定了路径,则path等于指定的路径,否则为当前路径
    # sys.argv[0]永远是被执行脚本本身
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = LoggingEventHandler()  # 事件处理器
    observer = Observer()  # 监视器
    observer.schedule(event_handler, path, recursive=True)  # 设置监视器
    observer.start()  # 启动监视器
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

- 使用`watchdog`的一般步骤:
 1. 创建`watchdog.observers.Observer`实例
 2. 实现`watchdog.events.FileSystemEventHandler`子类
 3. 将事件处理器绑定到监视器实例的时间表管理上
 4. 启动监视器

- `watchdog.events.FileSystemEvent`: 表示文件系统事件的不可变类,当监控的文件系统发生改变时,被触发.所有文件系统事件对象都是不可变的,因此可以被用作dict的key,或作为set的元素
 - event_type: 类型为str, 但默认为None
 - src_path: 触发事件的文件系统对象的源路径
 - 其他许多子类,见[官方文档](http://pythonhosted.org/watchdog/api.html#module-watchdog.events)
- `watchdog.events.FileSystemEventHandler`: 文件系统事件处理器基类,可以继承与覆盖
 - dispatch(event): 将事件转交给合适的方法,参数表示一个文件系统事件
 - on_any_event(event): 捕获全部事件
 - on_created(event): 当文件或目录被创建时,被调用的处理
 - on_deleted(event):
 - on_modified(event):
 - on_moved(event):
 - 其他子类见[官方文档](http://pythonhosted.org/watchdog/api.html#event-handler-classes)
- `watchdog.observers.Obeserver`: 观测器线程负责监视目标目录,当事件发生时调用相应的事件处理器
- 其他有一些api什么的,看[文档](http://pythonhosted.org/watchdog/api.html#module-watchdog.observers.api)

