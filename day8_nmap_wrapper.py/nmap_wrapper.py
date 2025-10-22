#!/usr/bin/env python3
"""
nmap_wrapper.py
Run nmap from Python, parse grepable output, and save results.
Usage:
  python3 nmap_wrapper.py -t scanme.nmap.org -p 22,80,443 -o results.json
"""

import subprocess
import argparse
import csv
import json
import logging
from datetime import datetime
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def run_nmap(target: str, ports: str, extra_args: List[str] = None) -> str:
    args = ["nmap", "-p", ports, "-oG", "-", target]
    if extra_args:
        args = args + extra_args
    logging.info(f"Running: {' '.join(args)}")
    proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0 and proc.stderr:
        logging.warning(f"nmap returned non-zero code: {proc.returncode}. stderr: {proc.stderr.strip()}")
    return proc.stdout

def parse_gnmap_output(gnmap: str) -> List[Dict]:
    """
    Parse nmap grepable (-oG) output lines and return list of dicts:
    [{ "host": ip, "status": "Up", "ports": [ (port,proto,state,service), ... ]}, ...]
    """
    results = []
    for line in gnmap.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Example line:
        # Host: 45.33.32.156 ()  Ports: 22/open/tcp//ssh///,80/open/tcp//http///  Ignored State: filtered (999)
        if line.startswith("Host:"):
            parts = line.split("Ports:")
            left = parts[0]
            right = parts[1] if len(parts) > 1 else ""
            # extract host/ip and status
            # Host: <ip> (<hostname>)  Status: Up
            host_part = left.split()[1]
            status = "Unknown"
            if "Status:" in left:
                status = left.split("Status:")[1].strip()
            ports = []
            for p in right.split(","):
                p = p.strip()
                if not p:
                    continue
                # p format: 22/open/tcp//ssh///
                tokens = p.split("/")
                try:
                    port = int(tokens[0])
                    state = tokens[1]
                    proto = tokens[2]
                    service = tokens[4] if len(tokens) > 4 else ""
                except Exception:
                    continue
                ports.append({"port": port, "state": state, "proto": proto, "service": service})
            results.append({"host": host_part, "status": status, "ports": ports})
    return results

def save_json(results: List[Dict], outpath: str):
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump({"scanned_at": datetime.utcnow().isoformat(), "results": results}, f, indent=2)

def save_csv(results: List[Dict], outpath: str):
    # flatten: host, port, state, proto, service
    with open(outpath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["host", "port", "state", "proto", "service"])
        for r in results:
            host = r.get("host")
            for p in r.get("ports", []):
                writer.writerow([host, p.get("port"), p.get("state"), p.get("proto"), p.get("service")])

def main():
    parser = argparse.ArgumentParser(description="Simple nmap wrapper to run scans and save results")
    parser.add_argument("-t", "--target", required=True, help="Target hostname or IP")
    parser.add_argument("-p", "--ports", default="1-1024", help="Ports (e.g., 22,80,443 or 1-1024)")
    parser.add_argument("-o", "--output", help="Output file (JSON or CSV by extension)")
    parser.add_argument("--extra", help="Extra nmap args (quoted)", default="")
    args = parser.parse_args()

    gnmap = run_nmap(args.target, args.ports, extra_args=(args.extra.split() if args.extra else None))
    results = parse_gnmap_output(gnmap)
    logging.info(f"Found {sum(len(r.get('ports',[])) for r in results)} open ports across {len(results)} hosts")

    if args.output:
        if args.output.endswith(".json"):
            save_json(results, args.output)
            logging.info(f"Saved JSON to {args.output}")
        elif args.output.endswith(".csv"):
            save_csv(results, args.output)
            logging.info(f"Saved CSV to {args.output}")
        else:
            logging.warning("Unknown output extension. Please use .json or .csv")

    # Print quick summary
    for r in results:
        print(f"{r['host']} ({r['status']})")
        for p in r['ports']:
            print(f"  - {p['port']}/{p['proto']} {p['state']} {p['service']}")

if __name__ == "__main__":
    main()