"""Scan/research universe.

`default_universe()` — ~230 liquid US-listed stocks: higher-beta growth
names (where large, fast moves happen), steadier large caps, and a set of
fallen former favourites, so research isn't measured only on the decade's
biggest winners.

`LARGECAP_2015` — companies that were already large, index-level names
around 2015 and still trade under the same ticker. This is the research
control group: it was chosen by size a decade ago, not by what happened
since, so it carries far less hindsight than a list of today's famous
growth stocks. A rule only earns trust if it also works here.

Survivorship caveat, stated plainly: any list written today over-represents
companies that are still listed. Free data (Yahoo) doesn't keep delisted
tickers, so this can be reduced but not eliminated. Research therefore
judges every rule against random picks from the same universe and dates,
and against the large-cap control group.

A ticker that has since been delisted or renamed simply fails to fetch and
is skipped (reported, never guessed).
"""
from __future__ import annotations

_GROUPS = {
    "megacap_tech": "AAPL MSFT NVDA AMZN GOOGL META TSLA AVGO ORCL CRM ADBE NFLX",
    "semis": "AMD INTC QCOM TXN AMAT LRCX KLAC MU MRVL ON NXPI ADI MCHP TSM ASML ARM SMCI MPWR ENTG TER CRDO ALAB COHR LITE",
    "hardware_infra": "DELL HPE ANET CSCO IBM VRT CIEN WDC STX NTNX",
    "software": "NOW INTU PANW CRWD ZS NET FTNT OKTA DDOG SNOW MDB TEAM WDAY HUBS SNPS CDNS GTLB PATH S ESTC BILL DOCN TWLO ZM DOCU",
    "internet_consumer": "SHOP UBER LYFT ABNB DASH SPOT TTD APP RDDT DUOL PINS SNAP U RBLX DKNG ROKU CVNA MELI SE",
    "fintech_crypto": "XYZ PYPL AFRM SOFI HOOD COIN UPST NU MSTR MARA RIOT CLSK HUT CIFR IREN WULF BTDR",
    "ai_speculative": "PLTR AI SOUN BBAI IONQ RGTI QBTS RKLB ASTS LUNR ACHR JOBY",
    "ev_clean_energy": "RIVN LCID NIO LI XPEV ENPH FSLR PLUG RUN SEDG QS BE CHPT",
    "biotech_health": "MRNA NVAX CRSP NTLA BEAM EDIT VRTX REGN BIIB AMGN GILD LLY NVO VKTX ISRG DXCM TDOC HIMS",
    "consumer": "CMG SBUX NKE LULU DECK CROX ONON W CHWY ETSY PTON GME AMC WING CAVA CELH ELF AXON TOST",
    "financials": "JPM GS MS BAC C WFC SCHW BX KKR APO",
    "industrials": "GE BA CAT DE LMT RTX GEV ETN PWR URI",
    "energy_materials": "XOM CVX OXY SLB FCX NEM CCJ MP ALB AA CLF",
    # Former high-flyers that mostly went nowhere or down — the kind of
    # name a hindsight-picked list leaves out.
    "fallen_favourites": "BYND SPCE OPEN FUBO LMND ROOT PENN CCL AAL NCLH LUMN VFC",
}

LARGECAP_2015 = tuple(
    """AAPL MSFT AMZN GOOGL META JNJ JPM XOM WFC GE PG T VZ PFE CVX KO MRK PEP INTC CSCO ORCL IBM HD DIS
    BAC C WMT UNH AMGN GILD BMY ABBV MDT QCOM MO PM MCD NKE SBUX UPS UNP MMM BA CAT HON LMT GD RTX EMR
    F GM COP OXY SLB HAL DVN FCX KMI SPG AIG MET AXP USB GS MS BK BLK COF CL MDLZ CVS LLY BIIB EBAY
    TXN AVGO NFLX CMCSA TGT LOW COST ABT DHR V MA ACN ADBE CRM NVDA BKNG TMO NEE DUK SO""".split()
)


def default_universe() -> tuple[str, ...]:
    seen: dict[str, None] = {}
    for tickers in _GROUPS.values():
        for ticker in tickers.split():
            seen.setdefault(ticker.upper(), None)
    return tuple(seen)


def research_universe() -> tuple[str, ...]:
    """Default universe plus the large-cap control group."""
    seen = dict.fromkeys(default_universe())
    for ticker in LARGECAP_2015:
        seen.setdefault(ticker, None)
    return tuple(seen)
