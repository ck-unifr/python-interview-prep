# 🧩 Python Set（集合）

> 适用 Python 3.8+。`set` 是保存唯一、可哈希元素的可变集合，适合去重、成员测试和集合运算。

## 目录

- [1. 核心概念](#1-核心概念)
- [2. 核心用法](#2-核心用法)
- [3. 关键机制](#3-关键机制)
- [4. 常见陷阱与工程实践](#4-常见陷阱与工程实践)
- [5. 面试速查](#5-面试速查)
- [6. 参考资料](#6-参考资料)

## 1. 核心概念

| 特性 | `set` | `frozenset` |
| --- | --- | --- |
| 元素唯一 | 是 | 是 |
| 元素需可哈希 | 是 | 是 |
| 可修改 | 是 | 否 |
| 自身可哈希 | 否 | 是 |
| 支持集合运算 | 是 | 是 |

集合不提供位置索引，也不承诺业务可依赖的迭代顺序。空集合必须写成 `set()`；`{}` 创建的是字典。

## 2. 核心用法

```python
tags = {"python", "backend", "python"}
tags.add("api")
tags.discard("missing")  # 元素不存在也不报错

print(len(tags))
print("python" in tags)  # True
```

常用集合运算同时提供运算符和方法：

| 运算 | 运算符 | 方法 |
| --- | :---: | --- |
| 并集 | `a \| b` | `a.union(b)` |
| 交集 | `a & b` | `a.intersection(b)` |
| 差集 | `a - b` | `a.difference(b)` |
| 对称差集 | `a ^ b` | `a.symmetric_difference(b)` |

```python
backend = {"Python", "SQL", "Linux"}
data = {"Python", "SQL", "Statistics"}

print(backend & data)  # {'Python', 'SQL'}
print(backend - data)  # {'Linux'}
print(backend | data)

required = {"Python", "SQL"}
print(required <= backend)       # True，子集
print(backend.isdisjoint({"Go"}))  # True
```

## 3. 关键机制

集合与字典一样基于哈希表。成员测试、添加和删除的平均复杂度为 `O(1)`，遍历为 `O(n)`；集合运算的成本与参与运算的集合大小相关。

元素必须可哈希，且哈希值在集合中保持稳定。`frozenset` 不可变，因此可用于嵌套集合或作为字典键：

```python
permissions = {
    frozenset({"read", "write"}): "editor",
    frozenset({"read"}): "viewer",
}

print(permissions[frozenset({"write", "read"})])  # editor
```

`update()`、`intersection_update()`、`difference_update()` 和 `symmetric_difference_update()` 会原地修改集合；对应的非 `update` 方法返回新集合。

## 4. 常见陷阱与工程实践

- `remove(x)` 在元素缺失时抛出 `KeyError`；允许缺失时使用 `discard(x)`。
- `pop()` 删除任意元素，不是随机抽样，也不能依赖返回顺序。
- `set(values)` 去重会丢失原顺序；需要保序去重时可用 `list(dict.fromkeys(values))`。
- 修改集合大小时不要同时遍历它；构造新集合或遍历副本。
- 高频成员测试适合集合；数据量很小或必须保留重复与顺序时，列表可能更直接。

```python
values = [3, 1, 3, 2, 1]
unique_in_order = list(dict.fromkeys(values))
print(unique_in_order)  # [3, 1, 2]
```

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| 如何创建空集合？ | 使用 `set()`，因为 `{}` 是空字典 |
| 为什么列表不能放入集合？ | 列表可变且不可哈希 |
| `remove()` 与 `discard()` 有何区别？ | 元素缺失时前者抛出 `KeyError`，后者不报错 |
| `set` 与 `frozenset` 有何区别？ | 前者可变且不可哈希，后者不可变且可哈希 |
| 集合成员测试为什么通常比列表快？ | 集合按哈希定位，列表需要线性扫描 |

## 6. 参考资料

- [Python 官方教程：Sets](https://docs.python.org/3/tutorial/datastructures.html#sets)
- [Python 官方文档：Set Types — set, frozenset](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)
- [CPython 源码：Objects/setobject.c](https://github.com/python/cpython/blob/main/Objects/setobject.c)
- [参考 Notebook：04-Sets.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/04-Sets.ipynb)
