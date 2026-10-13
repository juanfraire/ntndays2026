#!/usr/bin/env python3
"""Rebuild slides/index.html and slides/ntndays2026-slides.zip from the PDFs in slides/.

Run it from the repository root after dropping new decks into slides/:

    python3 build-slides.py

Naming convention for the PDFs: d<day>-s<session>-<HHMM>-<speaker>-<topic>.pdf, which
sorts in program order. Add the file name to TALKS below so the page picks it up.
"""

import os
import zipfile
from datetime import datetime

SLIDES = "slides"
ZIP_PREFIX = "ntndays2026-slides"

# (day, session, time, speaker, affiliation, title, file or None)
# The last field takes one file name, or a tuple of them when a speaker also sends the pptx
# they will actually present from.
TALKS = [
    (1, "Keynote", "09:15", "Hassan Fawaz", "Univity",
     "From Vision to Validation: Univity's 5G NTN Journey", None),
    (1, "Session 1", "10:30", "Flavien Ronteix", "EC-JRC",
     "IRIS², a catalyst for 5G NTN and European technological sovereignty",
     "d1-s1-1030-ronteix-iris2.pdf"),
    (1, "Session 1", "10:45", "Nicola Accettura", "LAAS-CNRS",
     "Standalone standard satellite-aided Internet connectivity",
     "d1-s1-1045-accettura-standalone-connectivity.pdf"),
    (1, "Session 1", "11:00", "Ali Khalesi", "IPSA, LINCS",
     "Beyond coverage: how mega-constellations will shape the future of non-terrestrial networks",
     "d1-s1-1100-khalesi-mega-constellations.pdf"),
    (1, "Session 1", "11:15", "Jihane Lghoury", "IRIT, Ericsson",
     "Interference-aware beam hopping scheduling for LEO satellite networks",
     ("d1-s1-1115-lghoury-beam-hopping.pdf", "d1-s1-1115-lghoury-beam-hopping.pptx")),
    (1, "Session 1", "11:30", "Ashutosh Balakrishnan", "Télécom Paris",
     "Doppler-Shannon association framework for non-terrestrial networks",
     "d1-s1-1130-balakrishnan-doppler-shannon.pdf"),
    (1, "Session 1", "11:45", "Graeme Young", "SKAO",
     "Radio astronomy protection for direct-to-device applications",
     "d1-s1-1145-young-radio-astronomy.pdf"),
    (1, "Session 2", "13:30", "Omar El Marzougui", "Toulouse INP, IRIT",
     "Chirp-based waveform design for next generation non-terrestrial networks",
     "d1-s2-1330-elmarzougui-chirp-waveform.pdf"),
    (1, "Session 2", "13:45", "Antony Pottier", "CEA-Leti",
     "Study of ODDM on NTN channels for LEO satellite communications",
     "d1-s2-1345-pottier-oddm.pdf"),
    (1, "Session 2", "14:00", "Vincent Deslandes", "Kinéis",
     "Kinéis wide area network for satellite IoT: performance and protocol optimisation",
     ("d1-s2-1400-deslandes-kiwan.pdf", "d1-s2-1400-deslandes-kiwan.pptx")),
    (1, "Session 2", "14:15", "Antonin Le Floch", "Kinéis",
     "NTN-IoT performance survey: from simulation to in-orbit testing",
     ("d1-s2-1415-lefloch-ntn-iot-survey.pdf", "d1-s2-1415-lefloch-ntn-iot-survey.pptx")),
    (1, "Session 2", "14:30", "Carlos Fernandez Hernandez", "INSA Lyon, Inria",
     "From ground to space: efficient downlink scheduling for direct-to-satellite LoRaWAN",
     "d1-s2-1430-fernandez-hernandez-downlink.pdf"),
    (2, "Keynote", "09:00", "François Baccelli", "Inria, Télécom Paris, LINCS",
     "Research on Non-Terrestrial Networks: Design Tools, Regulation, and Cooperation", None),
    (2, "Session 3", "10:15", "Emanuele Mengoli", "Télécom Paris, Inria",
     "Handover dynamics in LEO non-terrestrial networks: a stochastic-geometry view",
     "d2-s3-1015-mengoli-handover-dynamics.pdf"),
    (2, "Session 3", "10:30", "Sanjoy Kumar Jhawar", "Télécom Paris, Inria",
     "Seasonal statistics of Shannon rate in a dynamical Poisson-Voronoi cell",
     "d2-s3-1030-jhawar-shannon-rate.pdf"),
    (2, "Session 3", "10:45", "Louis Barbier", "ISAE-SUPAERO",
     "SatComTopology and SatGoNetEm: a flexible platform for dynamic satellite network experimentation",
     "d2-s3-1045-barbier-satcomtopology.pdf"),
    (2, "Session 3", "11:00", "Bastien Tauran", "Viveris Technologies",
     "CERES, a satellite constellation network emulator", None),
    (2, "Session 3", "11:15", "Juan A. Fraire", "Inria, INSA Lyon",
     "Ungrounded computing in low-Earth orbit",
     "d2-s3-1115-fraire-ungrounded-computing.pdf"),
    (2, "Session 4", "13:00", "Nicolas Gresset-Bourgeois", "TéSA",
     "On the optimal number of relays for nanosatellite swarm downlink",
     "d2-s4-1300-gresset-bourgeois-relays.pdf"),
    (2, "Session 4", "13:15", "Charlélie Pignol", "UGA, CSUG, LIG",
     "ThingSat: an in-orbit research vehicle for experimenting with satellite IoT", None),
    (2, "Session 4", "13:30", "Sarah Theoulle", "LIRMM",
     "CSPCL: a stepwise, non-disruptive transition to Delay-Tolerant Networking",
     "d2-s4-1330-theoulle-cspcl.pdf"),
    (2, "Session 4", "13:45", "Alice Le Bihan", "INSA Lyon",
     "A tool suite towards a Solar System Internet digital twin",
     "d2-s4-1345-lebihan-ssi-digital-twin.pdf"),
    (2, "Session 4", "14:00", "Alejandro Matias Toledo", "National University of Córdoba",
     "Lifespan-aware contact plan design for interplanetary free-space optical networks",
     "d2-s4-1400-toledo-contact-plan.pdf"),
]

DAY_LABEL = {1: "Day 1 &middot; Tuesday 13 October", 2: "Day 2 &middot; Wednesday 14 October"}


def human(nbytes):
    mb = nbytes / 1024 / 1024
    return f"{mb:.1f} MB" if mb >= 1 else f"{nbytes / 1024:.0f} KB"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(here)

    def files_of(talk):
        """Every file a row claims, as a list, whether the table holds one name or several."""
        raw = talk[6]
        if not raw:
            return []
        return [raw] if isinstance(raw, str) else list(raw)

    listed = [f for t in TALKS for f in files_of(t)]
    for f in listed:
        if not os.path.exists(os.path.join(SLIDES, f)):
            print(f"WARNING: listed but not on disk: {f}")

    on_disk = {f for f in os.listdir(SLIDES) if f.lower().endswith((".pdf", ".pptx", ".ppt", ".key"))}
    for u in sorted(on_disk - set(listed)):
        print(f"WARNING: on disk but not in TALKS: {u}")

    present = [t for t in TALKS
               if any(os.path.exists(os.path.join(SLIDES, f)) for f in files_of(t))]

    def slug(day, session):
        """d1-s1, d2-keynote, ... matching the file name prefix of that group."""
        tail = session.lower().replace(" ", "").replace("session", "s")
        return f"d{day}-{tail}"

    # one zip per session, rebuilt from scratch every time
    for old in os.listdir(SLIDES):
        if old.endswith(".zip"):
            os.remove(os.path.join(SLIDES, old))
    zips = {}
    for talk in present:
        key = (talk[0], talk[1])
        zips.setdefault(key, []).extend(
            f for f in files_of(talk) if os.path.exists(os.path.join(SLIDES, f)))
    zip_of = {}
    for key, files in zips.items():
        name = f"{ZIP_PREFIX}-{slug(*key)}.zip"
        path = os.path.join(SLIDES, name)
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            for f in files:
                z.write(os.path.join(SLIDES, f), f)
        zip_of[key] = (name, human(os.path.getsize(path)), len(files))

    rows = []
    last_key = None
    for talk in TALKS:
        day, session, time, who, aff, title = talk[:6]
        key = (day, session)
        if key != last_key:
            if last_key is not None and last_key[0] != day:
                rows.append("        </div>\n      </section>")
                rows.append(f'      <section>\n        <h2>{DAY_LABEL[day]}</h2>\n        <div class="rows">')
            elif last_key is None:
                rows.append(f'      <section>\n        <h2>{DAY_LABEL[day]}</h2>\n        <div class="rows">')
            if key in zip_of:
                name, size, count = zip_of[key]
                grab = (f'<a class="zip" href="{name}" download><span class="arrow">&darr;</span> '
                        f'{count} file{"s" if count > 1 else ""} <span class="size">{size}</span></a>')
            else:
                grab = ""
            rows.append(f'          <h3 class="sess">{session}{grab}</h3>')
            last_key = key
        have = [f for f in files_of(talk) if os.path.exists(os.path.join(SLIDES, f))]
        if have:
            links = []
            for f in have:
                kind = f.rsplit(".", 1)[-1].upper()
                size = human(os.path.getsize(os.path.join(SLIDES, f)))
                links.append(f'<a class="dl" href="{f}" download>'
                             f'<span class="arrow">&darr;</span> {kind} <span class="size">{size}</span></a>')
            action = f'<span class="files">{"".join(links)}</span>'
            state = "has"
        else:
            action = '<span class="pending">not received</span>'
            state = "no"
        rows.append(
            f'          <div class="row {state}">\n'
            f'            <span class="time">{time}</span>\n'
            f'            <span class="meta"><b>{who}</b> <span class="aff">&middot; {aff}</span><br>'
            f'<span class="title">{title}</span></span>\n'
            f'            {action}\n'
            f'          </div>'
        )
    rows.append("        </div>\n      </section>")

    html = TEMPLATE.format(
        rows="\n".join(rows),
        got=len(present),
        total=len([t for t in TALKS if t[1] != "Keynote"]) + 2,
        updated=datetime.now().strftime("%d %B %Y, %H:%M"),
    )
    with open(os.path.join(SLIDES, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"slides/index.html written: {len(present)} decks")
    for key in sorted(zip_of):
        name, size, count = zip_of[key]
        print(f"  {name}: {count} files, {size}")


TEMPLATE = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NTN Days 2026 | Speaker slides</title>
    <meta name="robots" content="noindex, nofollow">
    <link rel="icon" type="image/png" sizes="96x96" href="../favicon-96x96.png">
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap"
        rel="stylesheet">
    <style>
        :root {{
            --orbit-300: #fdba74;
            --orbit-400: #fb923c;
            --orbit-500: #f97316;
            --nebula-400: #a78bfa;
            --ink: #030712;
            --panel: #0b1220;
            --line: #1f2937;
            --text: #e5e7eb;
            --muted: #9ca3af;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            padding: 0 16px 64px;
            background: var(--ink);
            color: var(--text);
            font-family: 'Space Grotesk', system-ui, sans-serif;
            line-height: 1.5;
        }}

        .wrap {{
            max-width: 940px;
            margin: 0 auto;
        }}

        header {{
            padding: 48px 0 24px;
            border-bottom: 1px solid var(--line);
        }}

        h1 {{
            margin: 0 0 6px;
            font-size: 2rem;
            background: linear-gradient(90deg, var(--orbit-400), var(--nebula-400));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }}

        .sub {{
            margin: 0;
            color: var(--muted);
            font-size: 0.95rem;
        }}

        .notice {{
            margin: 20px 0 0;
            padding: 12px 14px;
            border: 1px solid rgba(194, 65, 12, 0.5);
            background: rgba(249, 115, 22, 0.08);
            border-radius: 10px;
            font-size: 0.85rem;
            color: #fed7aa;
        }}


        .count {{
            color: var(--muted);
            font-size: 0.85rem;
            margin: 20px 0 0;
        }}

        .count b {{
            color: var(--text);
        }}

        h2 {{
            margin: 44px 0 4px;
            font-size: 1.3rem;
        }}

        .sess {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            flex-wrap: wrap;
            margin: 26px 0 8px;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            color: var(--orbit-300);
            font-weight: 600;
        }}

        .zip {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 7px 16px;
            border-radius: 999px;
            background: linear-gradient(90deg, #ea580c, #f97316);
            color: #fff;
            text-decoration: none;
            text-transform: none;
            letter-spacing: 0;
            font-size: 0.82rem;
        }}

        .zip:hover {{
            opacity: 0.9;
        }}

        .zip .size {{
            color: rgba(255, 255, 255, 0.75);
        }}

        .row {{
            display: grid;
            grid-template-columns: 62px 1fr auto;
            gap: 14px;
            align-items: center;
            padding: 12px 14px;
            border: 1px solid var(--line);
            border-radius: 12px;
            background: var(--panel);
            margin-bottom: 8px;
        }}

        .row.no {{
            background: transparent;
            border-style: dashed;
            opacity: 0.6;
        }}

        .time {{
            color: var(--orbit-300);
            font-weight: 600;
            font-variant-numeric: tabular-nums;
        }}

        .aff {{
            color: var(--muted);
            font-weight: 400;
        }}

        .title {{
            color: var(--muted);
            font-size: 0.88rem;
        }}

        .files {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            justify-content: flex-end;
        }}

        .dl {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 14px;
            border-radius: 999px;
            border: 1px solid rgba(194, 65, 12, 0.6);
            color: var(--orbit-300);
            text-decoration: none;
            font-size: 0.85rem;
            white-space: nowrap;
        }}

        .dl:hover {{
            background: rgba(249, 115, 22, 0.12);
        }}

        .arrow {{
            font-size: 1rem;
        }}

        .size {{
            color: var(--muted);
        }}

        .pending {{
            color: var(--muted);
            font-size: 0.82rem;
            white-space: nowrap;
        }}

        footer {{
            margin-top: 48px;
            padding-top: 18px;
            border-top: 1px solid var(--line);
            color: var(--muted);
            font-size: 0.82rem;
        }}

        footer a {{
            color: var(--orbit-400);
        }}

        @media (max-width: 640px) {{
            .row {{
                grid-template-columns: 54px 1fr;
            }}

            .files,
            .pending {{
                grid-column: 2;
                justify-self: start;
                justify-content: flex-start;
            }}
        }}
    </style>
</head>

<body>
    <div class="wrap">
        <header>
            <h1>Speaker slides</h1>
            <p class="sub">NTN Days 2026 &middot; Cnam, Paris &middot; 13&ndash;14 October 2026</p>
            <p class="notice">Working page for the organizers and the presentation desk. It is not linked
                from the website and not indexed. Decks stay here until their authors agree to have them
                published.</p>
            <p class="count"><b>{got} of {total}</b> decks received. Each session has its own zip next
                to its heading, so the desk can pull one session at a time.</p>
        </header>

{rows}

        <footer>
            Updated {updated}. Back to the <a href="../">programme</a>.
        </footer>
    </div>
</body>

</html>
"""

if __name__ == "__main__":
    main()
