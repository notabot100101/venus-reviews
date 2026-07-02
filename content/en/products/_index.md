---
title: "All Product Reviews"
description: "Browse all our product reviews organized by category, brand, and rating."
---

<div class="product-filter">
    <h2>Product Reviews</h2>
    <div class="filter-buttons">
        <a href="/products/" class="filter-btn active">All Reviews</a>
        <a href="/products/?category=toys" class="filter-btn">Toys</a>
        <a href="/products/?category=lingerie" class="filter-btn">Lingerie</a>
        <a href="/products/?category=wellness" class="filter-btn">Wellness</a>
    </div>
</div>

<div class="reviews-list">
    {{ range .Pages }}
    <article class="review-card">
        <h3><a href="{{ .RelPermalink }}">{{ .Title }}</a></h3>
        {{ if .Params.image }}
        <img src="{{ .Params.image | relURL }}" alt="{{ .Title }}">
        {{ end }}
        <div class="rating">
            {{ range $i, $r := .Params.rating }}
            <span class="star {{ if lt $i $r }}★{{ else }}☆{{ end }}"></span>
            {{ end }}
        </div>
        <p>{{ .Params.summary | plainify }}</p>
        <a href="{{ .RelPermalink }}" class="btn-review">Read Full Review</a>
    </article>
    {{ end }}
</div>