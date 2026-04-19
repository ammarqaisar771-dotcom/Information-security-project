# Malicious App Permission Demo – README

## ⚠️ EDUCATIONAL USE ONLY
This demo is for the BIT Information Security project (BITF24A052).
Run **only** in an Android emulator. Never install on a real device with personal data.

---

## What This Demonstrates
- How a seemingly harmless app ("FlashLight Pro") requests **dangerous permissions**
  (SMS, Contacts, Location) that have nothing to do with its stated purpose.
- Once permissions are granted, the app can silently **read SMS messages, contact lists,
  and GPS location** — exactly how real-world spyware and malicious apps operate.

## Files
| File | Purpose |
|------|---------|
| `AndroidManifest.xml` | Declares dangerous permissions (READ_SMS, READ_CONTACTS, ACCESS_FINE_LOCATION) |
| `MainActivity.java` | Main Activity that requests permissions and reads data |
| `activity_main.xml` | Layout file with scrollable text output |

## How to Run (Safely)

### Prerequisites
- Android Studio installed
- Android Emulator configured (API 28+ recommended)

### Steps
1. **Create a new Android project** in Android Studio:
   - Application name: `FlashLight Pro`
   - Package: `com.edu.maliciouspermissiondemo`
   - Language: Java
   - Minimum SDK: API 23 (Android 6.0)

2. **Replace files**:
   - Copy `AndroidManifest.xml` → `app/src/main/AndroidManifest.xml`
   - Copy `MainActivity.java` → `app/src/main/java/com/edu/maliciouspermissiondemo/MainActivity.java`
   - Copy `activity_main.xml` → `app/src/main/res/layout/activity_main.xml`

3. **Add test data to emulator** (optional but recommended):
   - Open the emulator's Contacts app and add 2-3 fake contacts.
   - Send test SMS using `adb`:
     ```bash
     adb emu sms send 1234567890 "This is a test message for the demo"
     adb emu sms send 9876543210 "Another test SMS"
     ```
   - Set a mock GPS location via Extended Controls (≡) → Location.

4. **Build and run** the app on the emulator.

5. **When prompted, grant all permissions** to see the demo in action.

6. **Observe**: The app displays:
   - Which permissions were granted/denied
   - SMS messages from the inbox
   - Contacts list
   - Current GPS coordinates

## Key Teaching Points
- A flashlight app should **never** need SMS or Contacts access.
- Users should **always review permissions** before granting them.
- Android 6.0+ requires runtime permission requests, giving users a chance to deny.
- Defense: Only install apps from trusted sources; review permissions critically.

## Safety Checklist
- [x] Run only in emulator with fake data
- [x] No real personal data is accessed
- [x] Educational warning displayed in the app
- [x] Code comments explain each dangerous action
