# 🌐 From the Hills and Foothills – FINAL Publishing Workflow

## 🧱 SYSTEM OVERVIEW

WRITE → CONVERT → PUSH → LIVE

---

## 📍 FOLDER ROLES

### 🟢 WRITE (ONLY HERE)
C:\Users\ADMIN\Desktop\Hill&Foothills Research\Foundations\Hills_Foothills_Archive

### 🔵 PUBLISH (ONLY HERE)
C:\Users\ADMIN\Documents\From the Hills and Foothills\from-the-hills-and-foothills

---

## 🔄 STEP-BY-STEP WORKFLOW

### Step 1 — Write
- Open Obsidian
- Work inside Archive folder
- Create/edit `.md` files

---

### Step 2 — Convert
Run:
python convert.py

---

### Step 3 — Push
Run:

git add .
git commit -m "update"
git push

---

### Step 4 — Check
- Open your live site
- Refresh

---

## 🚨 RULES

- Always write in Archive
- Never edit repo files
- Always run convert.py before push

---

## ⚡ QUICK COMMAND

python convert.py && git add . && git commit -m "update" && git push

---

## 🧠 SUMMARY

WRITE → CONVERT → PUSH → LIVE