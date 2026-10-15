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

The site is in the **post-event phase** (October 16, 2026). A banner above the nav says the event has
concluded and points at the slides and the photos; the hero buttons are Program, Slides and Photos;
`#submit` became "After the event" and no longer links to the registration or poster forms; `#editions`
leads with a "Next edition" card for NTN Days 2027 at IRISA, Rennes, and lists 2026 among the editions.
Earlier phases, for the record: talk submissions closed September 21, the final programme went online
September 23, registration and poster submissions closed October 9.

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

### Opening slides (`welcome.html`)

Standalone deck for the Day 1 opening (09:00-09:15), published at https://ntndays.space/welcome.html and
linked from the opening row of `#program`. Reveal.js 5.1.0 from cdnjs, the site's own palette and font,
9 slides, no build step. Keys: space or arrows to advance, `S` for speaker notes (the slot is split
between Vania, Juan and Peng there), `O` for the overview, `F` for fullscreen.

- `welcome.html?print-pdf` then print to PDF gives a shareable deck and an offline backup. Make one
  before the event: the deck pulls Reveal, Font Awesome and Google Fonts from CDNs and needs the network.
- Below 435 px wide (phones) Reveal switches by itself to its scroll view, where its own stylesheet
  paints `body.reveal-viewport` and each `.scroll-page` white. The `<style>` block overrides both, so
  the deck stays dark there; check `?view=scroll` after any Reveal upgrade.
- Slide 7 announces the GDR RSD working group. It carries a comment saying it can be dropped, since
  the announcement depends on the coordination converging during the event.
- Facts duplicated from the program (headcount, talk and poster counts, session titles, keynote titles)
  have to be updated here too when `#program` changes.

### Speaker slides (`slides/`)

Public download page at https://ntndays.space/slides/, linked from the nav, from the line under
`#program`, and talk by talk from every programme row (`.program-slides`). One PDF per talk, grouped
by session, plus a zip per session.

Two directories, and the split is the whole point:

| Where | What | Served? |
|---|---|---|
| `../2026-paris/slides-received/` | every file exactly as the speaker sent it: pptx, superseded versions, the decks presented from | no, it is outside the repository |
| `slides/` | only what may go online, plus the session zips and the page | yes, everything in it is a public URL |

`build-slides.py` copies from the first to the second. For each row of its `TALKS` table it picks the
`-public` version when the author sent one, otherwise the PDF presented from, and never a pptx. A talk
listed in `DO_NOT_PUBLISH` (keyed by day and time) is skipped, and any file in `slides/` that no row
claims any more is deleted, so a withdrawal is one edit plus a rebuild. An optional eighth field on a
row records what an author asked; it is printed when the script runs and never reaches the page.

Workflow when a deck arrives or an author answers:

1. drop the file in `../2026-paris/slides-received/`, named `d<day>-s<session>-<HHMM>-<speaker>-<topic>.pdf`
   (a cleared variant takes the same name plus `-public`);
2. add or edit its row in `TALKS`;
3. run `python3 build-slides.py` from the repository root;
4. add the link to the programme row in `index.html` by hand (`.program-slides`), if the talk had none.

The script warns about files listed in `TALKS` but missing from `slides-received`, and about decks in
`slides-received` that no row claims. Files starting with `_` are ignored, which is where the duplicate
Drive left behind lives.

Standing requests from authors:

- Omar El Marzougui (Day 1, 13:30): publish the public version only, the presented deck holds
  unpublished results.

### Photos (`gallery/`, `#photos`)

Drifting two-row photo band between `#program` and `#dates`, with a lightbox (arrows, Escape,
swipe), ported from the STINT site. Same split as the slides:

| Where | What | Served? |
|---|---|---|
| `../2026-paris/pics/` | the phone originals, HEIC with EXIF and GPS | no, outside the repository |
| `gallery/` | web copies (long edge 1800 px, metadata stripped), thumbnails 400 px tall, and `gallery.js` | yes |

`make-gallery.py` derives the second from the first with ImageMagick, incrementally: only new or
changed originals are converted, and gallery files whose original is gone are deleted. So curating
the set means adding or removing files in `../2026-paris/pics/` and running it again.

    python3 make-gallery.py            # incremental
    python3 make-gallery.py --force    # reconvert everything

Captions are optional: `../2026-paris/pics/captions.txt`, one `IMG_8300: caption text` per line.
The band sorts by EXIF capture time, shows the time under each photo in the lightbox, and the whole
section stays hidden when `gallery.js` is missing.

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
- [x] Venue practical info (`#venue`: amphitheatre Jean-Baptiste Say, access Y, lower level; transport;
      `cnam-campus-map.jpg`, the Cnam campus map provided by Peng on October 6, annotated with a red circle
      and arrow on the JBS amphitheatre; the unannotated original is `../2026-paris/WhatsApp Image 2026-10-06
      at 18.14.20.jpeg`)
- [ ] Sponsor list confirmation (`#sponsors` section; Cnam, GDR RSD, GDR IASIS, Inria already in)
- [x] Talk submission form link (was live in hero and `#submit`; removed September 21 when talk review started)
- [x] Registration form link (live in hero and `#submit`)
- [x] Poster submission form link (live in hero and `#submit`)
- [x] Poster form: responses spreadsheet linked
- [x] Poster form: forms.gle short link live in `index.html`
- [ ] Poster form: banner still shows the talk header image (cosmetic; the form closes October 9)
- [x] Registration responses spreadsheet linked
- [x] Program section (`#program`, final, September 23; 2 keynotes, 4 sessions, 21 talks, poster session, roundtable)
- [x] Program: roundtable theme and panel live ("NTN: time to move from theory to implementation",
      Fawaz, Baccelli, Caillouet, Bucaille; moderated by Pengwenlong Gu)
- [x] Program: Fawaz keynote title, abstract and bio live (October 6)
- [x] Program: Baccelli approved the bio and sent a revised abstract on October 9; the site and the
      `.ics` now carry his wording, and no text on the site is unapproved by its subject
- [ ] Program: session chairs not assigned
- [x] Program: poster session lists four posters (Filipe, Rolland, Srour, Maatouk) and Stefano
      Taborelli's demo, complete after the form closed on October 9; the heading says "Student posters
      and demos" because Maatouk is an M2 student
- [x] Opening slides: `welcome.html`, 9 slides, linked from the opening row of `#program`
      (export a PDF backup with `?print-pdf` before travelling)
- [x] `ntndays2026.ics`: one umbrella event plus 19 timed slots (Europe/Paris VTIMEZONE, CRLF); regenerate it
      by hand whenever `#program` changes

## Edition numbering

The site says "4th Edition": 2023 IRIT/ENSEEIHT Toulouse (Oct 19-20, per irit.fr) -> 2024 Grenoble (Oct 17-18, called "deuxieme edition" by GDR IASIS) -> 2025 LAAS Toulouse -> 2026 Paris.
If there was an earlier edition not documented online, bump the hero badge in `index.html`.
