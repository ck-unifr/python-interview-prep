# ✳️ The Asterisk in Python（星号运算符）

> 适用 Python 3.8+。`*` 与 `**` 根据语法位置表示乘幂、重复、参数收集或可迭代对象与映射的解包。

## 目录

- [1. 核心概念](#1-核心概念)
- [2. 核心用法](#2-核心用法)
- [3. 关键机制](#3-关键机制)
- [4. 常见陷阱与工程实践](#4-常见陷阱与工程实践)
- [5. 面试速查](#5-面试速查)
- [6. 参考资料](#6-参考资料)

## 1. 核心概念

| 位置 | 含义 | 示例 |
| --- | --- | --- |
| 表达式 | 乘法、幂运算或序列重复 | `3 * 4`、`2 ** 8`、`"ab" * 2` |
| 函数定义 | 收集位置或关键字实参 | `def f(*args, **kwargs)` |
| 函数调用 | 解包可迭代对象或映射 | `f(*values, **options)` |
| 赋值 | 收集剩余元素 | `first, *rest = values` |
| 容器显示 | 合并可迭代对象或映射 | `[*left, *right]`、`{**a, **b}` |
| 函数签名中的裸 `*` | 后续参数仅限关键字 | `def f(x, *, timeout)` |

## 2. 核心用法

```python
print(7 * 5)       # 35
print(2 ** 4)      # 16
print("ab" * 3)   # ababab
print((1, 2) * 2) # (1, 2, 1, 2)
```

参数收集与调用解包：

```python
def request(path, *segments, timeout=5, **headers):
    return path, segments, timeout, headers

parts = ["users", "42"]
options = {"timeout": 10, "authorization": "token"}

result = request("/api", *parts, **options)
print(result)
```

扩展解包和容器合并：

```python
numbers = [1, 2, 3, 4, 5]
first, *middle, last = numbers
print(first, middle, last)  # 1 [2, 3, 4] 5

left = (1, 2)
right = {3, 4}
merged = [*left, *right]

defaults = {"debug": False, "port": 8000}
overrides = {"debug": True}
config = {**defaults, **overrides}
print(config)  # {'debug': True, 'port': 8000}
```

## 3. 关键机制

函数定义中的 `*args` 会创建元组，`**kwargs` 会创建新字典。名称 `args` 和 `kwargs` 只是惯例，真正决定语义的是星号。

调用时 `*iterable` 会消费可迭代对象并按位置绑定，`**mapping` 的键必须是字符串且符合参数名要求。重复绑定同一参数会抛出 `TypeError`。

PEP 448 允许在调用和容器显示中使用多个解包。字典显示中后出现的同名键覆盖前值：

```python
base = {"retries": 2, "timeout": 5}
environment = {"timeout": 10}
explicit = {"timeout": 3}

config = {**base, **environment, **explicit}
print(config["timeout"])  # 3
```

扩展赋值每一层最多有一个星号目标，该目标始终接收列表，即使右侧是元组或生成器。

## 4. 常见陷阱与工程实践

序列重复复制的是引用，不会递归复制可变元素：

```python
rows = [[0] * 2] * 3
rows[0][0] = 1
print(rows)  # [[1, 0], [1, 0], [1, 0]]

safe_rows = [[0] * 2 for _ in range(3)]
```

- `*generator` 会一次性消费生成器，可能占用大量内存。
- 展开集合时不能依赖顺序；需要稳定顺序时先排序。
- `**mapping` 的键必须是字符串，且不能与已绑定关键字冲突。
- 不要让 `*args/**kwargs` 掩盖稳定参数；公开 API 应尽可能显式。
- `**` 的结合优先级高于一元负号，例如 `-2 ** 2` 等于 `-(2 ** 2)`。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| `*args` 与 `**kwargs` 保存什么？ | 额外位置实参的元组与额外关键字实参的字典 |
| 星号解包目标是什么类型？ | 始终是列表 |
| `{**a, **b}` 键冲突时谁覆盖？ | 后出现的映射覆盖前值 |
| `[[0] * m] * n` 有什么问题？ | 外层重复同一个内层列表引用 |
| 裸 `*` 在函数签名中表示什么？ | 后续参数只能按关键字传入 |

## 6. 参考资料

- [Python 语言参考：Calls](https://docs.python.org/3/reference/expressions.html#calls)
- [Python 语言参考：Assignment statements](https://docs.python.org/3/reference/simple_stmts.html#assignment-statements)
- [PEP 448：Additional Unpacking Generalizations](https://peps.python.org/pep-0448/)
- [PEP 3102：Keyword-Only Arguments](https://peps.python.org/pep-3102/)
- [参考 Notebook：19-The Asterisk(*).ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/19-The%20Asterisk%28%2A%29.ipynb)
