## 🔐 **Day 3 – Failed Login Detector (`failedLoginDetector.py`)**

```markdown
# 🔐 Failed Login Detector

This script scans SSH or system log files to detect repeated failed login attempts — a common early cybersecurity detection task.

## 💡 Features
- Reads a log file line by line.
- Uses regex to extract failed login attempts.
- Counts number of attempts per IP address.
- Flags IPs with excessive failures.

## 🧰 Usage
```bash
python3 failedLoginDetector.py