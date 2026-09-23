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

The site is in the **program phase**: the final program is online in `#program` (published September 23, 2026),
"Program" is the primary hero button and a nav entry, registration (free, until October 9) and poster
submissions stay open alongside it. Talk submissions closed on September 21.

### Program section

`#program` is static HTML (no data file): two day panels (`#program-day1`, `#program-day2`) switched by the
sticky day tabs, each a list of slots. Three slot kinds share the `program-*` CSS classes defined in the
`<style>` block: `program-break` (one-line rows: coffee, lunch, opening, closing), `program-keynote`
(highlighted card, also used for the poster session and the roundtable) and `program-session` (header plus
an `<ol>` of `program-talk` rows: time, title, presenter, affiliation). Every slot and talk carries
`data-start`/`data-end` (HH:MM, Paris time); on October 13 and 14 the script at the bottom of the page opens
that day's tab and adds `program-now` to the slot in progress. `#program-day2` in the URL opens Day 2.
Print CSS shows both days flat.

The editorial source is `../2026-paris/PROGRAM.md` (session assignments, keynote status, open decisions).
When it changes, mirror it here by hand (and regenerate `ntndays2026.ics` too).

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

Dates shown on the site: talk submission September 11 (closed), final program published September 23
(links to `#program`), poster submission and registration deadlines October 9, event October 13-14.
Attendance is free, stated in the hero, in `#submit`, and as a zero-price `offers` node in the Event JSON-LD.

## TODOs before launch

- [x] Organizing committee list (`#committee`: Vania Conan and Pengwenlong Gu of Cnam, Juan A. Fraire of Inria,
      listed alphabetically; add members here as they join)
- [ ] Sponsor list confirmation (`#sponsors` section; Cnam, GDR RSD, GDR IASIS, Inria already in)
- [x] Talk submission form link (was live in hero and `#submit`; removed September 21 when talk review started)
- [x] Registration form link (live in hero and `#submit`)
- [x] Poster submission form link (live in hero and `#submit`)
- [x] Poster form: responses spreadsheet linked
- [x] Poster form: forms.gle short link live in `index.html`
- [ ] Poster form: upload the poster banner as header image (Forms UI > Customize theme); the API cannot
- [x] Registration responses spreadsheet linked
- [x] Program section (`#program`, final, September 23; 2 keynotes, 4 sessions, 21 talks, poster session, roundtable)
- [x] Program: roundtable theme and panel live ("NTN: time to move from theory to implementation",
      Fawaz, Baccelli, Caillouet, Bucaille; moderated by Pengwenlong Gu)
- [ ] Program: Fawaz keynote title is the placeholder "Challenges in V-LEO systems" (Vania confirms the
      week of Sep 28); Baccelli to confirm the title/abstract derived from his note; session chairs if wanted
- [x] `ntndays2026.ics`: one umbrella event plus 19 timed slots (Europe/Paris VTIMEZONE, CRLF); regenerate it
      by hand whenever `#program` changes

## Edition numbering

The site says "4th Edition": 2023 IRIT/ENSEEIHT Toulouse (Oct 19-20, per irit.fr) -> 2024 Grenoble (Oct 17-18, called "deuxieme edition" by GDR IASIS) -> 2025 LAAS Toulouse -> 2026 Paris.
If there was an earlier edition not documented online, bump the hero badge in `index.html`.
