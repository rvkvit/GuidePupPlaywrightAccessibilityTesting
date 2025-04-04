const { createServer } = require('http');
const guidepup = require('@guidepup/guidepup');
const url = require('url');

// Log available modules from guidepup
console.log('Available in guidepup:', Object.keys(guidepup));

// Use the nvda module directly
const nvda = guidepup.nvda;

// Initialize NVDA instance
let nvdaRunning = false;

// Create a simple HTTP server to provide an API for Python to interact with
const server = createServer(async (req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;
    
    // Set CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    // Handle preflight requests
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    // Handle API requests
    try {
        if (pathname === '/start') {
            if (!nvda) {
                throw new Error('NVDA module not available in guidepup');
            }
            
            // Start NVDA
            if (!nvdaRunning) {
                try {
                    await nvda.start();
                    nvdaRunning = true;
                } catch (e) {
                    throw new Error(`NVDA failed to start: ${e.message}`);
                }
            }
            
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'started' }));
        } 
        else if (pathname === '/stop') {
            // Stop NVDA
            if (nvda && nvdaRunning) {
                try {
                    await nvda.stop();
                    nvdaRunning = false;
                } catch (e) {
                    console.error('Error stopping NVDA:', e);
                }
            }
            
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'stopped' }));
        } 
        else if (pathname === '/speak') {
            // Get last spoken phrase
            if (!nvda || !nvdaRunning) {
                throw new Error('NVDA not running');
            }
            
            let speech = '';
            try {
                speech = await nvda.lastSpokenPhrase();
            } catch (e) {
                speech = `Error getting speech: ${e.message}`;
            }
            
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ speech }));
        } 
        else if (pathname === '/act') {
            // Perform action
            if (!nvda || !nvdaRunning) {
                throw new Error('NVDA not running');
            }
            
            try {
                await nvda.act();
            } catch (e) {
                throw new Error(`Error performing action: ${e.message}`);
            }
            
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'action_performed' }));
        } 
        else if (pathname === '/press') {
            // Press a key
            if (!nvda || !nvdaRunning) {
                throw new Error('NVDA not running');
            }
            
            const key = parsedUrl.query.key;
            if (!key) {
                throw new Error('Key parameter required');
            }
            
            try {
                await nvda.press(key);
            } catch (e) {
                throw new Error(`Error pressing key: ${e.message}`);
            }
            
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'key_pressed', key }));
        } 
        else if (pathname === '/version') {
            // Get guidepup version info
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ 
                guidepup: guidepup.version || 'unknown',
                modules: Object.keys(guidepup),
                nvdaAvailable: !!nvda
            }));
        }
        else {
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Not found' }));
        }
    } catch (error) {
        console.error('Error handling request:', error);
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: error.message }));
    }
});

const PORT = 3000;
server.listen(PORT, () => {
    console.log(`Guidepup bridge running at http://localhost:${PORT}`);
    console.log(`NVDA module available: ${!!nvda}`);
}); 