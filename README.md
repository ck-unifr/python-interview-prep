<div align="center">

# 🐍 Python Interview Prep

**面向 Python 后端面试的核心知识库**

从内建类型到底层机制，从 Pythonic 编程到并发实践，建立系统、可复用的 Python 知识体系。

<p>
  <a href="https://www.python.org/"><img alt="Python 3.8+" src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white"></a>
  <a href="./LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/License-MIT-2ea44f?style=flat-square"></a>
  <a href="https://github.com/ck-unifr/python-interview-prep/stargazers"><img alt="GitHub Stars" src="https://img.shields.io/github/stars/ck-unifr/python-interview-prep?style=flat-square&logo=github"></a>
  <a href="https://github.com/ck-unifr/python-interview-prep/pulls"><img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square"></a>
</p>

[学习路线](#-学习路线) · [开始使用](#-开始使用) · [参与贡献](#-参与贡献)

</div>

> 每个主题聚焦 **核心原理、可运行示例与高频面试考点**，适合系统复习和面试前快速查漏补缺。

## 🗺️ 学习路线

状态：⬜ 计划中 · 🚧 编写中 · ✅ 已完成

### 🧱 1. 数据结构与内建类型

| 主题 | 核心考点 | 状态 |
| --- | --- | :---: |
| **Lists** | 内存分配、时间复杂度、列表推导式 | ⬜ |
| **Tuples** | 不可变性、内存占用、序列解包 | ⬜ |
| **Dictionaries** | 哈希表、冲突处理、字典推导式 | ⬜ |
| **Sets** | 集合运算、去重原理、`frozenset` | ⬜ |
| **Strings** | 字符串驻留、不可变性、格式化 | ⬜ |
| **Collections** | `Counter`、`namedtuple`、`deque` | ⬜ |

### 🧠 2. 高级特性与底层机制

| 主题 | 核心考点 | 状态 |
| --- | --- | :---: |
| **Decorators** | 闭包、参数化装饰器、`functools.wraps` | ⬜ |
| **Generators** | `yield`、惰性计算、生成器与迭代器 | ⬜ |
| **Context Managers** | `with`、`__enter__`、`__exit__` | ⬜ |
| **Copying** | 浅拷贝、深拷贝、对象引用关系 | ⬜ |

### 🔁 3. 函数与迭代

| 主题 | 核心考点 | 状态 |
| --- | --- | :---: |
| **Function Arguments** | `*args`、`**kwargs`、参数传递机制 | ⬜ |
| **Lambda Functions** | 匿名函数、`map`、`filter`、`reduce` | ⬜ |
| **Itertools** | 无限迭代器、排列组合、迭代器组合 | ⬜ |

### ⚡ 4. 并发与性能

| 主题 | 核心考点 | 状态 |
| --- | --- | :---: |
| **Threading vs. Multiprocessing** | GIL、CPU 密集型与 I/O 密集型任务 | ⬜ |

### 🛠️ 5. 工程实践与标准库

| 主题 | 核心考点 | 状态 |
| --- | --- | :---: |
| **Exceptions** | 异常链、自定义异常、异常处理边界 | ⬜ |
| **Logging** | 日志级别、Handler、Formatter | ⬜ |
| **JSON** | 序列化、反序列化、自定义编码 | ⬜ |
| **Random** | 伪随机数、随机种子、`secrets` | ⬜ |

## 🚀 开始使用

```bash
git clone https://github.com/ck-unifr/python-interview-prep.git
cd python-interview-prep
```

建议按编号顺序学习：先理解原理，再运行示例，最后尝试脱离代码复述核心考点。

## 🤝 参与贡献

欢迎补充示例、完善考点或修正文档。提交 Pull Request 前，请确保：

- 示例可独立运行，并兼容 Python 3.8+
- 结论准确，关键机制有清晰解释
- 内容聚焦主题，不引入无关依赖

## 📜 License

本项目基于 [MIT License](./LICENSE) 开源。

<div align="center">

如果这个项目对你的面试准备有帮助，欢迎点亮一个 ⭐ **Star**。

</div>
