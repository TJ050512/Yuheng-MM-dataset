import json
import os
import shutil

json_path = 'sample_data.json'

# 读取json文件
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    # 适配 sample_data.json 的结构
    if isinstance(data, dict) and 'massage' in data:
        data = data['massage']

for item in data:
    image_path = item.get('image_path_clean')
    sample_id = item.get('id')
    if not image_path or not sample_id:
        continue

    # 获取文件扩展名
    ext = os.path.splitext(image_path)[1]
    # 构造新文件名，格式为 cleam_sample_{sample_id}_img + 扩展名
    new_name = f"{sample_id}_img{ext}"
    new_path = os.path.join(os.path.dirname(image_path), new_name)

    # 如果新路径和旧路径不同，且文件存在，则重命名
    if image_path != new_path and os.path.exists(image_path):
        print(f"重命名: {image_path} -> {new_path}")
        shutil.move(image_path, new_path)
        # 更新数据中的 image_path_clean 字段为新文件名
        item['image_path_clean'] = new_name
    else:
        print(f"跳过: {image_path}")

# 写回更新后的数据到 sample_data.json
with open(json_path, 'w', encoding='utf-8') as f:
    # 如果原始数据是带有 'massage' 键的 dict，需包裹回去
    if isinstance(data, list):
        json.dump({'massage': data}, f, ensure_ascii=False, indent=2)
    else:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("重命名完成，并已同步更新 image_path_clean 字段。")