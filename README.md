# NTN Days 2026 website

Static one-page site for NTN Days 2026 (October 13-14, 2026, Cnam, Paris), served via GitHub Pages.
Live at https://ntndays.space/ once the domain is moved (see below).

## Stack

Single `index.html` using Tailwind (CDN), Font Awesome (CDN), and Space Grotesk (Google Fonts).
No build step: edit, commit, push.

## Publishing and domain-move checklist

The file-side work is done in both working copies (July 2026): 2025 favicon/OG/canonical fixes and `CNAME` deletion, 2026 `CNAME` containing `ntndays.space`.
DNS at Namecheap needs no changes; the domain is reassigned on the GitHub side only, driven by the `CNAME` files.

1. Commit and push `ntndays2025` (the pushed `CNAME` deletion releases the custom domain; the 2025 site remains at https://juanfraire.github.io/ntndays2025/).
2. Commit and push `ntndays2026`, then enable GitHub Pages (Settings > Pages > Deploy from branch `main` / root). The `CNAME` file in the repo attaches `ntndays.space`.
3. In `ntndays2026` Pages settings, tick "Enforce HTTPS" once the certificate is issued (usually within minutes since DNS never changed).
4. Verify https://ntndays.space/ serves the 2026 site and the Past Editions links resolve.

## Phases

The site is currently in the **registration phase** (September 2026): registration is the primary call to action
in the hero and in `#submit`, with poster submissions (added September 20) and late talk proposals alongside it.

| Item | Link |
|---|---|
| Talk proposal form | https://forms.gle/UmhKRHDkSfNrGEkp7 |
| Talk proposal responses | https://docs.google.com/spreadsheets/d/18OI1zD9SVkUh16DTGt0tXX0EdQs_OQJog6knp8P9jTY/edit |
| Poster submission form | https://forms.gle/5kEsRvi6QpbvHxTHA |
| Poster submission form (edit) | https://docs.google.com/forms/d/1y85uWvPos-yHrr1Jln-g85tR1AbLDrDRvJANMb9mCEU/edit |
| Poster submission responses | https://docs.google.com/spreadsheets/d/1hm3USHkottdOjv9hhIRGHjZK7hfx6iuuDf3115GN7Rg/edit |
| Registration form | https://forms.gle/AoGMZSggLgMFyLUd7 |
| Registration form (edit) | https://docs.google.com/forms/d/1tCwBB9s-FZgVO5gmnDsu2YVplRTKfytsOsl-8L7bITE/edit |
| Registration responses | https://docs.google.com/spreadsheets/d/1trkjRsTSPzKN3KcxrSR8UfgkMnUwNYvQNYIKG20-qzI/edit |

Dates shown on the site: talk submission September 11 (past, tagged "late proposals considered"), preliminary
program September 18, final program September 23, poster submission and registration deadlines October 9,
event October 13-14.
Attendance is free, stated in the hero, in `#submit`, and as a zero-price `offers` node in the Event JSON-LD.

## TODOs before launch

- [x] Organizing committee list (`#committee`: Vania Conan and Pengwenlong Gu of Cnam, Juan A. Fraire of Inria,
      listed alphabetically; add members here as they join)
- [ ] Sponsor list confirmation (`#sponsors` section; Cnam, GDR RSD, GDR IASIS, Inria already in)
- [x] Talk submission form link (live in hero and `#submit`)
- [x] Registration form link (live in hero and `#submit`)
- [x] Poster submission form link (live in hero and `#submit`)
- [x] Poster form: responses spreadsheet linked
- [x] Poster form: forms.gle short link live in `index.html`
- [ ] Poster form: upload the poster banner as header image (Forms UI > Customize theme); the API cannot
- [x] Registration responses spreadsheet linked

## Edition numbering

The site says "4th Edition": 2023 IRIT/ENSEEIHT Toulouse (Oct 19-20, per irit.fr) -> 2024 Grenoble (Oct 17-18, called "deuxieme edition" by GDR IASIS) -> 2025 LAAS Toulouse -> 2026 Paris.
If there was an earlier edition not documented online, bump the hero badge in `index.html`.
