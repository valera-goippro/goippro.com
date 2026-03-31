<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS, PATCH');
header('Access-Control-Allow-Headers: Content-Type, Authorization, Accept, X-Requested-With');
header('Access-Control-Max-Age: 86400');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }

$backend = 'http://81.17.140.194';

$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$prefix = '/api';
$path = $uri;
if (strpos($uri, $prefix) === 0) {
    $path = $uri;
}

if (empty($path) || $path === '/' || $path === '/api' || $path === '/api/') {
    echo json_encode(['status' => 'GoIPPro API OK']);
    exit;
}

$targetUrl = $backend . $path;
$qs = $_SERVER['QUERY_STRING'] ?? '';
if (!empty($qs)) $targetUrl .= '?' . $qs;

$ch = curl_init($targetUrl);
$headers = [];
foreach (getallheaders() as $k => $v) {
    $kl = strtolower($k);
    if ($kl === 'host' || $kl === 'connection') continue;
    $headers[] = "$k: $v";
}

curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_HTTPHEADER => $headers,
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_TIMEOUT => 30,
    CURLOPT_CUSTOMREQUEST => $_SERVER['REQUEST_METHOD'],
]);

if ($_SERVER['REQUEST_METHOD'] !== 'GET' && $_SERVER['REQUEST_METHOD'] !== 'HEAD') {
    $input = file_get_contents('php://input');
    if ($input) {
        curl_setopt($ch, CURLOPT_POSTFIELDS, $input);
    }
}

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$contentType = curl_getinfo($ch, CURLINFO_CONTENT_TYPE);
curl_close($ch);

http_response_code($httpCode);
if ($contentType) header('Content-Type: ' . $contentType);
echo $response;
