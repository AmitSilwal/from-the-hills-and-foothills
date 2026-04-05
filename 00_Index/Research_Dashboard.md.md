## Research Progress

## Research Progress Meter

```dataviewjs
const history = dv.pages('"02_History/Frontier_Transition"').length;
const places = dv.pages('"06_Places"').length;
const people = dv.pages('"04_People"').length;
const sources = dv.pages('"08_Sources"').length;

function bar(current, total){
    let filled = Math.round((current/total)*10);
    return "█".repeat(filled) + "─".repeat(10-filled) + `  ${current} / ${total}`;
}


dv.paragraph("History Events      " + bar(history, 50));
dv.paragraph("Places Documented   " + bar(places, 40));
dv.paragraph("People Documented   " + bar(people, 30));
dv.paragraph("Sources Studied     " + bar(sources, 20));
```

---

## History Events Documented

```dataview
TABLE file.name AS "Event"
FROM "02_History/Frontier_Transition"
SORT file.name ASC
```

---

## Places Documented

```dataview
TABLE file.name AS "Place"
FROM "06_Places"
SORT file.name ASC
```

---

## People Documented

```dataview
TABLE file.name AS "Person"
FROM "04_People"
SORT file.name ASC
```

---

## Sources Studied

```dataview
TABLE file.name AS "Source"
FROM "08_Sources"
SORT file.name ASC
```


---

## Historical Timeline

```dataview
TABLE year AS Year
FROM "02_History/Frontier_Transition"
WHERE year
SORT year ASC
```
