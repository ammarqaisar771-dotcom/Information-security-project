<!--
  ============================================================
   EDUCATIONAL PHISHING DEMO – README
   Student: Muhammad Ammar Qaisar (BITF24A052)
   Project: How Attackers Target Smartphones
  ============================================================
-->

# Phishing Attack Demo – README

## ⚠️ EDUCATIONAL USE ONLY
This demo is created for the BIT Information Security project. It simulates a
phishing attack in a **controlled lab environment**. **Never** deploy this
against real users or on public networks.

---

## What This Demonstrates
- How attackers create convincing fake login pages that mimic legitimate services.
- How entered credentials are silently captured and logged.
- Why users must always verify the URL and look for HTTPS before entering credentials.

## Files
| File          | Purpose |
|---------------|---------|
| `index.html`  | Fake login page (HTML/CSS/JS) with educational warning banner |
| `server.js`   | Node.js backend that serves the page and records credentials |

## How to Run (Safely)

### Option A – Browser Only (No Server)
1. Open `index.html` directly in any browser.
2. Enter test credentials (e.g., `test@test.com` / `password123`).
3. Credentials appear in the on-page panel and in the browser console (`F12 → Console`).

### Option B – With Node.js Backend
1. Ensure Node.js (v14+) is installed.
2. Open a terminal in this directory.
3. Run: `node server.js`
4. Open **http://localhost:3000** in a browser.
5. Enter test credentials – they appear in the terminal **and** are saved to `captured_credentials.json`.
6. In `index.html`, uncomment the `fetch('/capture', …)` block inside `captureCredentials()` to enable server logging.

### Option C – PHP Backend (Alternative)
If you prefer PHP:
```php
<?php
// save as capture.php in the same directory
// Run: php -S localhost:8080
$data = json_decode(file_get_contents('php://input'), true);
$log  = json_decode(file_get_contents('captured_credentials.json') ?: '[]', true);
$log[] = $data;
file_put_contents('captured_credentials.json', json_encode($log, JSON_PRETTY_PRINT));
echo json_encode(['status' => 'logged']);
```
Point the fetch URL in `index.html` to `http://localhost:8080/capture.php`.

## Safety Checklist
- [x] Runs on localhost only
- [x] No data leaves the machine
- [x] Clear warning banner visible at all times
- [x] No real user data is used
