#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XMind 内容读取工具（使用 xmind 库）

⚠️ 本方式仅供了解，不推荐在生产环境中使用

优势：
- 不生成临时文件，直接在内存中解析
- 代码简洁

劣势：
- 需要安装额外依赖：pip install xmind
- 增加了项目的依赖负担
- 在受限环境中可能无法使用

作者：zeshawnwang
版本：1.5
更新日期：2026-05-11
"""

import json
import sys
from typing import Literal, Optional

try:
    import xmind
except ImportError:
    print("❌ 错误：需要安装 xmind 库")
    print("   运行：pip install xmind")
    sys.exit(1)


def format_tree(node: dict, indent: int = 0) -> str:
    """树形格式化"""
    result = []
    prefix = "  " * indent
    
    title = node.get('title', '')
    markers = node.get('markers', [])
    marker_ids = []
    
    if isinstance(markers, list):
        for marker in markers:
            if isinstance(marker, dict):
                marker_ids.append(marker.get('markerId', ''))
            elif isinstance(marker, str):
                marker_ids.append(marker)
    
    line = prefix + title
    if marker_ids:
        line += " [" + ", ".join(filter(None, marker_ids)) + "]"
    result.append(line)
    
    if 'children' in node:
        children = node['children']
        if isinstance(children, dict) and 'attached' in children:
            for child in children['attached']:
                result.extend(format_tree(child, indent + 1))
    
    return "\n".join(result)


def format_markdown(node: dict, indent: int = 0) -> str:
    """Markdown 格式化"""
    result = []
    
    title = node.get('title', '')
    markers = node.get('markers', [])
    marker_ids = []
    
    if isinstance(markers, list):
        for marker in markers:
            if isinstance(marker, dict):
                marker_ids.append(marker.get('markerId', ''))
            elif isinstance(marker, str):
                marker_ids.append(marker)
    
    if indent == 0:
        line = f"# {title}"
    elif indent == 1:
        line = f"## {title}"
    elif indent == 2:
        line = f"### {title}"
    else:
        line = f"{'  ' * indent}- {title}"
    
    if marker_ids:
        line += f" [{', '.join(filter(None, marker_ids))}]"
    
    result.append(line)
    
    if 'children' in node:
        children = node['children']
        if isinstance(children, dict) and 'attached' in children:
            for child in children['attached']:
                result.append(format_markdown(child, indent + 1))
    
    return "\n".join(result)


def read_xmind_with_xmindlib(
    file_path: str,
    output_format: Literal["tree", "markdown", "raw"] = "tree",
    verbose: bool = True
) -> str:
    """
    使用 xmind 库读取 XMind 文件
    
    ⚠️ 不推荐在生产环境中使用
    
    优势：
    - 不生成临时文件（直接在内存中解析）
    - 代码简洁
    
    劣势：
    - 需要安装额外依赖
    - 可能存在兼容性问题
    
    Args:
        file_path: XMind 文件完整路径
        output_format: 输出格式 ("tree", "markdown", "raw")
        verbose: 是否显示详细日志
    
    Returns:
        格式化后的文本内容
    """
    if verbose:
        print("=" * 60)
        print("XMind 内容读取 - xmind 库实现")
        print("=" * 60)
        print("⚠️ 警告：本方式仅供了解，不推荐在生产环境中使用")
        print()
    
    if verbose:
        print(f"✅ 文件验证：{file_path}")
        print("📦 正在使用 xmind 库解析...")
    
    try:
        workbook = xmind.load(file_path)
        
        if verbose:
            print("✅ 加载成功")
        
        primary_sheet = workbook.getFirstSheet()
        if not primary_sheet:
            raise ValueError("未找到工作表")
        
        root_topic = primary_sheet.getRootTopic()
        if not root_topic:
            raise ValueError("未找到根主题")
        
        root_dict = {
            'title': root_topic.getTitle(),
            'children': {}
        }
        
        children_list = []
        for child in root_topic.getChildren().values():
            child_dict = _topic_to_dict(child)
            if child_dict:
                children_list.append(child_dict)
        
        if children_list:
            root_dict['children']['attached'] = children_list
        
        if output_format == "tree":
            result_text = format_tree(root_dict)
        elif output_format == "markdown":
            result_text = format_markdown(root_dict)
        else:
            result_text = json.dumps(root_dict, ensure_ascii=False, indent=2)
        
        if verbose:
            print("✅ 格式化完成")
            print("✅ 不需要生成临时文件（内存中直接解析）")
            print("=" * 60)
        
        return result_text
    
    except Exception as e:
        if verbose:
            print(f"❌ 错误：{e}")
        raise


def _topic_to_dict(topic) -> dict:
    """将 xmind Topic 对象转换为字典"""
    if not topic:
        return {}
    
    topic_dict = {
        'title': topic.getTitle(),
        'children': {}
    }
    
    markers = []
    for marker in topic.getMarkers():
        markers.append({'markerId': marker})
    if markers:
        topic_dict['markers'] = markers
    
    children_list = []
    for child in topic.getChildren().values():
        child_dict = _topic_to_dict(child)
        if child_dict:
            children_list.append(child_dict)
    
    if children_list:
        topic_dict['children']['attached'] = children_list
    
    return topic_dict


def read_xmind_xmindlib_quick(
    file_path: str,
    output_format: Literal["tree", "markdown"] = "tree"
) -> str:
    """
    快速读取 XMind 文件（使用 xmind 库）
    
    ⚠️ 不推荐在生产环境中使用
    """
    return read_xmind_with_xmindlib(file_path, output_format, verbose=False)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 read_xmind_xmindlib.py <file.xmind> [format]")
        print("  format: tree (默认), markdown, raw")
        print()
        print("⚠️ 警告：本方式仅供了解，不推荐在生产环境中使用")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else "tree"
    
    try:
        content = read_xmind_with_xmindlib(file_path, output_format, verbose=True)
        print("\n--- 输出内容 ---")
        print(content)
    except Exception as e:
        print(f"\n❌ 操作失败：{e}")
        sys.exit(1)
