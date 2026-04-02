<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Access-Control-Expose-Headers: X-Transcript-User, X-Transcript-Bot, X-Language, X-Session-Id');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(200); exit; }

$BACKEND = 'http://81.17.140.198:8085';
$path = isset($_GET['path']) ? $_GET['path'] : '';
$path = preg_replace('/[^a-zA-Z0-9\/\-_]/', '', $path);
$allowed = ['api/chat', 'api/chat/stream', 'health', 'api/stats', 'api/voice', 'api/voice/status', 'api/escalate'];
if (!in_array($path, $allowed)) { echo json_encode(['error'=>'Not found']); http_response_code(404); exit; }
$url = $BACKEND . '/' . $path;

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $r = @file_get_contents($url);
    echo $r === false ? json_encode(['error'=>'Backend unavailable']) : $r;
    if ($r === false) http_response_code(502);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if ($path === 'api/voice') {
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true, CURLOPT_POST => true,
            CURLOPT_HEADER => true, CURLOPT_TIMEOUT => 60,
        ]);
        $post = [];
        if (isset($_FILES['audio'])) {
            $post['audio'] = new CURLFile($_FILES['audio']['tmp_name'],
                $_FILES['audio']['type'] ?: 'audio/webm',
                $_FILES['audio']['name'] ?: 'audio.webm');
        }
        if (isset($_POST['session_id'])) $post['session_id'] = $_POST['session_id'];
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post);
        $response = curl_exec($ch);
        $hdr_size = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
        $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        if ($response === false) {
            header('Content-Type: application/json');
            echo json_encode(['error'=>'Backend unavailable']); http_response_code(502); exit;
        }
        $hdrs = substr($response, 0, $hdr_size);
        $body = substr($response, $hdr_size);
        foreach (['X-Transcript-User','X-Transcript-Bot','X-Language','X-Session-Id'] as $h) {
            if (preg_match('/'.$h.': (.+)\r?\n/i', $hdrs, $m)) header($h.': '.trim($m[1]));
        }
        header($code >= 400 ? 'Content-Type: application/json' : 'Content-Type: audio/mpeg');
        http_response_code($code); echo $body; exit;
    }

    $input = file_get_contents('php://input');
    $opts = ['http'=>['method'=>'POST','header'=>"Content-Type: application/json\r\n",'content'=>$input,'timeout'=>30]];
    $ctx = stream_context_create($opts);

    if ($path === 'api/chat/stream') {
        header('Content-Type: text/event-stream'); header('Cache-Control: no-cache');
        $fp = @fopen($url, 'r', false, $ctx);
        if ($fp) { while (!feof($fp)) { echo fgets($fp, 4096); flush(); } fclose($fp); }
        else echo "data: ".json_encode(['error'=>'Backend unavailable'])."\n\n";
        exit;
    }

    $r = @file_get_contents($url, false, $ctx);
    if ($r === false) {
        echo json_encode(['error'=>'Backend unavailable','answer'=>'Contact @goippro_support']);
        http_response_code(502);
    } else echo $r;
}
