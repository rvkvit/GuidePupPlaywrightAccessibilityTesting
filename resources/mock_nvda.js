// Mock NVDA implementation for testing purposes
const { createServer } = require('http');
const url = require('url');

// Simulated speech responses for different elements
const mockResponses = {
    'input[type="text"]': 'edit field, username',
    'input[type="password"]': 'password edit, secure text',
    'button[type="submit"]': 'submit button, login',
    'h1': 'heading level 1, Welcome to LähiTapiola',
    'input[type="checkbox"]': 'checkbox not checked, remember me',
    'a': 'link, forgot password',
    'nav': 'navigation region'
};

// Keep track of the last focused element
let lastFocusedElement = null;
let nvdaRunning = false;

// Create a simple HTTP server to provide a mock NVDA API
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
            // Start mock NVDA
            nvdaRunning = true;
            console.log('Mock NVDA started');
            
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'started' }));
        } 
        else if (pathname === '/stop') {
            // Stop mock NVDA
            nvdaRunning = false;
            console.log('Mock NVDA stopped');
            
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'stopped' }));
        } 
        else if (pathname === '/speak') {
            // Get last spoken phrase
            if (!nvdaRunning) {
                throw new Error('Mock NVDA not running');
            }
            
            let speech = 'No element focused';
            if (lastFocusedElement && mockResponses[lastFocusedElement]) {
                speech = mockResponses[lastFocusedElement];
            }
            
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ speech }));
        } 
        else if (pathname === '/focus') {
            // Focus on a specific element
            if (!nvdaRunning) {
                throw new Error('Mock NVDA not running');
            }
            
            const selector = parsedUrl.query.selector;
            if (!selector) {
                throw new Error('Selector parameter required');
            }
            
            lastFocusedElement = selector;
            console.log(`Element focused: ${selector}`);
            
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'focused', selector }));
        }
        else if (pathname === '/act') {
            // Act on the current element (simulate pressing Enter)
            if (!nvdaRunning) {
                throw new Error('Mock NVDA not running');
            }
            
            console.log('Action performed on current element');
            
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'action_performed' }));
        } 
        else if (pathname === '/press') {
            // Press a key
            if (!nvdaRunning) {
                throw new Error('Mock NVDA not running');
            }
            
            const key = parsedUrl.query.key;
            if (!key) {
                throw new Error('Key parameter required');
            }
            
            console.log(`Key pressed: ${key}`);
            
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'key_pressed', key }));
        } 
        else if (pathname === '/version') {
            // Get version info
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ 
                version: 'mock-nvda-1.0.0',
                running: nvdaRunning
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
    console.log(`Mock NVDA bridge running at http://localhost:${PORT}`);
}); 