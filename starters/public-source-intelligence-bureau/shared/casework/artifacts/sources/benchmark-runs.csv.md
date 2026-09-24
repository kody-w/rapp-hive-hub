---
file: sources/benchmark-runs.csv
sha256: d8ceba2e2baa46a1a7f6e0f3bb43ab1ee77397561132021fadd92946bcbb4d58
---

```
record_id,published_at,build,offline_hours,cold_restart,attempted,acknowledged,recovered_ids,condition,origin_group,classification
run-01,2026-09-10,preview-0.8,2,0,1000,987,,No restart; credential still valid,lab-style-authored,SYNTHETIC
run-02,2026-09-13,preview-0.8,36,1,400,0,,Cold start blocked by expired credential,lab-style-authored,SYNTHETIC
run-03,2026-09-13,preview-0.8,36,1,400,0,,Repeat cold start blocked by expired credential,lab-style-authored,SYNTHETIC
run-04,2026-09-15,preview-0.8,6,1,400,398,390,Restart within credential period; recovered-ID accounting incomplete,lab-style-authored,SYNTHETIC
```
