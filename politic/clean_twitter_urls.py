import json
import re
import os

def clean_twitter_urls(text):
    """
    删除文本末尾的 https://t.co/ 类型的网址
    使用正则表达式匹配并删除末尾的Twitter短链接
    """
    if not text:
        return text
    
    pattern = r'\s*https://t\.co/[a-zA-Z0-9]+\s*$'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text.strip()

def process_json_file(input_file, output_file):
    """
    处理JSON文件，清理所有text_clean字段中的Twitter短链接，删除modal_consistency字段，插入新字段
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        total_records = 0
        cleaned_urls = 0
        if 'massage' in data:
            for item in data['massage']:
                total_records += 1
                # 删除modal_consistency字段
                if 'modal_consistency' in item:
                    del item['modal_consistency']
                # attack_type_text和attack_type_image设为None
                if 'text_attacked' in item:
                    item['text_attacked'] = None
                if 'image_path_attacked' in item:
                    item['image_path_attacked'] = None
                if 'attack_type_text' in item:
                    item['attack_type_text'] = None
                if 'attack_type_image' in item:
                    item['attack_type_image'] = None
                # 清理text_clean
                if 'text_clean' in item and item['text_clean']:
                    original_text = item['text_clean']
                    cleaned_text = clean_twitter_urls(original_text)
                    if cleaned_text != original_text:
                        cleaned_urls += 1
                        print(f"清理URL: {original_text[:50]}... -> {cleaned_text[:50]}...")
                    item['text_clean'] = cleaned_text
                # 插入新字段到指定位置
                # 先收集所有字段，准备插入
                new_fields = {
                    "text_attack_level": None,
                    "image_attack_level": None,
                    "text_metaphor_level": None,
                    "image_metaphor_level": None,
                    "joint_metaphor_level": None
                }
                # 重新构建item，插入新字段
                new_item = {}
                for k, v in item.items():
                    new_item[k] = v
                    if k == 'attack_type_image':
                        for nf, nv in new_fields.items():
                            new_item[nf] = nv
                # 保证source字段在新字段后
                if 'source' in item and 'source' not in new_item:
                    new_item['source'] = item['source']
                # 替换原item
                item.clear()
                item.update(new_item)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n处理完成！")
        print(f"总记录数: {total_records}")
        print(f"清理的URL数: {cleaned_urls}")
        print(f"输出文件: {output_file}")
    except FileNotFoundError:
        print(f"错误: 找不到文件 {input_file}")
    except json.JSONDecodeError:
        print(f"错误: {input_file} 不是有效的JSON文件")
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")

def main():
    input_file = "sample_data.json"
    output_file = "sample_data.json"
    if not os.path.exists(input_file):
        print(f"错误: 文件 {input_file} 不存在")
        return
    print(f"开始处理文件: {input_file}")
    print("正在清理 text_clean 字段中的 Twitter 短链接...")
    process_json_file(input_file, output_file)

if __name__ == "__main__":
    main() 