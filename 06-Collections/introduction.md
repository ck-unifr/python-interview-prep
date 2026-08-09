# 🧰 Python collections

> 适用 Python 3.8+。`collections` 提供针对计数、分组、队列和轻量记录等场景优化的容器类型。

## 目录

- [1. 核心概念](#1-核心概念)
- [2. 核心用法](#2-核心用法)
- [3. 关键机制](#3-关键机制)
- [4. 常见陷阱与工程实践](#4-常见陷阱与工程实践)
- [5. 面试速查](#5-面试速查)
- [6. 参考资料](#6-参考资料)

## 1. 核心概念

| 类型 | 主要用途 |
| --- | --- |
| `Counter` | 统计可哈希对象的出现次数 |
| `defaultdict` | 键缺失时通过工厂函数创建默认值 |
| `deque` | 在两端以近似 `O(1)` 复杂度增删元素 |
| `namedtuple` | 创建带字段名的不可变元组子类 |
| `OrderedDict` | 强调重排操作和顺序敏感相等性 |
| `ChainMap` | 将多个映射组合为分层查找视图 |

普通 `dict` 从 Python 3.7 起已保证插入顺序；只有需要 `move_to_end()`、双端弹出或顺序敏感比较时，`OrderedDict` 才更合适。

## 2. 核心用法

`Counter` 适合频次统计，`defaultdict` 适合分组：

```python
from collections import Counter, defaultdict

words = ["api", "db", "api", "cache", "db", "api"]
counts = Counter(words)
print(counts.most_common(2))  # [('api', 3), ('db', 2)]

groups = defaultdict(list)
for name, team in [("Ada", "A"), ("Linus", "B"), ("Grace", "A")]:
    groups[team].append(name)

print(groups["A"])  # ['Ada', 'Grace']
```

`deque` 适合队列、双端队列和固定长度窗口：

```python
from collections import deque

queue = deque(["task-1", "task-2"])
queue.append("task-3")
current = queue.popleft()

recent = deque(maxlen=3)
recent.extend([1, 2, 3, 4])

print(current)       # task-1
print(list(recent))  # [2, 3, 4]
```

`namedtuple` 用字段名替代位置索引，同时保留元组语义：

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
point = Point(x=3, y=4)

print(point.x)       # 3
print(point._asdict())  # {'x': 3, 'y': 4}
```

## 3. 关键机制

- `Counter` 是字典子类，缺失键读取为 `0`，但不会因此自动插入键。
- `defaultdict(factory)` 在 `mapping[key]` 缺失时调用无参数工厂并写入结果；`get()` 不会触发工厂。
- `deque` 为两端操作优化；中间索引和删除仍可能是 `O(n)`。
- `namedtuple` 实例不可变且可解包，但不会自动进行运行时类型校验。
- `ChainMap` 写入默认只作用于第一个映射，读取按映射顺序查找。

```python
from collections import ChainMap

defaults = {"debug": False, "port": 8000}
overrides = {"debug": True}
config = ChainMap(overrides, defaults)

print(config["debug"], config["port"])  # True 8000
```

## 4. 常见陷阱与工程实践

- `Counter` 会保留零次和负次数；需要清理时可使用一元加号：`clean = +counter`。
- 读取 `defaultdict[key]` 会改变字典；只检查时用 `key in mapping` 或 `get()`。
- `extendleft(iterable)` 逐个从左侧加入，因此最终顺序与输入相反。
- `deque` 不适合频繁随机访问；该场景继续使用列表。
- 需要默认值计算依赖键时，`defaultdict` 不够直接，应显式处理缺失逻辑。
- 需要可变记录、默认值和类型提示时，数据类通常比 `namedtuple` 更清晰。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| `defaultdict` 与普通字典有何区别？ | `[]` 访问缺失键时会调用工厂并写入默认值 |
| 为什么队列优先用 `deque`？ | 两端追加和弹出近似 `O(1)`，列表头部操作为 `O(n)` |
| `Counter` 的缺失键返回什么？ | 返回整数 `0` |
| Python 3.7+ 还需要 `OrderedDict` 吗？ | 仅在重排、双端弹出或顺序敏感相等性等专门场景需要 |
| `namedtuple` 是否会校验字段类型？ | 不会；它只提供字段名和元组行为 |

## 6. 参考资料

- [Python 官方文档：collections](https://docs.python.org/3/library/collections.html)
- [Python 官方文档：Counter](https://docs.python.org/3/library/collections.html#collections.Counter)
- [Python 官方文档：deque](https://docs.python.org/3/library/collections.html#collections.deque)
- [Python 官方文档：defaultdict](https://docs.python.org/3/library/collections.html#collections.defaultdict)
- [参考 Notebook：06-Collections.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/06-Collections.ipynb)
