# XMind Reader Skill

![GitHub License](https://img.shields.io/github/license/zeshawnwang/xmind-reader-skill)
![GitHub Stars](https://img.shields.io/github/stars/zeshawnwang/xmind-reader-skill)
![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)

一个用于读取和解析 XMind 思维导图文件内容的工具包，支持多种实现方式。

## 🎯 功能特性

- ✅ **零依赖设计** - 纯 Python 实现，无需额外安装依赖
- ✅ **多格式支持** - 自动兼容 XMind 8 (XML) 和 XMind 9+ (JSON) 格式
- ✅ **原文件保护** - 复制后操作，确保原文件不被修改
- ✅ **智能清理** - 自动清理临时文件
- ✅ **多输出格式** - 支持树形结构和 Markdown 格式输出
- ✅ **跨平台兼容** - 支持 macOS、Linux、Windows

## 📁 项目结构

```
Xmind-Read-Skill/
├── scripts/
│   ├── read_xmind.py              # Python 实现（强烈推荐）
│   ├── read_xmind_shell.sh        # Shell 实现（推荐）
│   ├── read_xmind_xmindparser.py  # xmindparser 库实现（仅供参考）
│   └── read_xmind_xmindlib.py     # xmind 库实现（仅供参考）
├── references/
│   └── example.md                 # 使用示例文档
├── README.md                      # 项目说明
├── SKILL.md                       # 完整技能文档
├── manifest.json                  # 技能元数据
├── LICENSE                        # MIT 许可证
└── .gitignore                     # Git 忽略配置
```

## 🚀 快速开始

### 方式一：Python 脚本（强烈推荐）

```bash
# 直接运行
python3 scripts/read_xmind.py /path/to/file.xmind tree

# 输出 Markdown 格式
python3 scripts/read_xmind.py /path/to/file.xmind markdown
```

### 方式二：Python 模块

```python
from scripts.read_xmind import read_xmind_quick

# 快速读取（树形格式）
content = read_xmind_quick("/path/to/file.xmind")
print(content)

# 读取为 Markdown 格式
content = read_xmind_quick("/path/to/file.xmind", output_format="markdown")
print(content)
```

### 方式三：Shell 脚本

```bash
chmod +x scripts/read_xmind_shell.sh
./scripts/read_xmind_shell.sh /path/to/file.xmind tree
```

### 方式四：第三方库（仅供参考，不推荐）

> ⚠️ **不推荐在生产环境中使用**

```bash
# 使用 xmindparser 库
pip install xmindparser
python3 scripts/read_xmind_xmindparser.py /path/to/file.xmind tree

# 使用 xmind 库
pip install xmind
python3 scripts/read_xmind_xmindlib.py /path/to/file.xmind tree
```

## 📊 实现方式对比

| 实现方式 | 推荐程度 | 优势 | 劣势 |
|---------|---------|------|------|
| **纯 Python 实现** | ⭐⭐⭐⭐⭐ | 零依赖、跨平台、可移植性强 | 需要生成临时文件（自动清理） |
| **纯 Shell 实现** | ⭐⭐⭐⭐ | 轻量级、无需 Python | 跨平台性稍差 |
| **xmindparser 库** | ⭐ | 不生成临时文件 | 需要安装依赖、可移植性降低 |
| **xmind 库** | ⭐ | 不生成临时文件 | 需要安装依赖、可移植性降低 |

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
- 调整持仓布局 [star-green]

## 投顾单品详情页
### 发车模块 [star-green]
```

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'Add some feature'`
4. 推送到分支：`git push origin feature/your-feature`
5. 提交 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👨‍💻 作者

**zeshawnwang**

## 🔄 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.5 | 2026-05-11 | 添加第三方库实现方式（xmindparser/xmind） |
| v1.4 | 2026-04-15 | 完善文档和元数据 |
| v1.3 | 2026-04-15 | 添加文件复制步骤，保护原文件 |
| v1.2 | 2026-04-15 | 完善两种方式对比 |
| v1.1 | 2026-04-15 | 添加 Shell 实现方式 |
| v1.0 | 2026-04-15 | 初始版本 |

---

⭐ 如果这个项目对你有帮助，请给个 Star！