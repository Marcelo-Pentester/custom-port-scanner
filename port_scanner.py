#!/usr/bin/env python3
import socket
import concurrent.futures
import sys

# Definições
COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "TELNET", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 3306: "MySQL",
    3389: "RDP", 5900: "VNC", 8080: "HTTP-Alt", 6379: "Redis", 5432: "PostgreSQL"
}

TIMEOUT = 1.5  # segundos

def scan_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            s.connect((host, port))
            service = COMMON_PORTS.get(port, "Desconhecido")
            return f"[+] Porta {port} aberta ({service})"
    except:
        return None

def scan_host(host, ports):
    print(f"\n🔎 Escaneando {host}...\n")
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(lambda p: scan_port(host, p), ports)
        for result in results:
            if result:
                open_ports.append(result)
                print(result)
    if not open_ports:
        print("Nenhuma porta comum aberta detectada.")
    print(f"\n✅ Varredura finalizada para {host}.\n")

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 port_scanner.py <host> [porta1 porta2 ...]")
        print("Exemplo: python3 port_scanner.py 192.168.1.1 22 80 443")
        sys.exit(1)

    host = sys.argv[1]
    if len(sys.argv) > 2:
        ports = list(map(int, sys.argv[2:]))
    else:
        ports = list(COMMON_PORTS.keys())

    scan_host(host, ports)

if __name__ == "__main__":
    main()

