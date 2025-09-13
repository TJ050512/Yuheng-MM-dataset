import json
import os

json_path = "sample_data.json"

print("当前工作目录：", os.getcwd())
print("操作的文件：", os.path.abspath(json_path))

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

if isinstance(data, dict) and "massage" in data and isinstance(data["massage"], list):
    arr = data["massage"]
    for item in arr:
        if isinstance(item, dict) and "text_clean" in item and isinstance(item["text_clean"], str):
            # 将所有连续的两个换行替换为一个换行
            while "\n\n" in item["text_clean"]:
                item["text_clean"] = item["text_clean"].replace("\n\n", "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("所有text_clean中的\\n\\n已替换为单个\\n。")
else:
    print("未找到'massage'数组，无法批量处理。")