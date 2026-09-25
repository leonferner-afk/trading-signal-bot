"""Default scan/research universe: ~250 liquid US-listed stocks across
sectors, weighted toward higher-beta growth names (where large, fast
moves happen) but deliberately including steadier large caps, energy,
financials and industrials so research isn't only measured on the
decade's biggest winners.

Survivorship caveat, stated plainly: this list is written today, so it
over-represents companies that are still around and liquid. Research
therefore compares every strategy against a random-entry baseline on this
same universe and period — a strategy only earns trust by beating that
baseline, not by posting big raw numbers that the universe itself drifted
into.

A ticker that has since been delisted or renamed simply fails to fetch
and is skipped (reported, never guessed).
"""
from __future__ import annotations

_GROUPS = {
    "megacap_tech": "AAPL MSFT NVDA AMZN GOOGL META TSLA AVGO ORCL CRM ADBE NFLX",
    "semis": "AMD INTC QCOM TXN AMAT LRCX KLAC MU MRVL ON NXPI ADI MCHP TSM ASML ARM SMCI MPWR ENTG TER CRDO ALAB COHR LITE",
    "hardware_infra": "DELL HPE ANET CSCO IBM VRT CIEN WDC STX PSTG NTNX",
    "software": "NOW INTU PANW CRWD ZS NET FTNT OKTA DDOG SNOW MDB TEAM WDAY HUBS SNPS CDNS GTLB PATH S ESTC CFLT BILL DOCN TWLO ZM",
    "internet_consumer": "SHOP UBER LYFT ABNB DASH SPOT TTD APP RDDT DUOL PINS SNAP U RBLX DKNG ROKU CVNA MELI SE",
    "fintech_crypto": "XYZ PYPL AFRM SOFI HOOD COIN UPST NU MSTR MARA RIOT CLSK HUT CIFR IREN WULF BTDR",
    "ai_speculative": "PLTR AI SOUN BBAI IONQ RGTI QBTS RKLB ASTS LUNR ACHR JOBY",
    "ev_clean_energy": "RIVN LCID NIO LI XPEV ENPH FSLR PLUG RUN SEDG QS BE CHPT",
    "biotech_health": "MRNA NVAX CRSP NTLA BEAM EDIT VRTX REGN BIIB AMGN GILD LLY NVO VKTX ISRG DXCM EXAS TDOC HIMS",
    "consumer": "CMG SBUX NKE LULU DECK CROX ONON W CHWY ETSY PTON GME AMC WING CAVA CELH ELF AXON TOST",
    "financials": "JPM GS MS BAC C WFC SCHW BX KKR APO",
    "industrials": "GE BA CAT DE LMT RTX GEV ETN PWR URI",
    "energy_materials": "XOM CVX OXY SLB FCX NEM CCJ MP ALB AA CLF",
}


def default_universe() -> tuple[str, ...]:
    seen: dict[str, None] = {}
    for tickers in _GROUPS.values():
        for ticker in tickers.split():
            seen.setdefault(ticker.upper(), None)
    return tuple(seen)
