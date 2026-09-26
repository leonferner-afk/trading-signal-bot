# Tradingbot — köp- och säljsignaler för amerikanska aktier

Boten läser av marknaden efter varje börsdag och säger **vad du ska köpa
och när du ska sälja**. Den handlar **aldrig** själv — du lägger orderna.

- Körs gratis och automatiskt på GitHub Actions (publikt repo = obegränsade minuter).
- Du får **🟢 KÖP NU** och **🔴 SÄLJ NU** som GitHub-notis (mejl/app) och, om du vill, i Telegram.
- Varje beslut följer exakt de regler som backtestats; siffrorna nedan kommer från den forskningen, inte från önsketänkande.

## Varje morgon

05:37 UTC tisdag–lördag (efter att varje amerikansk börsdag stängt):

1. Laddar ned dagsdata för universumet (~100 av USA:s största bolag) och SPY.
2. Stänger positioner i journalen som sålts (vid öppning efter en säljsignal, eller via stop-order).
3. Räknar ut varje akties relativa styrka (6-månadersavkastning som percentil i universumet) och om den ligger över sitt 200-dagars glidande medelvärde.
4. Fattar dagens beslut med regeln nedan och skickar KÖP NU / SÄLJ NU.
5. Skriver en rapport (`reports/ÅÅÅÅ-MM-DD.md` på grenen `bot-state`) och skapar en GitHub-issue när något ska göras.

Skydd som alltid gäller:

- **Ingen ny handelsdag** (amerikansk helgdag, omkörning) → inga nya beslut, inga notiser.
- **Gammal data** (senaste stängning äldre än 5 dagar) → inga beslut, och du får en varning.
- **Aktie utan data idag** → behålls, och köps inte. Den säljs aldrig på en gissning.
- **Kraschad körning** → du får en issue om det, så en tyst dag aldrig kan misstas för "inga affärer".

## Strategin: momentum-rotation ("trendledare")

Håll de starkaste aktierna så länge de är starka och i upptrend — sälj när de slutar vara det.

- **KÖP** när SPY är över sitt 200-dagars snitt och en aktie ligger över sitt eget 200-dagars snitt och hör till de 20 % starkaste (6 mån). De starkaste köps först, i lediga platser: max 8 innehav, lika stora (1/8 av portföljen var), högst 3 nya köp per dag.
- **SÄLJ** när aktien stänger under sitt 200-dagars snitt eller dess relativa styrka faller under 50 %.
- **Ordrar** läggs vid nästa börsöppning (det boten räknar med). Inget fast kursmål — vinnare får löpa.

## Evidens — ärliga siffror

Forskningen (`python -m app.cli research`, körs automatiskt varje söndag,
fullständig rapport i `research.md` på grenen `bot-state`) testar allt
på 10 års dagsdata med:

- **Realistiska affärer:** köp och sälj vid nästa öppning, 0,40 % kostnad per sida.
- **Jämförelser:** mot SPY, mot ett likaviktat innehav av samma aktier och mot slumpvis valda aktier bland samma kandidater.
- **Datumuppdelning:** reglerna väljs på träning + validering (fram till nov 2024), och den sista perioden (nov 2024–sep 2026) används bara för att rapportera.
- **Kontrollgrupp utan efterhandskunskap:** bolag som var stora **2015**, inte dagens vinnare. Utan den blir resultaten kraftigt missvisande (se nedan).

**Resultat för regeln boten använder (kontrollgruppen, jan 2018 – sep 2026):**

| | Avkastning/år | Största nedgång | Sharpe | Sharpe träning+validering | Sista perioden (nov 2024–) |
|---|---|---|---|---|---|
| SPY (köp och behåll) | +14,5 % | −34 % | 0,81 | 0,76 | +16,7 %/år |
| Samma bolag, likaviktat, utan kostnader | +13,8 % | −37 % | 0,79 | 0,75 | +13,7 %/år |
| **Rotation, topp 8** | **+16,1 %** | **−29 %** | **0,76** | **0,63** | +29,8 %/år |
| … utan sin bästa aktie (DVN) | +13,9 % | −28 % | 0,70 | | |
| … med 0,70 % kostnad per sida | +14,7 % | | | | |

| År | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (t.o.m. sep) |
|---|---|---|---|---|---|---|---|---|---|
| SPY | −6 % | +31 % | +18 % | +29 % | −18 % | +26 % | +25 % | +18 % | +14 % |
| Rotation, topp 8 | −6 % | +7 % | +16 % | +27 % | −0 % | +23 % | +26 % | +22 % | +32 % |

**Ärlig slutsats:**

- **Mot index:** regeln har gett ungefär samma avkastning som index, med något högre årsavkastning och mindre största nedgång men mer svängningar. Ett rekordår som 2019 missade den helt, medan 2022 skyddade den bra.
- **Riskjusterat** (Sharpe) har den **inte** slagit SPY, och **ingen** av de 16 testade varianterna klarade de förhandsbestämda kraven:
  - Sharpe över SPY:s,
  - rangordningen bättre än slumpen,
  - inte beroende av en enda aktie,
  - nedgångar nära SPY:s.
- **Rangordningen** slog däremot 100 % av slumpvisa urval bland samma kandidater, så urvalet är inte slump.
- **Den starka sista perioden** (+29,8 % mot +16,7 %) är för kort för att dra slutsatser av.

Boten skriver detta i varje rapport och KÖP-meddelande. Kraven prövas om
automatiskt varje vecka på ny data.

**Varför kontrollgruppen är avgörande:** på hela listan (dagens kända
tillväxtaktier) gav samma regel +32,7 %/år — men med −71 % största nedgång.
Redan ett likaviktat innehav av listan gav +26,5 %/år, eftersom listan är
skriven i efterhand. När NVDA (bara ~18 mdr USD 2015) av misstag låg i
kontrollgruppen gav regeln +22 %/år. När listan rättades försvann större
delen av fördelen.

## Så använder du signalerna

- **🟢 KÖP NU — XYZ:** köp vid börsöppningen, ungefär det antal aktier meddelandet anger (1/8 av portföljvärdet du angett). Ingen stop-order ingår i de testade reglerna — säljet kommer som en SÄLJ NU-signal.
- **🔴 SÄLJ NU — XYZ:** sälj vid börsöppningen.
- **Dagsrapporten** (issue eller `reports/latest.md` på `bot-state`) visar innehav, resultat hittills och vilka aktier som står näst på tur.
- **Portföljstorleken** sätter du som repo-variabel `PORTFOLIO_SIZE_USD` (Settings → Secrets and variables → Actions → Variables). Standard är 10 000 USD.

## Inställningar (valfria repo-variabler / secrets)

| Namn | Standard | Vad |
|---|---|---|
| `PORTFOLIO_SIZE_USD` (variabel) | 10000 | Portföljvärde som positionsstorlekarna räknas från |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` (secrets) | — | Notiser även i Telegram: skapa en bot via @BotFather, skriv till den, hämta chat-id via `https://api.telegram.org/bot<token>/getUpdates` |
| `TWELVE_DATA_API_KEY` (secret) | — | Reservkälla för kursdata om Yahoo strular (gratis nyckel) |
| `POLICY_MODE` | rotation | `swing` = de gamla stop/mål-signalerna (se nedan varför de inte är standard) |
| `ROTATION_*` | se `app/policy.py` | Ändrar regeln — gör det bara om forskningen stöder den nya varianten |

## Varför inte de gamla swing-signalerna?

Den första versionen skickade klassiska swing-signaler: utbrott eller
momentum med stop-loss på 1,5 × ATR och ett fast mål. I samma test gav
dessa i kontrollgruppen **+2,1 %/år** (Sharpe 0,27) mot SPY:s +15,0 %.
Även slumpvis valda aktier med samma stop/mål-regler gav bara +8,8 %/år.

Problemet är alltså utformningen. Tajta stopp slås ut av vanligt brus,
och kostnaden på ~0,8 % per affär äter resten. Dessutom var
signalstrategiernas tajming *sämre* än slumpvisa köpdagar under samma
filter. Läget finns kvar (`POLICY_MODE=swing`) för jämförelse, men det är
inte standard.

## Begränsningar — läs detta

- **Historik är ingen garanti.** Strategin har haft långa perioder under index, och dess största nedgång i testet var −29 % (SPY: −34 %).
- **Överlevnadsbias:** gratis data saknar avnoterade bolag. Kontrollgruppen väljer bolag efter storlek 2015 (inte efter vad som hände sedan), men bolag som köpts upp eller avnoterats efter 2015 kan inte hämtas. Det är sannolikt en liten fördel för testet.
- **Kostnader:** testet räknar med 0,40 % per affär och sida (courtage + valutaväxling + slippage för en svensk privatperson). Är dina kostnader högre, blir avkastningen lägre (se känslighetstabellen i `research.md`).
- **Skatt** ingår inte. Många affärer i ett vanligt depå-konto beskattas annorlunda än i ett ISK.
- **Universumet** (dagens storbolag i `app/universe.py`) bör uppdateras ungefär en gång per år.

## Köra själv / utveckla

```bash
cd backend
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q          # alla tester, syntetisk data, inget nätverk
python -m app.cli daily                # dagens körning lokalt (kräver att Yahoo Finance nås)
python -m app.cli research --years 10  # hela forskningen (~20 min)
```

Workflows: `.github/workflows/daily.yml` (daglig körning), `research.yml`
(forskning varje söndag, publicerar `evidence.json` + `research.md` på
`bot-state`), `diagnose.yml` (felsökning av datakällor).

Kod: `app/rotation.py` (regeln + simuleringen), `app/live_rotation.py`
(dagens beslut), `app/research.py` (all evidens), `app/daily.py`
(körningen), `app/paper_trading/simulator.py` (journalens faktiska
fyllnadspriser), `app/notify/` (meddelanden).

## Absoluta regler

Ingen automatisk handel. Inga påhittade data, backtester eller löften om
vinst. Inga påtvingade dagliga affärer — "inga köp idag" är ett korrekt svar.
Varje siffra kommer från riktig marknadsdata eller är uträknad ur den.
