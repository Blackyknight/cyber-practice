import re
import argparse
import csv
from collections import Counter
from pathlib import Path

PATTERN = re.compile(r'Failed password for(?: invalid user)? (\w+) from ([\d\.]+)')

def parse_log(filepath):
    users = Counter()
    ips = Counter()
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        for line in f:
            m = PATTERN.search(line)
            if m:
                user, ip = m.groups()
                users[user] += 1
                ips[ip] += 1
    return users, ips

def main():
    parser = argparse.ArgumentParser(description="Detect failed SSH login attempts")
    parser.add_argument("-f", "--file", required=True, help="Log file path")
    parser.add_argument("-t", "--top", type=int, default=10, help="Top results")
    parser.add_argument("-s", "--save", default='failed_login.txt', help="Path to the output file.")
    args = parser.parse_args()

    users, ips = parse_log(args.file)
    alerts = []

    print(f"\nTop {args.top} suspicious IPs:")
    for ip, cnt in ips.most_common(args.top):
        print(f"{ip:20} {cnt}")
        if cnt > 5:
            msg = f"[ALERT] {ip} had {cnt} failed attempts!"
            print(msg)
            alerts.append(msg)

    print(f"\nTop {args.top} targeted usernames:")
    for u, cnt in users.most_common(args.top):
        print(f"{u:20} {cnt}")

    # Write all alerts at the end
    with open(args.save, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        msgInfo = "Please Check The IP Address"
        for msg in alerts:
            writer.writerow([msg + " -- " + msgInfo])

if __name__ == "__main__":
    main()