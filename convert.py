import markdown
import os
import re
import json

input_folder = "content"
output_folder = "site"

os.makedirs(output_folder, exist_ok=True)

# ===== SLUG FUNCTION =====
def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

# ===== YAML EXTRACTOR =====
def extract_yaml(text):
    match = re.match(r"^---(.*?)---", text, re.DOTALL)
    if not match:
        return {}
    
    yaml_block = match.group(1)
    data = {}
    
    for line in yaml_block.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    
    return data

# ===== NAVBAR =====
def get_navbar(current_page):
    return f"""
<nav class="navbar">
  <div class="nav-container">
    <a href="index.html" class="nav-logo">Hills & Foothills</a>
    
    <ul class="nav-menu">
      <li><a href="index.html" class="{ 'active' if current_page=='index.html' else '' }">Home</a></li>
      <li><a href="timeline.html" class="{ 'active' if current_page=='timeline.html' else '' }">Timeline</a></li>
      <li><a href="history.html" class="{ 'active' if current_page=='history.html' else '' }">History</a></li>
      <li><a href="places.html" class="{ 'active' if current_page=='places.html' else '' }">Places</a></li>
      <li><a href="maps.html" class="{ 'active' if current_page=='maps.html' else '' }">Maps</a></li>
      <li><a href="notes.html" class="{ 'active' if current_page=='notes.html' else '' }">All Notes</a></li>
    </ul>

    <div class="search-box">
      <input type="text" id="searchInput" placeholder="Search..." onkeyup="searchNotes()">
      <div id="searchResults" class="search-results"></div>
    </div>
  </div>
</nav>
"""

# ===== TEMPLATE =====
def get_template(title, content, navbar, is_home=False):
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>

{navbar}

<div class="container">
{"" if is_home else f"<h1>{title}</h1>"}
{content}
</div>

<script src="search_index.js"></script>

<script>
function searchNotes() {{
  let input = document.getElementById("searchInput").value.toLowerCase();
  let resultsBox = document.getElementById("searchResults");

  if (!input) {{
    resultsBox.innerHTML = "";
    return;
  }}

  let results = searchIndex.filter(item =>
    item.title.toLowerCase().includes(input)
  );

  resultsBox.innerHTML = results
    .slice(0, 10)
    .map(r => `<div><a href="${{r.url}}">${{r.title}}</a></div>`)
    .join("");
}}
</script>

</body>
</html>
"""

# ===== TITLE CLEANING =====
def clean_title(filename):
    title = filename.replace(".md", "")
    title = re.sub(r'^\d+[_-]', '', title)
    title = title.replace("_", " ").replace("-", " ").title()
    return title

# ===== IMAGE HANDLING =====
def convert_images(text):
    return re.sub(
        r"!\[\[(.*?)\]\]",
        lambda m: f'<img src="content/{m.group(1)}" class="content-image">',
        text
    )

# ===== COLLECT FILES =====
all_pages = []
file_map = {}
raw_pages = []
timeline_data = []

for root, dirs, files in os.walk(input_folder):
    for file in files:
        if file.endswith(".md"):
            raw_pages.append((root, file))

# ===== BUILD FILE MAP =====
for root, file in raw_pages:
    name = os.path.splitext(file)[0]
    slug = slugify(name)
    html_file = f"{slug}.html"

    all_pages.append((name, html_file))
    file_map[slug] = html_file

# ===== LINK CONVERSION =====
def convert_links(match):
    name = match.group(1)
    slug = slugify(name)
    display_name = name.replace("_", " ").title()

    if slug in file_map:
        return f'<a href="{file_map[slug]}">{display_name}</a>'
    else:
        return display_name

# ===== BREADCRUMB =====
def generate_breadcrumb(filepath, filename):
    if filename == "index.md":
        return '<a href="index.html">Home</a>'

    parts = filepath.split(os.sep)
    breadcrumb = ['<a href="index.html">Home</a>']

    if "content" in parts:
        parts = parts[parts.index("content") + 1:]

    if parts and parts[-1] == filename:
        parts = parts[:-1]

    for part in parts:
        clean = re.sub(r'^\d+[_-]', '', part).replace("_", " ").title()
        link = slugify(part) + ".html"
        breadcrumb.append(f'<a href="{link}">{clean}</a>')

    breadcrumb.append(f"<span>{clean_title(filename)}</span>")

    return " > ".join(breadcrumb)

# ===== GENERATE PAGES =====
for root, file in raw_pages:

    filepath = os.path.join(root, file)

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # ===== EXTRACT YAML =====
    metadata = extract_yaml(text)

    # ===== STORE TIMELINE DATA =====
    if "year" in metadata:
        timeline_data.append({
            "year": metadata["year"],
            "title": clean_title(file),
            "url": slugify(file.replace(".md", "")) + ".html"
        })

    # ===== REMOVE YAML =====
    text = text.strip()
    text = re.sub(r"^---[\s\S]*?---", "", text).strip()

    # ===== PROCESS CONTENT =====
    text = convert_images(text)
    text = re.sub(r"\[\[(.*?)\]\]", convert_links, text)

    html_content = markdown.markdown(text, extensions=['extra'])

    title = "Home" if file == "index.md" else clean_title(file)
    slug = slugify(file.replace(".md", ""))
    output_file = f"{slug}.html"

    breadcrumb = generate_breadcrumb(filepath, file)
    html_content = f'<div class="breadcrumb">{breadcrumb}</div>' + html_content

    navbar = get_navbar(output_file)
    is_home = (output_file == "index.html")

    final_html = get_template(title, html_content, navbar, is_home)

    with open(os.path.join(output_folder, output_file), "w", encoding="utf-8") as f:
        f.write(final_html)

print("✅ Pages generated")

# ===== TIMELINE PAGE =====
timeline_data.sort(key=lambda x: x["year"])

timeline_html = "<h1>Historical Timeline</h1><ul>"

for item in timeline_data:
    timeline_html += f'<li><b>{item["year"]}</b> — <a href="{item["url"]}">{item["title"]}</a></li>'

timeline_html += "</ul>"

navbar = get_navbar("timeline.html")

timeline_page = get_template("Timeline", timeline_html, navbar)

with open(os.path.join(output_folder, "timeline.html"), "w", encoding="utf-8") as f:
    f.write(timeline_page)

print("✅ Timeline generated")

# ===== NOTES PAGE =====
all_pages.sort()

links = ""
for title, html_file in all_pages:
    clean = slugify(title).replace("-", " ").title()
    links += f'<li><a href="{html_file}">{clean}</a></li>\n'

navbar = get_navbar("notes.html")

notes_html = get_template(
    "Notes Archive",
    f"<h1>Notes Archive</h1><ul>{links}</ul>",
    navbar
)

with open(os.path.join(output_folder, "notes.html"), "w", encoding="utf-8") as f:
    f.write(notes_html)

# ===== SEARCH INDEX =====
search_index = [{"title": clean_title(t), "url": u} for t, u in all_pages]

with open(os.path.join(output_folder, "search_index.js"), "w", encoding="utf-8") as f:
    f.write("const searchIndex = " + json.dumps(search_index))

print("✅ Search index created")
