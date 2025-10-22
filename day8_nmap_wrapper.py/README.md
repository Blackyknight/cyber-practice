# 🛰️ nmap_wrapper.py

A small Python wrapper that runs `nmap` (using `-oG -` grepable output), parses the output, and saves results to JSON or CSV.  
Designed as a learning tool to automate scans in a safe lab environment and to practice `subprocess` usage, parsing, and reporting.

---

## 🔎 Purpose
- Automate running `nmap` from Python and capture results programmatically.  
- Parse `-oG` (grepable) output to extract hosts and open ports.  
- Save scan results to `JSON` or `CSV` for later analysis or reporting.  
- Practice safe scanning against lab targets (TryHackMe, HTB, `scanme.nmap.org`) and build a portfolio artifact.

---

## ✅ Features
- Runs `nmap` with chosen ports and extra arguments.  
- Parses `-oG` output into structured Python objects (host, status, ports).  
- Saves results as `.json` or `.csv`.  
- Prints a human-readable summary to stdout.  
- Basic logging of actions and warnings.

---

## ⚙️ Requirements
- Python 3.8+  
- `nmap` installed on the system (`sudo apt install nmap` on Debian/Ubuntu)  
- (Optional) `pytest` for running the basic test included

---

## ⚠️ Safety & Legal
**Only run scans against systems you own or have explicit permission to test.**  
Good targets for practice:
- `scanme.nmap.org` (permitted by Nmap for testing)
- TryHackMe or HackTheBox assigned targets
- Your own lab VMs / cloud instances

Unauthorized scanning of third-party systems may be illegal and unethical.