# SEO Testing & Core Web Vitals Verification Guide

## Quick Start - SEO Testing Checklist

### 1. On-Page SEO Testing

#### Meta Tags Verification
```bash
# Test if meta tags are present in page source
curl -s https://africawesterneducation.com/en/ | grep -i "meta name"

# Check for:
✓ Meta charset (UTF-8)
✓ Meta viewport (responsive)
✓ Meta description (160 chars)
✓ Title tag (60 chars)
✓ Language attributes (lang="en")
```

#### Structured Data Validation
Visit: https://schema.org/validate/
- Upload sitemap.xml and check schema validation
- Verify Organization, LocalBusiness, EducationalOrganization schemas
- Validate breadcrumb schema implementation

#### Open Graph Testing
Use: https://www.opengraph.xyz/
- Paste: `https://africawesterneducation.com/en/`
- Verify: og:title, og:description, og:image
- Test on Facebook: https://developers.facebook.com/tools/debug/

#### Twitter Card Testing
Use: https://cards-dev.twitter.com/validator
- Paste: `https://africawesterneducation.com/en/`
- Verify: twitter:card, twitter:title, twitter:description, twitter:image

### 2. Technical SEO Testing

#### robots.txt Verification
```bash
# Check robots.txt file
curl https://africawesterneducation.com/robots.txt

# Verify:
✓ No syntax errors
✓ All sitemaps listed
✓ Proper disallow rules
✓ Crawl-delay settings
```

#### Sitemap Testing
```bash
# Check main sitemap
curl https://africawesterneducation.com/sitemap.xml

# Check language-specific sitemaps
curl https://africawesterneducation.com/en/sitemap.xml
curl https://africawesterneducation.com/sw/sitemap.xml
curl https://africawesterneducation.com/ar/sitemap.xml
curl https://africawesterneducation.com/fr/sitemap.xml

# Verify:
✓ Valid XML format
✓ All pages listed
✓ Proper change frequencies
✓ Priority values set correctly
✓ Last modified dates included
```

#### hreflang Implementation Test
```bash
# Check hreflang tags in page source
curl -s https://africawesterneducation.com/en/ | grep -i "hreflang"

# Verify:
✓ hreflang="en" present
✓ hreflang="sw" present
✓ hreflang="ar" present
✓ hreflang="fr" present
✓ hreflang="x-default" present
```

#### Mobile Friendliness Test
Use: https://search.google.com/test/mobile-friendly
- Paste: `https://africawesterneducation.com/en/`
- Verify:
  - ✓ Mobile friendly status
  - ✓ Viewport meta tag
  - ✓ Font readability
  - ✓ Touch element sizing

### 3. Performance Testing (Core Web Vitals)

#### PageSpeed Insights (Google's Official Tool)
Link: https://pagespeed.web.dev/

**Test All Pages**:
1. Homepage: `/en/`
2. Courses: `/en/courses/`
3. About: `/en/about/`
4. Contact: `/en/contact/`
5. Swahili: `/sw/`
6. Arabic: `/ar/`
7. French: `/fr/`

**Metrics to Check**:
- **Largest Contentful Paint (LCP)**: < 2.5s (Good)
- **First Input Delay (FID)**: < 100ms (Good)
- **Cumulative Layout Shift (CLS)**: < 0.1 (Good)
- **First Contentful Paint (FCP)**: < 1.8s (Good)
- **Time to First Byte (TTFB)**: < 600ms (Good)

#### Lighthouse Audit
Built into PageSpeed Insights, reports on:
- Performance (90+)
- Accessibility (90+)
- Best Practices (90+)
- SEO (90+)

#### GTmetrix Performance Test
Link: https://gtmetrix.com/

**Key Metrics**:
- Page Load Time: Target < 2 seconds
- Total Page Size: Target < 3MB
- Requests: Target < 50 requests
- Grade: Target A or B

#### WebPageTest (Advanced)
Link: https://www.webpagetest.org/

**Settings**:
- Browser: Chrome
- Location: Frankfurt, Germany (or nearest to Africa)
- Connection: Cable
- Number of tests: 3

**Analyze**:
- Waterfall chart for resource loading
- Filmstrip showing page render
- Key metrics: First Paint, Start Render, Document Complete

### 4. Indexation & Crawlability Testing

#### Google Search Console
1. Go to: https://search.google.com/search-console
2. Add property: https://africawesterneducation.com
3. Verify ownership via meta tag, file upload, or DNS

**Check**:
- Coverage (indexed vs not indexed)
- Indexation status by language
- URL inspection (individual page crawl)
- Sitemap submission status
- Mobile usability

#### Bing Webmaster Tools
Link: https://www.bing.com/webmasters

**Features**:
- URL submission
- Sitemap status
- Keywords analysis
- Backlinks tracking

#### SEO Site Audit Tool
Use: https://www.seoseotools.com/website-crawler/ or Screaming Frog

**Crawl website and check**:
- Total pages crawled
- Meta tags completeness
- Duplicate content issues
- Broken links
- Page titles and descriptions
- Header structure (H1-H6 hierarchy)
- Images with/without alt text

### 5. Keyword Ranking Monitoring

#### Google Search Console (Free)
- Monitor keyword impressions
- Track average position
- Analyze click-through rate
- Identify low-hanging fruit keywords

#### SE Ranking (Paid Trial)
Link: https://seranking.com/
- Add domain and track 5 keywords free
- Monitor position changes daily
- Competitor keyword analysis

#### Ahrefs (Paid)
Link: https://ahrefs.com/
- Organic keywords tracking
- Keyword difficulty analysis
- Competitor keyword stealing
- Backlink analysis

**Target Keywords to Monitor**:
1. "study abroad Tanzania"
2. "international education"
3. "university admission consultant"
4. "scholarship assistance"
5. "visa processing help"
6. "study in USA"
7. "IELTS preparation"
8. "British universities"
9. "undergraduate programs"
10. "postgraduate degree"

### 6. Multilingual SEO Testing

#### Language Detection Test
```bash
# Test English
curl -H "Accept-Language: en-US" https://africawesterneducation.com/

# Test Swahili
curl -H "Accept-Language: sw-TZ" https://africawesterneducation.com/

# Test Arabic
curl -H "Accept-Language: ar-EG" https://africawesterneducation.com/

# Test French
curl -H "Accept-Language: fr-FR" https://africawesterneducation.com/

# Verify:
✓ Correct language version serves
✓ Proper charset (UTF-8)
✓ Correct dir attribute for Arabic (dir="rtl")
```

#### Translation Completeness Check
- [ ] All meta descriptions translated
- [ ] All page titles translated
- [ ] All navigation text translated
- [ ] All content sections translated
- [ ] All CTAs translated
- [ ] All form labels translated
- [ ] All error messages translated

#### RTL Language Testing (Arabic)
- [ ] Text aligns right-to-left
- [ ] Navigation flows right-to-left
- [ ] Form inputs display correctly
- [ ] Images don't conflict with RTL layout
- [ ] No left/right margin conflicts

### 7. Link Analysis

#### Backlink Auditing
Use: https://ahrefs.com/ or https://moz.com/link-explorer

**Analyze**:
- Total backlinks
- Referring domains
- Link quality (DA, PA scores)
- Anchor text distribution
- Lost vs new links

#### Internal Link Structure
**Check**: 
- Home links to all main pages
- Main pages link back to home
- Relevant content links to related content
- No excessive linking (100+ internal links per page)
- Anchor text is descriptive

#### External Links
**Best Practices**:
- Limit external links to high-authority sites
- Use rel="noopener noreferrer" for external links
- Prefer sites in education, news, business sectors

### 8. Security & HTTPS Testing

#### SSL Certificate Validation
Use: https://www.ssllabs.com/ssltest/

**Check**:
- Valid SSL certificate
- Grade A or A+ rating
- No security warnings
- Certificate renewal date

#### Security Headers Test
Use: https://securityheaders.com/

**Verify**:
- [ ] X-Frame-Options set
- [ ] X-Content-Type-Options set
- [ ] Content-Security-Policy set
- [ ] X-XSS-Protection set
- [ ] Referrer-Policy set
- [ ] HSTS enabled (in production)

### 9. Accessibility Testing (Bonus SEO)

#### WAVE Web Accessibility Evaluation
Link: https://wave.webaim.org/

**Check**:
- Contrast ratio (WCAG AA or AAA)
- Alt text for images
- Form label associations
- Heading hierarchy
- Keyboard navigation

#### Axe DevTools Browser Extension
- Install from Chrome Web Store
- Run scan on each page
- Check for violations and best practices

### 10. Monthly SEO Audit Checklist

```markdown
## Monthly SEO Audit

### Week 1: Indexation & Crawlability
- [ ] Google Search Console - check coverage
- [ ] Submit any new sitemaps
- [ ] Check for indexation errors
- [ ] Verify no manual penalties

### Week 2: Ranking & Keywords
- [ ] Check keyword rankings in GSC
- [ ] Monitor position changes
- [ ] Identify new ranking keywords
- [ ] Identify lost rankings

### Week 3: Performance & Technical
- [ ] Run PageSpeed Insights audit
- [ ] Check Core Web Vitals scores
- [ ] Test mobile friendliness
- [ ] Verify SSL certificate status

### Week 4: Content & Engagement
- [ ] Analyze top-performing pages
- [ ] Check bounce rate trends
- [ ] Review user engagement metrics
- [ ] Identify optimization opportunities

### Month-End Report
- [ ] Traffic trends (organic vs other)
- [ ] Conversion rate analysis
- [ ] ROI calculation
- [ ] Recommendations for next month
```

## Quick Testing Commands

```bash
# Check meta charset
curl -I https://africawesterneducation.com/en/ | grep -i charset

# Check gzip compression
curl -I -H "Accept-Encoding: gzip" https://africawesterneducation.com/en/

# Check response time
curl -o /dev/null -s -w "Time: %{time_total}s\n" https://africawesterneducation.com/en/

# Check headers
curl -I https://africawesterneducation.com/en/

# Validate sitemap
curl https://africawesterneducation.com/sitemap.xml | xmllint --format -

# Check robots.txt syntax
curl https://africawesterneducation.com/robots.txt
```

## Tools Summary Table

| Tool | Type | Cost | Purpose |
|------|------|------|---------|
| Google Search Console | Official | Free | Indexation, keywords, coverage |
| PageSpeed Insights | Official | Free | Core Web Vitals, performance |
| Google Mobile-Friendly | Official | Free | Mobile optimization check |
| Lighthouse | Official | Free | Audit (built into DevTools) |
| Bing Webmaster Tools | Official | Free | Alternative indexation tracking |
| GTmetrix | Third-party | Free | Performance waterfall analysis |
| WebPageTest | Third-party | Free | Advanced performance testing |
| Screaming Frog | Third-party | Paid | Website crawling & audits |
| SEMrush | Third-party | Paid | Keyword research & tracking |
| Ahrefs | Third-party | Paid | Backlink analysis & keywords |
| SE Ranking | Third-party | Paid/Free | Position tracking, audits |
| Moz | Third-party | Paid | Link analysis, keyword research |

## Next Steps

1. **Immediate** (This week):
   - Set up Google Search Console
   - Run PageSpeed Insights
   - Check robots.txt and sitemap

2. **Short-term** (This month):
   - Implement Google Analytics 4
   - Set up ranking tracking
   - Begin content optimization

3. **Long-term** (Next 3 months):
   - Build backlink profile
   - Optimize high-priority pages
   - Create SEO content strategy
   - Implement ongoing monitoring

---

**Remember**: SEO is a continuous process. Test regularly, analyze results, and iterate improvements based on data.
