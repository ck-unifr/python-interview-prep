# 🗂️ Python Dictionary（字典）

> 适用 Python 3.8+。`dict` 是保存键值映射的可变容器，适合按唯一键快速查询和更新数据。

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
| 键唯一 | 重复赋值会覆盖同一个键对应的值 |
| 键可哈希 | 字符串、数字及仅含可哈希元素的元组可作键 |
| 值类型不限 | 值可以是任意 Python 对象 |
| 可变 | 支持新增、更新和删除键值对 |
| 保持插入顺序 | Python 3.7+ 将插入顺序规定为语言行为 |

## 2. 核心用法

```python
user = {"name": "Ada", "age": 36}
user["city"] = "London"
user["age"] = 37

print(user["name"])           # Ada
print(user.get("email"))      # None
print(user.get("role", "user"))  # user

age = user.pop("age")
print(age)  # 37
```

`items()` 同时提供键和值；字典推导式适合做映射或过滤。

```python
scores = {"Ada": 95, "Linus": 88, "Grace": 92}

passed = {
    name: score
    for name, score in scores.items()
    if score >= 90
}

print(passed)  # {'Ada': 95, 'Grace': 92}
```

`update()` 原地合并，后出现的同名键覆盖原值：

```python
config = {"debug": False, "port": 8000}
config.update({"debug": True, "workers": 4})
print(config)
# {'debug': True, 'port': 8000, 'workers': 4}
```

## 3. 关键机制

CPython 字典采用哈希表。查询、插入和删除的平均时间复杂度为 `O(1)`，遍历为 `O(n)`；哈希冲突严重时理论最坏可退化到 `O(n)`。

查找过程先计算键的哈希值，再用相等性比较确认键。作为键的对象必须在生命周期内保持哈希值稳定，因此列表、字典和普通集合不能作为键。

| 操作 | 平均复杂度 |
| --- | :---: |
| `mapping[key]`、赋值、删除 | `O(1)` |
| `key in mapping` | `O(1)` |
| `len(mapping)` | `O(1)` |
| 遍历、`copy()` | `O(n)` |

`keys()`、`values()` 和 `items()` 返回动态视图，字典变化会反映到视图中，而不是立即复制全部数据。

## 4. 常见陷阱与工程实践

不要用 `dict.fromkeys()` 创建相互独立的可变默认值：

```python
bad = dict.fromkeys(["a", "b"], [])
bad["a"].append(1)
print(bad)  # {'a': [1], 'b': [1]}

good = {key: [] for key in ("a", "b")}
```

- `mapping[key]` 在键缺失时抛出 `KeyError`；允许缺失时用 `get()`，需要创建默认容器时用 `setdefault()` 或 `defaultdict`。
- 遍历字典时改变其大小会抛出 `RuntimeError`；需要删除时遍历 `list(mapping)` 或构造新字典。
- `copy()` 只复制最外层，嵌套可变值仍共享引用。
- 用 `in` 判断的是键；检查值需要显式使用 `value in mapping.values()`，其复杂度通常为 `O(n)`。
- 不可信输入不能直接驱动任意对象构造或属性访问。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| 字典为什么通常能 `O(1)` 查询？ | 通过键的哈希值定位槽位，再用相等性比较确认 |
| 字典是否有序？ | Python 3.7+ 保证保持插入顺序，但不会按键自动排序 |
| 哪些对象能作为键？ | 哈希值稳定且支持相等性比较的可哈希对象 |
| `get()` 与 `setdefault()` 有何区别？ | `get()` 不修改字典；缺失时 `setdefault()` 会写入默认值 |
| 浅拷贝能隔离嵌套值吗？ | 不能，嵌套对象仍然共享 |

## 6. 参考资料

- [Python 官方教程：Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)
- [Python 官方文档：Mapping Types — dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
- [Python 官方文档：Dictionary view objects](https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects)
- [CPython 源码：Objects/dictobject.c](https://github.com/python/cpython/blob/main/Objects/dictobject.c)
- [参考 Notebook：03-Dictionary.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/03-Dictionary.ipynb)
