import dns.resolver
import requests
import argparse
import socket
from prettytable import PrettyTable
from requests.exceptions import RequestException
import curses

def query_dns(domain, record_type='A'):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [str(rdata) for rdata in answers]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers, dns.resolver.Timeout):
        return None

def is_port_open(host, port):
    try:
        socket.setdefaulttimeout(1)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except socket.error:
        return False

def get_http_status_and_title(domain):
    try:
        response = requests.get(f"http://{domain}", timeout=2)
        status_code = response.status_code
        title = None
        if "<title>" in response.text:
            title = response.text.split("<title>")[1].split("</title>")[0]
        return status_code, title
    except RequestException:
        return None, None

def find_subdomains(domain):
    wordlist_url = "https://raw.githubusercontent.com/rbsec/dnscan/master/subdomains-10000.txt"
    wordlist = requests.get(wordlist_url).text.splitlines()
    subdomains = [f"{sub}.{domain}" for sub in wordlist]
    return subdomains

def check_subdomain(subdomain):
    ip_addresses = query_dns(subdomain)
    if ip_addresses:
        for ip in ip_addresses:
            if not ip.startswith("104.") and not ip.startswith("172.") and not ip.startswith("192.") and not ip.startswith("198.") and not ip.startswith("199.") and not ip.startswith("103.") and not ip.startswith("100."):
                return ip
    return None

def brute_force_subdomains(domain, stdscr):
    subdomains = find_subdomains(domain)
    total_subdomains = len(subdomains)
    found_subdomains = []
    table = PrettyTable(["Subdomain", "IP Address", "Original IP", "Port 80", "Port 22", "HTTP Status", "Title"])

    stdscr.clear()
    stdscr.addstr(0, 0, f"{'Subdomain':<30} {'IP Address':<15} {'Original IP':<15} {'Port 80':<7} {'Port 22':<7} {'HTTP Status':<12} {'Title':<30}")
    stdscr.addstr(1, 0, "="*150)
    stdscr.refresh()
    
    for i, subdomain in enumerate(subdomains):
        fqdn = subdomain
        ip_addresses = query_dns(fqdn)
        original_ip = check_subdomain(fqdn)
        if ip_addresses:
            port_80_status = "✔" if is_port_open(fqdn, 80) else "✘"
            port_22_status = "✔" if is_port_open(fqdn, 22) else "✘"
            http_status, title = get_http_status_and_title(fqdn) if port_80_status == "✔" else (None, None)
            http_status = http_status if http_status is not None else ""
            title = title if title is not None else ""
            for ip in ip_addresses:
                ip = ip if ip is not None else ""
                original_ip = original_ip if original_ip is not None else ""
                found_subdomains.append((fqdn, ip, original_ip, port_80_status, port_22_status, http_status, title))
                stdscr.addstr(len(found_subdomains) + 1, 0, f"{fqdn:<30} {ip:<15} {original_ip:<15} {port_80_status:<7} {port_22_status:<7} {http_status:<12} {title:<30}")
                stdscr.refresh()

        # Mostrar el progreso
        progress = (i + 1) / total_subdomains * 100
        stdscr.addstr(curses.LINES - 1, 0, f"Progress: {progress:.2f}%")
        stdscr.clrtoeol()
        stdscr.refresh()

    return found_subdomains, table

def main(stdscr):
    parser = argparse.ArgumentParser(description="Subdomain enumeration tool")
    parser.add_argument("domain", help="The domain to enumerate subdomains for")
    args = parser.parse_args()

    domain = args.domain

    stdscr.clear()
    stdscr.addstr(0, 0, f"Starting subdomain enumeration for {domain}")
    stdscr.refresh()
    found_subdomains, table = brute_force_subdomains(domain, stdscr)

    stdscr.addstr(curses.LINES - 2, 0, "\n\nSubdomains found:")
    stdscr.refresh()
    if found_subdomains:
        stdscr.addstr(curses.LINES - 1, 0, str(table))
        stdscr.refresh()
    else:
        stdscr.addstr(curses.LINES - 1, 0, "No subdomains found.")
        stdscr.refresh()

    stdscr.addstr(curses.LINES - 1, 0, "Finished searching for subdomains.")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
