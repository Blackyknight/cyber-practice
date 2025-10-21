import re
import argparse
from collections import Counter
import csv
import sys
from pathlib import Path

IP_RE = re.compile(r'(?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}(?:25[0-5]|2[0-4]\d|1?\d{1,2})')

def extract_ips_from_line(line):
    return IP_RE.findall(line)

def parse_file(path):
    counts = Counter()
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                ips = extract_ips_from_line(line)
                for ip in ips:
                    counts[ip] += 1
    except FileNotFoundError:
         print(f"File not found: {path}", file=sys.stderr)
         sys.exit(2)
    return counts

def write_csv(counts, outpath):
    with open(outpath, 'w', newline='', encoding='utf-8') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['ip','count'])
        for ip, cnt in counts.most_common():
            writer.writerow([ip, cnt])