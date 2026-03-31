<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS, PATCH');
header('Access-Control-Allow-Headers: Content-Type, Authorization, Accept, X-Requested-With');
header('Access-Control-Max-Age: 86400');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }

$backend = 'http://81.17.140.194';

// Get the forwarded path
$path = '';
if (isset($_GET['path']) && $_GET['path'] !== '') {
    $path = '/' . ltrim($_GET['path'], '/');
} else {
    $uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
    $prefix = '/api-proxy';
    if (strpos($uri, $prefix) === 0) {
        $path = substr($uri, strlen($prefix));
    }
}

if (empty($path) || $path === '/') {
    echo json_encode(['status' => 'GoIPPro API Proxy OK']);
    exit;
}

$targetUrl = $backend . $path;

$qs = $_GET; unset($qs['path']);
if (!empty($qs)) $targetUrl .= '?' . http_build_query($qs);

$ch = curl_init($targetUrl);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_TIMEOUT => 30,
    CURLOPT_CUSTOMREQUEST => $_SERVER['REQUEST_METHOD'],
]);

if (in_array($_SERVER['REQUEST_METHOD'], ['POST','PUT','PATCH'])) {
    curl_setopt($ch, CURLOPT_POSTFIELDS, file_get_contents('php://input'));
}

$h = ['Accept: application/json', 'Content-Type: application/json'];
$auth = $_SERVER['HTTP_AUTHORIZATION'] ?? $_SERVER['REDIRECT_HTTP_AUTHORIZATION'] ?? '';
if (!$auth && function_exists('apache_request_headers')) {
    $ah = apache_request_headers();
    $auth = $ah['Authorization'] ?? '';
}
if ($auth) $h[] = 'Authorization: ' . $auth;
curl_setopt($ch, CURLOPT_HTTPHEADER, $h);

$ct = 'application/json';
curl_setopt($ch, CURLOPT_HEADERFUNCTION, function($c, $line) use (&$ct) {
    if (stripos($line, 'content-type:') === 0) $ct = trim(explode(':', $line, 2)[1]);
    return strlen($line);
});

$resp = curl_exec($ch);
$code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$err = curl_error($ch);
curl_close($ch);

if ($err) { http_response_code(502); echo json_encode(['error' => $err]); exit; }

http_response_code($code);
header('Content-Type: ' . $ct);
echo $resp;
