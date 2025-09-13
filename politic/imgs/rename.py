import os

# 需要重命名的文件夹路径
folder = "imgs"

for filename in os.listdir(folder):
    if filename.startswith("cleam_sample_"):
        new_name = filename.replace("cleam_sample_", "", 1)
        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_name)
        print(f"重命名: {old_path} -> {new_path}")
        os.rename(old_path, new_path)

print("批量重命名完成。")