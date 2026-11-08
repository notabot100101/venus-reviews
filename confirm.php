<?php
/**
 * Grid Bot Weekly — double opt-in confirmation landing (pairs with subscribe.php).
 *
 * The recipient clicks the signed link from the confirmation email. We verify the HMAC and the
 * 7-day window, then add the address to the Brevo "trading" list with a consent record
 * (signup + confirmation timestamp and IP). Only here does anything get stored. On success we
 * redirect to the site's ?subscribed=1 thank-you.
 */
$configPath = dirname(__DIR__) . '/brevo-config-trade.php';

function page(string $title, string $body, int $code = 200): void {
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
  page('Nicht verfügbar', '<h1>Momentan nicht verfügbar</h1><p>Bitte versuchen Sie es später erneut.</p>', 503);
}
$cfg = require $configPath;

$email  = strtolower(trim($_GET['e'] ?? ''));
$source = (string) ($_GET['s'] ?? '');
$issued = (string) ($_GET['t'] ?? '');
$sigIp  = (string) ($_GET['i'] ?? '');
$mac    = (string) ($_GET['k'] ?? '');

$bad = static function () {
  page('Link ungültig',
    '<h1>Link ungültig oder abgelaufen</h1>'
  . '<p>Dieser Bestätigungslink ist nicht mehr gültig (max. 7 Tage). Bitte melden Sie sich erneut an.</p>'
  . '<p class="muted"><em>English:</em> This confirmation link is invalid or has expired (max. 7 days). Please sign up again.</p>'
  . '<p><a href="/#newsletter">&rarr; Zur Anmeldung / Back to signup</a></p>', 400);
};

if ($email === '' || $issued === '' || $mac === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
  $bad();
}
if (!preg_match('/^\d+$/', $issued)) {
  $bad();
}
$issuedTs = (int) $issued;
$now = time();
if ($issuedTs > $now + 300 || $issuedTs < $now - 604800) { // 7 days, small forward skew
  $bad();
}
$expect = hash_hmac('sha256', implode("\n", [$email, $source, $issued, $sigIp]), (string) $cfg['hmac_secret']);
if (!hash_equals($expect, $mac)) {
  $bad();
}

// Valid click -> add to the list with a consent record.
$confirmIp = substr(preg_replace('/[^0-9a-fA-F:.]/', '', $_SERVER['REMOTE_ADDR'] ?? ''), 0, 45);
$consent = sprintf('signup %s %s; confirm %s %s',
  gmdate('c', $issuedTs), ($sigIp !== '' ? $sigIp : '-'),
  gmdate('c', $now), ($confirmIp !== '' ? $confirmIp : '-'));

$attributes = ['CONSENT' => $consent];
$source = preg_replace('/[^A-Za-z0-9 ._\/-]/', '', $source);
if ($source !== '') {
  $attributes['SOURCE'] = substr($source, 0, 80);
}

$payload = json_encode([
  'email'         => $email,
  'listIds'       => [(int) $cfg['list_id']],
  'updateEnabled' => true,
  'attributes'    => $attributes,
]);

$ch = curl_init('https://api.brevo.com/v3/contacts');
curl_setopt_array($ch, [
  CURLOPT_POST           => true,
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

if ($status === 201 || $status === 204) {
  header('Location: ' . $cfg['redirect'], true, 302);
  exit;
}
page('Fehler',
  '<h1>Das hat gerade nicht geklappt</h1>'
. '<p>Bitte versuchen Sie es in einem Moment erneut, oder schreiben Sie an '
. '<a href="mailto:info@aiffiliation.de">info@aiffiliation.de</a>.</p>'
. '<p class="muted"><em>English:</em> That did not work just now. Please try again shortly or email us.</p>', 502);
