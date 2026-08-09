# 🔄 Python JSON

> 适用 Python 3.8+。标准库 `json` 用于 JSON 文本与 Python 基础对象之间的序列化和反序列化。

## 目录

- [1. 核心概念](#1-核心概念)
- [2. 核心用法](#2-核心用法)
- [3. 关键机制](#3-关键机制)
- [4. 常见陷阱与工程实践](#4-常见陷阱与工程实践)
- [5. 面试速查](#5-面试速查)
- [6. 参考资料](#6-参考资料)

## 1. 核心概念

| Python | JSON | 反序列化后的 Python 类型 |
| --- | --- | --- |
| `dict` | object | `dict` |
| `list`、`tuple` | array | `list` |
| `str` | string | `str` |
| `int`、`float` | number | `int`、`float` |
| `True`、`False` | true、false | `bool` |
| `None` | null | `None` |

序列化把对象转换为 JSON，反序列化执行反向转换。`dumps()/loads()` 操作字符串，`dump()/load()` 操作文件类对象。

## 2. 核心用法

```python
import json

payload = {
    "name": "Ada",
    "skills": ["Python", "SQL"],
    "active": True,
}

encoded = json.dumps(
    payload,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
)
decoded = json.loads(encoded)

print(encoded)
print(decoded == payload)  # True
```

`dump()` 和 `load()` 可直接处理打开的文本文件或内存流：

```python
import io
import json

buffer = io.StringIO()
json.dump({"status": "ok"}, buffer)
buffer.seek(0)

print(json.load(buffer))  # {'status': 'ok'}
```

自定义类型可通过 `default` 转换为 JSON 基础类型，并用 `object_hook` 恢复：

```python
import json
from datetime import datetime

def encode_object(value):
    if isinstance(value, datetime):
        return {"__type__": "datetime", "value": value.isoformat()}
    raise TypeError(f"unsupported type: {type(value).__name__}")

def decode_object(value):
    if value.get("__type__") == "datetime":
        return datetime.fromisoformat(value["value"])
    return value

encoded = json.dumps(datetime(2026, 8, 9, 10, 30), default=encode_object)
decoded = json.loads(encoded, object_hook=decode_object)
print(decoded)  # 2026-08-09 10:30:00
```

## 3. 关键机制

JSON object 的键必须是字符串。Python 字典中的整数键序列化后会变成字符串，因此往返转换不一定保持对象完全相等。

浮点数遵循二进制浮点语义。金融等需要十进制精度的场景，可在解析时使用 `Decimal`：

```python
import json
from decimal import Decimal

value = json.loads("0.1", parse_float=Decimal)
print(value, type(value).__name__)  # 0.1 Decimal
```

Python 默认允许输出 `NaN` 和无穷大，但它们不属于严格 JSON。跨系统接口可设置 `allow_nan=False`，在遇到这些值时及时失败。

`JSONEncoder` 和 `JSONDecoder` 可用于更复杂的扩展；多数业务场景使用 `default`、`object_hook` 以及显式数据映射已经足够。

## 4. 常见陷阱与工程实践

- JSON 不保存 Python 的元组、集合、日期时间、`Decimal` 或自定义类语义，需要明确编码协议。
- 不要用 `eval()` 解析 JSON；始终使用 `json.loads()`。
- 不可信 JSON 可能消耗大量 CPU 或内存，应在网关或读取层限制消息大小和嵌套深度。
- `object_hook` 会处理每个 JSON object，不应依据不可信字段动态导入模块或实例化任意类。
- API 输出应明确字符编码，通常使用 UTF-8，并统一日期、时区和数值约定。
- 用 `ensure_ascii=False` 保留可读 Unicode；写文件时仍需显式使用 UTF-8 编码。

## 5. 面试速查

| 问题 | 结论 |
| --- | --- |
| `dump` 与 `dumps` 有何区别？ | 前者写文件类对象，后者返回字符串 |
| `load` 与 `loads` 有何区别？ | 前者读文件类对象，后者解析字符串或字节数据 |
| 元组往返 JSON 后还是元组吗？ | 不是，JSON array 会解码为列表 |
| 如何序列化自定义对象？ | 用 `default` 函数或自定义 `JSONEncoder` 转为基础类型 |
| JSON 数字如何保留十进制精度？ | 使用 `parse_float=Decimal` 并制定输出编码策略 |

## 6. 参考资料

- [Python 官方文档：json](https://docs.python.org/3/library/json.html)
- [Python 官方文档：JSONEncoder](https://docs.python.org/3/library/json.html#json.JSONEncoder)
- [RFC 8259：The JavaScript Object Notation Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259)
- [参考 Notebook：11-JSON.ipynb](https://github.com/patrickloeber/python-engineer-notebooks/blob/master/advanced-python/11-JSON.ipynb)
