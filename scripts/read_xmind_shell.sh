#!/bin/bash

# ============================================================
# XMind 内容读取脚本（纯 Shell 实现）
# ============================================================
# 版本：1.3
# 作者：AI Assistant
# 更新：2026-04-15
# ============================================================

# 退出条件：遇到错误立即退出
set -e

# 函数：读取 XMind 文件内容（Shell 实现）
read_xmind_shell() {
    local file_path="$1"
    local output_format="${2:-tree}"
    
    echo "=============================================="
    echo "XMind 内容读取 - Shell 实现"
    echo "=============================================="
    
    # 1. 验证文件存在
    if [[ ! -f "$file_path" ]]; then
        echo "❌ 文件不存在：$file_path"
        return 1
    fi
    
    echo "✅ 文件验证通过"
    
    # 2. 获取文件名信息
    local dir=$(dirname "$file_path")
    local basename=$(basename "$file_path" .xmind)
    local original_file="$file_path"
    local copy_file="${dir}/${basename}_copy.xmind"
    local zip_file="${dir}/${basename}_copy.zip"
    local temp_dir="${dir}/${basename}_temp"
    
    echo "原始文件：$original_file"
    echo "副本文件：$copy_file"
    echo "ZIP 文件：$zip_file"
    echo "临时目录：$temp_dir"
    
    # 3. 复制文件（保护原文件）
    cp "$original_file" "$copy_file"
    echo ""
    echo "步骤 1: 复制文件完成"
    echo "  → ${basename}.xmind → ${basename}_copy.xmind"
    
    # 4. 重命名副本文件
    mv "$copy_file" "$zip_file"
    echo "步骤 2: 重命名副本完成"
    echo "  → ${basename}_copy.xmind → ${basename}_copy.zip"
    
    # 5. 解压文件
    unzip -o "$zip_file" -d "$temp_dir" > /dev/null 2>&1
    echo "步骤 3: 解压完成"
    echo "  → 已解压到 ${basename}_temp/"
    
    # 6. 验证解压成功（支持 XMind 8 XML 和 XMind 9+ JSON）
    local content_file="${temp_dir}/content.json"
    local xml_content_file="${temp_dir}/content.xml"
    local use_xml=false
    
    if [[ -f "${content_file}" ]]; then
        echo "步骤 4: 验证解压成功"
        echo "  → 找到 content.json (XMind 9+ 格式)"
    elif [[ -f "${xml_content_file}" ]]; then
        echo "步骤 4: 验证解压成功"
        echo "  → 找到 content.xml (XMind 8 格式)"
        content_file="${xml_content_file}"
        use_xml=true
    else
        echo "❌ 解压失败：未找到 content.json 或 content.xml"
        echo "正在清理临时文件..."
        rm -rf "$temp_dir"
        rm -f "$zip_file"
        echo "✅ 临时文件已清理"
        return 1
    fi
    
    # 7. 读取内容文件
    local file_size=$(stat -f%z "$content_file" 2>/dev/null || stat -c%s "$content_file" 2>/dev/null)
    echo "步骤 5: 读取文件"
    if [[ "$use_xml" == "true" ]]; then
        echo "  → XML 文件大小：$file_size 字节 (XMind 8)"
    else
        echo "  → JSON 文件大小：$file_size 字节 (XMind 9+)"
    fi
    
    # 8. 解析内容并格式化输出
    echo "步骤 6: 解析并格式化输出"
    echo ""
    
    # 使用 Python 解析（支持 JSON 和 XML）
    python3 - "$content_file" "$output_format" "$use_xml" << 'PYTHON_PARSER'
import json
import sys
import xml.etree.ElementTree as ET

def format_tree(node, indent=0):
    """树形格式化"""
    result = []
    prefix = "  " * indent
    title = node.get('title', '')
    markers = [m.get('markerId', '') for m in node.get('markers', [])]
    markers = [m for m in markers if m]  # 过滤空值
    
    line = prefix + title
    if markers:
        line += " [" + ", ".join(markers) + "]"
    result.append(line)
    
    if 'children' in node:
        children = node['children']
        if 'attached' in children:
            for child in children['attached']:
                result.extend(format_tree(child, indent + 1))
    
    return "\n".join(result)

def format_markdown(node, indent=0):
    """Markdown 格式化"""
    result = []
    title = node.get('title', '')
    markers = [m.get('markerId', '') for m in node.get('markers', [])]
    markers = [m for m in markers if m]
    
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
    
    if 'children' in node:
        children = node['children']
        if 'attached' in children:
            for child in children['attached']:
                result.append(format_markdown(child, indent + 1))
    
    return "\n".join(result)

def parse_xmind_xml(xml_path):
    """解析 XMind 8 XML 格式"""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        ns = {
            'xmap-content': 'urn:xmind:xmap:xmlns:content:2.0',
            'xlink': 'http://www.w3.org/1999/xlink'
        }
        
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
    """递归解析 XMind 主题节点"""
    if topic is None:
        return {}
    
    title = topic.find('xmap-content:title', ns)
    title_text = title.text if title is not None and title.text else ''
    
    markers = []
    for marker in topic.findall('xmap-content:markers/xmap-content:marker', ns):
        marker_id = marker.get('markerId')
        if marker_id:
            markers.append(marker_id)
    
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
        result['children'] = {'attached': children_data}
    
    return result

try:
    content_file = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else "tree"
    use_xml = sys.argv[3].lower() == "true" if len(sys.argv) > 3 else False
    
    if use_xml:
        # XML 格式（XMind 8）
        data = parse_xmind_xml(content_file)
    else:
        # JSON 格式（XMind 9+）
        with open(content_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    if output_format == "tree":
        print(format_tree(data[0]['rootTopic']))
    elif output_format == "markdown":
        print(format_markdown(data[0]['rootTopic']))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))

except Exception as e:
    print(f"❌ 解析失败：{e}", file=sys.stderr)
    sys.exit(1)
PYTHON_PARSER

    local exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        echo "❌ JSON 解析失败"
        echo "正在清理临时文件..."
        rm -rf "$temp_dir"
        rm -f "$zip_file"
        echo "✅ 临时文件已清理"
        return 1
    fi
    
    echo ""
    echo "步骤 7: 输出完成"
    
    # 9. 清理临时文件（使用 Shell 命令）
    echo ""
    echo "步骤 8: 清理临时文件"
    
    if [[ -d "$temp_dir" ]]; then
        rm -rf "$temp_dir"
        echo "  → 已删除：${basename}_temp/"
    fi
    
    if [[ -f "$zip_file" ]]; then
        rm -f "$zip_file"
        echo "  → 已删除：${basename}_copy.zip"
    fi
    
    # 注意：原文件保留在原始位置，无需恢复
    
    echo "✅ 临时文件清理完成"
    echo "✅ 原始文件保持不变：$original_file"
    echo "=============================================="
}

# 使用示例
# read_xmind_shell "/path/to/file.xmind" "tree"
# read_xmind_shell "/path/to/file.xmind" "markdown"

# 如果直接运行此脚本且有参数
if [[ "$#" -ge 1 ]]; then
    read_xmind_shell "$@"
fi
