const http = require('http');
const https = require('https');
const url = require('url');

const SUPABASE_URL = 'https://supabase.atenza.digital';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlzcyI6InN1cGFiYXNlIiwiaWF0IjoxNzcwNDQwNTE5LCJleHAiOjIwODU4MDA1MTl9.veBBi8SHSl7Ix9znnkIlFFjfTa2l0qmLJRz1WCIjV28';

const server = http.createServer((req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  if (req.url.startsWith('/api/')) {
    const path = req.url.substring(4); // Remove /api prefix
    const supabaseUrl = `${SUPABASE_URL}${path}`;

    console.log(`Proxying request to: ${supabaseUrl}`);

    const options = {
      method: req.method,
      headers: {
        'apikey': SUPABASE_KEY,
        'Authorization': `Bearer ${SUPABASE_KEY}`,
        'Content-Type': 'application/json'
      }
    };

    const proxyReq = https.request(supabaseUrl, options, (proxyRes) => {
      res.writeHead(proxyRes.statusCode, {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      });
      proxyRes.pipe(res);
    });

    proxyReq.on('error', (error) => {
      console.error('Proxy error:', error);
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: error.message }));
    });

    if (req.method === 'POST') {
      req.pipe(proxyReq);
    } else {
      proxyReq.end();
    }
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not Found');
  }
});

const PORT = 3002;
server.listen(PORT, () => {
  console.log(`Proxy server running on port ${PORT}`);
});
