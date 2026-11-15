# AI for Procurement & Warehouse Auditing

A self-paced, interactive course on using AI for procurement and multi-warehouse data auditing. It is written for complete beginners and builds up step by step to advanced topics.

- **12 modules in 5 levels:** Foundations → Talking to AI → AI for your audit work → Communicate & automate → Going further
- **20+ hands-on exercises:** a next-word predictor, a prompt builder, a seven-warehouse accuracy calculator, an Excel formula translator, an audit lab with planted issues, a finding builder, an automation scorer, a precision/recall tuner, a time-savings estimator and a 30-60-90 day plan
- **Reference pages:** a prompt library (34 prompts), a glossary and a sources page
- Progress, quiz answers and plan ticks are saved in the viewer's browser

## Open it

Open `index.html` in any modern browser. It is a single file and needs no install. Fonts load from Google Fonts when online.

## Published site

Once GitHub Pages is switched on (Settings → Pages → Source: "Deploy from a branch" → branch `claude/inspiring-thompson-4xkl6t`, folder `/ (root)` → Save), the course is live at:

https://bireshwarchakravarty.github.io/MyAItrainer/

Every push to that branch updates the site within a minute or two. The `.nojekyll` file tells GitHub to serve the files as they are.

## Edit it

Source files are in `src/`, one per module. After editing, rebuild:

```bash
./build.sh
```

This produces `index.html` (standalone page) and `dist/course.html` (body-only version used for publishing as a Claude artifact).
