# ⚙️ Python Generators（生成器）

> 适用 Python 3.8+。生成器按需产生值并在 `yield` 处保存执行状态，适合流式处理和大规模数据管道。

## 目录

- [1. 核心概念](#1-核心概念)
- [2. 核心用法](#2-核心用法)
- [3. 关键机制](#3-关键机制)
- [4. 常见陷阱与工程实践](#4-常见陷阱与工程实践)
- [5. 面试速查](#5-面试速查)
- [6. 参考资料](#6-参考资料)

## 1. 核心概念

函数体中出现 `yield` 后，调用该函数会返回生成器对象，而不会立即执行函数体。`next()` 恢复执行，直到下一个 `yield`；函数结束时抛出 `StopIteration`。

| 对比 | 列表 | 生成器 |
| --- | --- | --- |
| 计算时机 | 通常立即计算全部元素 | 按需计算一个元素 |
| 内存 | 保存全部结果 | 主要保存当前执行状态 |
| 重复遍历 | 可以 | 通常一次性 |
| 索引与长度 | 支持 | 不支持 |

## 2. 核心用法

```python
def countdown(start):
    while start > 0:
        yield start
        start -= 1

counter = countdown(3)
print(next(counter))  # 3
print(next(counter))  # 2
print(list(counter))  # [1]
```

生成器表达式使用圆括号，适合组合惰性处理步骤：

```python
numbers = range(1_000_000)
squares = (number * number for number in numbers)
even_squares = (value for value in squares if value % 2 == 0)

first_five = []
for value in even_squares:
    first_five.append(value)
    if len(first_five) == 5:
        break

print(first_five)  # [0, 4, 16, 36, 64]
```

`yield from` 将值生成委托给另一个可迭代对象：

```python
def flatten(groups):
    for group in groups:
        yield from group

print(list(flatten([[1, 2], [], [3, 4]])))  # [1, 2, 3, 4]
```

## 3. 关键机制

生成器对象同时实现 `__iter__()` 和 `__next__()`，因此既是可迭代对象也是迭代器。每次挂起时会保存局部变量、指令位置和异常处理状态。

生成器支持双向控制：

| 方法 | 作用 |
| --- | --- |
| `next(gen)` | 恢复执行并获取下一个值 |
| `gen.send(value)` | 向暂停的 `yield` 表达式发送值 |
| `gen.throw(error)` | 在暂停位置抛入异常 |
| `gen.close()` | 抛入 `GeneratorExit` 请求清理 |

生成器中的 `return value` 会结束迭代，`value` 存放在 `StopIteration.value` 中；`yield from` 可以接收该返回值。

## 4. 常见陷阱与工程实践

- 生成器耗尽后不能自动重置；需要再次遍历时重新调用生成器函数。
- 惰性只降低中间结果的内存占用；一旦 `list(generator)`，仍会保存全部结果。
- 生成器没有 `len()` 和随机索引，算法依赖这些能力时应选择序列。
- 不要在生成器内部显式 `raise StopIteration`；Python 3.7+ 会将其转换为 `RuntimeError`。
- 持有文件、锁等资源的生成器应使用 `try/finally`，并确保被完整消费或显式关闭。
- 生成器表达式捕获外部变量时，同样需要注意闭包的后期绑定。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| 调用生成器函数会立即执行吗？ | 不会，只创建生成器对象；首次迭代才开始执行 |
| `yield` 与 `return` 有何区别？ | `yield` 暂停并可恢复，`return` 结束当前调用 |
| 生成器为什么节省内存？ | 一次只产生当前值，不保存完整结果集合 |
| 生成器能重复遍历吗？ | 同一对象通常不能，耗尽后需重新创建 |
| 生成器与迭代器是什么关系？ | 生成器是由 Python 自动维护状态的一类迭代器 |

## 6. 参考资料

- [Python 语言参考：Yield expressions](https://docs.python.org/3/reference/expressions.html#yield-expressions)
- [Python 官方文档：Generator Types](https://docs.python.org/3/library/stdtypes.html#generator-types)
- [Python 官方 HOWTO：Functional Programming](https://docs.python.org/3/howto/functional.html#generators)
- [PEP 380：Syntax for Delegating to a Subgenerator](https://peps.python.org/pep-0380/)
- [参考 Notebook：14-Generators.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/14-Generators.ipynb)
