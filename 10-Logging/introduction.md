# 📝 Python Logging（日志）

> 适用 Python 3.8+。`logging` 将事件按级别发送到控制台、文件或集中式系统，是生产环境可观测性的基础组件。

## 目录

- [1. 核心概念](#1-核心概念)
- [2. 核心用法](#2-核心用法)
- [3. 关键机制](#3-关键机制)
- [4. 常见陷阱与工程实践](#4-常见陷阱与工程实践)
- [5. 面试速查](#5-面试速查)
- [6. 参考资料](#6-参考资料)

## 1. 核心概念

日志处理链路为：`Logger → LogRecord → Handler → Formatter → 输出目标`。`Filter` 可附加在 Logger 或 Handler 上进一步筛选记录。

| 级别 | 数值 | 典型用途 |
| --- | :---: | --- |
| `DEBUG` | 10 | 开发诊断细节 |
| `INFO` | 20 | 正常生命周期和关键业务事件 |
| `WARNING` | 30 | 可继续运行但需要关注的问题 |
| `ERROR` | 40 | 当前操作失败 |
| `CRITICAL` | 50 | 服务可能无法继续运行的严重故障 |

默认阈值为 `WARNING`，低于阈值的记录不会输出。

## 2. 核心用法

应用入口负责配置，业务模块通过 `logging.getLogger(__name__)` 获取分层 Logger：

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger(__name__)
user_id = 42
logger.info("user authenticated: user_id=%s", user_id)
```

复杂应用可为不同目标设置独立 Handler 和阈值：

```python
import logging

logger = logging.getLogger("interview.service")
logger.setLevel(logging.DEBUG)
logger.propagate = False

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(
    logging.Formatter("%(levelname)s %(name)s %(message)s")
)

if not logger.handlers:
    logger.addHandler(handler)

logger.debug("hidden by handler")
logger.info("service started")
```

异常处理器内使用 `logger.exception()` 自动附带 traceback：

```python
try:
    int("not-a-number")
except ValueError:
    logger.exception("failed to parse input")
```

## 3. 关键机制

Logger 名称以点分层，例如 `app.api` 的父 Logger 是 `app`。记录默认向祖先 Handler 传播；子 Logger 和根 Logger 同时配置 Handler 时，常出现重复日志。

Logger 和 Handler 都有级别过滤：记录必须先通过 Logger 阈值，再通过每个 Handler 的阈值。Formatter 只负责输出格式，不决定是否记录。

工程中通常使用 `logging.config.dictConfig()` 集中配置；文件增长可使用 `RotatingFileHandler` 或 `TimedRotatingFileHandler`。多进程直接写同一文件可能产生竞争，更稳妥的方案是通过 `QueueHandler` 汇总到单一监听器或外部日志系统。

参数化日志会推迟字符串格式化，低于阈值时避免不必要工作：

```python
logger.debug("loaded %d records for %s", 120, "users")
```

## 4. 常见陷阱与工程实践

- 库代码不要调用 `basicConfig()`，只创建模块 Logger；最终应用统一决定输出方式。
- 避免重复添加 Handler，并理解 `propagate` 是否开启。
- 使用 `%s` 参数化记录，不要提前拼接昂贵字符串。
- 日志中不得写入密码、访问令牌、完整身份证号等敏感信息。
- 不要同时记录并重新抛出每一层异常，否则同一失败会重复出现多次。
- 结构化日志应保持稳定字段，例如 `request_id`、`user_id`、`duration_ms`，便于检索聚合。
- 日志轮转不是长期归档方案；生产环境应结合采集、保留和访问控制策略。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| Logger、Handler、Formatter 分别负责什么？ | 创建记录、路由输出、格式化展示 |
| 为什么日志会重复？ | 子 Logger 自有 Handler 输出后又向祖先传播 |
| `logger.exception()` 与 `logger.error()` 有何区别？ | 前者在异常处理块中默认附带 traceback |
| 为什么推荐 `getLogger(__name__)`？ | Logger 名称与模块层级一致，便于统一配置和定位来源 |
| 参数化日志有何优势？ | 记录被过滤时可避免提前格式化，并分离消息模板与参数 |

## 6. 参考资料

- [Python 官方文档：logging](https://docs.python.org/3/library/logging.html)
- [Python 官方 HOWTO：Logging](https://docs.python.org/3/howto/logging.html)
- [Python 官方文档：Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
- [Python 官方文档：logging.config](https://docs.python.org/3/library/logging.config.html)
- [参考 Notebook：10-Logging.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/10-Logging.ipynb)
