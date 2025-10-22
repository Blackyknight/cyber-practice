## 🕵️ **Day 7 – REFinder (`REFinder.py`)**

```markdown
# 🕵️ REFinder (Recon Enumeration Finder)

A Python script to perform directory enumeration on websites — similar to `dirb` or `gobuster` but written manually for learning.

## 💡 Features
- Takes a target URL and wordlist.
- Tries each path (GET request).
- Reports discovered directories/files (status code 200 or 301).

## 🧰 Usage
```bash
python3 REFinder.py