#!/usr/bin/env python3
"""Builds the Divorce Prep GitHub Pages site (landing + privacy + support + 8 SEO pages)."""
import json
import os

OUT = os.path.dirname(os.path.abspath(__file__))
APP_NAME = "Divorce Prep"
APPSTORE_URL = "https://apps.apple.com/app/id0000000000"  # TODO: replace with real App Store ID
DOMAIN = "https://jerryjrdev.github.io/divorce-prep"

CSS = """
:root{--cream:#FAF7F2;--teal:#1E5A50;--teal-dark:#16463F;--sage:#7A9A8B;--sand:#C4B5A5;--ink:#2A2A26;--gray:#6B6B64;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Plus Jakarta Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--cream);color:var(--ink);line-height:1.7;}
.wrap{max-width:760px;margin:0 auto;padding:0 20px;}
header{padding:56px 0 8px;text-align:center;}
.logo{display:inline-flex;align-items:center;gap:10px;font-weight:800;color:var(--teal);font-size:1.35rem;letter-spacing:-.02em;}
.logo .mark{width:34px;height:34px;border-radius:50%;background:var(--teal);color:#fff;display:inline-flex;align-items:center;justify-content:center;font-size:1rem;}
main{padding:24px 0 48px;}
h1{font-size:2.4rem;line-height:1.15;letter-spacing:-.03em;color:var(--teal);margin:24px 0 12px;}
.lede{font-size:1.15rem;color:var(--gray);margin-bottom:28px;}
h2{font-size:1.45rem;color:var(--teal);margin:36px 0 10px;letter-spacing:-.01em;}
p{margin:0 0 14px;}
ul,ol{margin:0 0 16px 22px;}
li{margin-bottom:8px;}
.card{background:#fff;border-radius:20px;padding:22px 24px;box-shadow:0 2px 14px rgba(30,90,80,.08);margin:0 0 18px;}
.chip{display:inline-block;background:#E4EFEA;color:var(--teal);border-radius:999px;padding:4px 14px;font-size:.85rem;font-weight:600;margin:0 6px 8px 0;}
.cta{background:var(--teal);color:#fff;text-align:center;border-radius:999px;padding:16px 34px;font-weight:700;font-size:1.05rem;text-decoration:none;display:inline-block;margin:12px 0 4px;}
.cta:hover{background:var(--teal-dark);}
.cta-wrap{text-align:center;margin:34px 0;}
.muted{color:var(--gray);font-size:.92rem;}
footer{border-top:1px solid #E5DED2;margin-top:40px;padding:26px 0 48px;text-align:center;font-size:.88rem;color:var(--gray);}
footer a{color:var(--teal);text-decoration:none;margin:0 10px;}
table{width:100%;border-collapse:collapse;margin:0 0 16px;}
th,td{text-align:left;padding:9px 10px;border-bottom:1px solid #EAE4D8;font-size:.95rem;}
th{color:var(--teal);}
.qa{margin-bottom:8px;}
.qa strong{color:var(--teal);}
.badge{display:inline-flex;align-items:center;gap:8px;background:#fff;border:1px solid #E5DED2;border-radius:999px;padding:8px 20px;font-weight:700;color:var(--teal);text-decoration:none;}
.badge:hover{border-color:var(--teal);}
"""

HEADER = f"""
<header><div class="wrap">
<span class="logo"><span class="mark">&#9829;</span>{APP_NAME}</span>
</div></header>
"""

FOOTER = f"""
<footer><div class="wrap">
<a href="{DOMAIN}/">Home</a><a href="{DOMAIN}/privacy.html">Privacy</a><a href="{DOMAIN}/support.html">Support</a><a href="{DOMAIN}/california-divorce-checklist.html">CA Checklist</a><a href="{DOMAIN}/germany-divorce-checklist.html">DE Checklist</a>
<p class="muted" style="margin-top:14px">{APP_NAME} provides general information and organizational tools, not legal advice. &#169; 2026 Divorce Prep.</p>
</div></footer>
"""


def jsonld(extra=None):
    data = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Divorce Prep: Plan & Organizer",
        "operatingSystem": "iOS 17+",
        "applicationCategory": "FinanceApplication",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "description": "Free iOS app that turns divorce into a step-by-step plan: jurisdiction checklists for the US and Europe, asset and debt vault, expense tracking, settlement scenarios, and lawyer export. Private by design.",
    }
    if extra:
        data.update(extra)
    return json.dumps(data)


def page(path, title, meta, h1, lede, body_html, extra_jsonld=None):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="{DOMAIN}/{path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta}">
<meta property="og:type" content="website">
<meta property="og:url" content="{DOMAIN}/{path}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">{jsonld(extra_jsonld)}</script>
</head>
<body>
{HEADER}
<main><div class="wrap">
<h1>{h1}</h1>
<p class="lede">{lede}</p>
{body_html}
<div class="cta-wrap">
<a class="badge" href="{APPSTORE_URL}">&#8595; Download {APP_NAME} — start your 7-day free trial</a>
</div>
</div></main>
{FOOTER}
</body>
</html>
"""
    with open(os.path.join(OUT, path), "w") as f:
        f.write(html)
    print("wrote", path)


# ----------------------------------------------------------------------------
# 1. Landing page
# ----------------------------------------------------------------------------
landing_body = """
<div class="card">
<h2 style="margin-top:0">A step-by-step plan for your finances, documents, and deadlines</h2>
<p>Divorce is one of life's hardest transitions. {app} turns the chaos into a clear plan: a checklist built from your local family law, a vault for every asset and debt, expense tracking, settlement scenarios you can test before you sign, and a one-tap export of everything your lawyer needs.</p>
<p><strong>Private by design.</strong> Everything stays on your device, locked with Face ID. No accounts. No ads. No cloud.</p>
</div>
<h2>Everything, organized</h2>
<ul>
<li><strong>Jurisdiction checklists</strong> — California, Germany, France, England &amp; Wales, Spain, and Italy. Each checklist is built from local family law: waiting periods, required forms, deadlines.</li>
<li><strong>Asset &amp; debt vault</strong> — photograph, tag, and value every asset. Mark each one marital or separate. See your net worth at a glance.</li>
<li><strong>Expense tracker</strong> — log spending as marital or separate while your case is open.</li>
<li><strong>Settlement scenarios</strong> — test 50/50, 60/40, or any split you want. See what each of you keeps and estimated support.</li>
<li><strong>Document hub</strong> — statements, forms, and photos in one place, exportable as a ZIP bundle for your lawyer.</li>
<li><strong>Attorney prep</strong> — a consultation question bank, meeting notes, and court date reminders.</li>
</ul>
<h2>Frequently asked questions</h2>
<div class="qa"><strong>How much does Divorce Prep cost?</strong> Start with a 7-day free trial — no charges if you cancel during the trial. After that, choose $14.99 per week or $150.99 per year. Cancel anytime.</div>
<div class="qa"><strong>Is my data private?</strong> Yes. All data is stored only on your device. There are no accounts, no cloud sync, and no analytics. You can optionally lock the app with Face ID.</div>
<div class="qa"><strong>Which countries are supported?</strong> The United States (California) and Europe: Germany, France, England &amp; Wales, Spain, and Italy. More jurisdictions are coming.</div>
<div class="qa"><strong>Does the app replace a lawyer?</strong> No. Divorce Prep provides general information and organizational tools, not legal advice. Always consult a qualified family law professional for your situation.</div>
<h2>Checklists by jurisdiction</h2>
<p>
<a class="chip" href="{domain}/california-divorce-checklist.html">California</a>
<a class="chip" href="{domain}/germany-divorce-checklist.html">Germany</a>
<a class="chip" href="{domain}/france-divorce-checklist.html">France</a>
<a class="chip" href="{domain}/uk-divorce-checklist.html">England &amp; Wales</a>
<a class="chip" href="{domain}/spain-divorce-checklist.html">Spain</a>
<a class="chip" href="{domain}/italy-divorce-checklist.html">Italy</a>
</p>
<h2>From the blog</h2>
<p>
<a class="chip" href="{domain}/blog/how-to-prepare-financially-for-divorce.html">How to Prepare Financially for Divorce</a>
<a class="chip" href="{domain}/blog/divorce-financial-checklist.html">The Divorce Financial Checklist</a>
</p>
""".format(app=APP_NAME, domain=DOMAIN)

page(
    "index.html",
    "Divorce Prep — Divorce Checklist & Financial Organizer App",
    "iOS app that turns divorce into a step-by-step plan: jurisdiction checklists for the US & Europe, asset vault, expense tracking, settlement scenarios, and lawyer export. Private by design. Start with a 7-day free trial.",
    "The calm way through divorce.",
    "A personal plan for your finances, documents, and deadlines — step by step. Private, and on your device.",
    landing_body,
)

# ----------------------------------------------------------------------------
# 2. Privacy policy
# ----------------------------------------------------------------------------
privacy_body = """
<div class="card">
<p><strong>Last updated:</strong> October 21, 2026</p>
<p>Divorce Prep stores all data locally on your device. We do not collect, transmit, store, or have access to any information you enter into the app.</p>
</div>
<h2>What we collect: nothing</h2>
<p>There are no analytics, no advertising SDKs, no tracking pixels, and no accounts. The app does not connect to any server.</p>
<h2>Where your data lives</h2>
<p>All checklists, assets, expenses, documents, and notes are stored on your device only. Data leaves your device only when you explicitly export or share it yourself — for example, the JSON backup file or the lawyer export bundle. You choose where those files go.</p>
<h2>Deleting the app deletes your data</h2>
<p>Uninstalling Divorce Prep removes all data stored by the app. There is no copy anywhere else, because no copy ever leaves your device.</p>
<h2>Biometric authentication</h2>
<p>Face ID and Touch ID authentication is performed by the operating system. Biometric data never reaches the app and is never stored by the app.</p>
<h2>Children</h2>
<p>This app is intended for adults managing their own legal and financial affairs.</p>
<h2>Contact</h2>
<p>Questions about this policy: open an issue at github.com/jerryjrdev/divorce-prep or use the contact form on the <a href="{domain}/support.html">support page</a>.</p>
""".format(domain=DOMAIN)

page(
    "privacy.html",
    "Privacy Policy — Divorce Prep",
    "Divorce Prep stores all data locally on your device. No accounts, no cloud, no analytics. Read the full privacy policy.",
    "Privacy Policy",
    "Private by design — everything stays on your device.",
    privacy_body,
)

# ----------------------------------------------------------------------------
# 3. Support
# ----------------------------------------------------------------------------
support_body = """
<h2>Before you contact us</h2>
<ul>
<li><strong>Exporting for your lawyer?</strong> Open Documents &rarr; Export and choose "Create ZIP bundle".</li>
<li><strong>Backing up?</strong> Settings &rarr; Data &rarr; Export backup (JSON). Keep the file somewhere safe — the app only stores data on your device.</li>
<li><strong>Changing jurisdiction?</strong> Onboarding or Settings lets you switch; your checklist updates to local family law.</li>
</ul>
<h2>Contact</h2>
<div class="card">
<p>Open an issue at <strong>github.com/jerryjrdev/divorce-prep</strong> — that is the fastest way to reach us.</p>
<p class="muted">We aim to respond within a few days. Please do not include sensitive personal information in issues; describe your question in general terms.</p>
</div>
<h2>Legal note</h2>
<p class="muted">Divorce Prep provides general information and organizational tools, not legal advice. For advice about your specific case, consult a qualified family law professional in your jurisdiction.</p>
""".format(domain=DOMAIN)

page(
    "support.html",
    "Support — Divorce Prep",
    "Help and contact information for the Divorce Prep app: exports, backups, jurisdiction switching, and how to reach us.",
    "Support",
    "Answers for exports, backups, and getting help.",
    support_body,
)

# ----------------------------------------------------------------------------
# 4-9. Jurisdiction pages
# ----------------------------------------------------------------------------
JURISDICTIONS = {
    "california-divorce-checklist.html": {
        "title": "California Divorce Checklist 2026: FL-100 to Final Judgment",
        "meta": "The complete California divorce checklist for 2026: FL-100 petition, 6-month waiting period, financial disclosures, community property, and final judgment — step by step.",
        "h1": "California Divorce Checklist 2026",
        "lede": "Everything you need to file, disclose, and finalize a divorce in California — from the FL-100 petition to the final judgment.",
        "body": """
<h2>How divorce works in California</h2>
<p>California is a no-fault state: you file for "irreconcilable differences" and the court does not assign blame. California is also a <strong>community property</strong> state — assets and debts acquired during the marriage are generally split 50/50.</p>
<p>There is a mandatory <strong>6-month waiting period</strong> from the date your spouse is served (or files a response) before the divorce can be finalized, even if you both agree on everything.</p>
<h2>The California divorce checklist</h2>
<ol>
<li><strong>Gather personal identification documents</strong> — IDs, marriage certificate, Social Security numbers for both spouses.</li>
<li><strong>Complete the petition (FL-100)</strong> and summons (FL-110). File them at your county superior court and pay the filing fee (or request a fee waiver, FW-001).</li>
<li><strong>Serve your spouse</strong> — someone over 18 who is not you must deliver the papers; then file the proof of service (FL-115). Your spouse has 30 days to respond (FL-120).</li>
<li><strong>File Preliminary Declarations of Disclosure</strong> — each spouse must exchange an FL-140, income and expense declaration (FL-150), and a schedule of assets and debts (FL-142) within 60 days of filing.</li>
<li><strong>Inventory community and separate property</strong> — everything acquired during marriage vs. before marriage, by gift, or by inheritance.</li>
<li><strong>Track expenses</strong> while the case is open, marking marital vs. separate spending.</li>
<li><strong>Draft your settlement</strong> — asset split, spousal support, and any parenting plan. Use a marital settlement agreement (or form FL-180 paperwork for default).</li>
<li><strong>Dividing retirement accounts</strong> usually requires a QDRO filed with the court.</li>
<li><strong>Wait out the 6-month clock</strong> from service.</li>
<li><strong>File the judgment (FL-180)</strong> and receive the stamped final judgment.</li>
</ol>
<h2>Key deadlines</h2>
<table>
<tr><th>Step</th><th>Deadline</th></tr>
<tr><td>Respond to petition</td><td>30 days from service</td></tr>
<tr><td>Preliminary disclosures</td><td>60 days from filing</td></tr>
<tr><td>Earliest final judgment</td><td>6 months from service/response</td></tr>
</table>
<p class="muted">Deadlines can vary by county. This checklist is general information, not legal advice. The {app} app tracks these steps with reminders for your California case.</p>
""".format(app=APP_NAME),
    },
    "germany-divorce-checklist.html": {
        "title": "Scheidung in Deutschland: Trennungsjahr, Antrag & Versorgungsausgleich",
        "meta": "Divorce in Germany explained: the one-year separation period (Trennungsjahr), filing at the Familiengericht, Versorgungsausgleich pension equalization, and costs — a step-by-step checklist.",
        "h1": "Divorce in Germany: The Complete Checklist",
        "lede": "German divorce requires a year of separation and a family court filing. Here is the full process — Trennungsjahr, Scheidungsantrag, and Versorgungsausgleich.",
        "body": """
<h2>How divorce works in Germany</h2>
<p>Germany has only one ground for divorce: the marriage has broken down (&bdquo;Zerr&uuml;ttung&rdquo;). You must live <strong>separately for at least one year</strong> (the <em>Trennungsjahr</em>) before filing, and a court (Familiengericht) decides every divorce — there is no purely administrative divorce.</p>
<p>At least one spouse must be represented by a lawyer (<em>Anwaltszwang</em>) to file the <em>Scheidungsantrag</em>. Pensions are equalized automatically through the <em>Versorgungsausgleich</em>.</p>
<h2>The German divorce checklist</h2>
<ol>
<li><strong>Document your separation date</strong> — the Trennungsjahr starts when you begin living separately (separate households, or provably separate lives under one roof).</li>
<li><strong>Wait 12 months</strong> — the Trennungsjahr is mandatory. It can be waived only in genuine hardship cases.</li>
<li><strong>Engage a Rechtsanwalt</strong> — your lawyer files the Scheidungsantrag at the Familiengericht.</li>
<li><strong>Gather documents</strong> — marriage certificate (Eheurkunde), birth certificates of children, proof of income (Gehaltsnachweise) for the last 12 months, pension statements, and property/debt records.</li>
<li><strong>Prepare for the Versorgungsausgleich</strong> — the court equalizes pension rights acquired during the marriage. You will need pension information from the Deutsche Rentenversicherung.</li>
<li><strong>Decide on Folgeverfahren</strong> — maintenance (Unterhalt), asset division (Zugewinnausgleich), and custody can be resolved in the same proceedings or by agreement.</li>
<li><strong>Receive the Scheidungsantrag</strong> — the court serves it on your spouse.</li>
<li><strong>Attend the hearing</strong> — both spouses are usually heard in person.</li>
<li><strong>Receive the Scheidungsbeschluss</strong> — the divorce decree becomes final after a one-month appeal period (Rechtskraft).</li>
<li><strong>Update your records</strong> — pension funds, insurance, wills, and tax class.</li>
</ol>
<h2>What divorce costs in Germany</h2>
<p>Court and lawyer fees are based on the <em>Verfahrenswert</em> — roughly three months of combined net income plus assets. A typical uncontested divorce costs a few thousand euros in total; fee assistance (Verfahrenskostenhilfe) is available on low income.</p>
<p class="muted">This checklist is general information, not legal advice. The {app} app includes a Germany checklist with these steps and reminders.</p>
""".format(app=APP_NAME),
    },
    "france-divorce-checklist.html": {
        "title": "Divorce en France: Consentement Mutuel, Convention & Délais",
        "meta": "How divorce works in France: divorce by mutual consent without a judge, the 15-day reflection period, the convention de divorce, and the notaire filing — a complete checklist.",
        "h1": "Divorce in France: The Complete Checklist",
        "lede": "Most French divorces are by mutual consent — no judge, just lawyers and a notaire. Here is the full process and the deadlines.",
        "body": """
<h2>How divorce works in France</h2>
<p>French law recognizes several divorce types: <strong>divorce par consentement mutuel</strong> (mutual consent — no court hearing), divorce by accepted breakdown of the marriage, divorce for definitive alteration of the marital bond (after one year of separation), and fault-based divorce.</p>
<p>Since 2017, a mutual-consent divorce is handled by the spouses' lawyers and registered with a notaire — no judge is involved.</p>
<h2>The French divorce checklist</h2>
<ol>
<li><strong>Choose your divorce type</strong> — mutual consent is fastest when you agree on everything.</li>
<li><strong>Each spouse engages an avocat</strong> — separate lawyers are mandatory, even in mutual consent.</li>
<li><strong>Negotiate the convention de divorce</strong> — asset division, the <em>prestation compensatoire</em> (compensatory payment), child residence, and support.</li>
<li><strong>Respect the 15-day reflection period</strong> — after receiving the draft convention, both spouses must wait 15 days before signing.</li>
<li><strong>Sign the convention</strong> — together with both lawyers.</li>
<li><strong>File with the notaire</strong> — the notaire registers the convention within 15 days of signature. The divorce takes effect on registration.</li>
<li><strong>For contested divorces</strong> — the lawyer files the <em>assignation</em> with the family judge (JAF); expect a longer, court-led process.</li>
<li><strong>Update your records</strong> — livret de famille, banks, tax status, pensions, and inheritance documents.</li>
</ol>
<h2>How long does it take?</h2>
<p>A mutual-consent divorce typically completes in <strong>1 to 3 months</strong> after the convention is ready. Contested divorces take a year or more.</p>
<p class="muted">This checklist is general information, not legal advice. The {app} app includes a France checklist with these steps and reminders.</p>
""".format(app=APP_NAME),
    },
    "uk-divorce-checklist.html": {
        "title": "Divorce England & Wales: Form D8, 20-Week Rule & Final Order",
        "meta": "No-fault divorce in England and Wales explained: the D8 application, the 20-week reflection period, Conditional Order, and Final Order — the complete 2026 checklist.",
        "h1": "Divorce in England & Wales: The Complete Checklist",
        "lede": "Since April 2022, divorce in England and Wales is no-fault and mostly online. Here is the full process from the D8 application to the Final Order.",
        "body": """
<h2>How divorce works in England &amp; Wales</h2>
<p>Under the Divorce, Dissolution and Separation Act 2020, you no longer need to prove fault or wait two years. A <strong>sole application</strong> (one spouse applies) or a <strong>joint application</strong> (both apply together) states that the marriage has irretrievably broken down. That statement cannot be contested.</p>
<p>The process has a mandatory <strong>20-week reflection period</strong> and a final 6-week-and-1-day waiting step.</p>
<h2>The England &amp; Wales divorce checklist</h2>
<ol>
<li><strong>Check eligibility</strong> — one of you must be habitually resident or domiciled in England or Wales.</li>
<li><strong>Gather details</strong> — marriage certificate, full names, addresses, and your spouse's email for service.</li>
<li><strong>File the D8 application</strong> online via the HMCTS portal and pay the fee (a court fee remission is available on low income).</li>
<li><strong>Acknowledgment</strong> — for a sole application, your spouse has 14 days to acknowledge service.</li>
<li><strong>Wait through the 20-week reflection period</strong> — time to consider reconciliation and sort finances.</li>
<li><strong>Apply for the Conditional Order</strong> — the court confirms you are entitled to divorce.</li>
<li><strong>Sort the finances</strong> — division of assets is separate from the divorce itself. A <strong>consent order</strong> (with a Form D81 statement of information) makes your financial settlement legally binding; a <em>clean break</em> ends future claims.</li>
<li><strong>Wait 6 weeks and 1 day</strong> after the Conditional Order.</li>
<li><strong>Apply for the Final Order</strong> — the divorce is now final.</li>
<li><strong>Update your records</strong> — banks, pensions, wills, and insurance.</li>
</ol>
<h2>Key deadlines</h2>
<table>
<tr><th>Step</th><th>Timing</th></tr>
<tr><td>Acknowledge service</td><td>14 days</td></tr>
<tr><td>Reflection period</td><td>20 weeks</td></tr>
<tr><td>Conditional to Final Order</td><td>6 weeks + 1 day</td></tr>
</table>
<p class="muted">This checklist is general information, not legal advice. The {app} app includes an England &amp; Wales checklist with these steps and reminders.</p>
""".format(app=APP_NAME),
    },
    "spain-divorce-checklist.html": {
        "title": "Divorcio en España: Requisitos, Convenio Regulador y Plazos",
        "meta": "Divorce in Spain explained: the 3-month rule, mutual-consent divorce with a convenio regulador, contested divorce, and community property — a complete checklist.",
        "h1": "Divorce in Spain: The Complete Checklist",
        "lede": "Spanish divorce needs no cause — but there is a 3-month minimum. Here is the full process, from the convenio regulador to the sentencia.",
        "body": """
<h2>How divorce works in Spain</h2>
<p>Spain is a no-fault system: the only requirement is that <strong>three months have passed since the wedding</strong> (waived in cases of risk or violence). Divorce is by <strong>mutuo acuerdo</strong> (mutual consent, with a <em>convenio regulador</em> agreement) or <strong>contencioso</strong> (contested, decided by a judge).</p>
<p>In most regions the default marital regime is <strong>sociedad de gananciales</strong> — community property of the marriage.</p>
<h2>The Spanish divorce checklist</h2>
<ol>
<li><strong>Confirm the 3-month rule</strong> — the marriage must be at least three months old.</li>
<li><strong>Gather documents</strong> — marriage certificate (certificado de matrimonio), birth certificates of children, padrón registration, and financial records.</li>
<li><strong>Mutual consent: draft the convenio regulador</strong> — asset division, <em>pensión compensatoria</em> (compensatory pension), child custody, and use of the family home.</li>
<li><strong>File jointly with your abogado and procurador</strong> — both spouses sign the demanda de divorcio together.</li>
<li><strong>Contested route</strong> — one spouse files the demanda; the judge decides assets, custody, and support.</li>
<li><strong>Attend the hearing</strong> if required.</li>
<li><strong>Receive the sentencia de divorcio</strong> — the divorce decree.</li>
<li><strong>Register the divorce</strong> — it is recorded in the civil registry, and the marriage certificate is annotated.</li>
<li><strong>Update your records</strong> — tax status, banks, wills, and pensions.</li>
</ol>
<h2>How long does it take?</h2>
<p>A mutual-consent divorce can complete in <strong>a few months</strong> depending on the court. Contested divorces take longer.</p>
<p class="muted">This checklist is general information, not legal advice. The {app} app includes a Spain checklist with these steps and reminders.</p>
""".format(app=APP_NAME),
    },
    "italy-divorce-checklist.html": {
        "title": "Divorzio in Italia: Separazione, Tempi e Assegno di Mantenimento",
        "meta": "Divorce in Italy explained: legal separation first, the 12-month and 6-month waiting periods, assisted negotiation, and asset division — a complete checklist.",
        "h1": "Divorce in Italy: The Complete Checklist",
        "lede": "In Italy, divorce (divorzio) comes after legal separation (separazione). Here is the full two-stage process and its timelines.",
        "body": """
<h2>How divorce works in Italy</h2>
<p>Italian divorce is a <strong>two-stage process</strong>: first a legal separation (<em>separazione legale</em>), then — after a waiting period — the divorce (<em>divorzio</em>). Since the 2015 "divorzio breve" reform, the waiting period is <strong>12 months</strong> after a consensual separation or <strong>6 months</strong> after a contested one.</p>
<p>Many couples use <em>negoziazione assistita</em> — assisted negotiation by lawyers, registered with the prosecutor's office, with no judge involved when there are no minor children.</p>
<h2>The Italian divorce checklist</h2>
<ol>
<li><strong>Gather documents</strong> — marriage certificate (estratto dell'atto di matrimonio), children's birth certificates, income declarations, and property records.</li>
<li><strong>Choose the route</strong> — consensual separation (joint application), contested separation, or assisted negotiation.</li>
<li><strong>Consensual: agree the terms</strong> — asset division, <em>assegno di mantenimento</em> (spousal support), child custody, and the family home.</li>
<li><strong>File the separation</strong> — jointly with your lawyers, or via assisted negotiation at the public prosecutor's office.</li>
<li><strong>Separation is granted</strong> — the court homologates the agreement (or decides contested terms).</li>
<li><strong>Wait the statutory period</strong> — 12 months (consensual) or 6 months (contested) from the separation hearing.</li>
<li><strong>File for divorzio</strong> — jointly or by petition.</li>
<li><strong>Receive the divorce decree</strong> — ending the marriage and its financial effects.</li>
<li><strong>Update your records</strong> — anagrafe registration, tax status, banks, wills, and pensions.</li>
</ol>
<h2>How long does it take?</h2>
<p>Expect roughly <strong>12–18 months</strong> in total for the full two-stage process in most cases.</p>
<p class="muted">This checklist is general information, not legal advice. The {app} app includes an Italy checklist with these steps and reminders.</p>
""".format(app=APP_NAME),
    },
}

for path, data in JURISDICTIONS.items():
    page(path, data["title"], data["meta"], data["h1"], data["lede"], data["body"])

# ----------------------------------------------------------------------------
# 10-11. Blog articles
# ----------------------------------------------------------------------------
blog_financial_prep = """
<h2>Why financial preparation matters</h2>
<p>Money questions dominate divorce: who keeps the house, how retirement accounts split, what support looks like. The spouse who shows up with a complete, organized financial picture saves billable hours, reduces anxiety, and negotiates from strength.</p>
<h2>The 12 steps</h2>
<ol>
<li><strong>Collect statements</strong> — bank, investment, retirement, mortgage, and credit card statements for the last 12 months.</li>
<li><strong>Gather key documents</strong> — tax returns (2–3 years), pay stubs, deeds, car titles, and the marriage certificate.</li>
<li><strong>List every asset</strong> — home, vehicles, accounts, retirement plans, businesses, valuables. Note an approximate value and whether each is marital or separate.</li>
<li><strong>List every debt</strong> — mortgages, loans, credit cards. Note whose name is on each.</li>
<li><strong>Compute your net worth</strong> — assets minus debts. This single number frames every negotiation.</li>
<li><strong>Track your monthly spending</strong> — separate "marital" spending from "separate" spending once you know your jurisdiction's rules.</li>
<li><strong>Open your own accounts</strong> — a personal checking account and a credit card in your name, before joint accounts close.</li>
<li><strong>Check your credit</strong> — pull your report and watch for changes.</li>
<li><strong>Understand retirement division</strong> — in many jurisdictions a court order (like a QDRO in the US) is needed to split retirement accounts.</li>
<li><strong>Estimate support</strong> — most jurisdictions use income-based formulas; test scenarios with a calculator.</li>
<li><strong>Protect documents</strong> — store everything on your own device, backed up, and locked.</li>
<li><strong>Prepare questions for your lawyer</strong> — write them down before the consultation; billable time is precious.</li>
</ol>
<h2>Make it a habit</h2>
<p>A dedicated organizer app keeps all of this in one place: asset vault, expense tracker, document hub, and a checklist with deadlines. <a href="{domain}/">Divorce Prep</a> does exactly this, free and fully on-device.</p>
""".format(domain=DOMAIN)

page(
    "blog/how-to-prepare-financially-for-divorce.html",
    "How to Prepare Financially for Divorce: 12 Steps",
    "A practical 12-step guide to preparing your finances for divorce: statements, net worth, expenses, retirement division, and what to bring your lawyer.",
    "How to Prepare Financially for Divorce: 12 Steps",
    "The spouse with the organized financial picture negotiates from strength. Here is your 12-step plan.",
    blog_financial_prep,
)

blog_checklist = """
<h2>The one document that matters most</h2>
<p>Every divorce negotiation — and every settlement calculator — starts from the same input: a complete inventory of assets and debts. This template gives you the structure. Fill it in once and keep it updated.</p>
<h2>Assets</h2>
<table>
<tr><th>Asset</th><th>Value</th><th>Marital or separate?</th></tr>
<tr><td>Family home</td><td>$_______</td><td></td></tr>
<tr><td>Other real estate</td><td>$_______</td><td></td></tr>
<tr><td>Bank accounts</td><td>$_______</td><td></td></tr>
<tr><td>Investment/brokerage accounts</td><td>$_______</td><td></td></tr>
<tr><td>Retirement accounts (401k, IRA, pension)</td><td>$_______</td><td></td></tr>
<tr><td>Vehicles</td><td>$_______</td><td></td></tr>
<tr><td>Business interests</td><td>$_______</td><td></td></tr>
<tr><td>Valuables (art, jewelry, collectibles)</td><td>$_______</td><td></td></tr>
</table>
<h2>Debts</h2>
<table>
<tr><th>Debt</th><th>Balance</th><th>Whose name?</th></tr>
<tr><td>Mortgage(s)</td><td>$_______</td><td></td></tr>
<tr><td>Home equity loans</td><td>$_______</td><td></td></tr>
<tr><td>Car loans</td><td>$_______</td><td></td></tr>
<tr><td>Credit cards</td><td>$_______</td><td></td></tr>
<tr><td>Student loans</td><td>$_______</td><td></td></tr>
<tr><td>Tax debts</td><td>$_______</td><td></td></tr>
</table>
<h2>Why "marital vs. separate" matters</h2>
<p>In community-property systems (like California and much of Spain), property acquired during the marriage is shared; property owned before the marriage, or received by gift or inheritance, is usually separate. Other systems divide by different rules — but almost everywhere, the classification matters. Tag every item as you go.</p>
<h2>Keep it updated</h2>
<p>Values move; new spending happens; statements arrive monthly. The {app} app keeps this inventory live on your device — with photos, ownership tags, and a running net worth — and exports it as a bundle for your lawyer.</p>
""".format(app=APP_NAME)

page(
    "blog/divorce-financial-checklist.html",
    "Divorce Financial Checklist: Asset & Debt Inventory Template",
    "A free asset and debt inventory template for divorce: every account, property, and debt to list, with marital vs. separate classification.",
    "The Divorce Financial Checklist: Asset & Debt Inventory",
    "The single most useful document in any divorce: a complete, classified inventory of everything you own and owe.",
    blog_checklist,
)

print("SITE BUILD COMPLETE")
