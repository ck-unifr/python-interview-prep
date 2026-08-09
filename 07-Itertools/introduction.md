# ♾️ Python itertools

> 适用 Python 3.8+。`itertools` 提供可组合的惰性迭代器，用于高效处理排列组合、分组、累计和无限序列。

## 目录

- [1. 核心概念](#1-核心概念)
- [2. 核心用法](#2-核心用法)
- [3. 关键机制](#3-关键机制)
- [4. 常见陷阱与工程实践](#4-常见陷阱与工程实践)
- [5. 面试速查](#5-面试速查)
- [6. 参考资料](#6-参考资料)

## 1. 核心概念

`itertools` 中的大多数函数返回迭代器，按需生成结果，不会预先构造完整列表。

| 类别 | 常用工具 |
| --- | --- |
| 组合输入 | `chain()`、`zip_longest()` |
| 截取与筛选 | `islice()`、`takewhile()`、`dropwhile()` |
| 排列组合 | `product()`、`permutations()`、`combinations()` |
| 累计与分组 | `accumulate()`、`groupby()` |
| 无限迭代器 | `count()`、`cycle()`、`repeat()` |
| 复制迭代流 | `tee()` |

## 2. 核心用法

组合与截取不会复制全部输入：

```python
from itertools import chain, islice

merged = chain([1, 2], (3, 4), range(5, 8))
print(list(islice(merged, 5)))  # [1, 2, 3, 4, 5]
```

排列组合的顺序由输入位置决定：

```python
from itertools import combinations, permutations, product

print(list(product("AB", repeat=2)))
# [('A', 'A'), ('A', 'B'), ('B', 'A'), ('B', 'B')]

print(list(permutations([1, 2, 3], 2)))
print(list(combinations([1, 2, 3], 2)))
```

`accumulate()` 计算前缀累计值；`groupby()` 只合并连续且键相同的元素：

```python
from itertools import accumulate, groupby
from operator import mul

print(list(accumulate([1, 2, 3, 4])))       # [1, 3, 6, 10]
print(list(accumulate([1, 2, 3, 4], mul)))  # [1, 2, 6, 24]

records = sorted(
    [("A", "Ada"), ("B", "Linus"), ("A", "Grace")],
    key=lambda item: item[0],
)
groups = {
    key: [name for _, name in rows]
    for key, rows in groupby(records, key=lambda item: item[0])
}
print(groups)  # {'A': ['Ada', 'Grace'], 'B': ['Linus']}
```

## 3. 关键机制

迭代器通常是一次性的：每次 `next()` 消费一个元素，耗尽后再次遍历不会自动重置。若确实需要两条独立消费路径，可使用 `tee()`，但两者消费速度差异会转化为内部缓存。

无限迭代器必须搭配终止条件或 `islice()`：

```python
from itertools import count, islice

even_numbers = (number for number in count(0, 2))
print(list(islice(even_numbers, 5)))  # [0, 2, 4, 6, 8]
```

排列组合结果数量增长很快。若输入长度为 `n`、选择长度为 `r`：

| 工具 | 结果数量 |
| --- | --- |
| `product(items, repeat=r)` | `n ** r` |
| `permutations(items, r)` | `n! / (n-r)!` |
| `combinations(items, r)` | `n! / (r! * (n-r)!)` |

## 4. 常见陷阱与工程实践

- 不要对无限迭代器直接调用 `list()`、`sum()` 或无界循环。
- `groupby()` 分组的是相邻元素；全局分组前通常先按同一个键排序。
- `groupby()` 返回的组与底层迭代器共享数据，应在进入下一组前消费或保存当前组。
- `tee()` 不是线程安全队列，也不适合消费速度长期悬殊的分支。
- 惰性处理能降低峰值内存，但不会降低结果本身的组合规模。
- 逻辑简单时优先生成器表达式；多步迭代管道再使用 `itertools` 组合。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| `itertools` 为什么节省内存？ | 结果按需产生，不预先保存完整序列 |
| `permutations()` 与 `combinations()` 有何区别？ | 前者考虑顺序，后者不考虑顺序 |
| `groupby()` 为什么常需先排序？ | 它只合并连续且键相同的元素 |
| `islice()` 与普通切片有何区别？ | 它惰性截取迭代器，不要求对象支持索引 |
| `tee()` 的主要代价是什么？ | 分支消费不同步时需要缓存尚未被慢分支读取的元素 |

## 6. 参考资料

- [Python 官方文档：itertools](https://docs.python.org/3/library/itertools.html)
- [Python 官方文档：Iterator Types](https://docs.python.org/3/library/stdtypes.html#iterator-types)
- [Python 官方 HOWTO：Functional Programming](https://docs.python.org/3/howto/functional.html)
- [参考 Notebook：07-Itertools.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/07-Itertools.ipynb)
