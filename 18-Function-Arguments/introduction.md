# 🧭 Python Function Arguments（函数参数）

> 适用 Python 3.8+。清晰的参数设计能约束调用方式、表达 API 意图，并避免默认值和可变对象引发的隐蔽状态问题。

## 目录

- [1. 核心概念](#1-核心概念)
- [2. 核心用法](#2-核心用法)
- [3. 关键机制](#3-关键机制)
- [4. 常见陷阱与工程实践](#4-常见陷阱与工程实践)
- [5. 面试速查](#5-面试速查)
- [6. 参考资料](#6-参考资料)

## 1. 核心概念

参数是函数定义中的名称，实参是调用时提供的对象。Python 支持五类参数：

| 参数类别 | 定义形式 | 调用方式 |
| --- | --- | --- |
| 仅限位置 | `/` 之前 | 只能按位置 |
| 位置或关键字 | 普通参数 | 位置或关键字 |
| 可变位置 | `*args` | 收集额外位置实参为元组 |
| 仅限关键字 | `*` 之后 | 只能按关键字 |
| 可变关键字 | `**kwargs` | 收集额外关键字实参为字典 |

## 2. 核心用法

`/` 与 `*` 可以把公开 API 的调用约束写入签名：

```python
def connect(host, /, port=5432, *, timeout=5, ssl=False):
    return {
        "host": host,
        "port": port,
        "timeout": timeout,
        "ssl": ssl,
    }

config = connect("db.internal", 5433, timeout=10, ssl=True)
print(config)
```

可变参数适合数量真正不固定的输入：

```python
def summarize(title, *values, precision=2, **metadata):
    average = sum(values) / len(values)
    return {
        "title": title,
        "average": round(average, precision),
        "metadata": metadata,
    }

result = summarize(
    "latency",
    10.2, 12.4, 11.8,
    precision=1,
    unit="ms",
)
print(result)
```

容器可在调用点解包：

```python
def point(x, y, z=0):
    return x, y, z

coordinates = [3, 4]
options = {"z": 5}
print(point(*coordinates, **options))  # (3, 4, 5)
```

## 3. 关键机制

默认参数在执行 `def` 时求值一次，而不是每次调用时求值。可变默认值会跨调用共享：

```python
def append_bad(value, items=[]):
    items.append(value)
    return items

print(append_bad(1))  # [1]
print(append_bad(2))  # [1, 2]

def append_safe(value, items=None):
    if items is None:
        items = []
    items.append(value)
    return items
```

Python 常被描述为“对象共享调用”或“对象引用按值传递”：形参先引用传入对象。修改可变对象会被调用方观察到，重新绑定形参不会改变调用方变量。

```python
def mutate(items):
    items.append(4)

def rebind(items):
    items = [99]

values = [1, 2, 3]
mutate(values)
rebind(values)
print(values)  # [1, 2, 3, 4]
```

## 4. 常见陷阱与工程实践

- 可变默认值使用 `None` 哨兵，在函数体中创建新对象。
- 位置实参必须出现在关键字实参之前，同一参数不能绑定两次。
- 仅限关键字参数适合布尔开关、单位、超时等易混淆选项。
- 不要用无约束的 `**kwargs` 隐藏稳定 API；明确参数更利于校验、补全和重构。
- 函数内部尽量避免 `global`；跨闭包修改外层局部变量才使用 `nonlocal`。
- 修改传入容器前应在文档或函数名中明确副作用，必要时先复制。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| `*args` 和 `**kwargs` 分别是什么类型？ | 元组和字典 |
| 默认参数何时求值？ | 函数定义执行时，只求值一次 |
| Python 是按值还是按引用传递？ | 形参获得同一对象的引用；引用本身按调用绑定 |
| `/` 和 `*` 在签名中做什么？ | 分隔仅限位置参数与仅限关键字参数 |
| 重新绑定形参会改变外部变量吗？ | 不会；但修改其引用的可变对象可能影响调用方 |

## 6. 参考资料

- [Python 官方教程：More on Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions)
- [Python 语言参考：Function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions)
- [Python 官方 FAQ：Why are default values shared?](https://docs.python.org/3/faq/programming.html#why-are-default-values-shared-between-objects)
- [PEP 570：Python Positional-Only Parameters](https://peps.python.org/pep-0570/)
- [参考 Notebook：18-Functions arguments.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/18-Functions%20arguments.ipynb)
