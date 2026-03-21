import markdown
import os
import re

input_folder = "content"
output_folder = "."

# ===== HTML TEMPLATE =====
template = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>

<div class="container">
<h1>{title}</h1>

{content}
</div>

</body>
</html>
"""

# ===== FUNCTION: CLEAN TITLE =====
def clean_title(filename):
    title = filename.replace(".md.md", "").replace(".md", "")
    title = re.sub(r'^\d+_', '', title)  # remove 00_, 01_
    title = title.replace("_", " ").replace("-", " ").title()
    return title

# ===== CONVERT MARKDOWN TO HTML =====
all_pages = []

for root, dirs, files in os.walk(input_folder):
    for file in files:
        if file.endswith(".md"):

            filepath = os.path.join(root, file)

            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            # remove frontmatter
            if text.startswith("---"):
                parts = text.split("---", 2)
                if len(parts) > 2:
                    text = parts[2]

            # convert [[links]] to html links
            text = re.sub(r"\[\[(.*?)\]\]", r'<a href="\1.html">\1</a>', text)

            html_content = markdown.markdown(text)

            # clean title
            title = clean_title(file)

            output_file = file.replace(".md.md", ".html").replace(".md", ".html")

            # save html file
            with open(os.path.join(output_folder, output_file), "w", encoding="utf-8") as f:
                f.write(template.format(title=title, content=html_content))

            # store for notes page
            all_pages.append((title, output_file))

print("✅ All markdown files converted to HTML!")

# ===== GENERATE NOTES PAGE (NOT HOMEPAGE) =====

# Sort alphabetically
all_pages.sort()

links = ""
for title, html_file in all_pages:
    links += f'<li><a href="{html_file}">{title}</a></li>\n'

notes_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Notes Archive</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>

<div class="container">
<h1>Notes Archive</h1>
<p>All research notes from the archive</p>

<ul>
{links}
</ul>
</div>

</body>
</html>
"""

# ⚠️ IMPORTANT: This now writes to notes.html (NOT index.html)
with open("notes.html", "w", encoding="utf-8") as f:
    f.write(notes_html)

print("✅ Notes page created successfully!")
