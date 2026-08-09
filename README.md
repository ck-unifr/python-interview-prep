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

每个主题同时提供 `introduction.md` 与 `introduction.html`，表格中的主题链接默认打开 Markdown 版本。

### 🧱 1. 数据结构与内建类型

| 主题 | 核心考点 | 状态 |
| --- | --- | :---: |
| [**Lists**](./01-Lists/introduction.md) | 内存分配、时间复杂度、列表推导式 | ✅ |
| [**Tuples**](./02-Tuple/introduction.md) | 不可变性、可哈希条件、序列解包 | ✅ |
| [**Dictionaries**](./03-Dictionary/introduction.md) | 哈希表、插入顺序、字典推导式 | ✅ |
| [**Sets**](./04-Sets/introduction.md) | 集合运算、去重、`frozenset` | ✅ |
| [**Strings**](./05-Strings/introduction.md) | Unicode、不可变性、字符串驻留 | ✅ |
| [**Collections**](./06-Collections/introduction.md) | `Counter`、`defaultdict`、`deque` | ✅ |

### 🧠 2. 高级特性与底层机制

| 主题 | 核心考点 | 状态 |
| --- | --- | :---: |
| [**Decorators**](./13-Decorators/introduction.md) | 闭包、参数化装饰器、`functools.wraps` | ✅ |
| [**Generators**](./14-Generators/introduction.md) | `yield`、惰性计算、生成器协议 | ✅ |
| [**Context Managers**](./21-Context-Manager/introduction.md) | `with`、上下文协议、`contextlib` | ✅ |
| [**Copying**](./20-Copying/introduction.md) | 浅拷贝、深拷贝、对象图 | ✅ |

### 🔁 3. 函数与迭代

| 主题 | 核心考点 | 状态 |
| --- | --- | :---: |
| [**Function Arguments**](./18-Function-Arguments/introduction.md) | 参数类别、默认值、对象共享调用 | ✅ |
| [**Lambda Functions**](./08-Lambda/introduction.md) | 匿名函数、闭包、函数式工具 | ✅ |
| [**Itertools**](./07-Itertools/introduction.md) | 惰性迭代、排列组合、分组累计 | ✅ |
| [**Asterisk Operator**](./19-The-Asterisk/introduction.md) | 参数收集、解包、容器合并 | ✅ |
| [**Python Tricks**](./Python-Tricks/introduction.md) | 解包、`join`、`enumerate`、`zip` | ✅ |

### ⚡ 4. 并发与性能

| 主题 | 核心考点 | 状态 |
| --- | --- | :---: |
| [**Threading vs. Multiprocessing**](./15-Threading-vs-Multiprocessing/introduction.md) | GIL、任务类型、并发模型选型 | ✅ |
| [**Threading**](./16-Threading-in-Python/introduction.md) | 线程生命周期、锁、线程安全队列 | ✅ |
| [**Multiprocessing**](./17-Multiprocessing/introduction.md) | 进程池、IPC、共享内存、启动方式 | ✅ |

### 🛠️ 5. 工程实践与标准库

| 主题 | 核心考点 | 状态 |
| --- | --- | :---: |
| [**Exceptions**](./09-Exceptions/introduction.md) | 异常链、自定义异常、处理边界 | ✅ |
| [**Logging**](./10-Logging/introduction.md) | Logger、Handler、Formatter、传播 | ✅ |
| [**JSON**](./11-JSON/introduction.md) | 序列化、反序列化、自定义编码 | ✅ |
| [**Random Numbers**](./12-RandomNumbers/introduction.md) | 伪随机、随机种子、`secrets` | ✅ |

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
