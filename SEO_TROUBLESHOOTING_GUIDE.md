# SEO Troubleshooting Guide

## Quick Diagnosis for Common SEO Issues

---

## 🔴 Critical Issues

### Issue 1: Pages Not Showing Up in Google Search Results

**Symptoms**:
- Search Console shows "Discovered but not indexed"
- Site search query returns no results
- Organic traffic is zero

**Possible Causes**:
1. ❌ robots.txt blocking crawling
2. ❌ No HTTPS (if set to HTTPS-only)
3. ❌ noindex meta tag present
4. ❌ Canonical tag pointing elsewhere
5. ❌ Too-new website (needs time)
6. ❌ Server errors (500, 503)

**Solutions**:
```bash
# 1. Check robots.txt
curl https://africawesterneducation.com/robots.txt
# Ensure it doesn't have "Disallow: /" at the top

# 2. Verify no noindex tag
curl -s https://africawesterneducation.com/ | grep -i noindex
# Should return nothing

# 3. Check canonical tag
curl -s https://africawesterneducation.com/ | grep canonical
# Should point to current URL or be absent

# 4. Check for server errors
curl -I https://africawesterneducation.com/
# Should return 200 status code
```

**Action Items**:
- [ ] Verify robots.txt allows crawling
- [ ] Remove any noindex meta tags
- [ ] Fix canonical tags if incorrect
- [ ] Ensure HTTPS is properly configured
- [ ] Check Google Search Console for specific errors
- [ ] Wait 2-4 weeks for new sites
- [ ] Manually request indexation in Search Console

---

### Issue 2: Language Switching Returns 404 Errors

**Symptoms**:
- `/sw/` returns 404
- `/ar/` returns 404
- `/fr/` returns 404
- Only `/en/` works

**Root Causes**:
1. ❌ `prefix_default_language=False` in URLs
2. ❌ Language not in LANGUAGES list
3. ❌ Locale files not compiled (.mo files missing)
4. ❌ LocaleMiddleware not in MIDDLEWARE

**Solutions**:

Step 1: Check `globalagency_project/urls.py`
```python
# Should be:
urlpatterns += i18n_patterns(
    # ... urls ...
    prefix_default_language=True,  # This MUST be True
)
```

Step 2: Check `globalagency_project/settings.py`
```python
# Must include all 4 languages:
LANGUAGES = [
    ('en', 'English'),
    ('sw', 'Swahili'),
    ('ar', 'Arabic'),
    ('fr', 'French'),
]

# Must include locale path:
LOCALE_PATHS = [BASE_DIR / 'locale']

# Must include middleware:
MIDDLEWARE = [
    # ... other middleware ...
    'django.middleware.locale.LocaleMiddleware',
    # ... other middleware ...
]
```

Step 3: Check locale files exist
```bash
# All these should exist:
locale/en/LC_MESSAGES/django.mo
locale/sw/LC_MESSAGES/django.mo
locale/ar/LC_MESSAGES/django.mo
locale/fr/LC_MESSAGES/django.mo
```

Step 4: Recompile if missing
```bash
cd c:\Users\WINDOWS 11\Documents\Projects\Global-agency
python manage.py compilemessages
# Or use the custom script: python compile_messages.py
```

**Action Checklist**:
- [ ] Verify `prefix_default_language=True` in urls.py
- [ ] Verify all 4 languages in LANGUAGES setting
- [ ] Verify LocaleMiddleware in MIDDLEWARE
- [ ] Verify LOCALE_PATHS set correctly
- [ ] Check .mo files exist in locale folders
- [ ] Restart Django development server
- [ ] Clear browser cache

---

### Issue 3: Sitemap Not Generating or Invalid

**Symptoms**:
- `/sitemap.xml` returns 404
- Sitemap XML has syntax errors
- Search Console reports invalid sitemap

**Possible Causes**:
1. ❌ Sitemap app not in INSTALLED_APPS
2. ❌ Sitemap URL not configured in urls.py
3. ❌ Database errors in sitemap generation
4. ❌ Incorrect sitemap class syntax

**Solutions**:

Step 1: Verify INSTALLED_APPS
```python
INSTALLED_APPS = [
    # ...
    'django.contrib.sitemaps',  # Must be present
    # ...
]
```

Step 2: Verify URLs
```python
# urls.py should include:
from django.contrib.sitemaps.views import sitemap
from globalagency_project.sitemap import sitemaps

urlpatterns = [
    # ...
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    # ...
]
```

Step 3: Test sitemap generation
```bash
curl https://africawesterneducation.com/sitemap.xml
# Should return valid XML

# Validate XML syntax:
curl https://africawesterneducation.com/sitemap.xml | xmllint --format -
# Should show no errors
```

Step 4: Check sitemap.py
```python
# globalagency_project/sitemap.py should define:
# - StaticPagesSitemap class
# - UniversitiesSitemap class
# - CoursesSitemap class
# - BlogSitemap class
# - sitemaps dict at end

sitemaps = {
    'static': StaticPagesSitemap,
    'universities': UniversitiesSitemap,
    'courses': CoursesSitemap,
    'blog': BlogSitemap,
}
```

**Action Checklist**:
- [ ] Add 'django.contrib.sitemaps' to INSTALLED_APPS
- [ ] Configure sitemap URL in urls.py
- [ ] Verify sitemap.py exists and is correct
- [ ] Test sitemap.xml returns valid XML
- [ ] Submit sitemap to Google Search Console
- [ ] Check Search Console for sitemap errors

---

## 🟡 Moderate Issues

### Issue 4: Core Web Vitals Failing

**Symptoms**:
- PageSpeed Insights score < 70
- Core Web Vitals showing red
- LCP > 2.5s, FID > 100ms, CLS > 0.1

**Possible Causes**:
1. ❌ Large, unoptimized images
2. ❌ Render-blocking CSS/JavaScript
3. ❌ Missing caching headers
4. ❌ No gzip compression
5. ❌ Large JavaScript bundles

**Solutions**:

For LCP (Largest Contentful Paint):
```python
# In settings.py, ensure caching is enabled:
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 300,  # 5 minutes
    }
}

# Enable gzip compression:
GZIP_LEVEL = 9
```

For CLS (Cumulative Layout Shift):
```html
<!-- In templates, set fixed dimensions -->
<img src="..." width="400" height="300" alt="...">

<!-- Load critical fonts early -->
<link rel="preload" href="font.woff2" as="font" crossorigin>
```

For FID (First Input Delay):
```html
<!-- Defer non-critical scripts -->
<script defer src="..."></script>

<!-- Use async for analytics -->
<script async src="..."></script>
```

**Action Checklist**:
- [ ] Optimize images (< 200KB each)
- [ ] Enable gzip compression
- [ ] Implement caching (5-minute timeout)
- [ ] Preload critical fonts
- [ ] Defer non-critical JavaScript
- [ ] Remove unused CSS
- [ ] Test with PageSpeed Insights

---

### Issue 5: Low Click-Through Rate (CTR) from Search Results

**Symptoms**:
- High impressions but low clicks
- CTR below 3%
- Site ranking but not getting traffic

**Possible Causes**:
1. ❌ Unattractive title tag
2. ❌ Weak meta description
3. ❌ No rich snippets
4. ❌ Competing result more attractive
5. ❌ Wrong keyword targeting

**Solutions**:

Improve Title Tags:
```html
<!-- Bad: Too generic -->
<title>Home</title>

<!-- Good: Keyword-rich, compelling -->
<title>Study Abroad Tanzania | Expert Education Consultants | Africa Western</title>
```

Improve Meta Descriptions:
```html
<!-- Bad: Too short, no CTA -->
<meta name="description" content="Education services">

<!-- Good: Descriptive, with CTA -->
<meta name="description" content="Expert guidance for studying abroad. University admissions, visa assistance, scholarships. Get started today!">
```

Add Schema Markup:
```json
{
  "@type": "Organization",
  "name": "Africa Western Education",
  "aggregateRating": {
    "ratingValue": "4.8",
    "ratingCount": "500"
  }
}
```

**Action Checklist**:
- [ ] A/B test title tags (use Search Console)
- [ ] Rewrite weak meta descriptions
- [ ] Add rich snippets (ratings, FAQ, etc.)
- [ ] Monitor CTR improvements in Search Console
- [ ] Compare with top-ranking competitors

---

### Issue 6: Duplicate Content Warnings

**Symptoms**:
- Search Console reports duplicate content
- Multiple versions of same page appear
- Canonical tag issues

**Possible Causes**:
1. ❌ Missing canonical tags
2. ❌ Both www and non-www versions
3. ❌ HTTP and HTTPS versions
4. ❌ Multiple language versions with same content
5. ❌ Trailing slash inconsistency

**Solutions**:

Add Canonical Tags:
```html
<!-- In template, set canonical for each page -->
<link rel="canonical" href="{{ request.build_absolute_uri }}">
```

Redirect Duplicate Versions:
```python
# In settings.py, for HTTPS:
SECURE_SSL_REDIRECT = True

# For www redirects (in .htaccess):
RewriteCond %{HTTP_HOST} ^www\.(.*)$ [NC]
RewriteRule ^(.*)$ https://%1/$1 [R=301,L]
```

Use hreflang for Language Versions:
```html
<link rel="alternate" hreflang="en" href="...">
<link rel="alternate" hreflang="sw" href="...">
<link rel="alternate" hreflang="x-default" href="...">
```

**Action Checklist**:
- [ ] Add canonical tags to all pages
- [ ] Set preferred domain (www or non-www)
- [ ] Redirect duplicates to preferred version
- [ ] Implement hreflang for language variants
- [ ] Check Search Console for remaining duplicates

---

## 🟢 Minor Issues

### Issue 7: Missing Structured Data

**Symptoms**:
- Schema.org validation returns warnings
- No rich snippets in SERP
- Competitors showing ratings/reviews

**Solutions**:

Verify Current Implementation:
```bash
# Check what schema is present
curl -s https://africawesterneducation.com/ | grep -A5 "schema.org"
```

Add More Schema Types:
```html
<!-- Review/Rating Schema -->
<script type="application/ld+json">
{
  "@type": "AggregateRating",
  "ratingValue": "4.8",
  "ratingCount": "500",
  "bestRating": "5",
  "worstRating": "1"
}
</script>

<!-- FAQ Schema -->
<script type="application/ld+json">
{
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "How long does the admission process take?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Typically 2-4 weeks..."
    }
  }]
}
</script>
```

**Action Checklist**:
- [ ] Validate current schema at schema.org/validate
- [ ] Add rating/review schema if available
- [ ] Add FAQ schema for help pages
- [ ] Add video schema for multimedia
- [ ] Test with Search Console rich results

---

### Issue 8: Mobile Display Issues

**Symptoms**:
- Mobile text too small
- Buttons hard to click
- Horizontal scrolling needed

**Solutions**:

Check Viewport Meta Tag:
```html
<!-- Already implemented in base.html: -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

Test Font Sizes:
```css
/* Minimum readable font size: 16px */
body { font-size: 16px; }

/* Buttons minimum 48x48 touch targets */
button { min-height: 48px; min-width: 48px; }
```

Test on Real Devices:
```bash
# Use Google Mobile-Friendly Test:
# https://search.google.com/test/mobile-friendly
```

**Action Checklist**:
- [ ] Run Mobile-Friendly Test
- [ ] Test on iPhone and Android
- [ ] Verify buttons are 48px minimum
- [ ] Check font sizes are readable
- [ ] Remove horizontal scrolling

---

### Issue 9: Meta Tags Not Updating

**Symptoms**:
- Changes to meta tags don't appear in SERP
- Old description still showing
- Google bot not re-crawling

**Solutions**:

Force Update in Search Console:
```
1. Go to Google Search Console
2. Enter page URL in search box
3. Click "Inspect URL"
4. Click "Request Indexing"
```

Clear Browser Cache:
```bash
# Hard refresh in browser: Ctrl+Shift+R (Windows)
# Or: Cmd+Shift+R (Mac)
```

Wait for Re-crawl:
- Google re-crawls updated pages within 2-7 days
- Use Search Console to speed up process

**Action Checklist**:
- [ ] Make meta tag changes
- [ ] Hard refresh browser to verify
- [ ] Submit to Search Console
- [ ] Wait 2-7 days for re-indexing
- [ ] Monitor Search Console for updates

---

## 🔧 Maintenance Checks (Do Monthly)

### 1. Broken Link Check
```bash
# Use Screaming Frog or:
python -m pytest --test-links

# Or manual check key pages:
curl -s https://africawesterneducation.com/en/ | grep href | head -20
```

### 2. Check robots.txt
```bash
curl https://africawesterneducation.com/robots.txt
# Verify syntax is correct, no typos
```

### 3. Test Core Pages
```bash
for url in "/" "/about/" "/courses/" "/contact/"; do
  curl -I https://africawesterneducation.com$url
  # Should all return 200 OK
done
```

### 4. Monitor Search Console
```
1. Log in to Search Console
2. Check Coverage report - should have 0 errors
3. Check Performance - monitor CTR trends
4. Check Mobile Usability - should be clear
```

### 5. Check Performance
```bash
curl -o /dev/null -s -w "Response time: %{time_total}s\n" \
  https://africawesterneducation.com/
# Should be < 3 seconds
```

---

## 🆘 Emergency Procedures

### If Site Disappears from Search Results

**Do Immediately** (within 1 hour):
1. [ ] Check if site is online: `curl https://africawesterneducation.com`
2. [ ] Check robots.txt: `curl https://africawesterneducation.com/robots.txt`
3. [ ] Check Search Console for manual actions
4. [ ] Review recent changes to settings.py
5. [ ] Check error logs: `/logs/` directory

**Do Within 24 Hours**:
1. [ ] Review all DNS and hosting changes
2. [ ] Verify HTTPS certificate is valid
3. [ ] Check for hacking (login attempts, file changes)
4. [ ] Review security headers are present
5. [ ] Submit site to Search Console again if needed

**Recovery**:
- Fix any issues found
- Request re-indexation in Search Console
- Monitor crawl stats
- Results should return within 1-7 days

---

## 📞 When to Seek Help

**Contact Web Developer If**:
- Django errors in logs
- Database connection issues
- Settings.py syntax errors
- URL routing problems
- Template rendering errors

**Contact SEO Specialist If**:
- Content ranking dropped
- Traffic declining
- Competitors gaining ground
- Need content strategy
- Link building needed

**Contact Server Admin If**:
- 503 Service Unavailable
- HTTPS certificate issues
- Disk space full
- Server resources maxed
- DDoS attack suspected

---

## 📚 Quick Reference Links

- [Google Search Console](https://search.google.com/search-console)
- [PageSpeed Insights](https://pagespeed.web.dev/)
- [Schema.org Validator](https://schema.org/validate/)
- [Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)
- [Google Mobile Usability](https://support.google.com/webmasters/answer/7347094)
- [Django i18n Documentation](https://docs.djangoproject.com/en/4.2/topics/i18n/)
- [Django Sitemap Framework](https://docs.djangoproject.com/en/4.2/ref/contrib/sitemaps/)

---

## Troubleshooting Decision Tree

```
Is site getting organic traffic?
├─ NO → Check robots.txt
│       ├─ Too restrictive? → Fix robots.txt
│       └─ OK → Check Search Console
│               ├─ Manual action? → Fix issue
│               ├─ Pages indexed? → Wait 2-4 weeks
│               └─ Pages not indexed → Check noindex tag

├─ YES but declining → Check for ranking drops
                       ├─ Algorithm update? → Wait & optimize
                       ├─ Duplicate content? → Add canonical
                       └─ Penalties? → Review Search Console

└─ LOW → Check meta tags
         ├─ Title/description weak → Improve copy
         ├─ Schema missing → Add structured data
         └─ Competitors stronger → Better content needed
```

---

**Remember**: Most SEO issues take 2-4 weeks to manifest and resolve. Monitor continuously and be patient!
