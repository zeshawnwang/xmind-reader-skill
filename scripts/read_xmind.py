#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XMind 内容读取工具（纯 Python 实现）

特点：
- 不依赖 Shell 命令
- 使用 Python 标准库处理文件操作
- 复制文件保护原文件
- 自动清理临时文件
- 完善的错误处理

作者：zeshawnwang
版本：1.3
更新日期：2026-04-15
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Literal, Optional

# ============================================================
# 主函数
# ============================================================

def read_xmind_content(
    file_path: str,
    output_format: Literal["tree", "markdown", "raw"] = "tree",
    verbose: bool = True
) -> str:
    """
    读取并解析 XMind 文件内容（纯 Python 实现）
    
    Args:
        file_path: XMind 文件完整路径
        output_format: 输出格式 ("tree", "markdown", "raw")
        verbose: 是否显示详细日志
    
    Returns:
        格式化后的文本内容
    
    Raises:
        FileNotFoundError: 文件不存在
        PermissionError: 权限不足
        RuntimeError: 操作失败
    
    流程：
    1. 验证文件存在
    2. 复制文件到临时位置（保护原文件）
    3. 重命名 → .zip
    4. 解压到临时目录
    5. 读取 content.json
    6. 解析 JSON 并格式化
    7. 清理临时文件（Python 方式）
    8. 原文件保持不变
    """
    if verbose:
        print("=" * 60)
        print("XMind 内容读取 - Python 实现")
        print("=" * 60)
    
    # 1. 验证文件存在
    xmind_path = Path(file_path)
    if not xmind_path.exists():
        if verbose:
            print(f"❌ 文件不存在：{file_path}")
        raise FileNotFoundError(f"文件不存在：{file_path}")
    
    if verbose:
        print(f"✅ 文件验证：{file_path}")
    
    # 2. 获取文件信息
    original_path = xmind_path
    basename = xmind_path.stem  # 不带扩展名
    parent_dir = xmind_path.parent
    
    # 创建临时目录
    temp_base = tempfile.mkdtemp(prefix="xmind_")
    temp_dir = Path(temp_base)
    
    # 定义副本文件路径
    copy_xmind = temp_dir / f"{basename}_copy.xmind"
    copy_zip = temp_dir / f"{basename}_copy.zip"
    
    if verbose:
        print(f"  原始文件：{original_path}")
        print(f"  文件名：{basename}")
        print(f"  临时目录：{temp_dir}")
        print(f"  副本文件：{copy_xmind}")
        print(f"  ZIP 文件：{copy_zip}")
    
    try:
        # 3. 复制文件（保护原文件）
        if verbose:
            print("\n步骤 1: 复制文件")
        shutil.copy2(original_path, copy_xmind)
        if verbose:
            print(f"  → 已复制：{basename}.xmind → {basename}_copy.xmind")
            print(f"  → 原文件保持不变")
        
        # 4. 重命名副本文件
        if verbose:
            print("\n步骤 2: 重命名副本")
        copy_xmind.rename(copy_zip)
        if verbose:
            print(f"  → {basename}_copy.xmind → {basename}_copy.zip")
        
        # 5. 解压文件（调用 unzip 命令）
        if verbose:
            print("\n步骤 3: 解压文件")
        result = subprocess.run(
            ['unzip', '-o', str(copy_zip), '-d', str(temp_dir)],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            if verbose:
                print(f"  ❌ 解压失败：{result.stderr}")
            raise RuntimeError(f"解压失败：{result.stderr}")
        
        if verbose:
            print(f"  → 已解压到 {temp_dir}/")
        
        # 6. 验证解压成功（支持 XMind 8 XML 和 XMind 9+ JSON）
        content_path = temp_dir / 'content.json'
        xml_content_path = temp_dir / 'content.xml'
        
        # 优先使用 JSON 格式（XMind 9+）
        if not content_path.exists():
            # 回退到 XML 格式（XMind 8）
            if xml_content_path.exists():
                content_path = xml_content_path
                use_xml = True
                if verbose:
                    print("  ℹ 检测到 XMind 8 格式（XML），自动切换解析模式")
            else:
                if verbose:
                    print("  ❌ 解压失败：未找到 content.json 或 content.xml")
                raise FileNotFoundError(f"未找到 content.json 或 content.xml 在 {temp_dir}")
        else:
            use_xml = False
        
        if verbose:
            content_size = content_path.stat().st_size
            print(f"步骤 4: 验证解压成功")
            print(f"  → content.json 大小：{content_size} 字节")
        
        # 7. 读取并解析内容（支持 JSON 和 XML）
        if verbose:
            print("\n步骤 5: 解析内容")
        
        if use_xml:
            # XMind 8 格式 - XML 解析
            data = parse_xmind_xml(content_path)
        else:
            # XMind 9+ 格式 - JSON 解析
            with open(content_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        # 8. 格式化输出
        if verbose:
            print("步骤 6: 格式化输出")
        
        if output_format == "tree":
            result_text = format_tree(data[0]['rootTopic'])
        elif output_format == "markdown":
            result_text = format_markdown(data[0]['rootTopic'])
        else:
            result_text = json.dumps(data, ensure_ascii=False, indent=2)
            if verbose:
                print(f"  → 原始 JSON，共 {len(result_text)} 字节")
        
        # 9. 清理临时文件（Python 方式，不依赖 Shell）
        _cleanup_files(temp_dir, copy_zip, verbose)
        
        if verbose:
            print("=" * 60)
            print("✅ 原始文件保持不变：" + str(original_path))
        
        return result_text
    
    except Exception as e:
        # 失败时尽量清理
        if verbose:
            print(f"\n❌ 错误：{e}")
            print("正在尝试清理临时文件...")
        
        try:
            # 清理临时目录及其所有内容
            if temp_dir.exists() and temp_dir.is_dir():
                shutil.rmtree(temp_dir)
                if verbose:
                    print(f"  → 已删除临时目录：{temp_dir.name}/")
        except Exception as cleanup_error:
            if verbose:
                print(f"  ⚠ 清理过程中出错：{cleanup_error}")
        
        raise


# ============================================================
# XML 解析函数（XMind 8 支持）
# ============================================================

def parse_xmind_xml(xml_path):
    """
    解析 XMind 8 的 XML 格式内容
    
    Args:
        xml_path: XML 文件路径
    
    Returns:
        解析后的数据结构（与 JSON 格式兼容）
    """
    import xml.etree.ElementTree as ET
    
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # XMind XML 命名空间
        ns = {
            'xmap-content': 'urn:xmind:xmap:xmlns:content:2.0',
            'xlink': 'http://www.w3.org/1999/xlink'
        }
        
        # 查找所有主题节点
        data = []
        for sheet in root.findall('.//xmap-content:sheet', ns):
            sheet_data = {
                'rootTopic': parse_xmind_topic(sheet.find('xmap-content:topic', ns), ns)
            }
            data.append(sheet_data)
        
        return data
    
    except Exception as e:
        raise RuntimeError(f"XML 解析失败：{e}")


def parse_xmind_topic(topic, ns):
    """
    递归解析 XMind 主题节点
    
    Args:
        topic: XML 主题节点
        ns: 命名空间字典
    
    Returns:
        主题数据字典
    """
    if topic is None:
        return {}
    
    title = topic.find('xmap-content:title', ns)
    title_text = title.text if title is not None and title.text else ''
    
    # 获取标记
    markers = []
    for marker in topic.findall('xmap-content:markers/xmap-content:marker', ns):
        marker_id = marker.get('markerId')
        if marker_id:
            markers.append(marker_id)
    
    # 获取子节点
    children_data = []
    for child in topic.findall('xmap-content:children', ns):
        for attached in child.findall('xmap-content:topics', ns):
            for child_topic in attached.findall('xmap-content:topic', ns):
                children_data.append(parse_xmind_topic(child_topic, ns))
    
    result = {
        'title': title_text,
        'markers': [{'markerId': m} for m in markers]
    }
    
    if children_data:
        result['children'] = {
            'attached': children_data
        }
    
    return result


# ============================================================
# 辅助函数
# ============================================================

def _cleanup_files(
    temp_dir: Path,
    zip_path: Path,
    verbose: bool = True
) -> None:
    """
    清理临时文件（纯 Python 方式）
    
    不使用 Shell 的 rm 命令，完全使用 Python 标准库：
    - shutil.rmtree() 删除目录
    - os.remove() 删除文件
    """
    if verbose:
        print("\n步骤 7: 清理临时文件（Python 方式）")
    
    cleaned = []
    
    # 1. 删除临时目录（包含所有内容）
    if temp_dir.exists() and temp_dir.is_dir():
        shutil.rmtree(temp_dir)
        cleaned.append(f"{temp_dir.name}/")
        if verbose:
            print(f"  → 已删除目录：{temp_dir.name}/")
    
    # 2. 删除临时 zip 文件（如果未包含在目录中）
    if zip_path.exists():
        os.remove(zip_path)
        cleaned.append(zip_path.name)
        if verbose:
            print(f"  → 已删除文件：{zip_path.name}")
    
    if cleaned and verbose:
        print(f"✅ 已清理 {len(cleaned)} 个临时文件")
    elif verbose:
        print("ℹ 无需清理临时文件")


def format_tree(node: dict, indent: int = 0) -> str:
    """
    树形格式化
    
    输出格式：
        主题标题 [marker1, marker2]
          子主题 1
          子主题 2
    """
    result = []
    prefix = "  " * indent
    
    # 获取标题
    title = node.get('title', '')
    
    # 获取标记
    markers = []
    if 'markers' in node:
        for marker in node['markers']:
            if 'markerId' in marker:
                markers.append(marker['markerId'])
    
    # 构建行
    line = prefix + title
    if markers:
        line += " [" + ", ".join(markers) + "]"
    result.append(line)
    
    # 递归处理子节点
    if 'children' in node:
        children = node['children']
        
        # 处理 attached 子节点
        if 'attached' in children:
            for child in children['attached']:
                result.extend(format_tree(child, indent + 1))
        
        # 处理 linked 子节点
        if 'linked' in children:
            for child in children['linked']:
                result.extend(format_tree(child, indent + 1))
    
    return "\n".join(result)


def format_markdown(node: dict, indent: int = 0) -> str:
    """
    Markdown 格式化
    
    输出格式：
        # 主题标题 [marker1, marker2]
        ## 子主题
        - 更深层主题
    """
    result = []
    
    # 获取标题
    title = node.get('title', '')
    
    # 获取标记
    markers = []
    if 'markers' in node:
        for marker in node['markers']:
            if 'markerId' in marker:
                markers.append(marker['markerId'])
    
    # 根据缩进级别确定标记
    if indent == 0:
        line = f"# {title}"
    elif indent == 1:
        line = f"## {title}"
    elif indent == 2:
        line = f"### {title}"
    else:
        line = f"{'  ' * indent}- {title}"
    
    if markers:
        line += f" [{', '.join(markers)}]"
    
    result.append(line)
    
    # 递归处理子节点
    if 'children' in node:
        children = node['children']
        
        if 'attached' in children:
            for child in children['attached']:
                result.append(format_markdown(child, indent + 1))
        
        if 'linked' in children:
            for child in children['linked']:
                result.append(format_markdown(child, indent + 1))
    
    return "\n".join(result)


# ============================================================
# 便捷函数
# ============================================================

def read_xmind_quick(
    file_path: str,
    output_format: Literal["tree", "markdown"] = "tree"
) -> str:
    """
    快速读取 XMind 文件
    
    简化的调用方式，自动使用 Python 实现，静默运行。
    
    Args:
        file_path: XMind 文件路径
        output_format: 输出格式 ("tree", "markdown")
    
    Returns:
        格式化后的内容
    
    使用示例:
        >>> content = read_xmind_quick("/path/to/file.xmind")
        >>> print(content)
    """
    return read_xmind_content(file_path, output_format, verbose=False)


# ============================================================
# 命令行入口
# ============================================================

if __name__ == "__main__":
    # 命令行参数处理
    if len(sys.argv) < 2:
        print("用法：python3 read_xmind.py <file.xmind> [format]")
        print("  format: tree (默认), markdown, raw")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else "tree"
    
    try:
        content = read_xmind_content(file_path, output_format, verbose=True)
        print("\n--- 输出内容 ---")
        print(content)
    
    except FileNotFoundError as e:
        print(f"\n❌ 错误：{e}")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ 操作失败：{e}")
        sys.exit(1)
