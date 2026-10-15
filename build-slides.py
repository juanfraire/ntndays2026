#!/usr/bin/env python3
"""Publish the speaker decks: copy the cleared files into slides/ and write slides/index.html.

Run from the repository root:

    python3 build-slides.py

Two directories, on purpose:

  ../2026-paris/slides-received   every file as the speakers sent it, outside the repository,
                                  so nothing here is ever served from ntndays.space
  slides/                         only what may go online, plus one zip per session and the
                                  page that lists them

Everything in slides/ is published the moment the repository is pushed, so a deck only lands
there when its author has agreed. For each talk the script publishes the "-public" version if
the author sent one, otherwise the PDF they presented from. Source files (pptx, superseded
versions) stay in slides-received. A talk listed in DO_NOT_PUBLISH is left out altogether, and
any file in slides/ that no row claims any more is deleted, so withdrawing a deck is one edit
plus a rebuild.

Naming: d<day>-s<session>-<HHMM>-<speaker>-<topic>.pdf, which sorts in programme order.
"""

import os
import shutil
import zipfile
from datetime import datetime

RECEIVED = os.path.join("..", "2026-paris", "slides-received")
PUBLISH = "slides"
ZIP_PREFIX = "ntndays2026-slides"

# (day, time) of talks we must not put online, whatever files we hold.
DO_NOT_PUBLISH = set()

TALKS = [
    (1, "Keynote", "09:15", "Hassan Fawaz", "Univity",
     "From Vision to Validation: Univity's 5G NTN Journey",
     "d1-keynote-0915-fawaz-univity.pdf"),
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
     ("d1-s2-1330-elmarzougui-chirp-waveform.pdf",
      "d1-s2-1330-elmarzougui-chirp-waveform-public.pdf"),
     "Publish the public version only. The presented deck holds unpublished results "
     "(author's request, 2026-10-15)."),
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
     "CERES, a satellite constellation network emulator",
     "d2-s3-1100-tauran-ceres.pdf"),
    (2, "Session 3", "11:15", "Juan A. Fraire", "Inria, INSA Lyon",
     "Ungrounded computing in low-Earth orbit",
     "d2-s3-1115-fraire-ungrounded-computing.pdf"),
    (2, "Session 4", "13:00", "Nicolas Gresset-Bourgeois", "TéSA",
     "On the optimal number of relays for nanosatellite swarm downlink",
     "d2-s4-1300-gresset-bourgeois-relays.pdf"),
    (2, "Session 4", "13:15", "Charlélie Pignol", "UGA, CSUG, LIG",
     "ThingSat: an in-orbit research vehicle for experimenting with satellite IoT",
     "d2-s4-1315-pignol-thingsat.pdf"),
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


def files_of(talk):
    """Every file a row claims, as a list, whether the table holds one name or several."""
    raw = talk[6]
    if not raw:
        return []
    return [raw] if isinstance(raw, str) else list(raw)


def publishable(talk):
    """The one file that goes online for this talk, or None.

    The "-public" version wins when the author sent one. pptx never goes online: it is a
    working file, and the PDF is what we show.
    """
    if (talk[0], talk[2]) in DO_NOT_PUBLISH:
        return None
    pdfs = [f for f in files_of(talk)
            if f.lower().endswith(".pdf") and os.path.exists(os.path.join(RECEIVED, f))]
    public = [f for f in pdfs if f.rsplit(".", 1)[0].endswith("-public")]
    return (public or pdfs or [None])[0]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(here)
    os.makedirs(PUBLISH, exist_ok=True)

    for f in (f for t in TALKS for f in files_of(t)):
        if not os.path.exists(os.path.join(RECEIVED, f)):
            print(f"WARNING: listed but not in slides-received: {f}")
    claimed = {f for t in TALKS for f in files_of(t)}
    on_disk = {f for f in os.listdir(RECEIVED)
               if f.lower().endswith((".pdf", ".pptx", ".ppt", ".key")) and not f.startswith("_")}
    for u in sorted(on_disk - claimed):
        print(f"WARNING: in slides-received but in no row: {u}")

    chosen = {}
    for talk in TALKS:
        f = publishable(talk)
        if f:
            chosen[(talk[0], talk[2])] = f
            src, dst = os.path.join(RECEIVED, f), os.path.join(PUBLISH, f)
            if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(src):
                shutil.copy2(src, dst)
                print(f"published {f}")

    # anything in slides/ that is no longer published goes, so a withdrawal really withdraws
    keep = set(chosen.values()) | {"index.html"}
    for f in sorted(os.listdir(PUBLISH)):
        if f in keep or f.endswith(".zip"):
            continue
        os.remove(os.path.join(PUBLISH, f))
        print(f"REMOVED from slides/: {f}")

    for note in (f"NOTE {t[2]} {t[3]}: {t[7]}" for t in TALKS if len(t) > 7 and t[7]):
        print(note)

    def slug(day, session):
        tail = session.lower().replace(" ", "").replace("session", "s")
        return f"d{day}-{tail}"

    for old in os.listdir(PUBLISH):
        if old.endswith(".zip"):
            os.remove(os.path.join(PUBLISH, old))
    groups = {}
    for talk in TALKS:
        f = chosen.get((talk[0], talk[2]))
        if f:
            groups.setdefault((talk[0], talk[1]), []).append(f)
    zip_of = {}
    for key, files in groups.items():
        name = f"{ZIP_PREFIX}-{slug(*key)}.zip"
        path = os.path.join(PUBLISH, name)
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            for f in files:
                z.write(os.path.join(PUBLISH, f), f)
        zip_of[key] = (name, human(os.path.getsize(path)), len(files))

    rows = []
    last_key = None
    for talk in TALKS:
        day, session, time, who, aff, title = talk[:6]
        f = chosen.get((day, time))
        if not f:
            continue
        key = (day, session)
        if key != last_key:
            if last_key is not None:
                rows.append("        </div>\n      </section>")
            if last_key is None or last_key[0] != day:
                rows.append(f'      <section>\n        <h2>{DAY_LABEL[day]}</h2>\n        <div class="rows">')
            else:
                rows.append('      <section>\n        <div class="rows">')
            name, size, count = zip_of[key]
            grab = (f'<a class="zip" href="{name}" download><span class="arrow">&darr;</span> '
                    f'{count} deck{"s" if count > 1 else ""} <span class="size">{size}</span></a>')
            rows.append(f'          <h3 class="sess">{session}{grab}</h3>')
            last_key = key
        size = human(os.path.getsize(os.path.join(PUBLISH, f)))
        rows.append(
            f'          <div class="row">\n'
            f'            <span class="time">{time}</span>\n'
            f'            <span class="meta"><b>{who}</b> <span class="aff">&middot; {aff}</span><br>'
            f'<span class="title">{title}</span></span>\n'
            f'            <a class="dl" href="{f}"><span class="arrow">&darr;</span> PDF '
            f'<span class="size">{size}</span></a>\n'
            f'          </div>'
        )
    rows.append("        </div>\n      </section>")

    html = TEMPLATE.format(
        rows="\n".join(rows),
        got=len(chosen),
        total=len([t for t in TALKS if t[1] != "Keynote"]) + 2,
        updated=datetime.now().strftime("%d %B %Y"),
    )
    with open(os.path.join(PUBLISH, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"\nslides/index.html written: {len(chosen)} decks online")
    for key in sorted(zip_of):
        name, size, count = zip_of[key]
        print(f"  {name}: {count} decks, {size}")


TEMPLATE = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NTN Days 2026 | Slides</title>
    <meta name="description" content="Slides from the talks of NTN Days 2026, October 13-14, 2026, Cnam, Paris.">
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

        .note {{
            display: inline-block;
            margin-top: 4px;
            padding: 2px 8px;
            border-radius: 6px;
            background: rgba(249, 115, 22, 0.12);
            border: 1px solid rgba(194, 65, 12, 0.45);
            color: var(--orbit-300);
            font-size: 0.78rem;
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
            <h1>Slides</h1>
            <p class="sub">NTN Days 2026 &middot; Cnam, Paris &middot; 13&ndash;14 October 2026</p>
            <p class="count"><b>{got}</b> presentations, shared with the agreement of their authors.
                Each session can also be downloaded as a single zip.</p>
        </header>

{rows}

        <footer>
            Updated {updated}. Back to the <a href="../#program">programme</a>.
            Speakers: write to <a href="mailto:juan.fraire@inria.fr">juan.fraire@inria.fr</a> to have
            your slides replaced or taken down.
        </footer>
    </div>
</body>

</html>
"""

if __name__ == "__main__":
    main()
