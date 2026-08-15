# Freedom Builders Ltd — Website

A static website for Freedom Builders Ltd (Brendon Hayward), built with plain
HTML, CSS and JavaScript — no framework, no build step needed to run it, and
$0 in hosting costs on Netlify's free tier.

A small Python script (`scripts/build.py`) generates the HTML pages from
shared header/footer templates and from `data/projects.json`, so the "Our
Work" section and individual project pages can be updated by editing one
JSON file and re-running one command — you never have to touch the HTML by
hand to add a project.

---

## 1. Running it locally

You need Python 3 (already on most Macs/Linux; on Windows install from
python.org). No Node, no npm, nothing else required.

```bash
cd freedom-builders
python3 -m http.server 8080
```

Then open **http://localhost:8080** in your browser. Use a local server
(not double-clicking the HTML file) because the site fetches
`/data/projects.json` for the project gallery, which browsers block over
`file://` links.

---

## 2. Rebuilding the site

Whenever you edit `data/projects.json`, or change any of the page content
inside `scripts/build.py`, regenerate the HTML with:

```bash
python3 scripts/build.py
```

This rewrites `index.html`, `services/index.html`, `our-work/index.html`,
`about/index.html`, `contact/index.html`, every page under `projects/`, and
`sitemap.xml`. It's instant — there's no compiling or bundling involved.

---

## 3. Deploying to Netlify

1. Push this folder to a GitHub repository.
2. In Netlify: **Add new site → Import an existing project → GitHub** →
   select the repo.
3. Build settings:
   - **Build command:** `python3 scripts/build.py`
   - **Publish directory:** `.` (the repo root)
4. Deploy. Netlify will run the build script and publish the generated
   HTML automatically on every push.

If you'd rather not let Netlify run Python, you can instead run
`python3 scripts/build.py` yourself before pushing, and set the build
command to blank — the generated HTML files are already committed and
Netlify will just serve them.

### Connecting a custom domain

Netlify → **Domain settings → Add a domain** → follow the prompts to point
your domain's DNS at Netlify (either by changing nameservers or adding the
DNS records Netlify shows you). Netlify issues a free HTTPS certificate
automatically once the domain is verified.

Once the real domain is live, update `SITE_URL` at the top of
`scripts/build.py` (currently a placeholder: `https://freedombuilders.co.nz`)
and re-run the build — this feeds the canonical URLs, Open Graph tags,
sitemap and structured data.

---

## 4. Managing quote submissions

The quote form on the Contact page uses **Netlify Forms** — no third-party
service, no subscription. Submissions appear in your Netlify dashboard
under **Forms**, and you can turn on an email notification there (Site
settings → Forms → Form notifications) so each enquiry lands in your inbox
automatically.

Two technical notes for whoever maintains this:

- The visible form on `/contact/` submits via JavaScript (`fetch`) so the
  visitor sees an inline "thanks" message instead of leaving the page.
- Netlify only detects forms by scanning static HTML at deploy time, so a
  hidden duplicate form (matching field names) lives in
  `netlify-forms.html` purely so Netlify registers the form. You shouldn't
  need to touch this file unless you add or rename a form field — if you
  do, update both the real form in `scripts/build.py` (`build_contact`)
  and `netlify-forms.html` to match.

---

## 5. Adding a new project to "Our Work"

1. Drop the photo(s) into a `raw/` style folder and run them through the
   same resizing step used for the existing photos (see
   `scripts/build.py` header comment, or just resize to roughly 1600px on
   the long edge and export `-thumb` (480px), `-card` (900px) and `-large`
   (1600px) JPEGs into `images/projects/`, using a consistent filename
   prefix, e.g. `garage-build-1-card.jpg`.
2. Add an entry to `data/projects.json`:

```json
{
  "id": 5,
  "slug": "garage-build-bay-of-plenty",
  "title": "Garage Build",
  "category": "Garages & Sheds",
  "location": "Bay of Plenty",
  "stage": "completed",
  "featured": false,
  "short": "One-line summary shown on the project card.",
  "description": "A longer paragraph shown on the project's own page.",
  "cover": "garage-build-1",
  "gallery": ["garage-build-1", "garage-build-2"]
}
```

   - `stage` is either `"completed"` or `"in-progress"` — do not label an
     unfinished job as completed.
   - `featured: true` shows it in the "Our Work" preview on the homepage
     (keep this to 3 projects at a time).
   - `cover` and each entry in `gallery` are filename prefixes — the site
     automatically looks for `<name>-card.jpg` and `<name>-large.jpg`.
   - Never invent a project, address or category that doesn't reflect
     real completed or in-progress work.

3. Run `python3 scripts/build.py`. A new page appears automatically at
   `/projects/garage-build-bay-of-plenty/`, and the project shows up in the
   "Our Work" gallery and its category filter with no other changes needed.

### Creating a new project category

Categories aren't a separate list anywhere — they're just whatever string
you put in a project's `"category"` field. The filter buttons on
`/our-work/` are generated automatically from whatever categories exist in
`data/projects.json`.

---

## 6. Updating business details

| What | Where |
|---|---|
| Phone number | `PHONE_DISPLAY` / `PHONE_TEL` constants near the top of `scripts/build.py`, then re-run the build |
| Facebook link | `FACEBOOK_URL` constant, same file |
| Services list | `SERVICES` list in `scripts/build.py` |
| Brendon's photo | Replace `images/brendon/brendon-*.jpg` (keep the same three filenames/sizes, or update the `src` in `build_home()` / `build_about()`) |
| Logo | Replace files in `images/logo/` (see below) |
| Testimonials | Not built yet — see §8 |
| Service areas / suburb pages | Not built yet — see §9 |

Because the phone number and Facebook link are constants used everywhere
(header, footer, hero, contact page, structured data), updating them in
one place and re-running `python3 scripts/build.py` updates the entire
site consistently.

---

## 7. Replacing Brendon's photo

The current photo in the About section is a placeholder, sized and cropped
so it can be swapped without touching any layout code:

1. Save the new photo as `raw/brendon-portrait.jpeg` (or any name).
2. Re-run the resize step (see the Pillow snippet used originally, or any
   image tool) to produce `images/brendon/brendon-thumb.jpg` (480px),
   `brendon-card.jpg` (900px) and `brendon-large.jpg` (1600px), all at the
   same 4:5 portrait aspect ratio the layout expects.
3. No HTML changes needed — the same filenames are already wired into the
   homepage and About page.

## Replacing the logo

Drop a new logo into `raw/`, trim any surrounding white space, and export:

- `images/logo/logo-mark-header.png` — icon + "FREEDOM BUILDERS LTD."
  wordmark only (no tagline), used in the header and footer.
- `images/logo/favicon.png`, `favicon-32/180/192/512.png`,
  `apple-touch-icon.png` — a square icon-only crop.
- `images/og/freedom-builders-og.jpg` — regenerate the 1200×630 social
  share image if the brand mark changes.

---

## 8. Adding testimonials later

There's no testimonial section on the live site — none were supplied, and
the brief is explicit that no reviews should be invented. When real
testimonials are available:

1. Add a `TESTIMONIALS` list near `SERVICES` in `scripts/build.py`
   (name, suburb, quote).
2. Add a `build_testimonials_section()` helper that renders it the same
   way `SERVICES` is rendered, and drop the returned HTML into the
   homepage and/or About page body.
3. Re-run the build.

Keep it to genuine, attributable quotes only.

---

## 9. Local SEO / service-area pages

The site is currently written for the Bay of Plenty region generally, since
no specific towns were confirmed. When Brendon confirms specific towns he
services (e.g. Whakatāne, Tauranga, Ōpōtiki), the same pattern used for
projects can be reused: add a `data/service-areas.json`, and a
`build_service_area_pages()` function generating `/areas/<town>/` pages
with locally-relevant copy — genuinely useful copy for that town, not
duplicated boilerplate with the town name swapped in.

---

## 10. SEO configuration

- **Titles / meta descriptions / canonical / Open Graph:** set per page
  inside each `build_*()` function in `scripts/build.py`.
- **Sitemap:** regenerated automatically by `build_sitemap()` every time
  you run the build script — it lists every static page plus every
  project. No manual editing needed.
- **robots.txt:** at the site root, points to the sitemap.
- **Structured data:** `GeneralContractor` JSON-LD on the homepage,
  `ImageObject` JSON-LD on each project page — both pull only from
  confirmed information (name, phone, service area, Facebook). Don't add
  ratings, reviews, opening hours or an address unless Brendon confirms
  them; fabricated structured data can get a site penalised in search.

---

## 11. Performance & accessibility notes

- All project and portrait photos are exported at three sizes
  (`-thumb`/`-card`/`-large`) plus compressed JPEG — the gallery only ever
  loads the `-card` size, and the lightbox loads `-large` on demand.
- Images below the fold use `loading="lazy"`.
- Motion respects `prefers-reduced-motion`.
- Keyboard: skip-to-content link, visible focus rings on every
  interactive element, lightbox is operable with arrow keys / Escape.
- Colour palette (blue `#0F3A8C`, charcoal `#1A1A1A`, white) was chosen to
  meet AA contrast on white and dark backgrounds.

Run the site through Lighthouse (Chrome DevTools → Lighthouse) after any
significant content change to confirm performance/accessibility scores
stay high — large unoptimised photos are the most common thing that
regresses this.

---

## 12. What's real vs. placeholder right now

- **Real:** logo, Brendon's portrait, all "Our Work" photos (deck/pergola
  build, kitchen rebuild, kitchen splashback tiling, bathroom renovation),
  phone number, Facebook link, and every credential claim (Qualified
  Builder, LBP, 30+ years).
- **Placeholder / needs your input before launch:**
  - `SITE_URL` in `scripts/build.py` (currently a guessed domain).
  - No testimonials, no specific street addresses, no star ratings — by
    design, per the brief. Add these only when real ones exist (§8).
  - Only four real projects are loaded — add more via §5 as photos come
    in, so "Our Work" reflects the full body of work over time.
