import json, os, re, urllib.request, urllib.error

COUNTRY_MAP = {
    "GBR":"England","DEU":"Germany","ITA":"Italy","ESP":"Spain","FRA":"France","PRT":"Portugal",
    "NLD":"Netherlands","BEL":"Belgium","CHE":"Switzerland","AUT":"Austria","POL":"Poland",
    "CZE":"Czech Republic","UKR":"Ukraine","RUS":"Russia","TUR":"Turkey","GRC":"Greece",
    "HRV":"Croatia","SRB":"Serbia","ROU":"Romania","BGR":"Bulgaria","HUN":"Hungary",
    "SWE":"Sweden","NOR":"Norway","DNK":"Denmark","FIN":"Finland","IRL":"Ireland",
    "USA":"United States","CAN":"Canada","MEX":"Mexico","BRA":"Brazil","ARG":"Argentina",
    "COL":"Colombia","CHL":"Chile","PER":"Peru","URY":"Uruguay","ECU":"Ecuador","VEN":"Venezuela",
    "BOL":"Bolivia","PRY":"Paraguay","AUS":"Australia","NZL":"New Zealand","JPN":"Japan",
    "KOR":"South Korea","CHN":"China","IND":"India","IDN":"Indonesia","THA":"Thailand",
    "VNM":"Vietnam","MYS":"Malaysia","PHL":"Philippines","SAU":"Saudi Arabia","ARE":"UAE",
    "QAT":"Qatar","IRN":"Iran","IRQ":"Iraq","ISR":"Israel","EGY":"Egypt","ZAF":"South Africa",
    "NGA":"Nigeria","KEN":"Kenya","GHA":"Ghana","MAR":"Morocco","TUN":"Tunisia","DZA":"Algeria",
    "LBY":"Libya","SDN":"Sudan","ETH":"Ethiopia","TZA":"Tanzania","AGO":"Angola","MOZ":"Mozambique",
    "ZMB":"Zambia","ZWE":"Zimbabwe","CIV":"Ivory Coast","SEN":"Senegal","CMR":"Cameroon",
    "COD":"DR Congo","SYR":"Syria","JOR":"Jordan","LBN":"Lebanon","OMN":"Oman","BHR":"Bahrain",
    "KWT":"Kuwait","BGD":"Bangladesh","PAK":"Pakistan","LKA":"Sri Lanka","NPL":"Nepal",
    "PRK":"North Korea","HKG":"Hong Kong","TWN":"Taiwan","SGP":"Singapore","CUB":"Cuba",
    "DOM":"Dominican Republic","PRI":"Puerto Rico","CRI":"Costa Rica","GTM":"Guatemala",
    "HND":"Honduras","SLV":"El Salvador","PAN":"Panama","JAM":"Jamaica","TTO":"Trinidad",
    "BIH":"Bosnia","SVN":"Slovenia","SVK":"Slovakia","LTU":"Lithuania","LVA":"Latvia",
    "EST":"Estonia","BLR":"Belarus","MDA":"Moldova","GEO":"Georgia","ARM":"Armenia","AZE":"Azerbaijan",
    "ALB":"Albania","MKD":"North Macedonia","MNE":"Montenegro","ISL":"Iceland","MLT":"Malta",
    "LUX":"Luxembourg","CYP":"Cyprus","NIC":"Nicaragua","MNG":"Mongolia","MMR":"Myanmar",
    "KHM":"Cambodia","LAO":"Laos","PNG":"Papua New Guinea","FJI":"Fiji",
    "UZB":"Uzbekistan","KAZ":"Kazakhstan","TKM":"Turkmenistan","KGZ":"Kyrgyzstan","TJK":"Tajikistan",
    "SCO":"Scotland","WAL":"Wales"
}

SKIP_KEYWORDS = ["raceway", "speedway", "racecourse", "racetrack", "autodrome", "motor speedway",
                 "f1 circuit", "circuit", "hippodrome", "horse", "equestrian", "race-use",
                 "baseball", "cricket", "golf", "tennis", "velodrome", "dragstrip", "fairgrounds",
                 "rodeo", "greyhound", "dog track", "speedway", "motorsport"]

def is_stadium_keep(name, team, capacity):
    cap = int(capacity) if str(capacity).lstrip('-').isdigit() else 0
    if cap < 10000:
        return False
    nl = name.lower()
    for s in SKIP_KEYWORDS:
        if s in nl:
            return False
    tl = (team or "").lower()
    if tl in ["race-use", "horse racing-use", "equestrian-use", "horse-racing use", "horse racing use"]:
        return False
    return True

base = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(base, "..")
out_path = os.path.join(root, "data", "stadiums.json")

geo_path = os.path.join(root, "data", "world_stadiums.geojson")
print("Reading local stadium data...")
with open(geo_path, "r", encoding="utf-8") as f:
    geo = json.load(f)

with open(out_path, "r", encoding="utf-8") as f:
    existing = json.load(f)

existing_ids = set(s["id"] for s in existing["stadiums"])
existing_names = set(s["name"].lower().strip() for s in existing["stadiums"])
existing_cities = {(s["name"].lower().strip(), s["location"].lower().strip()) for s in existing["stadiums"]}

new_stadiums = []
seen_names = set()

for feat in geo["features"]:
    p = feat["properties"]
    name = (p.get("s_name") or "").strip()
    city = (p.get("city") or "").strip()
    country_code = (p.get("country") or "").strip()
    team = (p.get("team") or "").strip()
    capacity = p.get("capacity", "0")

    if not name or not is_stadium_keep(name, team, capacity):
        continue

    cap = int(capacity) if str(capacity).lstrip('-').isdigit() else 0
    if cap < 10000:
        continue

    nk = name.lower().strip()
    ck = city.lower().strip()
    if nk in existing_names or (nk, ck) in existing_cities:
        continue

    if nk in seen_names:
        continue
    seen_names.add(nk)

    country = COUNTRY_MAP.get(country_code, country_code)
    sid = re.sub(r'[^a-z0-9-]', '', name.lower()
                 .replace(" ", "-").replace("'", "")
                 .replace("\u00e1","a").replace("\u00e9","e").replace("\u00e3","a")
                 .replace("\u00f5","o").replace("\u00e2","a").replace("\u00ea","e")
                 .replace("\u00f3","o").replace("\u00ed","i").replace("\u00fa","u")
                 .replace("\u00f1","n").replace("\u00fc","u").replace("\u00e7","c")
                 .replace("\u00f4","o").replace("\u00ee","i").replace("--","-").strip("-"))

    if sid in existing_ids:
        sid = sid + "-" + country_code.lower()
    if sid in existing_ids:
        continue

    new_stadiums.append({
        "id": sid,
        "name": name,
        "location": city,
        "country": country,
        "capacity": cap
    })

merged = list(existing["stadiums"])
merged.extend(new_stadiums)

output = {"stadiums": merged}
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Existing: {len(existing['stadiums'])}, Added: {len(new_stadiums)}, Total: {len(merged)}")
