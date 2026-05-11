# XMind 内容读取技能 - 使用示例

## 快速开始

### 使用 Shell 脚本

```bash
# 1. 赋予执行权限
chmod +x scripts/read_xmind_shell.sh

# 2. 读取 XMind 文件（树形格式）
./scripts/read_xmind_shell.sh /path/to/投顾/建议型投顾/建议型投顾.xmind tree

# 3. 读取 XMind 文件（Markdown 格式）
./scripts/read_xmind_shell.sh /path/to/投顾/建议型投顾/建议型投顾.xmind markdown
```

### 使用 Python 脚本

```bash
# 1. 赋予执行权限
chmod +x scripts/read_xmind.py

# 2. 直接运行
python3 scripts/read_xmind.py /path/to/投顾/建议型投顾/建议型投顾.xmind tree

# 3. 使用 Markdown 格式
python3 scripts/read_xmind.py /path/to/投顾/建议型投顾/建议型投顾.xmind markdown
```

### 导入为 Python 模块

```python
# 导入模块
from scripts.read_xmind import read_xmind_quick

# 快速读取
content = read_xmind_quick("/path/to/投顾/建议型投顾/建议型投顾.xmind")
print(content)

# 或者使用完整功能
from scripts.read_xmind import read_xmind_content

content = read_xmind_content(
    "/path/to/投顾/建议型投顾/建议型投顾.xmind",
    output_format="markdown",
    verbose=True
)
```

## 输出示例

### 树形格式输出

```
建议型投顾前端
  投顾单品持仓页
    增加机构 logo [star-green]
    增加 tag [star-green]
    调整持仓布局 [star-green]
    我的定投换为跟车设置按钮 [star-green]
    资产配置模块
      投顾策略明细可以跳转单基持仓页 [star-green]
      持仓基金明细变更为四列 [star-green]
  投顾单品详情页
    发车模块 [star-green]
      普通发车 [star-blue]
        普通发车模块
      建议型投顾 [star-green]
        建议型发车模块
```

### Markdown 格式输出

```markdown
# 建议型投顾前端

## 投顾单品持仓页
- 增加机构 logo [star-green]
- 增加 tag [star-green]
- 调整持仓布局 [star-green]
- 我的定投换为跟车设置按钮 [star-green]
- 资产配置模块
  - 投顾策略明细可以跳转单基持仓页 [star-green]
  - 持仓基金明细变更为四列 [star-green]

## 投顾单品详情页
### 发车模块 [star-green]
#### 普通发车 [star-blue]
##### 普通发车模块
#### 建议型投顾 [star-green]
##### 建议型发车模块
```

## 高级用法

### 批量处理多个 XMind 文件

```bash
#!/bin/bash
# batch_read_xmind.sh

for file in /path/to/*.xmind; do
    echo "处理：$file"
    python3 scripts/read_xmind.py "$file" tree
    echo "----------------------------------------"
done
```

### 保存输出到文件

```bash
# 树形格式保存到 txt 文件
python3 scripts/read_xmind.py file.xmind tree > output.txt

# Markdown 格式保存到 md 文件
python3 scripts/read_xmind.py file.xmind markdown > output.md

# 原始 JSON 保存到 json 文件
python3 scripts/read_xmind.py file.xmind raw > output.json
```

### 在 Python 程序中使用

```python
from pathlib import Path
from scripts.read_xmind import read_xmind_content

def process_xmind_file(file_path):
    """处理 XMind 文件并返回结构化数据"""
    try:
        content = read_xmind_content(file_path, "markdown", verbose=False)
        
        # 处理内容
        lines = content.split('\n')
        for line in lines:
            if '[star-green]' in line:
                # 处理重要标记
                print(f"重要：{line.strip()}")
        
        return True
    except Exception as e:
        print(f"处理失败：{e}")
        return False

# 使用示例
process_xmind_file("/path/to/file.xmind")
```

## 注意事项

1. **原文件保护**：所有操作都在副本上进行，原文件保持不变
2. **临时文件**：操作完成后会自动清理所有临时文件
3. **错误处理**：如果操作失败，也会自动清理临时文件
4. **依赖要求**：
   - Shell 方式：需要 `bash`, `unzip`, `python3`
   - Python 方式：需要 `Python 3.6+`

## 常见问题

### Q: 为什么使用 Python 解析 JSON？

A: Bash 本身不支持 JSON 解析，使用 Python 是最简单可靠的方法。

### Q: 如果 unzip 命令不可用怎么办？

A: 可以先安装 unzip：
- macOS: `brew install unzip`
- Linux: `sudo apt-get install unzip`
- Windows: 安装 7-Zip 并添加到 PATH

### Q: 如何处理损坏的 XMind 文件？

A: 使用 XMind 软件重新打开并保存，确保文件完整性后再读取。

## ⚠️ 使用第三方库（不推荐）

> ⚠️ 以下方式仅供了解，不推荐在生产环境中使用

### 使用 xmindparser 库

```bash
# 1. 安装依赖
pip install xmindparser

# 2. 赋予执行权限
chmod +x scripts/read_xmind_xmindparser.py

# 3. 运行脚本
python3 scripts/read_xmind_xmindparser.py /path/to/file.xmind tree

# 4. 使用 Markdown 格式
python3 scripts/read_xmind_xmindparser.py /path/to/file.xmind markdown
```

**优势**：
- ✅ 不生成临时文件（直接在内存中解析）
- ✅ 代码简洁

**劣势**：
- ❌ 需要安装额外依赖
- ❌ 可能存在兼容性问题
- ❌ 代码可移植性降低

### 使用 xmind 库

```bash
# 1. 安装依赖
pip install xmind

# 2. 赋予执行权限
chmod +x scripts/read_xmind_xmindlib.py

# 3. 运行脚本
python3 scripts/read_xmind_xmindlib.py /path/to/file.xmind tree

# 4. 使用 Markdown 格式
python3 scripts/read_xmind_xmindlib.py /path/to/file.xmind markdown
```

**优势**：
- ✅ 不生成临时文件（直接在内存中解析）
- ✅ 代码简洁

**劣势**：
- ❌ 需要安装额外依赖
- ❌ 可能存在兼容性问题
- ❌ 代码可移植性降低

---

**文档版本**: 1.5
**更新日期**: 2026-05-11
