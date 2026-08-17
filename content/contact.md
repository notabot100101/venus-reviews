---
title: "Contact Us"
description: "Get in touch with the Venus Reviews team."
menu: "footer"
---

## Get in Touch

Have a question about a product? Need buying advice? Want to suggest a review? We'd love to hear from you.

### Send Us a Message

Fill out the form below and we'll get back to you within 24-48 hours.

<!-- FORMSPREE CONFIG: Endpoint configured 2026-08-03 -->
<!-- Format: https://formspree.io/f/XXXXXXXX -->
<form id="contact-form" class="venus-contact-form" action="https://formspree.io/f/xpqgkwaj" method="POST">
<!-- Formspree honeypot field for spam protection -->
<input type="text" name="_gotcha" style="display:none">
<!-- Redirect after submission (optional - update when endpoint is live) -->
<!-- <input type="hidden" name="_next" value="https://reviews.ultramarine963.com/contact/thank-you/"> -->
<!-- Subject prefix for Linear integration -->
<input type="hidden" name="_subject" value="[Venus Contact Form]">
<div class="form-row">
<div class="form-group">
<label for="email">Your Email <span class="required">*</span></label>
<input type="email" id="email" name="email" required placeholder="you@example.com" class="form-input">
</div>
<div class="form-group">
<label for="priority">Priority</label>
<select id="priority" name="priority" class="form-select">
<option value="low">Low - General inquiry</option>
<option value="medium" selected>Medium - Question or suggestion</option>
<option value="high">High - Issue or concern</option>
<option value="critical">Critical - Urgent problem</option>
</select>
</div>
</div>
<div class="form-group">
<label for="subject">Subject <span class="required">*</span></label>
<input type="text" id="subject" name="subject" required placeholder="What's this about?" class="form-input">
</div>
<div class="form-group">
<label for="message">Message <span class="required">*</span></label>
<textarea id="message" name="message" rows="6" required placeholder="Tell us how we can help..." class="form-textarea"></textarea>
</div>
<div class="form-actions">
<button type="submit" class="btn btn-primary form-submit">Send Message</button>
<p class="form-note"><span class="required">*</span> Required fields</p>
</div>
<div id="form-status" class="form-status" style="display: none;"></div>
</form>

### Alternative Contact

Prefer email? Use the form above — it reaches our team directly. We check messages regularly and typically respond within 24-48 hours.

### Response Time

We typically respond within 24-48 hours during business days.

### Frequently Asked Questions

**Q: Do you review products sent by manufacturers?**  
A: Yes, but our reviews remain independent. We disclose when products are provided for review.

**Q: Can I request a specific product review?**  
A: Absolutely. Use the form above and we'll consider it for our review queue.

**Q: How do I know your reviews are unbiased?**  
A: Reviews are based on documented product information, retailer policies, and published buyer feedback. Potential affiliate commissions never determine editorial conclusions — read our [Affiliate Disclosure](/affiliate-disclosure/).

---

*We respect your privacy. All communications are confidential.*

<style>
.venus-contact-form {
background: linear-gradient(135deg, rgba(107, 44, 145, 0.05) 0%, rgba(183, 110, 121, 0.05) 100%);
border: 1px solid rgba(107, 44, 145, 0.15);
border-radius: 16px;
padding: 2rem;
margin: 2rem 0;
box-shadow: 0 4px 24px rgba(107, 44, 145, 0.08);
}
.form-row {
display: grid;
grid-template-columns: 2fr 1fr;
gap: 1.5rem;
margin-bottom: 1.5rem;
}
@media (max-width: 600px) {
.form-row {
grid-template-columns: 1fr;
gap: 1rem;
}
}
.form-group {
margin-bottom: 1.5rem;
}
.form-row .form-group {
margin-bottom: 0;
}
.venus-contact-form label {
display: block;
font-family: 'Lato', sans-serif;
font-weight: 600;
font-size: 0.9375rem;
color: #2d2d2d;
margin-bottom: 0.5rem;
}
.venus-contact-form .required {
color: #B76E79;
}
.form-input,
.form-select,
.form-textarea {
width: 100%;
padding: 0.875rem 1rem;
border: 2px solid rgba(107, 44, 145, 0.15);
border-radius: 8px;
font-family: 'Lato', sans-serif;
font-size: 1rem;
color: #2d2d2d;
background: #ffffff;
transition: all 0.2s ease;
}
.form-input::placeholder,
.form-textarea::placeholder {
color: #999;
}
.form-input:focus,
.form-select:focus,
.form-textarea:focus {
outline: none;
border-color: #6B2C91;
box-shadow: 0 0 0 3px rgba(107, 44, 145, 0.1);
}
.form-select {
cursor: pointer;
appearance: none;
background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%236B2C91' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
background-repeat: no-repeat;
background-position: right 1rem center;
padding-right: 2.5rem;
}
.form-textarea {
resize: vertical;
min-height: 140px;
}
.form-actions {
display: flex;
align-items: center;
gap: 1.5rem;
flex-wrap: wrap;
}
.form-submit {
padding: 1rem 2.5rem;
font-size: 1rem;
letter-spacing: 0.03em;
}
.form-note {
font-size: 0.875rem;
color: #666;
margin: 0;
}
.form-status {
margin-top: 1.5rem;
padding: 1rem 1.25rem;
border-radius: 8px;
font-size: 0.9375rem;
}
.form-status.success {
background: rgba(76, 175, 80, 0.1);
border: 1px solid rgba(76, 175, 80, 0.3);
color: #2e7d32;
}
.form-status.error {
background: rgba(244, 67, 54, 0.1);
border: 1px solid rgba(244, 67, 54, 0.3);
color: #c62828;
}
</style>

<script>
(function() {
var form = document.getElementById('contact-form');
var status = document.getElementById('form-status');
var endpoint = form.getAttribute('action');
// Form endpoint configured: https://formspree.io/f/xpqgkwaj
// Formspree will handle submission; optional: add success/error handlers here
})();
</script>
