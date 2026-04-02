<?php
/**
 * GoIPPro Chat Support API Proxy
 * Routes chat requests from HTTPS site to HTTP backend on VPS
 */
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

$BACKEND = 'http://81.17.140.198:8085';

$path = isset($_GET['path']) ? $_GET['path'] : '';
$path = preg_replace('/[^a-zA-Z0-9\/\-_]/', '', $path);

$allowed = ['api/chat', 'api/chat/stream', 'health', 'api/stats'];
if (!in_array($path, $allowed)) {
    echo json_encode(['error' => 'Not found']);
    http_response_code(404);
    exit;
}

$url = $BACKEND . '/' . $path;

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $response = file_get_contents($url);
    echo $response;
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = file_get_contents('php://input');
    
    $opts = [
        'http' => [
            'method' => 'POST',
            'header' => "Content-Type: application/json\r\n",
            'content' => $input,
            'timeout' => 30,
        ]
    ];
    $context = stream_context_create($opts);
    
    // For streaming endpoint, we need special handling
    if ($path === 'api/chat/stream') {
        header('Content-Type: text/event-stream');
        header('Cache-Control: no-cache');
        header('Connection: keep-alive');
        
        $fp = fopen($url, 'r', false, $context);
        if ($fp) {
            while (!feof($fp)) {
                $line = fgets($fp, 4096);
                echo $line;
                flush();
            }
            fclose($fp);
        } else {
            echo "data: " . json_encode(['error' => 'Backend unavailable']) . "\n\n";
        }
        exit;
    }
    
    $response = @file_get_contents($url, false, $context);
    if ($response === false) {
        echo json_encode(['error' => 'Backend unavailable', 'answer' => 'Support is temporarily unavailable. Please contact us on Telegram: @goippro_support']);
        http_response_code(502);
    } else {
        echo $response;
    }
}
