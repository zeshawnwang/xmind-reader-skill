# 🚀 XMind Reader Skill：一个让 XMind 文件读取变得简单的开源工具

---

## 📖 项目背景

作为一名开发者，我经常使用 **XMind** 来整理思维导图和项目管理。无论是产品需求梳理、技术方案设计，还是项目复盘，XMind 都是我的得力助手。

但是，当我需要**在程序中读取 XMind 文件内容**时，问题来了...

---

## 😤 痛点分析

### 痛点一：官方库依赖复杂

XMind 官方虽然提供了 Python 库，但：
- 安装配置繁琐
- API 文档稀缺
- 学习成本较高

### 痛点二：第三方库问题多

尝试使用 `xmindparser` 等第三方库后，发现：
- ⚠️ 需要额外安装依赖
- ⚠️ 兼容性问题频发
- ⚠️ 在受限环境中无法使用
- ⚠️ 版本更新不及时

### 痛点三：临时文件管理噩梦

大多数解决方案都会：
- 生成大量临时文件
- 临时文件清理不及时
- 可能污染原文件
- 磁盘空间浪费

### 痛点四：可移植性差

在不同的开发环境中：
- Windows、macOS、Linux 配置各异
- CI/CD 环境依赖难以管理
- 容器化部署困难

---

## 💡 解决方案

**XMind Reader Skill** 应运而生！

这是一个**零依赖**的 XMind 文件读取工具，提供了**4种实现方式**，满足不同场景需求：

### ✅ 核心特性

| 特性 | 说明 |
|------|------|
| 🎯 **零依赖设计** | 纯 Python 标准库实现，无需安装任何第三方包 |
| 🛡️ **原文件保护** | 复制后操作，确保原始文件绝对安全 |
| 🧹 **自动清理** | 操作完成后自动清理所有临时文件 |
| 📦 **多格式支持** | 完美支持 XMind 8 (XML) 和 XMind 9+ (JSON) |
| 🎨 **多输出格式** | 支持树形结构和 Markdown 格式输出 |
| 🌐 **跨平台兼容** | macOS、Linux、Windows 完美运行 |

### 📊 实现方式对比

| 实现方式 | 推荐程度 | 适用场景 | 优势 |
|---------|---------|---------|------|
| **纯 Python** | ⭐⭐⭐⭐⭐ | 生产环境、通用场景 | 零依赖、跨平台、可移植性强 |
| **Shell 脚本** | ⭐⭐⭐⭐ | 快速原型、命令行工具 | 轻量级、执行效率高 |
| **xmindparser 库** | ⭐ | 学习研究 | 不生成临时文件 |
| **xmind 库** | ⭐ | 学习研究 | 不生成临时文件 |

---

## 🎯 谁适合使用？

### 👨‍💻 开发者
- 需要在程序中读取 XMind 内容
- 需要批量处理 XMind 文件
- 需要将 XMind 内容转换为其他格式

### 📋 产品经理
- 快速提取 XMind 思维导图内容
- 生成需求文档或报告

### 🔧 DevOps 工程师
- 自动化 XMind 文件处理流程
- CI/CD 集成

### 📚 学习者
- 学习 XMind 文件格式
- 研究思维导图结构

---

## 🚀 快速开始

### Python 脚本（推荐）

```bash
# 直接运行
python3 read_xmind.py /path/to/file.xmind tree

# 输出 Markdown 格式
python3 read_xmind.py /path/to/file.xmind markdown
```

### Python 模块

```python
from scripts.read_xmind import read_xmind_quick

content = read_xmind_quick("/path/to/file.xmind")
print(content)
```

### Shell 脚本

```bash
chmod +x scripts/read_xmind_shell.sh
./scripts/read_xmind_shell.sh /path/to/file.xmind tree
```

---

## 📝 输出示例

### 树形格式

```
建议型投顾前端
  投顾单品持仓页
    增加机构 logo [star-green]
    增加 tag [star-green]
    调整持仓布局 [star-green]
  投顾单品详情页
    发车模块 [star-green]
```

### Markdown 格式

```markdown
# 建议型投顾前端

## 投顾单品持仓页
- 增加机构 logo [star-green]
- 增加 tag [star-green]

## 投顾单品详情页
### 发车模块 [star-green]
```

---

## 🏗️ 项目架构

```
Xmind-Read-Skill/
├── scripts/
│   ├── read_xmind.py              # Python 实现（强烈推荐）
│   ├── read_xmind_shell.sh        # Shell 实现
│   ├── read_xmind_xmindparser.py  # xmindparser 库实现
│   └── read_xmind_xmindlib.py     # xmind 库实现
├── references/
│   └── example.md                 # 使用示例
├── README.md                      # 项目说明
├── SKILL.md                       # 完整技术文档
├── manifest.json                  # 元数据
└── LICENSE                        # MIT 许可证
```

---

## 🤔 为什么选择这个项目？

### 1️⃣ 零依赖，零烦恼
不需要 `pip install`，不需要配置环境，开箱即用！

### 2️⃣ 原文件绝对安全
**复制 → 操作 → 清理**，原文件纹丝不动。

### 3️⃣ 透明可控
所有代码清晰可见，没有黑盒操作，你可以完全理解并控制整个流程。

### 4️⃣ 学习价值
通过阅读代码，你可以深入了解：
- XMind 文件格式（ZIP + JSON/XML）
- Python 文件操作最佳实践
- 临时文件管理策略
- 跨平台兼容性处理

---

## 🤝 贡献与交流

项目完全开源，欢迎：

- ⭐ **Star** 项目表示支持
- 🐛 报告 **Bug** 或问题
- 💡 提出 **功能建议**
- 📝 提交 **Pull Request**
- 📖 完善 **文档和示例**

---

## 🔗 项目链接

### GitHub 仓库

**⭐ 仓库地址：**
```
https://github.com/zeshawnwang/xmind-reader-skill
```

**如果你觉得这个项目有帮助，欢迎点个 Star！**

---

## 📈 未来规划

- [ ] 添加单元测试
- [ ] 支持写入 XMind 文件
- [ ] 提供 Web API 接口
- [ ] 开发 GUI 界面
- [ ] 支持更多输出格式（HTML、PDF）

---

## 💬 写在最后

这个项目起源于我自己在实际工作中的需求。在尝试了各种方案后，我决定自己动手，编写一个**简单、可靠、易用**的工具。

希望通过开源，让更多人能够受益。如果你有任何想法或建议，欢迎在 GitHub 上提 Issue 或 Pull Request！

---

**再次感谢你的关注和支持！**

**项目地址：https://github.com/zeshawnwang/xmind-reader-skill**

**别忘了点个 ⭐ Star 哦！**

---

*作者：zeshawnwang*
*开源协议：MIT License*
*版本：v1.5*
