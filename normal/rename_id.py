import json
import os

json_path = "sample_data.json"

print("当前工作目录：", os.getcwd())
print("操作的文件：", os.path.abspath(json_path))

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

if isinstance(data, dict) and "massage" in data and isinstance(data["massage"], list):
    arr = data["massage"]
    for idx, item in enumerate(arr, 1):
        if isinstance(item, dict):
            item["id"] = f"clean_sample_{idx:03d}"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"ID重命名完成！共处理{len(arr)}条。")
else:
    print("未找到'massage'数组，无法批量重命名。")