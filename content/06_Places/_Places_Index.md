---
type: index
category: places
region: dooars
---

---

# Places Index

This index lists geographical locations referenced in the archive.

The lists below are generated automatically from place notes using metadata.

---
```dataview
TABLE WITHOUT ID file.link AS "Place"
FROM "06_Places"
WHERE type = "place" AND region = "dooars"
SORT file.name
```