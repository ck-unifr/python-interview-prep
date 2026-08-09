# 📦 Python Tuple（元组）

> 适用 Python 3.8+。`tuple` 是有序、不可变序列，适合表达结构固定且不应被重新赋值的数据。

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
| 有序 | 支持索引、切片和顺序遍历 |
| 不可变 | 创建后不能增删元素，也不能为某个索引重新赋值 |
| 可重复 | 同一个值可以出现多次 |
| 元素类型不限 | 元组可引用任意对象，包括可变对象 |
| 条件可哈希 | 仅当所有元素都可哈希时，元组才能作为字典键或集合元素 |

元组由逗号定义，圆括号主要用于分组。`(1)` 是整数，`(1,)` 才是单元素元组。

## 2. 核心用法

```python
user = ("Ada", 36, "London")
single = (42,)
numbers = tuple(range(5))

print(user[0])      # Ada
print(numbers[1:4]) # (1, 2, 3)
print(user.count("Ada"))  # 1
print(user.index(36))      # 1
```

序列解包要求变量数量与元素数量匹配；星号变量可以接收剩余元素，并始终得到一个列表。

```python
name, age, city = user
first, *middle, last = (1, 2, 3, 4, 5)

print(name, age, city)  # Ada 36 London
print(middle)           # [2, 3, 4]
```

函数用逗号分隔返回多个值时，实际返回的是元组：

```python
def min_max(values):
    return min(values), max(values)

minimum, maximum = min_max([3, 1, 8])
print(minimum, maximum)  # 1 8
```

## 3. 关键机制

不可变指元组保存的引用不能被替换，不代表引用对象本身一定不可变。

```python
record = ("settings", ["dark"])
record[1].append("compact")
print(record)  # ('settings', ['dark', 'compact'])
```

与列表相比，CPython 元组结构更简单，通常占用更少的容器内存，创建和遍历也可能略快。具体差异受 Python 版本、平台和数据规模影响，不应依赖固定字节数或微小性能差异做设计。

元组的哈希值取决于各元素。包含列表、字典或集合的元组不可哈希：

```python
coordinates = {(31.2, 121.5): "Shanghai"}
print(coordinates[(31.2, 121.5)])  # Shanghai

try:
    hash(([1, 2],))
except TypeError as error:
    print(type(error).__name__)  # TypeError
```

## 4. 常见陷阱与工程实践

- 单元素元组必须保留尾随逗号：`value = (42,)`。
- `a += (x,)` 会创建新元组并重新绑定变量，不是原地修改。
- 元组只提供浅层不可变性；若业务要求深层不可变，内部也应使用不可变对象。
- 结构具有明确字段含义时，优先考虑 `typing.NamedTuple`、`collections.namedtuple` 或数据类，提高可读性。
- 不要为了未经测量的性能差异，把需要频繁修改的数据强行改成元组。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| 元组为什么不可变？ | 其元素引用在创建后不能增删或重新赋值 |
| 元组一定可哈希吗？ | 不一定；所有元素都可哈希时才可哈希 |
| `(1)` 与 `(1,)` 有何区别？ | 前者是整数，后者是单元素元组 |
| 元组内的列表能修改吗？ | 能；元组限制的是保存的引用，不会冻结引用对象 |
| 何时优先使用元组？ | 数据结构固定、语义上不应修改，或需要可哈希序列时 |

## 6. 参考资料

- [Python 官方教程：Tuples and Sequences](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences)
- [Python 官方文档：Sequence Types](https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range)
- [Python 官方文档：Hashable](https://docs.python.org/3/glossary.html#term-hashable)
- [参考 Notebook：02-Tuple.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/02-Tuple.ipynb)
