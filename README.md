# ✈️ Nouvelair Delay Watch

**Automated Data Engineering project** that tracks, analyzes, and reports delays for Nouvelair airline flights globally.

---

## 🚀 Project Objective

Build an end-to-end automated pipeline that fetches daily flight data, detects delays, generates insightful reports, and publishes them online or via social media.

---

## 📁 Project Structure

```bash
nouvelair-delay-watch/
├── data/                 # Raw & processed data
├── src/                  # All source code
│   ├── etl/              # Extract and transform scripts
│   ├── analysis/         # Daily analytics code
│   ├── report/           # Report creation logic
│   └── post/             # Social/email publishing
├── notebooks/            # EDA and experiments
├── dashboard/            # Optional visual dashboard
├── README.md
├── requirements.txt
└── cronjob.sh / dag.py   # Task scheduler
```
