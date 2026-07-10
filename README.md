# NTN Days 2026 website

Static one-page site for NTN Days 2026 (October 13-14, 2026, Cnam, Paris), served via GitHub Pages.
Live at https://ntndays.space/ once the domain is moved (see below).

## Stack

Single `index.html` using Tailwind (CDN), Font Awesome (CDN), and Space Grotesk (Google Fonts).
No build step: edit, commit, push.

## Publishing checklist

1. Push to `main` and enable GitHub Pages (Settings > Pages > Deploy from branch `main` / root).
2. Verify at https://juanfraire.github.io/ntndays2026/.

## Moving the ntndays.space domain from the 2025 repo (do when ready to go live)

DNS at Namecheap needs no changes; the domain is reassigned on the GitHub side only.

1. In `ntndays2025`: fix root-relative favicon links in `index.html` (`/favicon.ico` -> `favicon.ico`, etc.) so they work at the github.io URL.
2. In `ntndays2025` repo settings (Pages): remove the custom domain, and delete the `CNAME` file. The 2025 site remains at https://juanfraire.github.io/ntndays2025/.
3. In `ntndays2026` repo settings (Pages): set custom domain to `ntndays.space` (this creates the `CNAME` file) and re-enable "Enforce HTTPS" once the certificate is issued.

## TODOs before launch

- [ ] Organizing committee list (`#committee` section)
- [ ] Sponsor list confirmation, Cnam logo (`#sponsors` section)
- [ ] Talk submission and registration form links (`#submit` section, currently disabled buttons)
- [ ] Exact 2024 edition dates in the Past Editions cards (currently Oct 17-18, 2024; verify)
