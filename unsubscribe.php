<?php
/**
 * Grid Bot Weekly — one-click unsubscribe.
 *
 * Linked from the footer of every email (and advertised via the List-Unsubscribe /
 * List-Unsubscribe-Post headers, so Gmail/Outlook show a native unsubscribe button).
 * The link is HMAC-signed over the email alone, so it never expires.
 *
 * GET  -> unsubscribe + show a confirmation page.
 * POST -> RFC 8058 one-click (mailbox provider posts "List-Unsubscribe=One-Click"); 200, no body.
 *
 * Unsubscribing sets emailBlacklisted=true in Brevo (global suppression) and unlinks the
 * address from the list, so campaigns and transactional mail both stop. Idempotent.
 */
$configPath = dirname(__DIR__) . '/brevo-config-trade.php';

$isPost = (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST');

function u_page(string $title, string $body, int $code = 200): void {
  http_response_code($code);
  header('Content-Type: text/html; charset=utf-8');
  echo '<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
     . '<title>' . htmlspecialchars($title, ENT_QUOTES, 'UTF-8') . '</title>'
     . '<style>body{font-family:Arial,Helvetica,sans-serif;max-width:560px;margin:12vh auto;padding:0 20px;color:#222;line-height:1.6}'
     . 'a{color:#111}.muted{color:#666;font-size:14px}</style></head><body>' . $body
     . '<p class="muted">&copy; 2026 Paul Budzisch – aiffiliation. <a href="/">trade.ultramarine963.com</a></p></body></html>';
  exit;
}

if (!is_file($configPath)) {
  if ($isPost) { http_response_code(503); exit; }
  u_page('Nicht verfügbar', '<h1>Momentan nicht verfügbar</h1><p>Bitte versuchen Sie es später erneut.</p>', 503);
}
$cfg = require $configPath;

$email = strtolower(trim($_GET['e'] ?? ''));
$mac   = (string) ($_GET['k'] ?? '');

$fail = static function (bool $isPost): void {
  if ($isPost) { http_response_code(400); exit; }
  u_page('Link ungültig',
    '<h1>Link ungültig</h1>'
  . '<p>Dieser Abmeldelink ist ung&uuml;ltig. Sie k&ouml;nnen sich jederzeit abmelden, indem Sie eine kurze E-Mail an '
  . '<a href="mailto:info@aiffiliation.de?subject=Abmelden">info@aiffiliation.de</a> schreiben.</p>'
  . '<p class="muted"><em>English:</em> This unsubscribe link is invalid. You can unsubscribe any time by emailing us.</p>', 400);
};

if ($email === '' || $mac === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
  $fail($isPost);
}
$expect = hash_hmac('sha256', $email, (string) $cfg['hmac_secret']);
if (!hash_equals($expect, $mac)) {
  $fail($isPost);
}

// Suppress globally + remove from the list.
$payload = json_encode(['emailBlacklisted' => true, 'unlinkListIds' => [(int) $cfg['list_id']]]);
$ch = curl_init('https://api.brevo.com/v3/contacts/' . rawurlencode($email));
curl_setopt_array($ch, [
  CURLOPT_CUSTOMREQUEST  => 'PUT',
  CURLOPT_POSTFIELDS     => $payload,
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_TIMEOUT        => 12,
  CURLOPT_HTTPHEADER     => [
    'accept: application/json',
    'content-type: application/json',
    'api-key: ' . $cfg['api_key'],
  ],
]);
curl_exec($ch);
$status = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
curl_close($ch);

// 204 = updated; 404 = contact unknown (already gone / never confirmed) — both mean "not subscribed".
$ok = ($status === 204 || $status === 404);

if ($isPost) {
  http_response_code($ok ? 200 : 502);
  exit;
}
if ($ok) {
  u_page('Abgemeldet',
    '<h1>Sie sind abgemeldet</h1>'
  . '<p>Ihre E-Mail-Adresse wurde aus dem Verteiler &bdquo;Grid Bot Weekly&ldquo; entfernt. Sie erhalten keine weiteren E-Mails.</p>'
  . '<p class="muted"><em>English:</em> You have been unsubscribed from Grid Bot Weekly and will receive no further emails. '
  . 'Changed your mind? You can <a href="/#newsletter">sign up again</a> any time.</p>');
}
u_page('Fehler',
  '<h1>Das hat gerade nicht geklappt</h1>'
. '<p>Bitte versuchen Sie es in einem Moment erneut, oder schreiben Sie an '
. '<a href="mailto:info@aiffiliation.de?subject=Abmelden">info@aiffiliation.de</a> &ndash; wir melden Sie dann ab.</p>'
. '<p class="muted"><em>English:</em> That did not work just now. Please try again shortly or email us to be removed.</p>', 502);
