<?php
/**
 * Grid Bot Weekly signup -> Brevo double opt-in (same pattern as books.ultramarine963.com).
 *
 * Config lives OUTSIDE the webroot, never in the repo, survives git deploys:
 *   ../brevo-config-trade.php  (next to this subdomain's docroot; create in hPanel File Manager or SSH)
 * Until it exists this endpoint answers 503 and index.php keeps its placeholder text,
 * so deploying this file changes nothing user-visible on its own.
 *
 *   <?php return [
 *     'api_key'     => 'xkeysib-...',   // Brevo: SMTP & API -> API keys
 *     'list_id'     => 0,               // Contacts -> Lists -> "trading"
 *     'template_id' => 0,               // double-opt-in confirmation template id
 *     'redirect'    => 'https://trade.ultramarine963.com/?subscribed=1',
 *   ];
 *
 * Only /contacts/doubleOptinConfirmation is called: Brevo sends the confirmation mail and the
 * address joins the list after the click (Agora #53, decision D2). Nothing is stored here.
 *
 * Attribution: an optional "source" field (set server-side in index.php from utm_source /
 * utm_campaign) is forwarded as the Brevo text contact attribute SOURCE. The account must have
 * a contact attribute named SOURCE (type Text); a plain signup with no source omits it entirely.
 */
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
  http_response_code(405);
  echo json_encode(['ok' => false, 'error' => 'method']);
  exit;
}

$configPath = dirname(__DIR__) . '/brevo-config-trade.php';
if (!is_file($configPath)) {
  http_response_code(503);
  echo json_encode(['ok' => false, 'error' => 'not-configured']);
  exit;
}
$cfg = require $configPath;

$email = trim($_POST['email'] ?? '');
$honeypot = trim($_POST['website'] ?? '');   // hidden field: humans leave it empty
if ($honeypot !== '') {                      // bot: pretend success, store nothing
  echo json_encode(['ok' => true]);
  exit;
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
  http_response_code(422);
  echo json_encode(['ok' => false, 'error' => 'email']);
  exit;
}

// Arrival channel for attribution; sanitised again here in case of a direct POST.
$source = preg_replace('/[^A-Za-z0-9 ._\/-]/', '', trim($_POST['source'] ?? ''));
$source = substr($source, 0, 80);

$contact = [
  'email'          => $email,
  'includeListIds' => [(int) $cfg['list_id']],
  'templateId'     => (int) $cfg['template_id'],
  'redirectionUrl' => $cfg['redirect'],
];
if ($source !== '') {
  $contact['attributes'] = ['SOURCE' => $source];
}
$payload = json_encode($contact);

$ch = curl_init('https://api.brevo.com/v3/contacts/doubleOptinConfirmation');
curl_setopt_array($ch, [
  CURLOPT_POST           => true,
  CURLOPT_POSTFIELDS     => $payload,
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_TIMEOUT        => 10,
  CURLOPT_HTTPHEADER     => [
    'accept: application/json',
    'content-type: application/json',
    'api-key: ' . $cfg['api_key'],
  ],
]);
curl_exec($ch);
$status = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
curl_close($ch);

// Brevo answers 201 (created) or 204 (already pending/subscribed) on success.
if ($status === 201 || $status === 204) {
  echo json_encode(['ok' => true]);
} else {
  http_response_code(502);
  echo json_encode(['ok' => false, 'error' => 'upstream']);
}
