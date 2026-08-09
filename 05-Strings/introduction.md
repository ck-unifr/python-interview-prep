# 🔤 Python String（字符串）

> 适用 Python 3.8+。`str` 是不可变的 Unicode 文本序列，文本与字节数据应在系统边界明确转换。

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
| Unicode 文本 | `str` 表示文本，`bytes` 表示原始字节 |
| 不可变 | 不能修改单个位置；所有变换都产生新字符串 |
| 有序序列 | 支持索引、切片、遍历和成员测试 |
| 可哈希 | 可作为字典键或集合元素 |

索引按 Unicode 码点工作，不等同于用户看到的“字符簇”。例如某些重音字符或 emoji 可能由多个码点组成。

## 2. 核心用法

```python
text = "  Python Interview  "
clean = text.strip()

print(clean.lower())              # python interview
print(clean.startswith("Python"))  # True
print(clean.find("Interview"))     # 7
print(clean.replace("Interview", "Guide"))
print(clean[0:6])                 # Python
```

`split()` 将字符串拆成列表，`separator.join(iterable)` 将多个字符串高效连接：

```python
line = "python,sql,linux"
skills = line.split(",")
result = " | ".join(skill.upper() for skill in skills)
print(result)  # PYTHON | SQL | LINUX
```

Python 3.8+ 中优先使用 f-string 表达格式化意图：

```python
name = "Ada"
score = 95.678

print(f"{name}: {score:.2f}")  # Ada: 95.68
print(f"{42:08d}")             # 00000042
```

## 3. 关键机制

因为字符串不可变，循环中反复执行 `result += piece` 可能持续创建新对象并复制已有内容。已知多个片段时，通常使用 `join()`：

```python
parts = ["api", "v1", "users"]
path = "/" + "/".join(parts)
print(path)  # /api/v1/users
```

CPython 可能自动驻留部分字符串，也可通过 `sys.intern()` 主动驻留，以减少大量重复标识符的存储和比较成本。驻留是实现优化，判断字符串内容必须使用 `==`，不能使用 `is`。

编码用于把文本变为字节，解码执行反向转换：

```python
message = "你好，Python"
payload = message.encode("utf-8")
restored = payload.decode("utf-8")

print(restored == message)  # True
```

## 4. 常见陷阱与工程实践

- `strip(chars)` 删除两端属于 `chars` 集合的字符，不是删除完整前后缀。
- `find()` 未找到时返回 `-1`；`index()` 未找到时抛出 `ValueError`。
- 不要混用 `str` 与 `bytes`；文件、网络和数据库边界应明确字符编码。
- 不可信内容不要直接拼接到 SQL、Shell 或 HTML；应使用参数化查询和对应的转义机制。
- 需要不区分大小写比较时，国际化文本通常用 `casefold()` 比 `lower()` 更稳妥。
- 等价 Unicode 文本可能有不同码点组合，必要时使用 `unicodedata.normalize()`。

```python
import unicodedata

left = "é"
right = "e\u0301"
print(left == right)  # False
print(unicodedata.normalize("NFC", right) == left)  # True
```

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| 为什么字符串不可变？ | 内容变化会创建新对象，因此字符串可安全哈希和共享 |
| `str` 与 `bytes` 有何区别？ | `str` 表示 Unicode 文本，`bytes` 表示字节序列 |
| 大量片段如何拼接？ | 使用 `separator.join(parts)`，避免循环反复复制 |
| `==` 与 `is` 比较字符串有何区别？ | `==` 比较内容，`is` 比较对象身份，不能依赖驻留结果 |
| `find()` 与 `index()` 有何区别？ | 未找到时分别返回 `-1` 和抛出 `ValueError` |

## 6. 参考资料

- [Python 官方文档：Text Sequence Type — str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)
- [Python 官方文档：Format String Syntax](https://docs.python.org/3/library/string.html#format-string-syntax)
- [Python 官方文档：Unicode HOWTO](https://docs.python.org/3/howto/unicode.html)
- [Python 官方文档：sys.intern](https://docs.python.org/3/library/sys.html#sys.intern)
- [参考 Notebook：05-Strings.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/05-Strings.ipynb)
