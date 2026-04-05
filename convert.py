import markdown
import os
import re
import json

# -----------------------
# FOLDERS (FIXED)
# -----------------------
input_folder = "content"

# 🔥 OUTPUT → REPO FOLDER (IMPORTANT FIX)
output_folder = r"C:\Users\ADMIN\Documents\From the Hills and Foothills\from-the-hills-and-foothills"

os.makedirs(output_folder, exist_ok=True)

pages = []
search_index = []
file_map = {}

# -----------------------
# SLUG FUNCTION
# -----------------------
def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


# -----------------------
# LINK CONVERSION
# -----------------------
def convert_links(text):
    def replace(match):
        name = match.group(1)
        if name in file_map:
            return f'<a href="{file_map[name]}">{name}</a>'
        return name

    return re.sub(r"\[\[(.*?)\]\]", replace, text)


# -----------------------
# STEP 1: MAP FILES
# -----------------------
for root, dirs, files in os.walk(input_folder):
    for file in files:
        if file.endswith(".md") and file.lower() != "index.md":
            name = file.replace(".md", "")
            file_map[name] = slugify(name) + ".html"


# -----------------------
# STEP 2: CONVERT FILES
# -----------------------
for root, dirs, files in os.walk(input_folder):
    for file in files:
        if file.endswith(".md") and file.lower() != "index.md":

            path = os.path.join(root, file)

            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            text = convert_links(text)
            html = markdown.markdown(text)

            name = file.replace(".md", "")
            output_file = slugify(name) + ".html"

            print("CREATED:", name, "->", output_file)

            final_html = f"""
<html>
<head>
    <title>{name.replace('-', ' ')}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<!-- NAVBAR -->
<div style="background:#1f3c88;padding:12px;color:white;">
    <b>Hills & Foothills</b>
    <span style="margin-left:20px;">
        <a href="index.html" style="color:white;margin-right:15px;">Home</a>
        <a href="00-timeline-dooars.html" style="color:white;margin-right:15px;">Timeline</a>
        <a href="00-history-index.html" style="color:white;margin-right:15px;">History</a>
        <a href="places-index.html" style="color:white;margin-right:15px;">Places</a>
        <a href="maps.html" style="color:white;margin-right:15px;">Maps</a>
        <a href="notes.html" style="color:white;">All Notes</a>
    </span>
</div>

<!-- CONTENT -->
<div style="max-width:900px;margin:auto;padding:20px;">

{html}

<br><br>
<a href="notes.html">Back to Notes</a>

</div>

</body>
</html>
"""

            # 🔥 WRITE TO REPO FOLDER
            with open(os.path.join(output_folder, output_file), "w", encoding="utf-8") as f:
                f.write(final_html)

            pages.append((name, output_file))
            search_index.append({"title": name, "url": output_file})


print("Pages generated")


# -----------------------
# STEP 3: NOTES PAGE
# -----------------------
links = ""
for name, file in pages:
    links += f'<li><a href="{file}">{name}</a></li>\n'

notes_html = f"""
<html>
<head>
    <title>Notes Archive</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>

<!-- NAVBAR -->
<div style="background:#1f3c88;padding:12px;color:white;">
    <b>Hills & Foothills</b>
    <span style="margin-left:20px;">
        <a href="index.html" style="color:white;margin-right:15px;">Home</a>
        <a href="00-timeline-dooars.html" style="color:white;margin-right:15px;">Timeline</a>
        <a href="00-history-index.html" style="color:white;margin-right:15px;">History</a>
        <a href="places-index.html" style="color:white;margin-right:15px;">Places</a>
        <a href="maps.html" style="color:white;margin-right:15px;">Maps</a>
        <a href="notes.html" style="color:white;">All Notes</a>
    </span>
</div>

<div style="max-width:900px;margin:auto;padding:20px;">
<h1>Notes Archive</h1>

<ul>
{links}
</ul>

</div>

</body>
</html>
"""

with open(os.path.join(output_folder, "notes.html"), "w", encoding="utf-8") as f:
    f.write(notes_html)

print("Notes page generated")


# -----------------------
# STEP 4: SEARCH INDEX
# -----------------------
with open(os.path.join(output_folder, "search_index.js"), "w", encoding="utf-8") as f:
    f.write("const searchIndex = ")
    json.dump(search_index, f)
    f.write(";")

print("Search index created")
