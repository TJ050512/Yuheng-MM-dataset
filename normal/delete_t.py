import json

# 读取原始数据
with open('sample_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 遍历并删除每条数据中的 text_attacked 字段
for item in data.get('massage', []):
    if 'text_attacked' in item:
        del item['text_attacked']

# 保存修改后的数据
with open('sample_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("已成功删除所有 text_attacked 字段。")