# Rogue Wi-Fi / MITM Simulation – README

## ⚠️ EDUCATIONAL USE ONLY
This demo is for the BIT Information Security project (BITF24A052).
Run **only** on an isolated lab network that you own and control.
Unauthorized network interception is **illegal**.

---

## What This Demonstrates
- How an attacker on the same network can perform **ARP spoofing** to become
  a Man-in-the-Middle between a victim and the gateway.
- How **HTTP traffic** (unencrypted) can be intercepted, revealing URLs,
  cookies, and even login credentials.
- This simulates the risk of connecting to a **rogue/evil-twin Wi-Fi** hotspot.

## Files
| File | Purpose |
|------|---------|
| `mitm_simulation.py` | Python script using scapy for ARP spoofing + HTTP sniffing |
| `bettercap_guide.md` | Alternative step-by-step instructions using Bettercap |

## Lab Network Setup

### Recommended Setup (VirtualBox/VMware)
1. **Attacker VM**: Kali Linux – `192.168.56.10`
2. **Victim VM**: Ubuntu – `192.168.56.20`
3. **Network**: Host-Only adapter (`192.168.56.0/24`), gateway `192.168.56.1`

### Why Host-Only?
A host-only network is completely isolated from the internet and your real
network, ensuring no real traffic is affected.

## Running the Python Script

### Prerequisites
```bash
# On Kali Linux (attacker VM)
pip install scapy
```

### Run
```bash
sudo python3 mitm_simulation.py \
    --target 192.168.56.20 \
    --gateway 192.168.56.1 \
    --iface eth1
```

### On the Victim VM
1. Open Firefox and visit an HTTP site: `http://neverssl.com`
2. The attacker's terminal will display the captured HTTP request.
3. If you submit a form on an HTTP page, POST data will appear.

### Stop
Press `Ctrl+C` – the script automatically:
- Stops ARP spoofing
- Restores original ARP tables
- Disables IP forwarding

## Running with Bettercap
See `bettercap_guide.md` for detailed Bettercap instructions.

## Key Teaching Points
- HTTPS encrypts traffic and prevents this type of interception.
- VPNs add an extra layer of protection on untrusted networks.
- Users should avoid connecting to unknown/open Wi-Fi networks.
- Modern browsers warn about HTTP sites – always look for the 🔒 icon.

## Safety Checklist
- [x] Run only on isolated host-only virtual network
- [x] No real user data or production networks
- [x] ARP tables restored on exit
- [x] IP forwarding disabled on exit
- [x] Clear educational warnings in all output
