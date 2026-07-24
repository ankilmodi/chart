"""
Stock universe: NIFTY 50, NIFTY Next 50, Bank NIFTY constituents.
"""
from typing import List, Dict
from app.scanner.schemas import StockInfo

# ---------------------------------------------------------------------------
# NIFTY 50
# ---------------------------------------------------------------------------
NIFTY50 = [
    StockInfo(symbol="RELIANCE",   name="Reliance Industries",       sector="Energy",         index="NIFTY50",      ticker="RELIANCE.NS"),
    StockInfo(symbol="TCS",        name="Tata Consultancy Services", sector="IT",             index="NIFTY50",      ticker="TCS.NS"),
    StockInfo(symbol="HDFCBANK",   name="HDFC Bank",                 sector="Banking",        index="NIFTY50",      ticker="HDFCBANK.NS"),
    StockInfo(symbol="ICICIBANK",  name="ICICI Bank",                sector="Banking",        index="NIFTY50",      ticker="ICICIBANK.NS"),
    StockInfo(symbol="INFY",       name="Infosys",                   sector="IT",             index="NIFTY50",      ticker="INFY.NS"),
    StockInfo(symbol="HINDUNILVR", name="Hindustan Unilever",        sector="FMCG",           index="NIFTY50",      ticker="HINDUNILVR.NS"),
    StockInfo(symbol="ITC",        name="ITC",                       sector="FMCG",           index="NIFTY50",      ticker="ITC.NS"),
    StockInfo(symbol="SBIN",       name="State Bank of India",       sector="Banking",        index="NIFTY50",      ticker="SBIN.NS"),
    StockInfo(symbol="BHARTIARTL", name="Bharti Airtel",             sector="Telecom",        index="NIFTY50",      ticker="BHARTIARTL.NS"),
    StockInfo(symbol="KOTAKBANK",  name="Kotak Mahindra Bank",       sector="Banking",        index="NIFTY50",      ticker="KOTAKBANK.NS"),
    StockInfo(symbol="LT",         name="Larsen & Toubro",           sector="Infrastructure", index="NIFTY50",      ticker="LT.NS"),
    StockInfo(symbol="HCLTECH",    name="HCL Technologies",          sector="IT",             index="NIFTY50",      ticker="HCLTECH.NS"),
    StockInfo(symbol="ASIANPAINT", name="Asian Paints",              sector="Paints",         index="NIFTY50",      ticker="ASIANPAINT.NS"),
    StockInfo(symbol="AXISBANK",   name="Axis Bank",                 sector="Banking",        index="NIFTY50",      ticker="AXISBANK.NS"),
    StockInfo(symbol="MARUTI",     name="Maruti Suzuki",             sector="Auto",           index="NIFTY50",      ticker="MARUTI.NS"),
    StockInfo(symbol="BAJFINANCE", name="Bajaj Finance",             sector="Finance",        index="NIFTY50",      ticker="BAJFINANCE.NS"),
    StockInfo(symbol="SUNPHARMA",  name="Sun Pharmaceutical",        sector="Pharma",         index="NIFTY50",      ticker="SUNPHARMA.NS"),
    StockInfo(symbol="TITAN",      name="Titan Company",             sector="Consumer",       index="NIFTY50",      ticker="TITAN.NS"),
    StockInfo(symbol="WIPRO",      name="Wipro",                     sector="IT",             index="NIFTY50",      ticker="WIPRO.NS"),
    StockInfo(symbol="ULTRACEMCO", name="UltraTech Cement",          sector="Cement",         index="NIFTY50",      ticker="ULTRACEMCO.NS"),
    StockInfo(symbol="ONGC",       name="ONGC",                      sector="Energy",         index="NIFTY50",      ticker="ONGC.NS"),
    StockInfo(symbol="POWERGRID",  name="Power Grid Corp",           sector="Power",          index="NIFTY50",      ticker="POWERGRID.NS"),
    StockInfo(symbol="NTPC",       name="NTPC",                      sector="Power",          index="NIFTY50",      ticker="NTPC.NS"),
    StockInfo(symbol="TATAMOTORS", name="Tata Motors",               sector="Auto",           index="NIFTY50",      ticker="TATAMOTORS.NS"),
    StockInfo(symbol="TECHM",      name="Tech Mahindra",             sector="IT",             index="NIFTY50",      ticker="TECHM.NS"),
    StockInfo(symbol="TATASTEEL",  name="Tata Steel",                sector="Metal",          index="NIFTY50",      ticker="TATASTEEL.NS"),
    StockInfo(symbol="BAJAJFINSV", name="Bajaj Finserv",             sector="Finance",        index="NIFTY50",      ticker="BAJAJFINSV.NS"),
    StockInfo(symbol="NESTLEIND",  name="Nestle India",              sector="FMCG",           index="NIFTY50",      ticker="NESTLEIND.NS"),
    StockInfo(symbol="JSWSTEEL",   name="JSW Steel",                 sector="Metal",          index="NIFTY50",      ticker="JSWSTEEL.NS"),
    StockInfo(symbol="ADANIPORTS", name="Adani Ports",               sector="Infrastructure", index="NIFTY50",      ticker="ADANIPORTS.NS"),
    StockInfo(symbol="GRASIM",     name="Grasim Industries",         sector="Diversified",    index="NIFTY50",      ticker="GRASIM.NS"),
    StockInfo(symbol="CIPLA",      name="Cipla",                     sector="Pharma",         index="NIFTY50",      ticker="CIPLA.NS"),
    StockInfo(symbol="DRREDDY",    name="Dr. Reddy's Labs",          sector="Pharma",         index="NIFTY50",      ticker="DRREDDY.NS"),
    StockInfo(symbol="EICHERMOT",  name="Eicher Motors",             sector="Auto",           index="NIFTY50",      ticker="EICHERMOT.NS"),
    StockInfo(symbol="HEROMOTOCO", name="Hero MotoCorp",             sector="Auto",           index="NIFTY50",      ticker="HEROMOTOCO.NS"),
    StockInfo(symbol="DIVISLAB",   name="Divi's Laboratories",       sector="Pharma",         index="NIFTY50",      ticker="DIVISLAB.NS"),
    StockInfo(symbol="APOLLOHOSP", name="Apollo Hospitals",          sector="Healthcare",     index="NIFTY50",      ticker="APOLLOHOSP.NS"),
    StockInfo(symbol="BPCL",       name="BPCL",                      sector="Energy",         index="NIFTY50",      ticker="BPCL.NS"),
    StockInfo(symbol="COALINDIA",  name="Coal India",                sector="Mining",         index="NIFTY50",      ticker="COALINDIA.NS"),
    StockInfo(symbol="TATACONSUM", name="Tata Consumer Products",    sector="FMCG",           index="NIFTY50",      ticker="TATACONSUM.NS"),
    StockInfo(symbol="HINDALCO",   name="Hindalco Industries",       sector="Metal",          index="NIFTY50",      ticker="HINDALCO.NS"),
    StockInfo(symbol="INDUSINDBK", name="IndusInd Bank",             sector="Banking",        index="NIFTY50",      ticker="INDUSINDBK.NS"),
    StockInfo(symbol="SBILIFE",    name="SBI Life Insurance",        sector="Insurance",      index="NIFTY50",      ticker="SBILIFE.NS"),
    StockInfo(symbol="HDFCLIFE",   name="HDFC Life Insurance",       sector="Insurance",      index="NIFTY50",      ticker="HDFCLIFE.NS"),
    StockInfo(symbol="BRITANNIA",  name="Britannia Industries",      sector="FMCG",           index="NIFTY50",      ticker="BRITANNIA.NS"),
    StockInfo(symbol="SHRIRAMFIN", name="Shriram Finance",           sector="Finance",        index="NIFTY50",      ticker="SHRIRAMFIN.NS"),
    StockInfo(symbol="BEL",        name="Bharat Electronics",        sector="Defence",        index="NIFTY50",      ticker="BEL.NS"),
    StockInfo(symbol="TRENT",      name="Trent",                     sector="Retail",         index="NIFTY50",      ticker="TRENT.NS"),
    StockInfo(symbol="M&M",        name="Mahindra & Mahindra",       sector="Auto",           index="NIFTY50",      ticker="M&M.NS"),
    StockInfo(symbol="BAJAJ-AUTO", name="Bajaj Auto",                sector="Auto",           index="NIFTY50",      ticker="BAJAJ-AUTO.NS"),
]

# ---------------------------------------------------------------------------
# NIFTY Next 50
# ---------------------------------------------------------------------------
NIFTY_NEXT50 = [
    StockInfo(symbol="ADANIENT",   name="Adani Enterprises",         sector="Diversified",    index="NIFTY_NEXT50", ticker="ADANIENT.NS"),
    StockInfo(symbol="ADANIGREEN", name="Adani Green Energy",        sector="Power",          index="NIFTY_NEXT50", ticker="ADANIGREEN.NS"),
    StockInfo(symbol="ADANITRANS", name="Adani Transmission",        sector="Power",          index="NIFTY_NEXT50", ticker="ADANITRANS.NS"),
    StockInfo(symbol="AMBUJACEM",  name="Ambuja Cements",            sector="Cement",         index="NIFTY_NEXT50", ticker="AMBUJACEM.NS"),
    StockInfo(symbol="AUROPHARMA", name="Aurobindo Pharma",          sector="Pharma",         index="NIFTY_NEXT50", ticker="AUROPHARMA.NS"),
    StockInfo(symbol="BERGEPAINT", name="Berger Paints",             sector="Paints",         index="NIFTY_NEXT50", ticker="BERGEPAINT.NS"),
    StockInfo(symbol="BIOCON",     name="Biocon",                    sector="Pharma",         index="NIFTY_NEXT50", ticker="BIOCON.NS"),
    StockInfo(symbol="BOSCHLTD",   name="Bosch",                     sector="Auto",           index="NIFTY_NEXT50", ticker="BOSCHLTD.NS"),
    StockInfo(symbol="CANBK",      name="Canara Bank",               sector="Banking",        index="NIFTY_NEXT50", ticker="CANBK.NS"),
    StockInfo(symbol="CHOLAFIN",   name="Cholamandalam Finance",     sector="Finance",        index="NIFTY_NEXT50", ticker="CHOLAFIN.NS"),
    StockInfo(symbol="COLPAL",     name="Colgate-Palmolive",         sector="FMCG",           index="NIFTY_NEXT50", ticker="COLPAL.NS"),
    StockInfo(symbol="DABUR",      name="Dabur India",               sector="FMCG",           index="NIFTY_NEXT50", ticker="DABUR.NS"),
    StockInfo(symbol="DLF",        name="DLF",                       sector="Realty",         index="NIFTY_NEXT50", ticker="DLF.NS"),
    StockInfo(symbol="GODREJCP",   name="Godrej Consumer Products",  sector="FMCG",           index="NIFTY_NEXT50", ticker="GODREJCP.NS"),
    StockInfo(symbol="HAVELLS",    name="Havells India",             sector="Consumer",       index="NIFTY_NEXT50", ticker="HAVELLS.NS"),
    StockInfo(symbol="ICICIPRULI", name="ICICI Prudential Life",     sector="Insurance",      index="NIFTY_NEXT50", ticker="ICICIPRULI.NS"),
    StockInfo(symbol="ICICIGI",    name="ICICI Lombard GI",          sector="Insurance",      index="NIFTY_NEXT50", ticker="ICICIGI.NS"),
    StockInfo(symbol="INDIGO",     name="IndiGo (InterGlobe)",       sector="Aviation",       index="NIFTY_NEXT50", ticker="INDIGO.NS"),
    StockInfo(symbol="INDUSTOWER", name="Indus Towers",              sector="Telecom",        index="NIFTY_NEXT50", ticker="INDUSTOWER.NS"),
    StockInfo(symbol="LODHA",      name="Macrotech Developers",      sector="Realty",         index="NIFTY_NEXT50", ticker="LODHA.NS"),
    StockInfo(symbol="LUPIN",      name="Lupin",                     sector="Pharma",         index="NIFTY_NEXT50", ticker="LUPIN.NS"),
    StockInfo(symbol="MARICO",     name="Marico",                    sector="FMCG",           index="NIFTY_NEXT50", ticker="MARICO.NS"),
    StockInfo(symbol="MUTHOOTFIN", name="Muthoot Finance",           sector="Finance",        index="NIFTY_NEXT50", ticker="MUTHOOTFIN.NS"),
    StockInfo(symbol="NAUKRI",     name="Info Edge (Naukri)",        sector="IT",             index="NIFTY_NEXT50", ticker="NAUKRI.NS"),
    StockInfo(symbol="PATANJALI",  name="Patanjali Foods",           sector="FMCG",           index="NIFTY_NEXT50", ticker="PATANJALI.NS"),
    StockInfo(symbol="PFC",        name="Power Finance Corp",        sector="Finance",        index="NIFTY_NEXT50", ticker="PFC.NS"),
    StockInfo(symbol="PIDILITIND", name="Pidilite Industries",       sector="Chemicals",      index="NIFTY_NEXT50", ticker="PIDILITIND.NS"),
    StockInfo(symbol="PIIND",      name="PI Industries",             sector="Chemicals",      index="NIFTY_NEXT50", ticker="PIIND.NS"),
    StockInfo(symbol="PNB",        name="Punjab National Bank",      sector="Banking",        index="NIFTY_NEXT50", ticker="PNB.NS"),
    StockInfo(symbol="RECLTD",     name="REC Limited",               sector="Finance",        index="NIFTY_NEXT50", ticker="RECLTD.NS"),
    StockInfo(symbol="SIEMENS",    name="Siemens India",             sector="Capital Goods",  index="NIFTY_NEXT50", ticker="SIEMENS.NS"),
    StockInfo(symbol="SRF",        name="SRF",                       sector="Chemicals",      index="NIFTY_NEXT50", ticker="SRF.NS"),
    StockInfo(symbol="TORNTPHARM", name="Torrent Pharmaceuticals",   sector="Pharma",         index="NIFTY_NEXT50", ticker="TORNTPHARM.NS"),
    StockInfo(symbol="TVSMOTOR",   name="TVS Motor Company",         sector="Auto",           index="NIFTY_NEXT50", ticker="TVSMOTOR.NS"),
    StockInfo(symbol="UPL",        name="UPL",                       sector="Chemicals",      index="NIFTY_NEXT50", ticker="UPL.NS"),
    StockInfo(symbol="VBL",        name="Varun Beverages",           sector="FMCG",           index="NIFTY_NEXT50", ticker="VBL.NS"),
    StockInfo(symbol="VEDL",       name="Vedanta",                   sector="Metal",          index="NIFTY_NEXT50", ticker="VEDL.NS"),
    StockInfo(symbol="ZOMATO",     name="Zomato",                    sector="Consumer Tech",  index="NIFTY_NEXT50", ticker="ZOMATO.NS"),
    StockInfo(symbol="ZYDUSLIFE",  name="Zydus Lifesciences",        sector="Pharma",         index="NIFTY_NEXT50", ticker="ZYDUSLIFE.NS"),
]

# ---------------------------------------------------------------------------
# Bank NIFTY
# ---------------------------------------------------------------------------
BANKNIFTY = [
    StockInfo(symbol="HDFCBANK",   name="HDFC Bank",                 sector="Banking",        index="BANKNIFTY",    ticker="HDFCBANK.NS"),
    StockInfo(symbol="ICICIBANK",  name="ICICI Bank",                sector="Banking",        index="BANKNIFTY",    ticker="ICICIBANK.NS"),
    StockInfo(symbol="KOTAKBANK",  name="Kotak Mahindra Bank",       sector="Banking",        index="BANKNIFTY",    ticker="KOTAKBANK.NS"),
    StockInfo(symbol="SBIN",       name="State Bank of India",       sector="Banking",        index="BANKNIFTY",    ticker="SBIN.NS"),
    StockInfo(symbol="AXISBANK",   name="Axis Bank",                 sector="Banking",        index="BANKNIFTY",    ticker="AXISBANK.NS"),
    StockInfo(symbol="INDUSINDBK", name="IndusInd Bank",             sector="Banking",        index="BANKNIFTY",    ticker="INDUSINDBK.NS"),
    StockInfo(symbol="BANDHANBNK", name="Bandhan Bank",              sector="Banking",        index="BANKNIFTY",    ticker="BANDHANBNK.NS"),
    StockInfo(symbol="FEDERALBNK", name="Federal Bank",              sector="Banking",        index="BANKNIFTY",    ticker="FEDERALBNK.NS"),
    StockInfo(symbol="AUBANK",     name="AU Small Finance Bank",     sector="Banking",        index="BANKNIFTY",    ticker="AUBANK.NS"),
    StockInfo(symbol="IDFCFIRSTB", name="IDFC First Bank",           sector="Banking",        index="BANKNIFTY",    ticker="IDFCFIRSTB.NS"),
    StockInfo(symbol="PNB",        name="Punjab National Bank",      sector="Banking",        index="BANKNIFTY",    ticker="PNB.NS"),
    StockInfo(symbol="CANBK",      name="Canara Bank",               sector="Banking",        index="BANKNIFTY",    ticker="CANBK.NS"),
]

# ---------------------------------------------------------------------------
# Combined universe
# ---------------------------------------------------------------------------

def get_full_universe() -> List[StockInfo]:
    seen = set()
    result = []
    for stock in NIFTY50 + NIFTY_NEXT50 + BANKNIFTY:
        if stock.symbol not in seen:
            seen.add(stock.symbol)
            result.append(stock)
    return result


def get_by_index(index: str) -> List[StockInfo]:
    mapping = {
        "NIFTY50":      NIFTY50,
        "NIFTY_NEXT50": NIFTY_NEXT50,
        "BANKNIFTY":    BANKNIFTY,
        "ALL":          get_full_universe(),
    }
    return mapping.get(index.upper(), get_full_universe())


def get_sectors() -> List[str]:
    return sorted(set(s.sector for s in get_full_universe()))


TICKER_MAP: Dict[str, StockInfo] = {s.ticker: s for s in get_full_universe()}
SYMBOL_MAP: Dict[str, StockInfo] = {s.symbol: s for s in get_full_universe()}
