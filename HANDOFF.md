# Divorce Prep & Financial Organizer — Full Project Handoff

> Prepared 2026-11-10. Covers everything from project start (2026-10-21) through today, including the current App Store rejection fix in progress. Written for a new assistant (Claude) taking over.

## 1. Project overview

"Divorce Prep: Plan & Organizer" is a **SwiftUI iOS app** (iPhone + iPad) that guides people through divorce: what to file, what they own, what they owe, what it costs, what comes after. **All data stays on-device** — no network calls, no analytics, no accounts.

- Bundle ID: `app.divorceprep.organizer`
- App Store Apple ID: **6825617653** — store URL https://apps.apple.com/app/id6825617653
- Team: **QIDIENT GLOBAL LTD** (9K3RFFQLWC), Apple ID signed into Xcode: miracleodi1@gmail.com
- Copyright: © 2026 QIDIENT GLOBAL LTD
- Min iOS 17.0, SwiftUI + SwiftData, **zero third-party dependencies** (system frameworks only), XcodeGen (`project.yml` is source of truth; the checked-in `DivorcePrep.xcodeproj` is generated — edit project.yml, not the pbxproj)

## 2. What was built (all complete)

10 features + gates, per the product spec:

1. **AI-guided jurisdiction checklist** — on-device rules engine (deliberately NOT a cloud LLM — privacy + offline + free; provider abstraction left loose). Jurisdiction packs are data files: `generic`, `us-ca`, and EU packs `de`, `fr`, `gb`, `es`, `it` (~19–22 items each). Never hardcode rules; everything routes through the pack abstraction. Engine `requires` is all-satisfied (no OR), so alternative legal routes are folded into one summary item.
2. **Asset & debt vault** — photos, statements, valuations, marital-vs-separate classification.
3. **Expense tracker** — merchant-rule auto-categorization.
4. **Settlement calculator** — split scenarios + support estimates.
5. **Document hub** — categories, one-tap lawyer export bundle.
6. **Attorney meeting prep** — notes + question bank.
7. **Court date & deadline calendar** — local notifications.
8. **Post-divorce transition checklist** — lives inside Checklist as a second checklist type.
9. **Legal disclaimer** — first-launch acceptance gate (fullScreenCover, `disclaimerAccepted` AppStorage), also reachable from onboarding + Settings.
10. **Hard paywall** — StoreKit 2 auto-renewable subscriptions: **$14.99/week** and **$150.99/year**, 7-day free trial advertised on both (trial config is an ASC intro offer — **not yet set up**, see §8). Gate order: Face ID → disclaimer → paywall → app. Paywall is an in-hierarchy overlay (cannot be swiped away). Dev bypass launch arg: **`-bypassPaywall`**.

Tab layout (fixed, 5 tabs): Home, Checklist, Finances (vault+expenses+calculator), Documents, Attorney. Face ID gate on launch.

**Status:** all 13 stages (0–12) complete + redesign (13) complete; 12/12 XCTests green. The living roadmap + decisions log is in `README.md` (update it at the end of every future stage).

## 3. Design system — "Serene Haven"

Full visual redesign (Stages 12–13), generated via Google Stitch then hand-ported to SwiftUI:

- Cream `#FAF7F2` background, deep teal `#1E5A50` primary, sage/sand accents, charcoal ink, amber reserved for deadlines; 20px-radius white cards, pill buttons.
- **Plus Jakarta Sans** bundled TTFs (`DivorcePrep/Resources/Fonts/`, registered via `UIAppFonts` in project.yml), semantic styles via `AppFont` in `AppTheme.swift`.
- 14-screen emotional onboarding arc; privacy lock = deep-teal gradient.
- **Stitch outputs are design references only** — they hallucinate data (wrong tab names, invented people/numbers). The app always renders real SwiftData. Canonical demo data if needed: Alex & Sam Morgan, California, married 2017-10-21, filing 2026-08-21, net worth $393,700 ($784,900 assets − $391,200 debts), 25 checklist steps in 4 phases.
- Stitch project: `projects/929983003257028773`, design system "Serene Haven" `assets/25b6ab53e405472c9282181b57a8d585`, API `https://stitch.googleapis.com/mcp`, GCP project `divorce-prep`, token at `~/.stitch-mcp-auto/tokens.json` (refresh via `gcloud auth print-access-token`).
- Reference screens: `Design/previews/` (v1 rejected screens in `Design/previews/v1/`).

## 4. Marketing website (LIVE)

Static site generated from `Website/` via `Website/build-site.py` — 11 pages, JSON-LD SoftwareApplication schema, real App Store link. Live at **https://jerryjrdev.github.io/divorce-prep/** (GitHub repo `jerryjrdev/divorce-prep`, branch main, public). Privacy page at `.../privacy.html`, support at `.../support.html`.

## 5. App Store screenshots & assets (all rendered, all uploaded)

**Logo unification (2026-10-23):** the teal "scales of justice over document" app icon is THE logo (source `DivorcePrep/Assets.xcassets/AppIcon.appiconset/icon.png`). All promo headers use the icon embedded as a base64 `<img>` data-URI (`/tmp/icon-108.b64`). The old cream "heart of two figures" design is deprecated. `AppStore/icon-1024.png` is the final 1024×1024 no-alpha icon (sRGB-mapped).

Screenshot sets (marketing-style promos, canonical numbers used throughout):
| Set | Folder | Size | Slot |
|---|---|---|---|
| iPhone 6.7" | `AppStore/screenshots/` | 1290×2796 | 6.7" |
| iPhone 6.5" | `AppStore/screenshots-65/` | 1284×2778 | 6.5" |
| iPhone medium (6.1"/6.3" Dynamic Island) | `AppStore/screenshots-61/` | **1179×2556 exactly** | medium display |
| iPad 13" | `AppStore/screenshots-ipad/` | 2048×2732 | 13" |

- All 19 assets (7+7+5) are in the ASC **Asset Library**; the medium slot has 7/10 uploaded from the 6.1" set.
- **Critical quirk:** ASC product-page slot uploads reject PNGs that lack an sRGB chunk ("File dimensions are invalid" / "An error occurred during upload"). Headless-Chrome PNGs come out with only IHDR+IDAT. Fix: `sips -s format png in.png --out out.png` (embeds sRGB+eXIf). `sips -z` same-size is a no-op; actual resizes do embed sRGB.
- Render pipeline: HTML templates (`*.html` next to the PNGs) rendered headless via CDP: `NODE_PATH="/Users/a0000/node_modules" node /tmp/cdp.js <file://…html> <out.png> <w> <h> <dpr>` (iPhone 430 932 3; iPad 1024 1366 2). `/tmp/cdp.js` prints RECTS metrics + saves the shot. **Material Symbols font never loads headless** — all 131 icon spans were replaced with inline SVGs; never reintroduce font icons into promo HTML.
- 4 minor copy flags Apple noted but accepted: promo-06 "client-attorney privilege" overclaim, ipad-03 extra filled radio dots, promo-07 "Private & Confident" typo, promo-04 "Serene Haven Engine" subtext.
- **Risk:** Apple's 2.3.3 guidance says screenshots must show actual app usage — our promos are marketing-style. They passed once, but if flagged next round, real-UI screenshots may be needed.

## 6. App Store Connect record (as of 2026-11-10)

- **App record:** name "Divorce Prep: Plan & Organizer", subtitle saved, categories Finance + Lifestyle, age 4+, Content Rights: no third-party content, App Privacy: **Data Not Collected** (+ privacy URL), export compliance answered **"None of the algorithms mentioned above"** (verified: zero direct crypto calls in the codebase).
- **Version 1.0** metadata saved: promo text, ~2,660-char description, keywords 94/100 (`divorce,planner,organizer,checklist,finances,settlement,attorney,alimony,support,custody,legal`), support/marketing URLs.
- **Version string MUST be exactly "1.0"** — Apple matches `CFBundleShortVersionString` exactly. project.yml has `MARKETING_VERSION: "1.0"`.
- **App Review Information saved:** contact Miracle Odi, miracleodi1@gmail.com, phone **+234 903 198 4319**, sign-in required: NO, 613-char notes.
- **Subscriptions:** group **"Premium"** (ID **22502473**), group localization saved (English U.S., Display Name "Premium"). Products: **Weekly Premium** `app.divorceprep.organizer.weekly` (1 week, $14.99, Apple ID 6825621387) and **Yearly Premium** `app.divorceprep.organizer.yearly` (1 year, $150.99, EU €179.99, Apple ID 6825890739) — both across 175 territories, with saved review notes ("Hard paywall… no login required").
- **Build uploaded: 1.0 (2)** — supports iPhone Portrait+LandscapeL+LandscapeR and iPad all 4 orientations (fixed ASC error 90474). History: 0.1.0 (1) failed validation (stale pbxproj had MARKETING_VERSION 0.1.0), 1.0 (1) had upside-down-only iPhone portrait — superseded. Xcode auto-bumped build 1→2 at upload; pbxproj `CURRENT_PROJECT_VERSION` is still 1 — **do not re-upload without bumping**.
- **App icon in ASC (General → App Information → App Icon): NOT confirmed uploaded** — user may still need to upload `AppStore/icon-1024.png`.
- **7-day introductory offers: NOT set up yet** — ASC only shows "Set up Introductory Offer" after the app/subscription is active. The paywall copy already advertises the trial, so offers MUST be configured before launch.

## 7. Submission history

1. **Submitted 2026-10-23 1:31 PM** — submission ID `a620a731-26f9-44b7-9c8a-ae5153fa1d19`, 1 item (iOS 1.0), build 1.0 (2).
2. **REJECTED 2026-10-31** — Guideline **2.1.0 Performance: App Completeness**, with a hint of 3.1.1 (in-app purchase). Apple's message: "Guideline 2.1 - Information Needed - New App Submission" with a 6-point request: (1) purpose/audience description, (2) access instructions, (3) external services, (4) regional consistency, (5) regulated-industry status, (6) **screen recording of the app on a physical device**.
3. **Root cause of the rejection:** the Premium subscription group + both subscription products were **never attached to the submission** (IAPs must be submitted with the app version).
4. **Fix in progress (right now, 2026-11-10):**
   - Group localization was created (it was blocking "Add for Review" with "You must add at least one subscription group localization").
   - A **new draft** was started **Today (2026-11-10) at 1:03 PM** by Miracle Odi; the Premium group has been added to it.
   - Remaining: add **iOS App 1.0** + **Weekly Premium** + **Yearly Premium** to that same draft. The user is doing this right now with click-level instructions:
     - Version page (left sidebar → "1.0 Rejected") → **Update Review** button → choose the Today-1:03-PM draft.
     - Monetization → In-App Purchases → Premium → click **Weekly Premium** row → **Add for Review** → same draft; repeat for **Yearly Premium**.
   - **Important UI facts learned:** the Draft Submission panel has NO "+"/"Add Items" button — items are added only from their own pages via "Add for Review"/"Update Review", choosing the target draft in the dropdown. The old draft "Draft iOS Submission (5)" (Oct 23 8:09 AM, 5 stale items) should be ignored; optionally discard later.
   - Draft-panel warnings to clear: "New subscription groups must be submitted with an auto-renewable subscription from within that group." and "To submit your items for review, add an app version for the selected platform."

## 8. What still must happen (in order)

1. **Finish the draft** (user in progress): all 4 items (iOS 1.0, Premium group, Weekly, Yearly) in the Today-1:03-PM draft, no yellow warnings.
2. **Reply to Apple** on the rejected submission (App Review page → Submissions table → Oct 23 row → open → Messages → Reply to App Review). The reply must cover Apple's 6 points; our answers:
   - **Purpose/audience:** self-help financial & legal-preparation organizer for people going through divorce; guides filing, asset division, settlement planning.
   - **Access instructions:** no login/account; the app opens behind a hard paywall with a **7-day free trial** on both plans ($14.99/week, $150.99/year); reviewer can start the trial free of charge.
   - **External services:** NONE — fully on-device, no server components, no third-party services.
   - **Regional consistency:** jurisdiction packs for US (California) and Europe (DE/FR/GB/ES/IT) included; metadata is English for all territories.
   - **Regulated industry:** N/A — not a licensed service, includes a legal disclaimer (not legal advice).
   - **Screen recording:** attach the recording (step 3).
   - Also paste the same info into App Review Information → Notes.
   - *(A fuller drafted reply text exists in the earlier chat transcript: `/Users/a0000/.qoder/projects/-Users-a0000-Desktop-Divorce-prep---financial-organizer/062deb22-cfa3-489c-9a4a-82ccaac39074.jsonl` — search for the 6-point reply draft. If unavailable, redraft from the bullets above.)*
3. **Physical-device screen recording** — needs the user's iPhone plugged into the Mac. Content: paywall shown, then full feature tour (build & run with `-bypassPaywall` to skip the paywall, or show trial flow). Capture via iOS Control Center screen recording (or Xcode device window), transfer to Mac (AirDrop/Files), attach to the reply. Click-level instructions should be given to the user (they are a novice with Xcode/GUI).
4. **Submit** — ONLY after explicit user confirmation. Never auto-submit.
5. **After approval:** set up 7-day introductory offers on both subscriptions (paywall advertises the trial); optionally discard the old "Draft iOS Submission (5)"; upload the app icon if still missing.

## 9. Hard constraints (do not violate)

- **Never submit for review without explicit user confirmation.**
- **Never touch other apps on the account:** VectaMarkets (6820480583), WallSight (6792202006), Sakeena (6787559144).
- **Never interfere with the user's Apple authentication flows** (2FA, Apple ID prompts).
- **User prefers manual, numbered, click-level instructions** for their logged-in App Store Connect / Apple UIs over browser automation.
- **Never automate the user's booted simulators** — use a dedicated headless one for UI tests.
- App Review phone number must come from the user; never fabricate contact data (real: Miracle Odi, +234 903 198 4319, miracleodi1@gmail.com).
- Do not run credential-scanning greps in the shell (the Bash classifier blocks them; ask the user if ASC API CLI work is needed).

## 10. Build/signing environment

- Xcode 26.5; automatic signing with team QIDIENT GLOBAL LTD (9K3RFFQLWC). Distribution cert "Apple Distribution: QIDIENT GLOBAL LTD" valid to 2027-07-21.
- `altool` is gone in Xcode 26.5; `iTMSTransporter` remains at `/Applications/Xcode.app/Contents/Developer/usr/bin/`.
- ASC API keys exist in `~/Downloads` (`AuthKey_JB3YVH3TLJ.p8`, `AuthKey_P2UJGC5RWS.p8`, `SubscriptionKey_A84TBP5J39.p8` = server notifications) — but the Issuer ID was never located; ask the user if CLI uploads are needed.
- Generate + build: `xcodegen generate` then `xcodebuild -project DivorcePrep.xcodeproj -scheme DivorcePrep -destination 'platform=iOS Simulator,name=iPhone 17' build`. Tests: 12-test XCTest suite (SwiftData test lesson: @Model objects must be created inside a ModelContainer, in-memory in tests).
- Test-harness args: `-openScreen=onboarding|settings`, `-bypassPaywall`.

## 11. Key paths

- Project root: `/Users/a0000/Desktop/Divorce prep & financial organizer/`
- App source: `DivorcePrep/` (App/, Features/, Models/, Jurisdictions/, Security/)
- Project config: `project.yml`
- ASC assets: `AppStore/` (icon-1024.png, screenshots/, screenshots-65/, screenshots-61/, screenshots-ipad/)
- Website: `Website/` (build via `Website/build-site.py`)
- Stitch previews: `Design/previews/`
- CDP render script: `/tmp/cdp.js` (volatile — /tmp; expected to be rewritten after reboot)
- Chat transcript (full history incl. drafted Apple reply): `/Users/a0000/.qoder/projects/-Users-a0000-Desktop-Divorce-prep---financial-organizer/062deb22-cfa3-489c-9a4a-82ccaac39074.jsonl`
