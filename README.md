# AI for Procurement & Warehouse Auditing

A self-paced, interactive course on using AI for procurement and multi-warehouse data auditing. It is written for complete beginners and builds up step by step to advanced topics.

- **12 modules in 5 levels:** Foundations → Talking to AI → AI for your audit work → Communicate & automate → Going further
- **20+ hands-on labs:** a next-word predictor, a prompt builder, a seven-warehouse accuracy calculator, an Excel formula translator, an audit lab with planted issues, a finding builder, an automation scorer, a precision/recall tuner, a time-savings estimator and a 30-60-90 day plan
- **Reference pages:** a prompt library (34 prompts), a glossary and a sources page
- Progress, quiz answers and plan ticks are saved in the viewer's browser

## Open it

Open `index.html` in any modern browser. It is a single file and needs no install. Fonts load from Google Fonts when online.

To host it, enable GitHub Pages on this repository (Settings → Pages → deploy from branch, root folder). `index.html` is the entry point.

## Edit it

Source files are in `src/`, one per module. After editing, rebuild:

```bash
./build.sh
```

This produces `index.html` (standalone page) and `dist/course.html` (body-only version used for publishing as a Claude artifact).
