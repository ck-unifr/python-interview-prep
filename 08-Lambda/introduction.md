# λ Python Lambda（匿名函数）

> 适用 Python 3.8+。`lambda` 用单个表达式创建匿名函数，适合短小、局部且语义直观的回调。

## 目录

- [1. 核心概念](#1-核心概念)
- [2. 核心用法](#2-核心用法)
- [3. 关键机制](#3-关键机制)
- [4. 常见陷阱与工程实践](#4-常见陷阱与工程实践)
- [5. 面试速查](#5-面试速查)
- [6. 参考资料](#6-参考资料)

## 1. 核心概念

语法为 `lambda parameters: expression`。表达式的结果会自动返回，无需写 `return`。

```python
add = lambda left, right: left + right
print(add(2, 3))  # 5
```

`lambda` 可以使用与普通函数相同的参数形式，但函数体只能包含一个表达式，不能直接写赋值、`try`、`while` 等语句。

## 2. 核心用法

最常见场景是提供短小的排序键：

```python
users = [
    {"name": "Linus", "score": 88},
    {"name": "Ada", "score": 95},
    {"name": "Grace", "score": 95},
]

ranked = sorted(
    users,
    key=lambda user: (-user["score"], user["name"]),
)
print([user["name"] for user in ranked])
# ['Ada', 'Grace', 'Linus']
```

`map()` 和 `filter()` 返回迭代器；简单转换或过滤通常用推导式更易读：

```python
numbers = [1, 2, 3, 4]

doubled = list(map(lambda value: value * 2, numbers))
evens = list(filter(lambda value: value % 2 == 0, numbers))

# 等价且通常更直观
doubled_comp = [value * 2 for value in numbers]
evens_comp = [value for value in numbers if value % 2 == 0]
```

`functools.reduce()` 将序列归约为一个值，但已有专用函数时优先使用 `sum()`、`min()`、`max()` 等：

```python
from functools import reduce
from operator import mul

product = reduce(mul, [1, 2, 3, 4], 1)
print(product)  # 24
```

## 3. 关键机制

Lambda 与普通嵌套函数一样形成闭包，并按名称在调用时查找外层变量。循环中直接创建闭包容易出现后期绑定：

```python
bad = [lambda: number for number in range(3)]
print([function() for function in bad])  # [2, 2, 2]

# 默认参数在函数创建时求值，可固定当前值
good = [lambda number=number: number for number in range(3)]
print([function() for function in good])  # [0, 1, 2]
```

排序的 `key` 函数对每个输入元素调用一次，其返回值用于比较。把昂贵计算放进键函数通常仍优于在比较函数中反复计算。

返回 lambda 可以构造简单函数工厂：

```python
def multiplier(factor):
    return lambda value: value * factor

double = multiplier(2)
print(double(6))  # 12
```

## 4. 常见陷阱与工程实践

- 已命名并会复用的复杂逻辑应使用 `def`，便于文档、类型标注、调试和测试。
- 不要为了“一行代码”嵌套多个 lambda；可读性优先于行数。
- 循环闭包需注意后期绑定，可用默认参数固定值，或定义显式函数工厂。
- Lambda 的跟踪信息通常显示为 `<lambda>`，大量使用会降低故障定位效率。
- `map()`、`filter()` 在 Python 3 中是惰性迭代器；需要列表时显式转换。
- 仅为赋值命名 lambda 不符合常见风格，此时直接使用 `def` 更清晰。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| Lambda 能写多少个表达式？ | 只能写一个表达式，但可接收任意合法参数形式 |
| Lambda 是否自动返回值？ | 是，表达式结果就是返回值 |
| 为什么循环中的 lambda 常返回同一个值？ | 闭包在调用时读取同一个外层变量，属于后期绑定 |
| `map/filter` 与推导式如何选择？ | 简单转换过滤优先推导式；已有函数或惰性管道可用前者 |
| Lambda 与 `def` 的本质差异是什么？ | 都创建函数对象；Lambda 受单表达式限制且名称通常为 `<lambda>` |

## 6. 参考资料

- [Python 语言参考：Lambdas](https://docs.python.org/3/reference/expressions.html#lambda)
- [Python 官方 HOWTO：Functional Programming](https://docs.python.org/3/howto/functional.html)
- [Python 官方文档：functools.reduce](https://docs.python.org/3/library/functools.html#functools.reduce)
- [Python 官方文档：Sorting HOW TO](https://docs.python.org/3/howto/sorting.html)
- [参考 Notebook：08-Lambda.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/08-Lambda.ipynb)
