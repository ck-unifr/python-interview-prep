# 🪞 Python Copying（浅拷贝与深拷贝）

> 适用 Python 3.8+。赋值、浅拷贝和深拷贝创建的对象关系不同，选择依据是哪些可变层级必须独立。

## 目录

- [1. 核心概念](#1-核心概念)
- [2. 核心用法](#2-核心用法)
- [3. 关键机制](#3-关键机制)
- [4. 常见陷阱与工程实践](#4-常见陷阱与工程实践)
- [5. 面试速查](#5-面试速查)
- [6. 参考资料](#6-参考资料)

## 1. 核心概念

| 操作 | 外层对象 | 嵌套对象 |
| --- | --- | --- |
| `alias = original` | 共享 | 共享 |
| `copy.copy(original)` | 新建 | 共享引用 |
| `copy.deepcopy(original)` | 新建 | 递归复制可变对象 |

变量保存对象引用。赋值只创建新的名称绑定，不会复制对象。

## 2. 核心用法

```python
from copy import copy, deepcopy

original = {"name": "Ada", "skills": ["Python", "SQL"]}
alias = original
shallow = copy(original)
deep = deepcopy(original)

original["skills"].append("Linux")
original["name"] = "Grace"

print(alias["name"])       # Grace，共享外层对象
print(shallow["name"])     # Ada，外层已独立
print(shallow["skills"])   # ['Python', 'SQL', 'Linux']
print(deep["skills"])      # ['Python', 'SQL']
```

内建容器通常提供简洁的浅拷贝方式：

```python
source_list = [1, 2, 3]
copy_a = source_list.copy()
copy_b = list(source_list)
copy_c = source_list[:]

source_dict = {"a": 1}
copy_d = source_dict.copy()
copy_e = dict(source_dict)
```

## 3. 关键机制

`deepcopy()` 使用内部 memo 字典记录已复制对象，因此能够处理循环引用，并尽量保持原对象图中的共享关系：

```python
from copy import deepcopy

shared = [1, 2]
original = [shared, shared]
cloned = deepcopy(original)

print(cloned[0] is cloned[1])  # True
print(cloned[0] is shared)     # False
```

不可变对象可能被安全复用，因此深拷贝不保证每个节点都有新身份。函数、类等对象通常按原对象返回；模块、栈帧、套接字等资源对象不适合通用复制。

自定义类可实现 `__copy__()` 和 `__deepcopy__(memo)` 控制行为。实现深拷贝时必须使用并传递 `memo`，否则循环引用可能导致无限递归或破坏共享结构。

## 4. 常见陷阱与工程实践

- 深拷贝不是默认安全选项；对象图大时会显著增加时间和内存成本。
- 文件、锁、数据库连接和网络套接字应明确管理所有权，通常不应复制。
- 浅拷贝足以隔离外层增删，但无法隔离嵌套可变对象。
- 只需修改少数字段时，显式构造新对象通常比深拷贝整个图更清晰。
- 不可变数据结构能减少复制需求，并让并发代码更易推理。
- 测试复制逻辑时同时检查 `==` 与关键节点的 `is` 关系。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| `b = a` 是否复制对象？ | 不复制，只让两个名称引用同一对象 |
| 浅拷贝复制几层？ | 创建新外层容器，嵌套对象仍共享 |
| 深拷贝如何处理循环引用？ | 通过 memo 记录已复制对象，避免无限递归 |
| 深拷贝是否让所有对象身份都不同？ | 不一定，不可变或特殊对象可能被复用 |
| 何时应避免深拷贝？ | 对象图很大、包含外部资源或只需局部更新时 |

## 6. 参考资料

- [Python 官方文档：copy](https://docs.python.org/3/library/copy.html)
- [Python 官方文档：Object identity](https://docs.python.org/3/reference/datamodel.html#objects-values-and-types)
- [Python 官方 FAQ：How do I copy an object?](https://docs.python.org/3/faq/programming.html#how-do-i-copy-an-object-in-python)
- [参考 Notebook：20-Copying.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/20-Copying.ipynb)
