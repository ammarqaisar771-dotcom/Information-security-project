/*
 * ============================================================
 *  MainActivity.java – Malicious App Permission Demo
 *  Student: Muhammad Ammar Qaisar (BITF24A052)
 *  Project: How Attackers Target Smartphones
 *
 *  ⚠️  EDUCATIONAL USE ONLY
 *      This code shows how a malicious app can access SMS,
 *      contacts, and location once dangerous permissions are
 *      granted. Run ONLY in an Android emulator.
 * ============================================================
 */

package com.edu.maliciouspermissiondemo;

import android.Manifest;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.net.Uri;
import android.os.Bundle;
import android.provider.ContactsContract;
import android.util.Log;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "MalPermDemo";
    private static final int REQ_CODE = 100;

    private TextView tvOutput;

    /* Dangerous permissions the "malicious" app requests */
    private final String[] DANGEROUS_PERMISSIONS = {
        Manifest.permission.READ_SMS,
        Manifest.permission.READ_CONTACTS,
        Manifest.permission.ACCESS_FINE_LOCATION
    };

    // ── Lifecycle ──────────────────────────────────────────────

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        tvOutput = findViewById(R.id.tvOutput);

        appendLine("╔══════════════════════════════════════╗");
        appendLine("║  ⚠️  EDUCATIONAL DEMO ONLY           ║");
        appendLine("║  Malicious App Permission Demo       ║");
        appendLine("║  Student: BITF24A052                 ║");
        appendLine("╚══════════════════════════════════════╝\n");
        appendLine("This app pretends to be \"FlashLight Pro\"");
        appendLine("but requests dangerous permissions to");
        appendLine("access your SMS, Contacts, and Location.\n");
        appendLine("Requesting permissions now...\n");

        requestDangerousPermissions();
    }

    // ── Permission request ────────────────────────────────────

    private void requestDangerousPermissions() {
        ActivityCompat.requestPermissions(this, DANGEROUS_PERMISSIONS, REQ_CODE);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode,
            @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);

        if (requestCode != REQ_CODE) return;

        for (int i = 0; i < permissions.length; i++) {
            String perm    = permissions[i];
            boolean granted = grantResults[i] == PackageManager.PERMISSION_GRANTED;
            appendLine((granted ? "✅" : "❌") + " " + shortName(perm)
                       + " → " + (granted ? "GRANTED" : "DENIED"));
        }

        appendLine("\n──── Data Accessible After Granting ────\n");

        // Demo: read SMS
        if (hasPermission(Manifest.permission.READ_SMS)) {
            readSmsDemo();
        } else {
            appendLine("[SMS] Permission denied – cannot read messages.\n");
        }

        // Demo: read Contacts
        if (hasPermission(Manifest.permission.READ_CONTACTS)) {
            readContactsDemo();
        } else {
            appendLine("[Contacts] Permission denied.\n");
        }

        // Demo: read Location
        if (hasPermission(Manifest.permission.ACCESS_FINE_LOCATION)) {
            readLocationDemo();
        } else {
            appendLine("[Location] Permission denied.\n");
        }
    }

    // ── SMS Demo ──────────────────────────────────────────────

    private void readSmsDemo() {
        appendLine("📩  SMS INBOX (first 5 messages):");
        try {
            Uri smsUri = Uri.parse("content://sms/inbox");
            Cursor cursor = getContentResolver().query(smsUri,
                    new String[]{"address", "body", "date"},
                    null, null, "date DESC");

            if (cursor != null) {
                int count = 0;
                while (cursor.moveToNext() && count < 5) {
                    String from = cursor.getString(0);
                    String body = cursor.getString(1);
                    appendLine("   From: " + from);
                    appendLine("   Body: " + truncate(body, 60));
                    appendLine("   ---");
                    count++;
                }
                if (count == 0) appendLine("   (No SMS found on this emulator)");
                cursor.close();
            }
        } catch (Exception e) {
            appendLine("   Error reading SMS: " + e.getMessage());
        }
        appendLine("");
    }

    // ── Contacts Demo ─────────────────────────────────────────

    private void readContactsDemo() {
        appendLine("📇  CONTACTS (first 5 entries):");
        try {
            Cursor cursor = getContentResolver().query(
                    ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
                    new String[]{
                        ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME,
                        ContactsContract.CommonDataKinds.Phone.NUMBER
                    },
                    null, null, null);

            if (cursor != null) {
                int count = 0;
                while (cursor.moveToNext() && count < 5) {
                    String name  = cursor.getString(0);
                    String phone = cursor.getString(1);
                    appendLine("   " + name + " – " + phone);
                    count++;
                }
                if (count == 0) appendLine("   (No contacts found on this emulator)");
                cursor.close();
            }
        } catch (Exception e) {
            appendLine("   Error reading contacts: " + e.getMessage());
        }
        appendLine("");
    }

    // ── Location Demo ─────────────────────────────────────────

    private void readLocationDemo() {
        appendLine("📍  LOCATION (requesting last known):");
        try {
            LocationManager lm = (LocationManager) getSystemService(LOCATION_SERVICE);
            Location loc = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);

            if (loc != null) {
                appendLine("   Lat: " + loc.getLatitude());
                appendLine("   Lon: " + loc.getLongitude());
                appendLine("   Accuracy: " + loc.getAccuracy() + " m");
            } else {
                appendLine("   (No cached location – requesting update...)");
                lm.requestSingleUpdate(LocationManager.GPS_PROVIDER,
                    new LocationListener() {
                        @Override
                        public void onLocationChanged(@NonNull Location l) {
                            appendLine("   Lat: " + l.getLatitude());
                            appendLine("   Lon: " + l.getLongitude());
                        }
                        @Override public void onStatusChanged(String s, int i, Bundle b) {}
                        @Override public void onProviderEnabled(@NonNull String s) {}
                        @Override public void onProviderDisabled(@NonNull String s) {}
                    }, null);
            }
        } catch (SecurityException e) {
            appendLine("   Security exception: " + e.getMessage());
        }
        appendLine("");
    }

    // ── Helpers ───────────────────────────────────────────────

    private boolean hasPermission(String perm) {
        return ContextCompat.checkSelfPermission(this, perm)
               == PackageManager.PERMISSION_GRANTED;
    }

    private String shortName(String perm) {
        return perm.replace("android.permission.", "");
    }

    private String truncate(String s, int max) {
        if (s == null) return "";
        return s.length() > max ? s.substring(0, max) + "…" : s;
    }

    private void appendLine(String line) {
        Log.d(TAG, line);
        runOnUiThread(() -> tvOutput.append(line + "\n"));
    }
}
