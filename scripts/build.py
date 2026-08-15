#!/usr/bin/env python3
"""
Freedom Builders Ltd — static site builder.

Assembles the shared header, mobile nav, mobile sticky bar and footer into
every page, and generates a real, clean-URL page for each project listed in
data/projects.json (so /projects/<slug>/ works with no JavaScript routing).

Run from the project root:
    python3 scripts/build.py

Re-run any time you edit data/projects.json or the page content below —
see README.md for the full "adding a project" workflow.
"""
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "data", "projects.json")))

SITE_URL = "https://freedombuilders.co.nz"  # update once the real domain is connected
PHONE_DISPLAY = "022 537 1325"
PHONE_TEL = "tel:0225371325"
FACEBOOK_URL = "https://www.facebook.com/share/1A9sNbgAdS/?mibextid=wwXIfr"

NAV_ITEMS = [
    ("home", "Home", "/"),
    ("services", "Services", "/services/"),
    ("work", "Our Work", "/our-work/"),
    ("about", "About", "/about/"),
    ("contact", "Contact", "/contact/"),
]

STAGE_LABEL = {"completed": "Completed", "in-progress": "In Progress"}


def nav_html(active, mobile=False):
    cls = "mobile-nav" if mobile else "main-nav"
    items = []
    for key, label, href in NAV_ITEMS:
        current = ' aria-current="page"' if key == active else ""
        items.append(f'<li><a href="{href}"{current}>{label}</a></li>')
    extra = '<a class="btn btn-primary btn-block" href="/contact/">Get a Free Quote</a>' if mobile else ""
    return f'<nav class="{cls}" aria-label="{"Mobile" if mobile else "Primary"} navigation"><ul>{"".join(items)}</ul>{extra}</nav>'


def header_html(active):
    return f"""
  <a class="skip-link" href="#main">Skip to main content</a>
  <header class="site-header">
    <div class="container">
      <a class="brand" href="/" aria-label="Freedom Builders Ltd — home">
        <img src="/images/logo/logo-mark-header.png" alt="Freedom Builders Ltd" width="230" height="60">
      </a>
      {nav_html(active)}
      <div class="header-cta">
        <span class="header-phone">{PHONE_DISPLAY}</span>
        <a class="btn btn-primary" href="{PHONE_TEL}">Call Brendon</a>
      </div>
      <button class="hamburger" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-nav">
        <span></span><span></span><span></span>
      </button>
    </div>
    <div id="mobile-nav">{nav_html(active, mobile=True)}</div>
  </header>
"""


def mobile_bar_html():
    return f"""
  <div class="mobile-bar">
    <a class="call" href="{PHONE_TEL}">📞 Call Brendon</a>
    <a class="quote" href="/contact/">Free Quote</a>
  </div>
"""


def footer_html():
    return f"""
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <img src="/images/logo/logo-mark-header.png" alt="Freedom Builders Ltd" width="180" height="47">
          <p>Freedom Builders Ltd<br>Brendon Hayward — Qualified Builder, Licensed Building Practitioner<br>Serving the Bay of Plenty</p>
        </div>
        <div class="footer-col">
          <h4>Navigation</h4>
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/services/">Services</a></li>
            <li><a href="/our-work/">Our Work</a></li>
            <li><a href="/about/">About</a></li>
            <li><a href="/contact/">Contact</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Get In Touch</h4>
          <ul>
            <li><a href="{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
            <li><a href="/contact/">Request a free quote</a></li>
            <li><a class="footer-social" href="{FACEBOOK_URL}" target="_blank" rel="noopener">Facebook →</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; <span id="year">2026</span> Freedom Builders Ltd. All rights reserved.</span>
        <span>Bay of Plenty, New Zealand</span>
      </div>
    </div>
  </footer>
"""


def lightbox_html():
    return """
  <div class="lightbox" role="dialog" aria-modal="true" aria-label="Project photo viewer">
    <button class="lightbox-close" aria-label="Close">&times;</button>
    <button class="lightbox-prev" aria-label="Previous photo">&#8249;</button>
    <img src="" alt="">
    <button class="lightbox-next" aria-label="Next photo">&#8250;</button>
    <p class="lightbox-caption"></p>
  </div>
"""


def page_shell(active, title, description, body, og_image="/images/og/freedom-builders-og.jpg",
               canonical=None, extra_head="", body_class=""):
    canonical = canonical or SITE_URL
    return f"""<!doctype html>
<html lang="en-NZ">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/images/logo/favicon.png">
<link rel="apple-touch-icon" href="/images/logo/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/styles.css">
{extra_head}
</head>
<body class="{body_class}">
{header_html(active)}
<main id="main">
{body}
</main>
{footer_html()}
{mobile_bar_html()}
{lightbox_html()}
<script src="/js/main.js" defer></script>
</body>
</html>
"""


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(html)
    print("wrote", path)


# ---------------------------------------------------------------------------
# Project detail pages
# ---------------------------------------------------------------------------
def build_project_pages():
    for p in DATA:
        gallery_items = "".join(
            f'''<a class="thumb-wrap" style="aspect-ratio:4/3;border-radius:2px;overflow:hidden;box-shadow:var(--shadow-card)"
                 href="/images/projects/{img}-large.jpg" data-lightbox="proj-{p['slug']}">
                <img src="/images/projects/{img}-card.jpg" alt="{p['title']} — {p['category']}" loading="lazy" width="900" height="675">
              </a>'''
            for img in p["gallery"]
        )
        stage_class = "stage-completed" if p["stage"] == "completed" else ""
        body = f"""
<section class="page-hero no-media" style="padding-top:150px;">
  <div class="container">
    <span class="eyebrow on-dark">{p['category']} · {p['location']}</span>
    <h1>{p['title']}</h1>
    <p class="lede">{p['short']}</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr;gap:44px;">
      <div style="max-width:70ch;">
        <span class="stage-tag {stage_class}" style="position:static;display:inline-flex;margin-bottom:18px;">{STAGE_LABEL[p['stage']]}</span>
        <p class="lede" style="max-width:70ch;">{p['description']}</p>
      </div>
      <div class="work-grid">
        {gallery_items}
      </div>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="container">
    <h2>Thinking About Something Similar?</h2>
    <p class="lede">Give Brendon a call and have a chat about your project, or send through a few details for a free quote.</p>
    <div class="actions">
      <a class="btn btn-primary btn-lg" href="{PHONE_TEL}">Call Brendon — {PHONE_DISPLAY}</a>
      <a class="btn btn-outline btn-lg" href="/contact/">Get a Free Quote</a>
    </div>
  </div>
</section>
"""
        ld_json = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ImageObject",
  "name": "{p['title']}",
  "description": "{p['short']}",
  "contentUrl": "{SITE_URL}/images/projects/{p['cover']}-large.jpg"
}}
</script>"""
        html = page_shell(
            active="work",
            title=f"{p['title']} | Freedom Builders Ltd, Bay of Plenty",
            description=p["short"],
            body=body,
            canonical=f"{SITE_URL}/projects/{p['slug']}/",
            og_image=f"/images/projects/{p['cover']}-card.jpg",
            extra_head=ld_json,
        )
        write(f"projects/{p['slug']}/index.html", html)


def build_sitemap():
    urls = ["/", "/services/", "/our-work/", "/about/", "/contact/"]
    urls += [f"/projects/{p['slug']}/" for p in DATA]
    body = "\n".join(
        f"  <url><loc>{SITE_URL}{u}</loc></url>" for u in urls
    )
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
"""
    write("sitemap.xml", xml)


# ---------------------------------------------------------------------------
# Homepage
# ---------------------------------------------------------------------------
def build_home():
    featured = [p for p in DATA if p.get("featured")][:3]
    featured_cards = "".join(
        f'''<article class="project-card reveal">
              <a class="thumb-wrap" href="/projects/{p['slug']}/" aria-label="View {p['title']}">
                <span class="stage-tag {'stage-completed' if p['stage']=='completed' else ''}">{STAGE_LABEL[p['stage']]}</span>
                <img src="/images/projects/{p['cover']}-card.jpg" alt="{p['title']} — {p['category']}, {p['location']}" loading="lazy" width="900" height="675">
              </a>
              <div class="body">
                <span class="cat">{p['category']}</span>
                <h3>{p['title']}</h3>
                <p class="loc">{p['location']}</p>
                <p class="desc">{p['short']}</p>
                <a class="view-link" href="/projects/{p['slug']}/">View project →</a>
              </div>
            </article>'''
        for p in featured
    )

    body = f"""
<section class="hero">
  <div class="hero-media">
    <img src="/images/projects/deck-completed-large.jpg" alt="A completed deck and pergola built by Freedom Builders in the Bay of Plenty" width="1179" height="1560">
  </div>
  <div class="container hero-inner">
    <span class="eyebrow on-dark">Bay of Plenty · Freedom Builders Ltd</span>
    <h1>Building Experience You Can Rely On.</h1>
    <p class="lede">Quality building across the Bay of Plenty, backed by more than 30 years of hands-on experience.</p>
    <div class="hero-credentials">
      <span>Qualified Builder</span>
      <span>Licensed Building Practitioner</span>
      <span>30+ Years Experience</span>
    </div>
    <div class="hero-actions">
      <a class="btn btn-primary btn-lg" href="{PHONE_TEL}">Call Brendon — {PHONE_DISPLAY}</a>
      <a class="btn btn-outline on-dark btn-lg" href="/contact/">Get a Free Quote</a>
      <a class="btn-ghost" href="/our-work/">View Our Work</a>
    </div>
  </div>
</section>

<section class="trust-strip">
  <div class="container trust-cards">
    <div class="trust-card"><span class="num">30+</span><span class="label"><strong>Years</strong>Building experience</span></div>
    <div class="trust-card"><span class="num">QB</span><span class="label"><strong>Qualified</strong>Builder</span></div>
    <div class="trust-card"><span class="num">LBP</span><span class="label"><strong>Licensed</strong>Building Practitioner</span></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Whatever You're Building</span>
      <h2>Let's Talk.</h2>
      <p class="lede">Freedom Builders takes on building projects big and small across the Bay of Plenty. From decks, repairs and alterations through to renovations and larger residential projects, Brendon brings decades of practical building experience to every job.</p>
    </div>
    <a class="btn-ghost" href="/services/">Explore Our Services</a>
  </div>
</section>

<section class="section section-offwhite">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Our Work</span>
      <h2>Real Projects, Real Building Work.</h2>
      <p class="lede">A look at some of the projects completed by Freedom Builders across the Bay of Plenty.</p>
    </div>
    <div class="work-grid">
      {featured_cards}
    </div>
    <div class="section-foot">
      <a class="btn-ghost" href="/our-work/">See all our work</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container about-hero-grid">
    <div class="about-photo reveal">
      <img src="/images/brendon/brendon-card.jpg" alt="Brendon Hayward, owner and builder at Freedom Builders Ltd" width="900" height="964">
    </div>
    <div class="about-copy reveal">
      <span class="eyebrow">Meet Brendon</span>
      <h2>30+ Years of Practical Building Experience.</h2>
      <p>Brendon Hayward is the owner and builder behind Freedom Builders Ltd. A Qualified Builder and Licensed Building Practitioner, Brendon works across the Bay of Plenty on projects ranging from smaller building jobs through to renovations and larger residential work.</p>
      <p>You deal directly with Brendon from the first phone call through to the finished job — no call centres, no middlemen.</p>
      <a class="btn-ghost" href="/about/">More about Brendon</a>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="container">
    <h2>Have Something You Need Built?</h2>
    <p class="lede">From a smaller repair to a major renovation, give Brendon a call and have a chat about your project.</p>
    <div class="actions">
      <a class="btn btn-primary btn-lg" href="{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
      <a class="btn btn-outline btn-lg" href="/contact/">Request a Free Quote</a>
    </div>
  </div>
</section>
"""
    ld_json = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "GeneralContractor",
  "name": "Freedom Builders Ltd",
  "founder": "Brendon Hayward",
  "telephone": "{PHONE_TEL.replace('tel:', '')}",
  "areaServed": "Bay of Plenty, New Zealand",
  "url": "{SITE_URL}",
  "sameAs": ["{FACEBOOK_URL}"],
  "description": "Qualified Builder and Licensed Building Practitioner with 30+ years of experience, based in the Bay of Plenty, New Zealand."
}}
</script>"""
    html = page_shell(
        active="home",
        title="Freedom Builders Ltd | Builder Bay of Plenty — Brendon Hayward, LBP",
        description="Qualified Builder and Licensed Building Practitioner with 30+ years of experience across the Bay of Plenty. Free quotes. Call Brendon on 022 537 1325.",
        body=body,
        canonical=f"{SITE_URL}/",
        og_image="/images/projects/deck-completed-card.jpg",
        extra_head=ld_json,
    )
    write("index.html", html)


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------
SERVICES = [
    ("01", "New Builds", "Residential building projects from plans through construction."),
    ("02", "Renovations", "Transforming and upgrading existing homes."),
    ("03", "Extensions & Alterations", "Creating more space and modifying existing homes."),
    ("04", "Kitchens & Bathrooms", "Building and renovation work for kitchens and bathrooms."),
    ("05", "Decks & Outdoor Living", "Decks, covered areas, stairs, pergolas and outdoor spaces."),
    ("06", "Garages & Sheds", "Garages, sheds, workshops and additional structures."),
    ("07", "Repairs & Maintenance", "Repairs, replacements and general building maintenance."),
    ("08", "General Building", "Have something else that needs building? Get in touch."),
]


def build_services():
    cards = "".join(
        f'''<div class="service-card reveal">
              <span class="num">{num}</span>
              <h3>{title}</h3>
              <p>{desc}</p>
            </div>'''
        for num, title, desc in SERVICES
    )
    body = f"""
<section class="page-hero">
  <div class="page-hero-media"><img src="/images/projects/kitchen-renovation-large.jpg" alt="A kitchen rebuild in progress by Freedom Builders" width="1179" height="1557"></div>
  <div class="container">
    <span class="eyebrow on-dark">Services</span>
    <h1>Building Services</h1>
    <p class="lede">From smaller jobs around the home to major building projects, Freedom Builders can help.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="services-grid">{cards}</div>
  </div>
</section>

<section class="section section-offwhite">
  <div class="container why-grid">
    <div class="why-item reveal">
      <div class="mark">30+</div>
      <div><h3>Experience</h3><p>More than 30 years in the building industry.</p></div>
    </div>
    <div class="why-item reveal">
      <div class="mark">QB</div>
      <div><h3>Qualified</h3><p>Qualified Builder and Licensed Building Practitioner.</p></div>
    </div>
    <div class="why-item reveal">
      <div class="mark">✓</div>
      <div><h3>Versatility</h3><p>Building projects big and small, right across the Bay of Plenty.</p></div>
    </div>
    <div class="why-item reveal">
      <div class="mark">☎</div>
      <div><h3>Direct Contact</h3><p>Deal directly with Brendon from the first conversation.</p></div>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="container">
    <h2>Whatever You're Building, Let's Talk.</h2>
    <div class="actions">
      <a class="btn btn-primary btn-lg" href="{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
      <a class="btn btn-outline btn-lg" href="/contact/">Get a Free Quote</a>
    </div>
  </div>
</section>
"""
    html = page_shell(
        active="services",
        title="Building Services | Freedom Builders Ltd — Bay of Plenty",
        description="New builds, renovations, extensions, kitchens & bathrooms, decks, garages, repairs and general building across the Bay of Plenty. Free quotes.",
        body=body,
        canonical=f"{SITE_URL}/services/",
        og_image="/images/projects/kitchen-renovation-card.jpg",
    )
    write("services/index.html", html)


# ---------------------------------------------------------------------------
# Our Work
# ---------------------------------------------------------------------------
def build_our_work():
    body = f"""
<section class="page-hero">
  <div class="page-hero-media"><img src="/images/projects/bathroom-renovation-large.jpg" alt="A bathroom renovation in progress by Freedom Builders" width="1179" height="1462"></div>
  <div class="container">
    <span class="eyebrow on-dark">Our Work</span>
    <h1>A Look at Our Projects</h1>
    <p class="lede">A look at some of the projects completed by Freedom Builders across the Bay of Plenty — both finished work and work still underway.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="filters" data-filters></div>
    <div class="work-grid" data-work-grid></div>
  </div>
</section>

<section class="cta-band">
  <div class="container">
    <h2>Thinking About Something Similar?</h2>
    <div class="actions">
      <a class="btn btn-primary btn-lg" href="{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
      <a class="btn btn-outline btn-lg" href="/contact/">Get a Free Quote</a>
    </div>
  </div>
</section>
"""
    html = page_shell(
        active="work",
        title="Our Work | Freedom Builders Ltd — Bay of Plenty",
        description="Real building projects completed and underway across the Bay of Plenty — decks, kitchens, bathrooms, renovations and more.",
        body=body,
        canonical=f"{SITE_URL}/our-work/",
        og_image="/images/projects/bathroom-renovation-card.jpg",
    )
    write("our-work/index.html", html)


# ---------------------------------------------------------------------------
# About
# ---------------------------------------------------------------------------
def build_about():
    body = f"""
<section class="page-hero no-media" style="background:var(--charcoal);padding-top:150px;">
  <div class="container">
    <span class="eyebrow on-dark">About</span>
    <h1>Meet Brendon</h1>
  </div>
</section>

<section class="section">
  <div class="container about-hero-grid">
    <div class="about-photo reveal">
      <img src="/images/brendon/brendon-card.jpg" alt="Brendon Hayward, owner and builder at Freedom Builders Ltd" width="900" height="964">
    </div>
    <div class="about-copy reveal">
      <p class="lede">Brendon Hayward is the owner and builder behind Freedom Builders Ltd.</p>
      <p>A Qualified Builder and Licensed Building Practitioner with more than 30 years of building experience, Brendon works across the Bay of Plenty on projects ranging from smaller building jobs through to renovations and larger residential work.</p>
      <p>He's built his reputation on practical building knowledge and quality workmanship, dealing directly with clients from the first phone call through to the finished job. No call centres, no sales team — just straightforward communication and pride in getting the job done properly.</p>
      <div class="credential-row">
        <span class="credential-pill">30+ Years Building Experience</span>
        <span class="credential-pill">Qualified Builder</span>
        <span class="credential-pill">Licensed Building Practitioner</span>
        <span class="credential-pill">Bay of Plenty</span>
      </div>
    </div>
  </div>
</section>

<section class="section section-offwhite">
  <div class="container why-grid">
    <div class="why-item reveal">
      <div class="mark">30+</div>
      <div><h3>Experience</h3><p>More than 30 years in the building industry.</p></div>
    </div>
    <div class="why-item reveal">
      <div class="mark">QB</div>
      <div><h3>Qualified</h3><p>Qualified Builder and Licensed Building Practitioner.</p></div>
    </div>
    <div class="why-item reveal">
      <div class="mark">✓</div>
      <div><h3>Versatility</h3><p>Building projects big and small.</p></div>
    </div>
    <div class="why-item reveal">
      <div class="mark">☎</div>
      <div><h3>Direct Contact</h3><p>Deal directly with Brendon from the first conversation.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Got a Project in Mind?</span>
      <h2>How It Works</h2>
    </div>
    <div class="steps">
      <div class="step reveal"><span class="step-num">01</span><h3>Give Brendon a Call</h3><p>Tell him what you're thinking about.</p></div>
      <div class="step reveal"><span class="step-num">02</span><h3>Discuss the Job</h3><p>Talk through what you need and the best way forward.</p></div>
      <div class="step reveal"><span class="step-num">03</span><h3>Site Visit</h3><p>Arrange a site visit where required.</p></div>
      <div class="step reveal"><span class="step-num">04</span><h3>Free Quote</h3><p>Receive a quote for the proposed work where appropriate.</p></div>
      <div class="step reveal"><span class="step-num">05</span><h3>Get Building</h3><p>Once everything is agreed, the project can get underway.</p></div>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="container">
    <h2>Whatever You're Building, Let's Talk.</h2>
    <div class="actions">
      <a class="btn btn-primary btn-lg" href="{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
      <a class="btn btn-outline btn-lg" href="/contact/">Get a Free Quote</a>
    </div>
  </div>
</section>
"""
    html = page_shell(
        active="about",
        title="About Brendon Hayward | Freedom Builders Ltd — Bay of Plenty",
        description="Brendon Hayward — Qualified Builder and Licensed Building Practitioner with 30+ years of experience across the Bay of Plenty.",
        body=body,
        canonical=f"{SITE_URL}/about/",
        og_image="/images/brendon/brendon-card.jpg",
    )
    write("about/index.html", html)


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------
def build_contact():
    body = f"""
<section class="page-hero no-media" style="background:var(--charcoal);padding-top:150px;">
  <div class="container">
    <span class="eyebrow on-dark">Contact</span>
    <h1>Get In Touch</h1>
    <p class="lede">Call Brendon directly, or send through a few details and he'll get back to you.</p>
  </div>
</section>

<section class="section">
  <div class="container contact-grid">
    <div>
      <div class="contact-card reveal">
        <h3>Freedom Builders Ltd</h3>
        <div class="contact-line"><span class="ico">☎</span><div>Brendon Hayward<br><a href="{PHONE_TEL}">{PHONE_DISPLAY}</a></div></div>
        <div class="contact-line"><span class="ico">✓</span><div>Qualified Builder<br>Licensed Building Practitioner</div></div>
        <div class="contact-line"><span class="ico">📍</span><div>Bay of Plenty, New Zealand</div></div>
        <div class="contact-line"><span class="ico">f</span><div><a href="{FACEBOOK_URL}" target="_blank" rel="noopener">Facebook</a></div></div>
        <a class="btn btn-primary btn-block" href="{PHONE_TEL}">Call Brendon Now</a>
      </div>
    </div>

    <div>
      <h3>Request a Free Quote</h3>
      <p class="muted" style="margin:10px 0 24px;">Fill in as much as you can — phone number is all we need to get back to you.</p>

      <div id="form-success" class="form-success reveal">
        <h3>Thanks — that's through to Brendon.</h3>
        <p>He'll be in touch soon. If it's urgent, give him a call directly on <a href="{PHONE_TEL}">{PHONE_DISPLAY}</a>.</p>
      </div>

      <form id="quote-form" name="quote" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="/contact/thanks/">
        <input type="hidden" name="form-name" value="quote">
        <p class="sr-only"><label>Don't fill this in: <input name="bot-field"></label></p>

        <div class="form-grid two">
          <div class="field">
            <label for="name">Name</label>
            <input id="name" name="name" type="text" required>
          </div>
          <div class="field">
            <label for="phone">Phone</label>
            <input id="phone" name="phone" type="tel" required>
          </div>
        </div>

        <div class="form-grid two" style="margin-top:18px;">
          <div class="field">
            <label for="email">Email <span class="opt">(optional)</span></label>
            <input id="email" name="email" type="email">
          </div>
          <div class="field">
            <label for="location">Project Location</label>
            <input id="location" name="location" type="text" placeholder="e.g. Whakat\u0101ne">
          </div>
        </div>

        <div class="field" style="margin-top:18px;">
          <label for="job-type">What do you need done?</label>
          <select id="job-type" name="job-type">
            <option>New Build</option>
            <option>Renovation</option>
            <option>Extension / Alteration</option>
            <option>Kitchen</option>
            <option>Bathroom</option>
            <option>Deck / Outdoor Area</option>
            <option>Garage / Shed</option>
            <option>Repair / Maintenance</option>
            <option>General Building</option>
            <option>Other</option>
          </select>
        </div>

        <div class="field" style="margin-top:18px;">
          <label for="details">Tell us about the job</label>
          <textarea id="details" name="details" rows="5"></textarea>
        </div>

        <div class="form-grid two" style="margin-top:18px;">
          <div class="field">
            <label for="timeframe">When are you hoping to get started? <span class="opt">(optional)</span></label>
            <input id="timeframe" name="timeframe" type="text">
          </div>
          <div class="field">
            <label for="files">Photos or Plans <span class="opt">(optional)</span></label>
            <input id="files" name="files" type="file" multiple>
          </div>
        </div>

        <button class="btn btn-primary btn-lg btn-block" type="submit" style="margin-top:26px;">Request Free Quote</button>
        <p class="form-note">Submissions are sent straight to Freedom Builders via Netlify Forms — see the site README for where these are received.</p>
      </form>
    </div>
  </div>
</section>
"""
    html = page_shell(
        active="contact",
        title="Contact & Free Quotes | Freedom Builders Ltd — Bay of Plenty",
        description="Call Brendon Hayward on 022 537 1325 or request a free quote online. Freedom Builders Ltd, Bay of Plenty.",
        body=body,
        canonical=f"{SITE_URL}/contact/",
    )
    write("contact/index.html", html)

    # Static form target so Netlify Forms can detect the form at build/deploy time
    thanks = page_shell(
        active="contact",
        title="Thanks | Freedom Builders Ltd",
        description="Thanks for your enquiry.",
        body=f"""<section class="section" style="padding-top:170px;text-align:center;">
  <div class="container">
    <h1>Thanks — that's through to Brendon.</h1>
    <p class="lede" style="margin:16px auto 30px;">He'll be in touch soon. If it's urgent, give him a call directly.</p>
    <a class="btn btn-primary btn-lg" href="{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
  </div>
</section>""",
        canonical=f"{SITE_URL}/contact/thanks/",
    )
    write("contact/thanks/index.html", thanks)

    # Hidden Netlify-detectable form stub (Netlify parses HTML at deploy time;
    # the real UX form above is submitted via JS fetch to "/").
    netlify_stub = """<!doctype html><html><head><meta charset="utf-8"></head><body>
<form name="quote" data-netlify="true" netlify-honeypot="bot-field" hidden>
  <input name="bot-field">
  <input name="name"><input name="phone"><input name="email"><input name="location">
  <select name="job-type"><option>New Build</option></select>
  <textarea name="details"></textarea>
  <input name="timeframe"><input name="files" type="file" multiple>
</form>
</body></html>"""
    write("netlify-forms.html", netlify_stub)


if __name__ == "__main__":
    build_home()
    build_services()
    build_our_work()
    build_about()
    build_contact()
    build_project_pages()
    build_sitemap()
