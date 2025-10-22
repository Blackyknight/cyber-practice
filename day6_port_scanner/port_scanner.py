import socket, logging

logging.basicConfig(
    filename="port_scanner.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a",
)

try:
    target = input("Enter target IP address or domain: ")
    print(f"\nScanning {target}...\n")

    common_ports = list(range(1025))

    for port in common_ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        socket.setdefaulttimeout(0.1)

        result = s.connect_ex((target, port))

        if result == 0:
            print(f"Port {port}: is Open")
            logging.info(f"Port {port} on {target} is Open")

        s.close()

    print("\nScan completed.")

except socket.gaierror:
    print("Invalid input. Please enter a valid IP address or domain.")

except KeyboardInterrupt:
    print("\nScan interrupted by user.")
