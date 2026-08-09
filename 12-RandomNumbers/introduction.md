# 🎲 Python Random Numbers（随机数）

> 适用 Python 3.8+。仿真与测试使用 `random`，密码、令牌和安全选择必须使用 `secrets`。

## 目录

- [1. 核心概念](#1-核心概念)
- [2. 核心用法](#2-核心用法)
- [3. 关键机制](#3-关键机制)
- [4. 常见陷阱与工程实践](#4-常见陷阱与工程实践)
- [5. 面试速查](#5-面试速查)
- [6. 参考资料](#6-参考资料)

## 1. 核心概念

| 工具 | 随机源 | 适用场景 |
| --- | --- | --- |
| `random` | 确定性伪随机生成器 | 仿真、抽样、游戏、可复现测试 |
| `secrets` | 操作系统提供的安全随机源 | 令牌、密码重置链接、安全选择 |
| `random.SystemRandom` | 操作系统提供的随机源 | 需要 `random` 风格 API 的安全抽样 |
| NumPy `Generator` | 独立的向量化伪随机生成器 | 科学计算和多维数组 |

`random` 默认核心生成器是 Mersenne Twister，可复现但不具备密码学安全性。

## 2. 核心用法

使用独立 `Random` 实例可避免修改模块级全局状态：

```python
import random

rng = random.Random(42)

print(rng.random())          # [0.0, 1.0)
print(rng.uniform(1.0, 5.0))
print(rng.randint(1, 6))     # 两端都包含
print(rng.randrange(0, 10))  # 不包含 10
print(rng.choice(["A", "B", "C"]))
print(rng.sample(range(10), k=3))  # 不放回抽样

items = [1, 2, 3, 4]
rng.shuffle(items)           # 原地打乱并返回 None
```

`choices()` 支持放回抽样和权重：

```python
import random

rng = random.Random(7)
result = rng.choices(
    population=["common", "rare"],
    weights=[95, 5],
    k=5,
)
print(result)
```

安全令牌使用 `secrets`：

```python
import secrets

token = secrets.token_urlsafe(32)
code = "".join(secrets.choice("0123456789") for _ in range(6))

print(len(token) > 32)  # True
print(len(code))        # 6
```

## 3. 关键机制

相同种子使伪随机状态从同一起点演化，因此同一调用序列可复现：

```python
import random

first = random.Random(123)
second = random.Random(123)

print([first.randrange(100) for _ in range(4)])
print([second.randrange(100) for _ in range(4)])
```

复现依赖种子、调用顺序和受控的软件环境。并发共享同一个生成器会让调用顺序不稳定；测试中可为每个任务提供独立实例。

NumPy 使用独立随机状态，调用 `random.seed()` 不会设置 NumPy 生成器。现代代码使用 `default_rng()`：

```python
# 需要额外安装 NumPy
import numpy as np

rng = np.random.default_rng(42)
values = rng.integers(0, 10, size=(2, 3))
print(values)
```

## 4. 常见陷阱与工程实践

- 不要用 `random` 生成会话令牌、验证码密钥或密码；使用 `secrets`。
- 不要在每次取样前重新设置种子，这会重复产生相同模式。
- `randint(a, b)` 包含 `b`，`randrange(a, b)` 不包含 `b`。
- `sample()` 不放回，`choices()` 默认放回；前者要求 `k` 不超过总体大小。
- `shuffle()` 原地修改列表并返回 `None`。
- 安全令牌应有足够熵、设置有效期并在服务端安全存储；随机性不能替代完整安全设计。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| 伪随机是否等于不可预测？ | 不等于；已知状态或种子时序列可预测 |
| `random` 与 `secrets` 如何选择？ | 普通仿真用前者，任何安全用途用后者 |
| `sample` 与 `choices` 有何区别？ | 前者不放回，后者默认放回且支持权重 |
| `seed()` 的主要用途是什么？ | 让受控环境中的伪随机调用序列可复现 |
| NumPy 是否共享 `random` 的种子？ | 不共享，应独立创建和传递 NumPy Generator |

## 6. 参考资料

- [Python 官方文档：random](https://docs.python.org/3/library/random.html)
- [Python 官方文档：secrets](https://docs.python.org/3/library/secrets.html)
- [Python 官方文档：random.SystemRandom](https://docs.python.org/3/library/random.html#random.SystemRandom)
- [NumPy 官方文档：Random Generator](https://numpy.org/doc/stable/reference/random/generator.html)
- [参考 Notebook：12-RandomNumbers.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/12-RandomNumbers.ipynb)
