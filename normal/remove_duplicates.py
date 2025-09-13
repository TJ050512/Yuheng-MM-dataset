#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
找出所有重复的text_clean并只保留其中一个
"""

import json
from collections import defaultdict
import os

def remove_duplicate_text_clean(input_file, output_file=None):
    """
    找出所有重复的text_clean并只保留其中一个
    
    Args:
        input_file (str): 输入JSON文件路径
        output_file (str): 输出JSON文件路径，如果为None则覆盖原文件
    
    Returns:
        dict: 包含统计信息的字典
    """
    # 读取JSON文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 统计信息
    stats = {
        'original_count': len(data['massage']),
        'duplicates_found': 0,
        'duplicate_groups': 0,
        'kept_count': 0,
        'removed_ids': []
    }
    
    # 用于存储text_clean和对应的消息列表
    text_to_messages = defaultdict(list)
    
    # 遍历所有消息，按text_clean分组
    for message in data['massage']:
        text_clean = message['text_clean']
        text_to_messages[text_clean].append(message)
    
    # 找出重复的text_clean
    duplicate_texts = {text: messages for text, messages in text_to_messages.items() 
                      if len(messages) > 1}
    
    # 统计重复信息
    stats['duplicate_groups'] = len(duplicate_texts)
    for text, messages in duplicate_texts.items():
        stats['duplicates_found'] += len(messages) - 1  # 减去保留的一个
        # 记录被删除的ID（保留第一个，删除其余的）
        for message in messages[1:]:
            stats['removed_ids'].append(message['id'])
    
    # 创建新的消息列表，对于重复的text_clean只保留第一个
    new_messages = []
    for text, messages in text_to_messages.items():
        if len(messages) == 1:
            # 没有重复，直接添加
            new_messages.append(messages[0])
        else:
            # 有重复，只保留第一个
            new_messages.append(messages[0])
    
    # 更新数据
    data['massage'] = new_messages
    stats['kept_count'] = len(new_messages)
    
    # 确定输出文件路径
    if output_file is None:
        output_file = input_file
    
    # 保存结果
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return stats

def print_duplicate_details(input_file):
    """
    打印重复的text_clean详细信息
    
    Args:
        input_file (str): 输入JSON文件路径
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 按text_clean分组
    text_to_messages = defaultdict(list)
    for message in data['massage']:
        text_clean = message['text_clean']
        text_to_messages[text_clean].append(message)
    
    # 找出重复的text_clean
    duplicate_texts = {text: messages for text, messages in text_to_messages.items() 
                      if len(messages) > 1}
    
    print(f"\n发现 {len(duplicate_texts)} 组重复的text_clean:")
    print("=" * 80)
    
    for i, (text, messages) in enumerate(duplicate_texts.items(), 1):
        print(f"\n第 {i} 组重复 (共 {len(messages)} 条):")
        print(f"text_clean: {text[:100]}...")
        print("重复的ID:")
        for j, message in enumerate(messages):
            print(f"  {j+1}. {message['id']} (保留第1个)")
        print("-" * 40)

def main():
    """主函数"""
    input_file = "sample_data.json"
    
    # 检查文件是否存在
    if not os.path.exists(input_file):
        print(f"错误: 文件 {input_file} 不存在")
        return
    
    print("开始处理重复的text_clean...")
    
    # 先显示重复详情
    print_duplicate_details(input_file)
    
    # 处理重复
    stats = remove_duplicate_text_clean(input_file)
    
    # 输出统计信息
    print(f"\n处理完成!")
    print(f"原始数据条数: {stats['original_count']}")
    print(f"重复组数: {stats['duplicate_groups']}")
    print(f"重复条数: {stats['duplicates_found']}")
    print(f"保留条数: {stats['kept_count']}")
    print(f"删除条数: {stats['original_count'] - stats['kept_count']}")
    
    if stats['removed_ids']:
        print(f"\n被删除的ID列表:")
        for i, id in enumerate(stats['removed_ids'], 1):
            print(f"  {i}. {id}")

if __name__ == "__main__":
    main()
