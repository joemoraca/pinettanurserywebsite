# Pinetta Nursery

Static copy of [pinettanursery.com](https://pinettanursery.com/), the WordPress site for Pinetta Nursery (fruit, nuts, and flowers for north Florida). The pages are plain HTML and CSS. There is no WordPress, PHP, or database.

The public WordPress site was only read. Nothing on it was changed.

## Preview on your computer

From this folder:

```bash
python3 -m http.server 8000
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Use the same paths as the live site, for example [http://127.0.0.1:8000/about-us/](http://127.0.0.1:8000/about-us/).

## Edit a page

Page text lives in `content/`. The HTML files next to this README are generated from those sources.

1. Edit the matching file:
   - Home: `content/home.html`
   - For Sale: `content/for-sale.html`
   - About: `content/about-us.html`
   - Food Forests: `content/food-forests.html`
   - Contact: `content/contact-form.html`
   - Posts: `content/build-greenhouse.html`, `content/irrigation.html`, `content/how-to-start.html`
2. Pictures already on the site are in `images/`. In a content file, refer to one as `{{img:logo.png}}`. Link to another page as `{{url:contact-form/}}`.
3. Rebuild:

```bash
python3 build.py
```

`build.py` uses only the Python standard library. It rewrites `index.html`, each `*/index.html` page, `404.html`, and `js/search-index.js`.

The home page, category pages (`/category/business/` and `/category/homesteading/`), tag pages, and the author page (`/author/joe-moraca/`) are built from the three posts. Post titles, dates, categories, and tags are listed near the top of `build.py`.

To add a post, add a `content/your-slug.html` file, add an entry to `POSTS` in `build.py`, and run `python3 build.py`. The new URL will be `/your-slug/`.

Editing a generated `index.html` directly also works until the next build, which overwrites it. Prefer the files in `content/`.

The For Sale prices and quantities are the ones published on the WordPress site. Update `content/for-sale.html` when the list changes.

## Contact form

The old contact page used WPForms (name, email, message, and reCAPTCHA) plus the phone number **Joe Moraca, 386-288-9689**. The public site does not list an email address, so this copy does not invent one and does not sign up for a form service.

`/contact-form/` keeps that phone number as a tap-to-call link (`tel:+13862889689`) and keeps the same fields. The form is a placeholder: submitting it does nothing and tells the visitor to call. A hidden “Name Message or” field is still there so it can act as a spam trap later.

To attach a free form host later (Formspree, Getform, Web3Forms, or similar):

1. Create the form on that service. Field names on this site are `first`, `last`, `email`, and `message`.
2. In `content/contact-form.html`, set the form tag to the endpoint they give you, for example `action="https://formspree.io/f/xxxxxxxx"`. Leave `method="post"`.
3. Remove the green note that says the form is not connected, or replace it with a shorter sentence.
4. Run `python3 build.py`.

Until `action` is filled in, the form will not send mail.

The old reCAPTCHA widget was not copied. It only works with a Google key and a server. Add whatever spam protection the form service provides.

## Enable GitHub Pages

This repository is ready to publish from the root of the `main` branch.

1. On GitHub, open **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Choose branch **main** and folder **/ (root)**, then save.

GitHub will serve the site. With the `CNAME` file in place, GitHub Pages treats the custom domain as `pinettanursery.com` and redirects `https://joemoraca.github.io/pinettanurserywebsite/` to that domain.

**Do not change DNS until the new site has been reviewed.** While `pinettanursery.com` still points at the old host, that redirect is not a useful preview.

Review the site locally with `python3 -m http.server` first. To preview on GitHub before switching DNS, temporarily rename `CNAME` (for example to `CNAME.disabled`), push, and open the `github.io` project URL. Put the `CNAME` file back before you point the domain at GitHub, or the custom domain will not be configured.

Links are relative, so the same files work on your computer, on a `github.io` project URL, and on `pinettanursery.com`.

## Point pinettanursery.com at GitHub Pages

Do this only after the new site looks right.

The repository already contains a `CNAME` file with `pinettanursery.com`. After Pages is enabled, **Settings → Pages** should show that custom domain. Enable **Enforce HTTPS** once GitHub has issued a certificate (that can fail until DNS points here).

At the domain registrar, leave the old records in place until you are ready to switch. Then:

- **Apex (`pinettanursery.com`)**: set these A records to GitHub Pages:
  - `185.199.108.153`
  - `185.199.109.153`
  - `185.199.110.153`
  - `185.199.111.153`
- **www**: add a CNAME record for `www` pointing at `joemoraca.github.io`.

Remove old A or CNAME records that still point at the WordPress host, or visitors will keep seeing the old site. DNS can take a while to update. Confirm `https://pinettanursery.com/` shows this static site before considering the move finished.

GitHub’s current instructions are at [Configuring a custom domain for your GitHub Pages site](https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site).

## What was copied

Pages and posts, at the same paths:

- `/` home
- `/for-sale/`
- `/about-us/`
- `/food-forests/`
- `/contact-form/`
- `/build-greenhouse/`
- `/irrigation/`
- `/how-to-start/`
- `/category/business/`, `/category/homesteading/`
- `/tag/greenhouse/`, `/tag/infrastructure/`, `/tag/nursery/`, `/tag/propagation/`
- `/author/joe-moraca/`
- `404.html` (the old “not the droid you are looking for” message). The WordPress search box is now a small search of these pages, because search needed PHP.

Every file in the WordPress media library is in `images/`, including the logo. Pages use local copies, not links back to WordPress.

These library images were not placed on any public page, but they are still in `images/`:

- `apple.jpg`
- `avo-seedlings-scaled.jpg`
- `elderberry.png`
- `pinkflower.png`
- `cropped-pinkflower.png`

The two Food Forests videos stay as YouTube embeds. They were not downloaded.

Navigation is For Sale, About, Food Forests, and Contact. Colors, the pale green header frame, and the logo match the Twenty Twenty-Three layout that was on the live site. Fonts used there (DM Sans, Comic Neue, and ADLaM Display) are in `fonts/`.

## What was not copied

- The footer line “Proudly powered by WordPress”. This site is not WordPress. The footer uses the site name and the tagline instead.
- WPForms submission and reCAPTCHA. See Contact form above.
- A Bitcoin Lightning plugin stylesheet was loaded by WordPress, but no lightning button or other lightning content was on the public pages.
- There were no published comments.
