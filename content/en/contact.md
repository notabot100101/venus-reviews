---
title: "Contact Us"
layout: "single"
description: "Contact information and support"
---

<div class="section">
  <div class="container">
    <h1>Contact Us</h1>
    
    <p>Have questions about products, orders, or privacy? We're here to help.</p>
    
    <h2>Get in Touch</h2>
    
    <form action="mailto:{{ .Site.Params.email }}" method="post" enctype="text/plain">
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-md);">
        <input type="text" name="name" placeholder="Your Name" class="newsletter-input">
        <input type="email" name="email" placeholder="Your Email" class="newsletter-input">
      </div>
      <textarea name="message" placeholder="Your Message" rows="5" class="newsletter-input" style="width: 100%;"></textarea>
      <div style="display: flex; gap: var(--space-md);">
        <button type="submit" class="btn btn-primary">Send Message</button>
      </div>
    </form>
    
    <h2>Response Time</h2>
    <p>We typically respond within 24-48 hours during business days (Mon-Fri).</p>
    
    <h2>Support Hours</h2>
    <p>Monday - Friday: 9:00 - 18:00 CET<br>Saturday: 10:00 - 14:00 CET</p>
    
  </div>
</div>
