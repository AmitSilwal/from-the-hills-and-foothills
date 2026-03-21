import markdown
import os

input_folder = "content"
output_folder = "."

template = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>

<h1>{title}</h1>

{content}

</body>
</html>
"""

for root, dirs, files in os.walk(input_folder):
    for file in files:
        if file.endswith(".md"):
            filepath = os.path.join(root, file)

            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            html_content = markdown.markdown(text)

            title = file.replace(".md.md", "").replace(".md", "").replace("-", " ").title()

            output_file = file.replace(".md.md", ".html").replace(".md", ".html")

            with open(os.path.join(output_folder, output_file), "w", encoding="utf-8") as f:
                f.write(template.format(title=title, content=html_content))

print("✅ All markdown files converted to HTML!")
