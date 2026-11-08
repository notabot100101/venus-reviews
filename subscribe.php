<?php
/**
 * Grid Bot Weekly signup -> self-managed double opt-in via Brevo transactional email.
 *
 * Why self-managed: Brevo's /contacts/doubleOptinConfirmation requires a DOI template that only
 * the Brevo dashboard can create (isDoubleOptIn flag is UI-only); that step blocked go-live for
 * weeks. This endpoint instead sends the confirmation mail itself (Brevo transactional /smtp/email)
 * and NOTHING is stored or added to any list until the recipient clicks the signed link, which
 * confirm.php verifies. Same compliant double-opt-in outcome, no Brevo-UI dependency.
 *
 * Config lives OUTSIDE the webroot, never in the repo, survives git deploys:
 *   ../brevo-config-trade.php  (next to this subdomain's docroot; create via SSH / hPanel)
 * Until it exists this endpoint answers 503 and index.php keeps its placeholder text.
 *
 *   <?php return [
 *     'api_key'     => 'xkeysib-...',                                  // Brevo: SMTP & API -> API keys
 *     'list_id'     => 4,                                             // Contacts -> Lists -> "trading"
 *     'hmac_secret' => '<64+ hex chars, random, secret>',            // signs the confirm link
 *     'confirm_url' => 'https://trade.ultramarine963.com/confirm.php',
 *     'redirect'    => 'https://trade.ultramarine963.com/?subscribed=1',
 *   ];
 *
 * Attribution: an optional "source" field (set in index.php from utm_source / utm_campaign) rides
 * the signed token and becomes the Brevo text attribute SOURCE on confirmation.
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
if ($honeypot !== '') {                      // bot: pretend success, store/send nothing
  echo json_encode(['ok' => true]);
  exit;
}
$email = strtolower($email);
if (!filter_var($email, FILTER_VALIDATE_EMAIL) || strlen($email) > 254) {
  http_response_code(422);
  echo json_encode(['ok' => false, 'error' => 'email']);
  exit;
}

// Arrival channel for attribution; sanitised again here in case of a direct POST.
$source = preg_replace('/[^A-Za-z0-9 ._\/-]/', '', trim($_POST['source'] ?? ''));
$source = substr($source, 0, 80);

// --- signed, stateless confirmation token: HMAC over email|source|issued_ts|signup_ip ---
$issued = time();
$signupIp = substr(preg_replace('/[^0-9a-fA-F:.]/', '', $_SERVER['REMOTE_ADDR'] ?? ''), 0, 45);
$mac = hash_hmac('sha256', implode("\n", [$email, $source, (string) $issued, $signupIp]), (string) $cfg['hmac_secret']);
$q = http_build_query([
  'e' => $email,
  's' => $source,
  't' => $issued,
  'i' => $signupIp,
  'k' => $mac,
]);
$confirmUrl = rtrim($cfg['confirm_url'], '?') . '?' . $q;

// --- confirmation email (Lex-approved DE+EN wording, verified Brevo entity, 7-day window) ---
$esc = fn($s) => htmlspecialchars($s, ENT_QUOTES, 'UTF-8');
$link = $esc($confirmUrl);
$html = '<!doctype html><html><body style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#222;line-height:1.55">'
  . '<p>Hallo,</p>'
  . '<p>Sie haben sich f&uuml;r den Newsletter &bdquo;Grid Bot Weekly&ldquo; angemeldet. Bitte best&auml;tigen Sie Ihre Anmeldung mit einem Klick:</p>'
  . '<p><a href="' . $link . '" style="background:#111;color:#fff;padding:11px 20px;border-radius:6px;text-decoration:none;display:inline-block">Anmeldung best&auml;tigen</a></p>'
  . '<p style="font-size:12px;color:#666">Falls der Button nicht funktioniert: ' . $link . '</p>'
  . '<p>Wenn Sie diese Anmeldung nicht selbst vorgenommen haben, k&ouml;nnen Sie diese E-Mail ignorieren &ndash; ohne Best&auml;tigung werden Sie nicht in den Verteiler aufgenommen und es werden keine Daten gespeichert.</p>'
  . '<ul style="font-size:13px;color:#444">'
  . '<li>Nach Ihrer Best&auml;tigung speichern wir Ihre E-Mail-Adresse sowie Zeitpunkt und IP-Adresse von Anmeldung und Best&auml;tigung als Nachweis Ihrer Einwilligung (Art. 6 Abs. 1 lit. a, Art. 7 Abs. 1 DSGVO).</li>'
  . '<li>Der Versand erfolgt &uuml;ber den Dienst Brevo (Brevo GmbH, K&ouml;penicker Str. 126, 10179 Berlin, Deutschland).</li>'
  . '<li>Sie k&ouml;nnen Ihre Einwilligung jederzeit &uuml;ber den Abmeldelink in jeder E-Mail oder per E-Mail an info@aiffiliation.de widerrufen.</li>'
  . '</ul>'
  . '<p style="font-size:12px;color:#666">Bitte best&auml;tigen Sie innerhalb von 7 Tagen. Verantwortlicher: Paul Budzisch, Papierm&uuml;hlenweg 3, 07973 Greiz, Deutschland (info@aiffiliation.de).</p>'
  . '<hr style="border:none;border-top:1px solid #eee;margin:18px 0">'
  . '<p style="font-size:13px;color:#444"><em>English:</em> You subscribed to the &ldquo;Grid Bot Weekly&rdquo; newsletter. Please confirm via the button above. If this was not you, ignore this email &ndash; without confirmation you are not added to the list and no data is stored. Legal basis: your consent (Art. 6(1)(a) GDPR); sent via Brevo (Brevo GmbH, Berlin). Withdraw anytime via the unsubscribe link or info@aiffiliation.de. Please confirm within 7 days.</p>'
  . '</body></html>';

$payload = json_encode([
  'sender'      => ['name' => 'aiffiliation', 'email' => 'info@aiffiliation.de'],
  'to'          => [['email' => $email]],
  'subject'     => 'Bitte bestätigen Sie Ihre Newsletter-Anmeldung / Please confirm your subscription',
  'htmlContent' => $html,
  'tags'        => ['grid-bot-weekly-doi'],
]);

$ch = curl_init('https://api.brevo.com/v3/smtp/email');
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

if ($status === 201 || $status === 202) {
  echo json_encode(['ok' => true]);
} else {
  http_response_code(502);
  echo json_encode(['ok' => false, 'error' => 'upstream']);
}
