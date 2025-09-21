## Language Converter (CN/EN → JP + Romaji)
**Status:** 🚧 **In progress** (actively building; APIs and UI are evolving)

**Overview.**  
A lightweight web tool that converts Chinese/English text into Japanese and appends Romaji for readability/pronunciation. Built to be fast, reliable, and easy to demo.

**Motivation.**  
For non-native speakers it’s often inconvenient to convert **your own name** into natural Japanese and Romaji.  
Example: **“YOUR NAME” → 「かな例」 → `romaji-example`** (style is configurable).  
This project focuses on making that flow one-click and consistent.

**Key features (planned).**  
- Name handling: katakana mode / kanji-reading mode / custom dictionary & per-user overrides  
- Romaji styles: Hepburn / kunrei, ascii (`ryou`) or macron (`ryō`)  
- Batch input + export; deterministic post-edit rules; minimal UI

**Tech stack.** Next.js (TypeScript); FastAPI (Python). Planned libs: fugashi/MeCab, romkan, optional transformer-based translation. Dockerized for local dev and CI.

**Roadmap.**  
MVP (mock → real pipeline) → batch/export → caching + tests → small demo deploy.
