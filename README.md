# Logging 的简单使用和原理
## 简单使用
- 三大部分 Logger、Handler、Formatter
- Logger，提供对外的使用接口 `logger.info` `logger.warning` 等
- Handler，提供处理 LogRecord 的能力（输出到指定位置），常见的有 `StreamHandler`、`FileHandler` 等
- Formatter，提供格式化日志的能力

### 示例
```python
# 获取 logger
import logging
logger = logging.getLogger(__name__)

# 设置日志等级 LogLevel
# NOTSET、DEBUG、INFO、WARNING、ERROR、CRITICAL
logger.setLevel(logging.INFO)

# 尝试一下
logger.info('hello world')
# No handlers could be found for logger "xxx"

# 添加 Handler
logger.addHandler(logging.StreamHandler())
logger.info('hello world')

# 添加 Formatter
sh = logging.StreamHandler()
fmt = logging.Formatter('[%(asctime)s][%(levelname)s]%(message)s')
sh.setFormatter(fmt)
logger.addHandler(sh)
logger.warn('hello world')
# 输出：
# hello world （第一个 Handler 输出的）
# [2018-11-28 10:39:40,543][WARNING]hello world （第二个带 Formatter 的 StreamHandler 输出的）
```

formatter 参考


参数 | 说明
--- | ---
%(name)s | Name of the logger (logging channel)
%(levelno)s | Numeric logging level for the message (DEBUG, INFO, WARNING, ERROR, CRITICAL)
%(levelname)s | ext logging level for the message (“DEBUG”, “INFO”, “WARNING”, “ERROR”, “CRITICAL”)
%(pathname)s | Full pathname of the source file where the loggingcall was issued (if available)
%(filename)s | Filename portion of pathname
%(module)s | Module (name portion of filename)
%(lineno)d | Source line number where the logging call was issued (if available)
%(funcName)s | Function name
%(created)f | Time when the LogRecord was created (time.time() return value)
%(asctime)s | Textual time when the LogRecord was created
%(msecs)d | Millisecond portion of the creation time
%(relativeCreated)d | Time in milliseconds when the LogRecord was created, relative to the time the logging module was loaded (typically at application startup time)
%(thread)d | Thread ID (if available)
%(threadName)s | Thread name (if available)
%(process)d | Process ID (if available)
%(message)s | The result of record.getMessage(), computed just as the record is emitted

## 原理
1. Logger & Handler，基本打印日志 [戳我](/commit/b80857f6f232fdb99a349d4c54a6a6bed95f7ccd)
2. 增加 Formatter，引入 LogRecord，支持各种格式 [戳我](/commit/e634d014b304a487b2650326b24a7e006f582355)
3. 引入 LogLevel [打印不同等级的接口](/commit/dfa03f72ed6c5de107c1b6e45187b9a1819580ec)
4. logLevel 过滤 [logger 对 level 过滤](/commit/668dee9819ea02278d14d637e71aece46f36b595) [Handler 对 level 的过滤](/commit/ad5855e40d4d7b255a42e4b5a6f006c630a8f252)
5. logger 父子关系引入 [戳我](/commit/b4ddaa14f95fdff6da67703af9f46a3bbc7dcf83)
6. 魔改姿势 [戳我](/commit/5c265c654846bd96eff8911eddf4ae1d6442d0d4)
	- 外面包一层，转发到 Logger
	- 根据需求，更改 Logger、Handler、Formatter


附：[logger flow](https://upload-images.jianshu.io/upload_images/477558-a099cc71d0a4c453.png?imageMogr2/auto-orient/)
