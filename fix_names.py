import os

base_folder = "content"

for root, dirs, files in os.walk(base_folder):
    for file in files:
        if file.endswith(".md.md"):
            old_path = os.path.join(root, file)
            new_name = file.replace(".md.md", ".md")
            new_path = os.path.join(root, new_name)

            os.rename(old_path, new_path)
            print(f"Renamed: {file} → {new_name}")

print("✅ All files cleaned!")
