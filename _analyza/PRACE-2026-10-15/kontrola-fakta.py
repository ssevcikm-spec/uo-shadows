# kontrola-fakta.py -- samo-kontrola FAKTA.md (struktura, diakritika, cislovani)
# Spusteni: $env:PYTHONIOENCODING='utf-8'; python _analyza\PRACE-2026-10-15\kontrola-fakta.py
import pathlib
import re
import sys

f = pathlib.Path(__file__).with_name("FAKTA.md")
t = f.read_text(encoding="utf-8")
ls = t.splitlines()

print(f"soubor: {f}")
print(f"radku: {len(ls)}, znaku: {len(t)}, bajtu: {f.stat().st_size}")
print(f"prvni 3 bajty: {f.read_bytes()[:3].hex()} (BOM by byl efbbbf)")
print()
print("NADELPISY:")
for h in ls:
    if h.startswith("#"):
        print("  " + h)
print()

rows = [l for l in ls if re.match(r"^\| \d+ \|", l)]
nums = [int(re.match(r"^\| (\d+) \|", l).group(1)) for l in rows]
print(f"radku tabulky faktu (| cislo |): {len(rows)}")
print(f"cisla faktu: {min(nums)}..{max(nums)}")
chybi = sorted(set(range(1, max(nums) + 1)) - set(nums))
print(f"chybejici cisla: {chybi if chybi else 'zadna'}")
dup = sorted({n for n in nums if nums.count(n) > 1})
print(f"duplicitni cisla: {dup if dup else 'zadna'}")
print(f"radku se stavem NEMERENO: {sum(1 for l in rows if 'NEMĚŘENO' in l)}")
print()

povinne = {
    "hlavicka: HEAD commitu": "6986b0d" in t,
    "hlavicka: datum": "15. 10. 2026" in t,
    "hlavicka: cim mereno": "Godot `4.7.2" in t,
    "hlavicka: upozorneni na commit": "Platí k tomuto commitu" in t,
    "sloupec: jak bylo změřeno": "jak bylo změřeno" in t,
    "sloupec: zdroj": "| zdroj (soubor) |" in t,
    "sloupec: stav": "| stav |" in t,
    "oddil: Co zůstalo neměřeno": "## Co zůstalo neměřeno" in t,
    "oddil: Rozpory": "## Rozpory" in t,
    # POZOR: prvni verze teto kontroly pozadovala VSECH 15 znaku 'ěščřžýáíéúůňďť'
    # a hlasila falesny poplach -- 'ď' a 'ť' se v textu prirozene nevyskytuji.
    # Druha verze pozadovala konkretni slova a spadla na 'vůbec', ktere jsem
    # v textu nepouzil. Spravne meritko je POCET ruznych znaku s diakritikou
    # (kolik jich je), ne pritomnost konkretniho slova.
    "diakritika (aspon 10 z 15 znaku)": sum(1 for c in "ěščřžýáíéúůňďť" if c in t) >= 10,
    "zadny mojibake": "Ã" not in t and "Å" not in t,
}
for k, v in povinne.items():
    print(f"  {'OK ' if v else 'CHYBI'} {k}")

# kontrola: kazdy radek tabulky ma 6 sloupcu
spatne = [l for l in rows if l.count("|") != 7]
print()
print(f"radky tabulky s jinym poctem sloupcu nez 6: {len(spatne)}")
for l in spatne[:5]:
    print("   " + l[:160])

# kontrola: NEMERENO ma pojmenovany duvod v oddilu Co zustalo nemereno
oddil = t.split("## Co zůstalo neměřeno")[1].split("## Jak tenhle list použít")[0]
pocet_polozek = len(re.findall(r"^\d+\. \*\*", oddil, re.M))
print(f"polozek v 'Co zůstalo neměřeno': {pocet_polozek}")
print(f"  z toho s pojmenovanym duvodem ('Důvod:'): {oddil.count('Důvod:')}")

sys.exit(0 if not chybi and not spatne and all(povinne.values()) else 1)
