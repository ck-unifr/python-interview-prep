# 🧱 Python List（列表）

> 适用 Python 3.8+。`list` 是按位置保存元素的可变序列，适合有序存储、索引访问和顺序遍历。

## 目录

- [1. 核心概念](#1-核心概念)
- [2. 核心用法](#2-核心用法)
- [3. 关键机制](#3-关键机制)
- [4. 常见陷阱与工程实践](#4-常见陷阱与工程实践)
- [5. 面试速查](#5-面试速查)
- [6. 参考资料](#6-参考资料)

## 1. 核心概念

| 特性 | 说明 |
| --- | --- |
| 有序 | 元素按位置保存；有序不等于自动排序 |
| 可变 | 创建后可以新增、删除或替换元素 |
| 可重复 | 同一个值可以出现多次 |
| 元素类型不限 | 可引用任意对象；工程代码通常保持元素类型一致 |
| 不可哈希 | `list` 不能作为集合元素或字典键 |

## 2. 核心用法

列表可通过 `[]` 或 `list(iterable)` 创建。索引从 `0` 开始，负索引从末尾计数。

```python
fruits = ["apple", "banana", "apple"]
fruits[1] = "pear"
fruits.append("orange")
fruits.extend(["lemon", "mango"])
removed = fruits.pop()

print(fruits[0])         # apple
print(fruits[-1])        # lemon
print("pear" in fruits)  # True
print(removed)           # mango
```

| 操作 | 作用 |
| --- | --- |
| `append(x)` | 在末尾添加一个对象 |
| `extend(iterable)` | 逐个追加可迭代对象中的元素 |
| `insert(i, x)` | 在索引 `i` 前插入 |
| `pop([i])` | 删除并返回指定元素，默认处理末尾 |
| `remove(x)` | 删除第一个等于 `x` 的元素 |
| `index(x)`、`count(x)` | 查询首次位置和出现次数 |
| `reverse()`、`sort()` | 原地反转和排序 |

切片语法为 `items[start:stop:step]`，包含 `start`、不包含 `stop`：

```python
numbers = list(range(10))

print(numbers[2:7:2])  # [2, 4, 6]
print(numbers[-3:])    # [7, 8, 9]
print(numbers[::-1])   # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

numbers[2:5] = [20, 30]  # 切片赋值可改变列表长度
```

推导式适合简单映射和过滤，`enumerate()` 同时提供位置和值：

```python
names = ["Ada", "Guido", "Grace"]
lengths = [len(name) for name in names]
long_names = [name for name in names if len(name) > 4]

for position, name in enumerate(names, start=1):
    print(position, name)

print(lengths)     # [3, 5, 5]
print(long_names)  # ['Guido', 'Grace']
```

`sort()` 原地排序并返回 `None`；`sorted()` 接收任意可迭代对象并返回新列表。两者都是稳定排序，并支持 `key` 和 `reverse`。

## 3. 关键机制

赋值共享同一列表；`copy()`、`list(source)` 和 `source[:]` 只复制最外层：

```python
from copy import deepcopy

original = [[1, 2], [3, 4]]
alias = original
shallow = original.copy()
deep = deepcopy(original)

original[0].append(99)

print(alias)    # [[1, 2, 99], [3, 4]]
print(shallow)  # [[1, 2, 99], [3, 4]]
print(deep)     # [[1, 2], [3, 4]]
```

设 `n` 为列表长度，`k` 为本次处理的元素数：

| 操作 | 时间复杂度 |
| --- | :---: |
| `len(items)`、`items[i]`、索引赋值 | `O(1)` |
| `append(x)` | 均摊 `O(1)` |
| `pop()` | `O(1)` |
| `extend(iterable)`、切片复制 | `O(k)` |
| 中间插入、删除或 `pop(i)` | `O(n)` |
| `x in items`、`index()`、`remove()` | `O(n)` |
| `copy()` | `O(n)` |
| `sort()` | 通常及最坏 `O(n log n)`；已有顺序时可接近 `O(n)` |

在 CPython 中，列表底层是连续的对象引用数组。扩容时会预留空间，因此多数 `append()` 为 `O(1)`，少数操作需要重新分配并复制引用，整体为均摊 `O(1)`。中间增删需要移动后续引用，所以为 `O(n)`。该内存布局属于 CPython 实现细节。

## 4. 常见陷阱与工程实践

序列乘法会重复引用，不能用来创建相互独立的二维列表：

```python
bad = [[0] * 3] * 2
bad[0][0] = 1
print(bad)  # [[1, 0, 0], [1, 0, 0]]

good = [[0] * 3 for _ in range(2)]
good[0][0] = 1
print(good)  # [[1, 0, 0], [0, 0, 0]]
```

- 遍历时直接删除元素可能漏处理；过滤时构造新列表。
- 原地修改方法通常返回 `None`，不要把 `append()` 或 `sort()` 的结果重新赋给列表。
- 频繁从头部增删使用 `collections.deque`，避免整体移动。
- 高频成员测试且允许去重时使用 `set`。
- 推导式包含多层嵌套、复杂条件或副作用时，普通循环更清晰。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| `append(x)` 与 `extend(xs)` 有何区别？ | 前者添加一个对象，后者逐个追加元素 |
| 为什么 `append()` 是均摊 `O(1)`？ | CPython 扩容时预留空间，只有少数追加需要重新分配 |
| 切片是深拷贝吗？ | 不是，只创建新的外层列表 |
| `sort()` 与 `sorted()` 如何选择？ | 允许修改原列表用前者；需保留原数据或处理任意迭代对象用后者 |
| 为什么头部插入是 `O(n)`？ | 需要移动后续元素引用 |

## 6. 参考资料

- [Python 官方教程：More on Lists](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)
- [Python 官方文档：Sequence Types — list](https://docs.python.org/3/library/stdtypes.html#lists)
- [Python 官方文档：Sorting HOW TO](https://docs.python.org/3/howto/sorting.html)
- [CPython 源码：Objects/listobject.c](https://github.com/python/cpython/blob/main/Objects/listobject.c)
- [Python Wiki：TimeComplexity](https://wiki.python.org/moin/TimeComplexity)
- [参考 Notebook：01-Lists.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/01-Lists.ipynb)
