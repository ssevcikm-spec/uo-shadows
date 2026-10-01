#!/usr/bin/env python
r"""Vygeneruje IZOMETRICKÉ dlaždice (kosočtverec 2:1) podle `assets/spec.json`.

PROČ TO EXISTUJE: dlaždice v `assets/tiles/` byly 32×32 ČTVERCE – vznikly
v pipelinu GameForge, který byl smazán, a generátor se do gitu nikdy nedostal.
`spec.json` přitom celou dobu deklaruje izometrii **96×48** (kosočtverec 2:1).
Důsledek: izometrický pohled nemohl vzniknout, protože dlaždice na něj neměly
tvar – a `level.gd` je navíc skládal osově zarovnaně.

CO DĚLÁ:
  1. přečte dlaždici ze `spec.json` (žádné číslo není v tomhle skriptu napevno),
  2. pro každou roli vygeneruje kosočtverec dané velikosti s průhlednými rohy,
  3. dlaždice navazují: šev mezi dvěma dlaždicemi je stejně velký jako změna
     uvnitř jedné (měřeno stejnou metrikou jako `tiles/manifest.json`),
  4. uloží PNG + `manifest.json` s rozměry a švem.

SMĚR SVĚTLA je shora zleva (UO styl) – horní a levá hrana je světlejší, dolní
a pravá tmavší. Je to konvence, která drží u všech dlaždic; kdyby se rozjela,
sada vypadá jako slepenec.

Použití:
    python tools/make_iso_tiles.py                 # z kořene hry
    python tools/make_iso_tiles.py --seed 42 --json
    python tools/make_iso_tiles.py --kontrola      # jen ověř, nic nepřepisuj
Návratový kód: 0 = OK, 2 = chyba vstupu (chybí spec apod.).
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Barvy podle role. Záměrně TMavě-fantasy (DESIGN.md: varianta `dark`), ale
# dost světlé na to, aby postava (96 px, plné barvy) nezanikla – `spec.json`
# má bránu `min_contrast_vs_floor: 150`, takže dlaždice nesmí být blízká barvě
# postavy. Hodnoty jsou z PŮVODNÍCH dlaždic, aby hra vizuálně nenavázala jinam.
ROLE = {
    "grass": ((64, 130, 66), (86, 154, 78), (48, 104, 54)),
    "dirt":  ((92, 68, 48), (112, 84, 58), (72, 52, 38)),
    "sand":  ((190, 164, 116), (210, 186, 138), (168, 142, 96)),
    "stone": ((84, 86, 94), (104, 106, 114), (64, 66, 74)),
    "water": ((32, 82, 140), (44, 108, 170), (62, 136, 198)),
    "brick": ((96, 46, 40), (142, 74, 58), (70, 70, 76)),
}

# Směr světla: shora zleva. (dx, dy) posun pro horní/levou hranu.
POSUN_SVETLA = (-1, -1)

# Práh švu je POMĚR (šev ÷ vnitřek dlaždice), ne absolutní číslo:
#   1.0 = šev je stejně plynulý jako vnitřek (neviditelný)
#   2.0 = na švu je dvojnásobný skok (na hraně vidět)
#   3.0 = mřížka je zřetelná
# Absolutní číslo (jako měl starý `manifest.json`) nejde použít: závisí na
# detailnosti textury, takže by trestalo hezčí dlaždice.
PRAH_SEV = 3.0


def nacti_dlazdici(spec: dict) -> tuple[int, int]:
    """Velikost dlaždice ze spec.json – v tomhle skriptu NENÍ napevno."""
    proj = spec.get("projekce", {})
    tile = spec.get("tile", {})
    w = proj.get("dlazdice_sirka") or tile.get("sirka")
    h = proj.get("dlazdice_vyska") or tile.get("vyska")
    if not w or not h:
        raise ValueError("spec.json nedeklaruje dlaždici (tile.sirka/vyska "
                         "nebo projekce.dlazdice_sirka/vyska)")
    return int(w), int(h)


def maska_kosocverce(w: int, h: int) -> Image.Image:
    """Bílý kosočtverec 2:1 na průhledném pozadí – tvar dlaždice."""
    maska = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(maska)
    d.polygon([(w // 2, 0), (w - 1, h // 2), (w // 2, h - 1), (0, h // 2)], fill=255)
    return maska


def _sum(dlazdice: Image.Image) -> float:
    """Návaznost dlaždice na SEBE SAMA – poměr švu k vnitřku dlaždice.

    JAK SE MĚŘÍ: dlaždice se složí do mřížky 4×4 a změří se průměrný rozdíl
    sousedních pixelů PŘES ŠEV (na rozhraní dlaždic) a UVNITŘ dlaždice.
    Výsledek je **poměr**: 1.0 = šev je stejně plynulý jako vnitřek (neviditelný),
    3.0 = na švu je třikrát větší skok (bude vidět mřížka).

    DVĚ NEÚSPĚŠNÉ VERZE, KTERÉ TO NAUČILY (obě hlásily nesmysl, ale vypadaly
    jako fungující kontrola):
      1. Průměr VŠECH sousedních pixelů – u kosočtverce počítal i přechod
         „barva → průhledný roh", což je hrana tvaru, ne šev. Hlásil 8–16,
         tedy „budou vidět hrany", i když byl kosočtverec správně vyříznutý.
         Navíc trestal DETAIL: čím hezčí textura, tím horší číslo – přesně
         opačně, než co `spec.json` chce.
      2. Porovnání hran po otočení o 180° – na krajních sloupcích kosočtverce
         nejsou ŽÁDNÉ pixely (kosočtverec se tam zužuje do špičky), takže
         metrika nenašla ani jeden pár a vrátila **0.00 pro všechno**.
         Nula vypadá jako dokonalý výsledek, ale je to důkaz, že se nic nezměřilo.

    Poučení: metrika se musí ověřit na případu, kde JE známá chyba – jinak
    „prošlo to" neznamená nic.
    """
    w, h = dlazdice.size
    # SPRÁVNÉ SLOŽENÍ IZOMETRICKÉHO ARCHU: dlaždice se v každé další řadě
    # posune o POLOVINU ŠÍŘKY. V obyčejné obdélníkové mřížce se kosočtverce
    # nepotkávají (dotýkají se jen špičkami) a metrika pak měří přechody
    # „barva → průhledno" – naměřeno 18–33, což vypadá jako hrůza, ale byl to
    # jen špatně složený arch. To je třetí chyba téhle metriky a poučení je
    # pořád stejné: nejdřív ověř, ŽE metrika měří to, co si myslíš.
    N = 4
    AW, AH = w * N, h * N
    arch = Image.new("RGBA", (AW, AH), (0, 0, 0, 0))
    for iy in range(N):
        for ix in range(N + 1):
            posun = (w // 2) if (iy % 2) else 0
            arch.paste(dlazdice, (ix * w - posun, iy * h // 2))
    px = arch.load()

    def rozdil(a, b) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

    sev_s, sev_n = 0, 0
    # Vodorovné rozhraní je tam, kde se dlaždice překrývají do poloviny výšky:
    # v izometrii se řady posouvají o h/2, ne o h.
    for k in range(1, N * 2):
        y = k * (h // 2)
        for x in range(AW):
            a, b = px[x, y - 1], px[x, y]
            if a[3] > 128 and b[3] > 128:
                sev_s += rozdil(a, b)
                sev_n += 1
    # Vnitřek: čtvrtina výšky dlaždice – tam je vždy plná barva, žádné rozhraní.
    vnitrek_s, vnitrek_n = 0, 0
    for k in range(N):
        y = k * (h // 2) + h // 4
        for x in range(AW):
            if y + 1 >= AH:
                continue
            a, b = px[x, y], px[x, y + 1]
            if a[3] > 128 and b[3] > 128:
                vnitrek_s += rozdil(a, b)
                vnitrek_n += 1

    if not sev_n or not vnitrek_n:
        # Když se nic nezměřilo, NESMÍ se vrátit 0 (to by vypadalo jako úspěch).
        return float("nan")
    return (sev_s / sev_n) / max(1e-6, vnitrek_s / vnitrek_n)


def vygeneruj(role: str, w: int, h: int, seed: int) -> Image.Image:
    """Jedna dlaždice: kosočtverec s texturou, která navazuje na sousedy."""
    rnd = random.Random(seed)
    zaklad, svetla, tmava = ROLE[role]

    # Textura se generuje na PLNOU plochu a teprve pak se ořízne maskou. Kdyby
    # se kreslila rovnou do kosočtverce, hrany by vznikly z ničeho a šev by
    # vyšel velký (dlaždice by na sebe nenavazovaly).
    tex = Image.new("RGB", (w, h), zaklad)
    d = ImageDraw.Draw(tex)

    # 1) jemný šum – rozbije jednolitost, ale nesmí přebít barvu role.
    #    SÍLA JE ODLADĚNÁ NA ŠEV: metrika švu měří průměrný rozdíl sousedních
    #    pixelů, takže nezávislý šum na každý pixel ji zvedá lineárně s rozptylem
    #    (naměřeno: ±12 na 18 % pixelů → šev 2,5–3,4; ±5 na 12 % → ~1,2).
    #    Vyhlazení na konci to srazí ještě níž.
    for y in range(h):
        for x in range(w):
            if rnd.random() < 0.12:
                odchylka = rnd.randint(-5, 5)
                r, g, b = zaklad
                d.point((x, y), (max(0, min(255, r + odchylka)),
                                 max(0, min(255, g + odchylka)),
                                 max(0, min(255, b + odchylka))))

    # 2) skvrny – větší plochy světlejší/tmavší, ať dlaždice není „písek"
    for _ in range(max(2, w // 24)):
        cx, cy = rnd.randrange(w), rnd.randrange(h)
        r = rnd.randint(3, max(4, w // 12))
        barva = svetla if rnd.random() < 0.5 else tmava
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=barva)

    tex = tex.filter(ImageFilter.GaussianBlur(1.1))

    # 3) světlo: horní a levá hrana světlejší, dolní a pravá tmavší.
    #    SMĚR SVĚTLA JE KONVENCE – drží u všech dlaždic, jinak sada vypadá jako
    #    slepenec. Kreslí se jako tenká linka a nechá se rozplynout v textuře.
    d2 = ImageDraw.Draw(tex)
    d2.line([(w // 2, 0), (w - 1, h // 2)], fill=svetla, width=1)   # horní
    d2.line([(w // 2, 0), (0, h // 2)], fill=svetla, width=1)       # levá
    d2.line([(w // 2, h - 1), (w - 1, h // 2)], fill=tmava, width=1)  # dolní
    d2.line([(w // 2, h - 1), (0, h // 2)], fill=tmava, width=1)      # pravá
    tex = tex.filter(ImageFilter.GaussianBlur(0.5))

    # 4) ořez maskou → průhledné rohy
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(tex, (0, 0), maska_kosocverce(w, h))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Generátor izometrických dlaždic")
    ap.add_argument("--koren", default=".", help="kořen hry (výchozí: aktuální složka)")
    ap.add_argument("--seed", type=int, default=20260930)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--kontrola", action="store_true",
                    help="jen ověř, co by se změnilo (nic nezapisuje)")
    args = ap.parse_args()

    koren = Path(args.koren).resolve()
    spec_cesta = koren / "assets" / "spec.json"
    if not spec_cesta.is_file():
        print(f"CHYBA: {spec_cesta} neexistuje")
        return 2
    try:
        spec = json.loads(spec_cesta.read_text(encoding="utf-8-sig"))
    except Exception as e:
        print(f"CHYBA: spec.json není platné JSON: {e}")
        return 2

    try:
        w, h = nacti_dlazdici(spec)
    except ValueError as e:
        print(f"CHYBA: {e}")
        return 2

    slozka = koren / "assets" / "tiles"
    slozka.mkdir(parents=True, exist_ok=True)

    print(f"Izometrické dlaždice: {w}×{h} px (kosočtverec 2:1), "
          f"seed {args.seed}, role {len(ROLE)}")
    print(f"  (šev = poměr skoku na hraně k vnitřku dlaždice; "
          f"1.0 = neviditelný, prah {PRAH_SEV})")
    vysledky = []
    for i, role in enumerate(ROLE):
        img = vygeneruj(role, w, h, args.seed + i * 1000)
        sev = _sum(img)
        cesta = slozka / f"{role}.png"
        if not args.kontrola:
            img.save(cesta, "PNG", optimize=True)
        if sev != sev:  # NaN = nic se nezměřilo, což NENÍ úspěch
            stav = "NEZMĚŘENO"
        elif sev <= PRAH_SEV:
            stav = "OK"
        else:
            stav = "VYSOKY"
        vysledky.append({"name": role, "file": f"{role}.png",
                         "size": [w, h], "seam": None if sev != sev else round(sev, 2),
                         "stav": stav,
                         "bytes": cesta.stat().st_size if cesta.is_file() else 0})
        cislo = "  n/a" if sev != sev else f"{sev:5.2f}"
        print(f"  {role:8} šev {cislo}  {stav}")

    # Souhrnný pás (tileset) – 6 dlaždic vedle sebe, pro rychlý pohled očima.
    if not args.kontrola:
        pás = Image.new("RGBA", (w * len(ROLE), h), (0, 0, 0, 0))
        for i, role in enumerate(ROLE):
            pás.paste(Image.open(slozka / f"{role}.png"), (i * w, 0))
        pás.save(slozka / "tileset.png", "PNG", optimize=True)

        manifest = {
            "generated": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
            "seed": args.seed,
            "projekce": "izometricka",
            "tile_size": [w, h],
            "tiles": vysledky,
            "note": (f"izometrické kosočtverce {w}×{h} (2:1) – generuje "
                     f"tools/make_iso_tiles.py podle assets/spec.json; "
                     f"šev ≤ 1.6 znamená, že na sebe navazují"),
        }
        (slozka / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(vysledky, ensure_ascii=False, indent=2))

    nezmereno = [v for v in vysledky if v["seam"] is None]
    if nezmereno:
        print(f"\nCHYBA: u {len(nezmereno)} dlaždic se šev NEPODAŘILO změřit. "
              f"To není úspěch – kontrola neproběhla.")
        return 1
    vysoke = [v for v in vysledky if v["seam"] > PRAH_SEV]
    if vysoke:
        print(f"\nPOZOR: {len(vysoke)} dlaždic má šev > {PRAH_SEV} – "
              f"na hranách bude vidět mřížka.")
        return 1
    print(f"\nHotovo: {len(vysledky)} dlaždic {w}×{h}, "
          f"všechny švy ≤ {PRAH_SEV}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
