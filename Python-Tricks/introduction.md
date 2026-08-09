# 🪄 Python Tricks（实用技巧）

> 适用 Python 3.8+。这些惯用写法用于减少样板代码并清晰表达意图，前提是团队成员能快速读懂。

## 目录

- [1. 核心概念](#1-核心概念)
- [2. 核心用法](#2-核心用法)
- [3. 关键机制](#3-关键机制)
- [4. 常见陷阱与工程实践](#4-常见陷阱与工程实践)
- [5. 面试速查](#5-面试速查)
- [6. 参考资料](#6-参考资料)

## 1. 核心概念

Pythonic 代码强调直接表达数据关系，而不是追求最短字符数。常见工具包括序列解包、`join()`、`enumerate()`、`zip()`、推导式、`any()` 和 `all()`。

判断一个技巧是否值得使用，可以检查三点：

- 是否让意图比展开写法更清晰；
- 是否避免不必要的中间对象或重复查找；
- 是否保留正确的边界行为和错误处理。

## 2. 核心用法

序列解包可交换变量，无需临时变量：

```python
left, right = 5, 10
left, right = right, left
print(left, right)  # 10 5

values = [1, 2, 3, 4]
values[0], values[-1] = values[-1], values[0]
print(values)  # [4, 2, 3, 1]
```

连接字符串使用 `join()`，同时处理索引和值使用 `enumerate()`：

```python
words = ["Python", "is", "clear"]
sentence = " ".join(words)
print(sentence)  # Python is clear

for position, word in enumerate(words, start=1):
    print(position, word)
```

`zip()` 按位置组合多个可迭代对象，`any()` 与 `all()` 表达整体条件：

```python
names = ["Ada", "Linus", "Grace"]
scores = [95, 88, 92]
ranking = dict(zip(names, scores))

print(any(score >= 95 for score in scores))  # True
print(all(score >= 60 for score in scores))  # True
print(ranking["Ada"])                        # 95
```

## 3. 关键机制

多目标赋值先计算右侧，再按左侧结构绑定，因此变量交换不会覆盖旧值。

`str.join()` 先基于片段构造结果，避免循环拼接不可变字符串时反复复制已有内容。连接对象必须全部是字符串，否则抛出 `TypeError`。

`enumerate()`、`zip()`、`any()` 和 `all()` 都是惰性消费输入：

- `zip()` 默认在最短输入耗尽时停止；
- `any()` 遇到第一个真值即停止；
- `all()` 遇到第一个假值即停止；
- `any([])` 为 `False`，`all([])` 为 `True`。

链式比较只对中间表达式求值一次：

```python
age = 36
print(18 <= age < 65)  # True
```

## 4. 常见陷阱与工程实践

- `zip()` 长度不一致时会静默截断；需要保留缺失项时使用 `itertools.zip_longest()`。
- `join()` 不会自动转换非字符串元素，应显式使用 `map(str, values)` 或格式化逻辑。
- `all([])` 为真属于空真值，业务上要求“至少一个且全部满足”时还需检查输入非空。
- 复杂的一行推导式或解包会降低可读性，应拆成有名称的步骤。
- 技巧不能替代异常处理、类型边界和性能测量。
- 不要在同一表达式中依赖集合或无序来源的迭代顺序。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| Python 如何无临时变量交换值？ | 多目标赋值先计算右侧，再统一绑定左侧 |
| 为什么批量字符串拼接用 `join()`？ | 避免不可变字符串在循环中反复复制 |
| `zip()` 输入长度不同会怎样？ | 默认在最短输入结束时停止 |
| `any([])` 和 `all([])` 分别是什么？ | `False` 和 `True` |
| `enumerate()` 比手动索引好在哪里？ | 直接生成位置和值，避免额外状态和越界错误 |

## 6. 参考资料

- [Python 官方教程：Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Python 官方文档：Built-in Functions](https://docs.python.org/3/library/functions.html)
- [Python 官方文档：str.join](https://docs.python.org/3/library/stdtypes.html#str.join)
- [Python 官方文档：itertools.zip_longest](https://docs.python.org/3/library/itertools.html#itertools.zip_longest)
- [参考 Notebook：Python Tricks.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/Python%20Tricks.ipynb)
