#!/usr/bin/env python3
"""Builds hofmannmoritz.com (GitHub Pages serves the generated files as they are).

    python3 build.py

Writes index.html (German) and en/index.html, plus imprint and privacy policy in
both languages. Texts live here; the wedding section comes from src/hochzeit-de.html
and src/hochzeit-en.html, the markup of fastpal.com/hochzeit as of 2026-10-24, so it
looks the same as there (styles in assets/hochzeit.css, unchanged).
"""
import html
import pathlib

ROOT = pathlib.Path(__file__).parent
DOWNLOAD = "https://fastpal.com/download"
LINKEDIN = "https://www.linkedin.com/in/moritzhofmann/"

PROJEKTE = {
    "de": [
        {
            "titel": "farmula.de", "tab": "farmula.de", "domain": "www.farmula.de",
            "art": "Tiergesundheit für Landwirte, WooCommerce. Ich baue und betreue den Shop als E-Commerce-Manager der Farmula GmbH.",
            "bild": "farmula.jpg", "breite": 1280, "hoehe": 640,
            "alt": "Startseite von farmula.de mit der Herbstaktion für Kälberdecken",
            "punkte": [
                "Neues Theme nach einem Figma-Entwurf",
                "Kasse in Schritten und ein Warenkorb, der von der Seite einfährt",
                "Staffelpreise, Mehrfachpackungen und Aktions-Sets als eigenes Plugin",
                "Google-Shopping-Feed, Google Ads und ein Test mit Anzeigen in ChatGPT",
                "Tracking mit GA4, Google Tag Manager und Mixpanel",
                "Seiten-Cache für kurze Ladezeiten und ein Korrekturlauf über alle Seiten",
            ],
            "links": [("Shop ansehen", "https://www.farmula.de")],
        },
        {
            "titel": "topro.nl", "tab": "topro.nl", "domain": "www.topro.nl",
            "art": "Der niederländische Shop der Farmula B.V., WooCommerce.",
            "bild": "topro.jpg", "breite": 1280, "hoehe": 640,
            "alt": "Startseite von topro.nl mit der Herbstaktion",
            "punkte": [
                "Neu gestaltet, live seit Oktober 2026",
                "Umzug auf einen eigenen Server",
                "Neue Produkte und Unterkategorien, ohne dass sich Produkt-Adressen ändern (die QR-Codes in den Broschüren funktionieren weiter)",
                "Preise ohne Mehrwertsteuer für Geschäftskunden",
                "GA4 mit Kauf-Tracking vom Server und Spamschutz im Kontaktformular",
            ],
            "links": [("Shop ansehen", "https://www.topro.nl")],
        },
        {
            "titel": "gold4sms.de", "tab": "gold4sms.de", "domain": "www.gold4sms.de",
            "art": "Mein eigener Shop für Gamecards und Gutscheincodes, 2008 bis 2018.",
            "bild": "gold4sms-2016.jpg", "breite": 1280, "hoehe": 800,
            "alt": "Startseite von gold4sms.de im Mai 2016",
            "unterschrift": "Mai 2016, Design von 2011",
            "punkte": [
                "Aufgebaut und zehn Jahre selbst betrieben",
                "Über 80.000 Kunden",
                "1,2 Mio. Euro Jahresumsatz",
                "2018 verkauft",
            ],
            "links": [],
        },
        {
            "titel": "Hochzeitswebseiten", "tab": "Hochzeitsseiten", "domain": "lena-und-jonas.de",
            "art": "Einladungsseiten für Paare, von Hand gebaut, mit eigener .de-Adresse.",
            "bild": "hochzeitsseite.jpg", "breite": 1280, "hoehe": 640,
            "alt": "Der Umschlag der Beispielseite lena-und-jonas.de mit Wachssiegel, Calla und Perlen",
            "unterschrift": "Beispielseite mit erfundenem Paar",
            "punkte": [
                "Digitaler Umschlag, Zu- und Absage online, Gästeliste mit Export",
                "Nach der Feier laden die Gäste ihre Fotos hoch",
                "Zwei Gestaltungen: mit Fotos oder mit gemalten Aquarellen",
                "Die ersten Seiten laufen für echte Paare",
            ],
            "links": [("Beispiel ansehen", "https://lena-und-jonas.de"), ("Angebot weiter unten", "#hochzeit")],
        },
    ],
    "en": [
        {
            "titel": "farmula.de", "tab": "farmula.de", "domain": "www.farmula.de",
            "art": "Animal health for farmers, WooCommerce. I build and run the shop as e-commerce manager at Farmula GmbH.",
            "bild": "farmula.jpg", "breite": 1280, "hoehe": 640,
            "alt": "Home page of farmula.de with the autumn offer for calf blankets",
            "punkte": [
                "New theme built from a Figma design",
                "Checkout in steps and a cart that slides in from the side",
                "Volume pricing, multipacks and bundles as a plugin of my own",
                "Google Shopping feed, Google Ads and a test with ads in ChatGPT",
                "Tracking with GA4, Google Tag Manager and Mixpanel",
                "Page cache for fast loading and a proofreading pass over every page",
            ],
            "links": [("Visit the shop", "https://www.farmula.de")],
        },
        {
            "titel": "topro.nl", "tab": "topro.nl", "domain": "www.topro.nl",
            "art": "The Dutch shop of Farmula B.V., WooCommerce.",
            "bild": "topro.jpg", "breite": 1280, "hoehe": 640,
            "alt": "Home page of topro.nl with the autumn offer",
            "punkte": [
                "Redesigned, live since October 2026",
                "Moved to a server of its own",
                "New products and subcategories without changing product addresses (the QR codes in the brochures keep working)",
                "Prices without VAT for business customers",
                "GA4 with server-side purchase tracking and spam protection on the contact form",
            ],
            "links": [("Visit the shop", "https://www.topro.nl")],
        },
        {
            "titel": "gold4sms.de", "tab": "gold4sms.de", "domain": "www.gold4sms.de",
            "art": "My own shop for game cards and voucher codes, 2008 to 2018.",
            "bild": "gold4sms-2016.jpg", "breite": 1280, "hoehe": 800,
            "alt": "Home page of gold4sms.de in May 2016",
            "unterschrift": "May 2016, design from 2011",
            "punkte": [
                "Built it and ran it myself for ten years",
                "More than 80,000 customers",
                "€1.2 million annual revenue",
                "Sold in 2018",
            ],
            "links": [],
        },
        {
            "titel": "Wedding websites", "tab": "Wedding sites", "domain": "lena-und-jonas.de",
            "art": "Invitation sites for couples, built by hand, with their own domain.",
            "bild": "hochzeitsseite.jpg", "breite": 1280, "hoehe": 640,
            "alt": "The envelope of the sample site lena-und-jonas.de with wax seal, calla lilies and pearls",
            "unterschrift": "Sample site with a made-up couple",
            "punkte": [
                "Digital envelope, RSVP online, guest list with export",
                "After the party, guests upload their photos",
                "Two designs: with photos or with painted watercolours",
                "The first sites are live for real couples",
            ],
            "links": [("See the sample", "https://lena-und-jonas.de"), ("Offer further down", "#hochzeit")],
        },
    ],
}

TEXTE = {
    "de": {
        "titel": "Moritz Hofmann: Onlineshops und Hochzeitswebseiten",
        "beschreibung": "Moritz Hofmann aus Münster. Onlineshops seit 2008: farmula.de, topro.nl, gold4sms.de. Dazu handgebaute Hochzeitswebseiten.",
        "locale": "de_DE",
        "nav": "Bereiche",
        "tab_projekte": "E-Commerce",
        "tab_hochzeit": "Hochzeitswebseiten",
        "sprache": "Sprache",
        "h1": "Moritz Hofmann",
        "lead": "Ich baue und betreue Onlineshops, seit 2008. Hier steht, woran ich gearbeitet habe und was ich dort gemacht habe. Dazu baue ich Hochzeitswebseiten für Paare.",
        "mail": "E-Mail schreiben",
        "projekte": "Projekte",
        "gemacht": "Was ich gemacht habe",
        "fusszeile": "Hofmann GmbH, Nottuln",
        "impressum": "Impressum",
        "datenschutz": "Datenschutz",
        "app": "App herunterladen",
        "seiten": {"impressum": "impressum.html", "datenschutz": "datenschutz.html"},
        "startseite": "Zur Startseite",
    },
    "en": {
        "titel": "Moritz Hofmann: online shops and wedding websites",
        "beschreibung": "Moritz Hofmann from Münster, Germany. Online shops since 2008: farmula.de, topro.nl, gold4sms.de. Plus hand-built wedding websites.",
        "locale": "en_US",
        "nav": "Sections",
        "tab_projekte": "E-commerce",
        "tab_hochzeit": "Wedding websites",
        "sprache": "Language",
        "h1": "Moritz Hofmann",
        "lead": "I build and run online shops, since 2008. Here is what I have worked on and what I did there. I also build wedding websites for couples.",
        "mail": "Write an e-mail",
        "projekte": "Projects",
        "gemacht": "What I did",
        "fusszeile": "Hofmann GmbH, Nottuln, Germany",
        "impressum": "Imprint",
        "datenschutz": "Privacy",
        "app": "Download the app",
        "seiten": {"impressum": "imprint.html", "datenschutz": "privacy.html"},
        "startseite": "Back to the home page",
    },
}

IMPRESSUM = {
    "de": ("Impressum", """
<p>Angaben gemäß § 5 DDG:</p>
<p>Hofmann GmbH<br>Regerstr. 1<br>48301 Nottuln</p>
<p>Geschäftsführer: Moritz Hofmann<br>Registergericht: Amtsgericht Coesfeld, HRB 18001<br>USt-IdNr.: DE303275460</p>
<p>E-Mail: <a data-mail></a></p>
"""),
    "en": ("Imprint", """
<p>Information according to § 5 DDG (German Digital Services Act):</p>
<p>Hofmann GmbH<br>Regerstr. 1<br>48301 Nottuln<br>Germany</p>
<p>Managing director: Moritz Hofmann<br>Register court: Amtsgericht Coesfeld, HRB 18001<br>VAT ID: DE303275460</p>
<p>E-mail: <a data-mail></a></p>
"""),
}

DATENSCHUTZ = {
    "de": ("Datenschutzerklärung", """
<h2>1. Verantwortlicher</h2>
<p>Hofmann GmbH, Regerstr. 1, 48301 Nottuln, vertreten durch den Geschäftsführer Moritz Hofmann. E-Mail: <a data-mail></a></p>
<h2>2. Hosting und Auslieferung</h2>
<p>Diese Seite liegt bei GitHub Pages (GitHub Inc., USA) und wird über Cloudflare (Cloudflare Inc., USA) ausgeliefert. Beim Aufruf verarbeiten beide technisch nötige Daten wie IP-Adresse, Zeitpunkt, aufgerufene Seite und Browserkennung, um die Seite auszuliefern und vor Angriffen zu schützen. Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO. Beide Anbieter sind nach dem EU-US Data Privacy Framework zertifiziert.</p>
<h2>3. Keine Cookies, kein Tracking</h2>
<p>Diese Seite setzt keine Cookies und nutzt keine Analyse- oder Werbedienste. Schriften und Bilder liegen auf dieser Seite selbst, es werden keine Inhalte von Dritten nachgeladen.</p>
<h2>4. Anfrage über das Formular</h2>
<p>Wenn Sie uns über das Formular im Bereich Hochzeitswebseiten schreiben, verarbeiten wir Ihren Namen, Ihre Telefonnummer, freiwillig Ihre E-Mail-Adresse, freiwillig das Hochzeitsdatum und Ihre Nachricht. Das Formular sendet an einen Server der Hofmann GmbH unter fastpal.com (Vercel Inc., USA). Wir speichern die Angaben dort nicht: Sie gehen als E-Mail an Moritz Hofmann. Für den Versand nutzen wir Resend (Resend Inc., USA, Versand über Server in der EU), auf Grundlage von EU-Standardvertragsklauseln.</p>
<p>Zweck: Ihre Anfrage beantworten, auf Wunsch per WhatsApp unter der angegebenen Nummer. Rechtsgrundlage: Art. 6 Abs. 1 lit. b DSGVO (Anbahnung eines Vertrags). Wir löschen die Anfrage, wenn sie erledigt ist und kein Auftrag zustande kommt, spätestens nach sechs Monaten.</p>
<h2>5. E-Mail</h2>
<p>Schreiben Sie uns eine E-Mail, verarbeiten wir Ihre Angaben, um zu antworten (Art. 6 Abs. 1 lit. b oder f DSGVO), und löschen sie, wenn sie nicht mehr gebraucht werden und keine Aufbewahrungspflicht besteht.</p>
<h2>6. Ihre Rechte</h2>
<p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch. Schreiben Sie dazu an die Adresse oben. Sie können sich außerdem bei einer Datenschutz-Aufsichtsbehörde beschweren, für uns zuständig ist die Landesbeauftragte für Datenschutz und Informationsfreiheit Nordrhein-Westfalen.</p>
<p>Stand: Oktober 2026</p>
"""),
    "en": ("Privacy policy", """
<h2>1. Controller</h2>
<p>Hofmann GmbH, Regerstr. 1, 48301 Nottuln, Germany, represented by its managing director Moritz Hofmann. E-mail: <a data-mail></a></p>
<h2>2. Hosting and delivery</h2>
<p>This site is hosted on GitHub Pages (GitHub Inc., USA) and delivered through Cloudflare (Cloudflare Inc., USA). When you open it, both process technically necessary data such as IP address, time, page and browser, to deliver the site and protect it from attacks. Legal basis: Art. 6(1)(f) GDPR. Both providers are certified under the EU-US Data Privacy Framework.</p>
<h2>3. No cookies, no tracking</h2>
<p>This site sets no cookies and uses no analytics or advertising services. Fonts and images are served from this site itself, nothing is loaded from third parties.</p>
<h2>4. Requests through the form</h2>
<p>If you write to us through the form in the wedding websites section, we process your name, your phone number, optionally your e-mail address, optionally the wedding date and your message. The form sends to a server of Hofmann GmbH at fastpal.com (Vercel Inc., USA). We do not store the data there: it goes to Moritz Hofmann as an e-mail. For sending we use Resend (Resend Inc., USA, sending from servers in the EU), based on EU standard contractual clauses.</p>
<p>Purpose: answering your request, on WhatsApp at the number you gave if you wish. Legal basis: Art. 6(1)(b) GDPR (steps prior to a contract). We delete the request once it is settled and no order follows, at the latest after six months.</p>
<h2>5. E-mail</h2>
<p>If you send us an e-mail, we process your data to reply (Art. 6(1)(b) or (f) GDPR) and delete it once it is no longer needed and no retention duty applies.</p>
<h2>6. Your rights</h2>
<p>You have the right of access, rectification, erasure, restriction of processing, data portability and objection. Write to the address above. You can also complain to a data protection supervisory authority; ours is the State Commissioner for Data Protection and Freedom of Information of North Rhine-Westphalia.</p>
<p>As of October 2026</p>
"""),
}

e = html.escape


def asset(up, name):
    """Asset URL with a content hash, so a changed file gets a new URL (Cloudflare tells
    browsers to keep CSS and JS for 4 hours)."""
    import hashlib
    digest = hashlib.sha256((ROOT / "assets" / name).read_bytes()).hexdigest()[:10]
    return f"{up}assets/{name}?v={digest}"


def kopf(lang, titel, beschreibung, pfad, tiefe):
    up = "../" * tiefe
    t = TEXTE[lang]
    de_url = "https://hofmannmoritz.com/" + ("" if pfad == "index" else pfad_in("de", pfad))
    en_url = "https://hofmannmoritz.com/en/" + ("" if pfad == "index" else pfad_in("en", pfad))
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titel)}</title>
<meta name="description" content="{e(beschreibung)}">
<meta property="og:title" content="{e(titel)}">
<meta property="og:description" content="{e(beschreibung)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{t['locale']}">
<meta property="og:image" content="https://hofmannmoritz.com/assets/farmula.jpg">
<link rel="alternate" hreflang="de" href="{de_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="icon" href="data:,">
<link rel="stylesheet" href="{asset(up, 'fonts.css')}">
<link rel="stylesheet" href="{asset(up, 'tabs.css')}">
<link rel="stylesheet" href="{asset(up, 'hochzeit.css')}">
<link rel="stylesheet" href="{asset(up, 'site.css')}">
<script defer src="{asset(up, 'site.js')}"></script>
</head>
<body>
"""


def pfad_in(lang, seite):
    return TEXTE[lang]["seiten"][seite]


def navigation(lang, seite, tiefe):
    t = TEXTE[lang]
    # The language switch keeps the page: imprint <-> imprint, home <-> home.
    datei = {"de": "" if seite == "index" else pfad_in("de", seite), "en": "" if seite == "index" else pfad_in("en", seite)}
    de_link = ("../" if lang == "en" else "") + datei["de"] or "./"
    en_link = ("en/" if lang == "de" else "") + datei["en"] or "./"
    anker = "" if seite == "index" else "./"
    return f"""<nav class="st-tabs pf-nav" aria-label="{t['nav']}">
<div class="st-zeile">
<ul><li><a href="{anker}#projekte">{t["tab_projekte"]}</a></li><li><a href="{anker}#hochzeit">{t["tab_hochzeit"]}</a></li></ul>
<div class="st-sprachwahl" role="group" aria-label="{t['sprache']}">
<a href="{de_link}" hreflang="de" lang="de"{' aria-current="true"' if lang == 'de' else ''}>DE</a>
<a href="{en_link}" hreflang="en" lang="en"{' aria-current="true"' if lang == 'en' else ''}>EN</a>
</div>
</div>
</nav>
"""


def fuss(lang):
    t = TEXTE[lang]
    return f"""<footer class="pf-footer">
<div class="pf-wrap">
<p>{t['fusszeile']}</p>
<nav>
<a href="{pfad_in(lang, 'impressum')}">{t['impressum']}</a>
<a href="{pfad_in(lang, 'datenschutz')}">{t['datenschutz']}</a>
<a href="{DOWNLOAD}">{t['app']}</a>
</nav>
</div>
</footer>
</body>
</html>
"""


def projekt(p, i, up, t):
    """One project: a tab panel with the screenshot in a browser frame, the info below."""
    links = "".join(f'<a href="{e(href)}"{"" if href.startswith("#") else " target=\"_blank\" rel=\"noopener\""}>{e(text)}</a>' for text, href in p["links"])
    adresse = e(p["domain"]) + (f' <span class="pf-adresse-zusatz">· {e(p["unterschrift"])}</span>' if p.get("unterschrift") else "")
    return f"""<div class="pf-projekt" role="tabpanel" id="projekt-{i}" aria-labelledby="reiter-{i}">
<div class="pf-browser">
<div class="pf-leiste" aria-hidden="true"><span></span><span></span><span></span></div>
<p class="pf-adresse">{adresse}</p>
<img src="{up}assets/{p['bild']}" alt="{e(p['alt'])}" width="{p['breite']}" height="{p['hoehe']}"{' loading="lazy"' if i else ''}>
</div>
<div class="pf-info">
<div class="pf-was">
<h3>{e(p['titel'])}</h3>
<p class="pf-art">{e(p['art'])}</p>
{f'<p class="pf-links">{links}</p>' if links else ''}
</div>
<div class="pf-gemacht">
<p class="pf-label">{t['gemacht']}</p>
<ul>{''.join(f'<li>{e(x)}</li>' for x in p['punkte'])}</ul>
</div>
</div>
</div>"""


def startseite(lang):
    t = TEXTE[lang]
    tiefe = 1 if lang == "en" else 0
    up = "../" * tiefe
    projekte = PROJEKTE[lang]
    panels = "\n".join(projekt(p, i, up, t) for i, p in enumerate(projekte))
    reiter = "".join(
        f'<button type="button" role="tab" id="reiter-{i}" aria-controls="projekt-{i}" aria-selected="{"true" if i == 0 else "false"}"{"" if i == 0 else " tabindex=\"-1\""}>{e(p["tab"])}</button>'
        for i, p in enumerate(projekte)
    )
    hochzeit = (ROOT / "src" / f"hochzeit-{lang}.html").read_text()
    return (
        kopf(lang, t["titel"], t["beschreibung"], "index", tiefe)
        + navigation(lang, "index", tiefe)
        + f"""<div class="pf-root">
<header class="pf-wrap pf-hero">
<img class="pf-foto" src="{up}assets/moritz.jpg" alt="Moritz Hofmann" width="612" height="612">
<div class="pf-hero-text">
<h1>{t['h1']}</h1>
<p class="pf-lead">{e(t['lead'])}</p>
<p class="pf-kontakt"><a data-mail data-mail-label>{t['mail']}</a><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></p>
</div>
</header>
<section class="pf-wrap pf-projekte" id="projekte" aria-labelledby="projekte-titel" data-reiter>
<div class="pf-kopf">
<h2 id="projekte-titel">{t['projekte']}</h2>
<div class="pf-reiter" role="tablist" aria-labelledby="projekte-titel">{reiter}</div>
</div>
{panels}
</section>
</div>
<div class="hz-root" id="hochzeit" lang="{lang}" style="--hz-ground:#f6eee2;--hz-paper:#fbf4e8;--hz-band:#efe0cc;--hz-line:#d9c4a5;--hz-ink:#3a2f26;--hz-body:#5a4a3c;--hz-muted:#7a6248;--hz-gold:#9a7745;--hz-on-ink:#fbf4e8;min-height:0">
<main>
{hochzeit}</main>
</div>
"""
        + fuss(lang)
    )


def rechtsseite(lang, seite, titel, inhalt):
    tiefe = 1 if lang == "en" else 0
    t = TEXTE[lang]
    return (
        kopf(lang, f"{titel} | Moritz Hofmann", titel, seite, tiefe)
        + navigation(lang, seite, tiefe)
        + f"""<div class="pf-root"><main class="pf-wrap pf-recht">
<a class="pf-zurueck-link" href="./">{t['startseite']}</a>
<h1>{titel}</h1>
{inhalt}</main></div>
"""
        + fuss(lang)
    )


def main():
    for lang, ziel in (("de", ROOT), ("en", ROOT / "en")):
        ziel.mkdir(exist_ok=True)
        (ziel / "index.html").write_text(startseite(lang))
        titel, inhalt = IMPRESSUM[lang]
        (ziel / pfad_in(lang, "impressum")).write_text(rechtsseite(lang, "impressum", titel, inhalt))
        titel, inhalt = DATENSCHUTZ[lang]
        (ziel / pfad_in(lang, "datenschutz")).write_text(rechtsseite(lang, "datenschutz", titel, inhalt))
    print("built index.html, en/index.html and the legal pages")


if __name__ == "__main__":
    main()
