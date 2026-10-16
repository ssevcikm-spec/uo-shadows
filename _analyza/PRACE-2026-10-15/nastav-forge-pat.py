"""nastav-forge-pat.py — nastaví v repu hry secret `FORGE_PAT`.

PROČ (naměřeno 15. 10. 2026):
  Krok „Otevři pull request" v `.github/workflows/agent.yml:540` používá
  `secrets.FORGE_PAT`. V repu `uo-shadows` ten secret chybí (nebo je prázdný),
  takže `create-pull-request` spadne na `fatal: could not read Username for
  'https://github.com'` — a agentem vyrobený kód se NIKDY nedostane do PR.
  Naměřený rozdíl: `coin-picker` má od 13. 10. 2026 **14 PR**, `uo-shadows` **0**,
  přičemž obě hry používají stejný workflow.

BEZPEČNOST: hodnota se čte ze souboru v `.secrets/` a **nikdy se nevypisuje**;
do GitHubu jde zašifrovaná veřejným klíčem repa (libsodium sealed box), jak
vyžaduje API. Skript vypíše jen jméno secretu a výsledek HTTP.

POUŽITÍ:
  python _analyza/PRACE-2026-10-15/nastav-forge-pat.py            # kontrolní běh (nic nemění)
  python _analyza/PRACE-2026-10-15/nastav-forge-pat.py --zapis    # skutečně nastaví
"""

import base64
import io
import json
import os
import sys
import urllib.request

REPO = "ssevcikm-spec/uo-shadows"
NAZEV = "FORGE_PAT"
# Kterým tokenem se secret NASTAVUJE (musí umět `secrets: write` — to umí jen
# klasický PAT; fine-grained `conductor_pat` na secrets nedosáhne).
PAT_SOUBOR = r"E:\Workspaces\forge-orchestra\.secrets\github_pat.txt"
# Která HODNOTA se nastavuje. Ověřeno 16. 10. 2026 testem „vytvoř větev a smaž ji":
#   conductor_pat.txt ............ 201 (umí pushovat)  ← používá se
#   github_pat.txt ............... 201 (umí pushovat)
#   conductor_github_token.txt ... 403 Resource not accessible  ← NEFUNGUJE
#   coin-picker_forge_pat.txt .... 403 (fine-grained bez Contents: write)
HODNOTA_SOUBOR = r"E:\Workspaces\forge-orchestra\.secrets\conductor_pat.txt"


def http(url, metoda="GET", telo=None, token=None):
    data = json.dumps(telo).encode("utf-8") if telo is not None else None
    req = urllib.request.Request(url, data=data, method=metoda)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        return e.code, {"chyba": e.read().decode("utf-8")[:200]}


def main():
    zapis = "--zapis" in sys.argv
    with io.open(PAT_SOUBOR, encoding="utf-8") as f:
        pat = f.read().strip()
    with io.open(HODNOTA_SOUBOR, encoding="utf-8") as f:
        hodnota = f.read().strip()

    print("repo:   %s" % REPO)
    print("secret: %s" % NAZEV)
    print("nastavuje se tokenem: %s" % os.path.basename(PAT_SOUBOR))
    print("hodnota ze souboru:   %s (%d znaků), NEVYPISUJE SE"
          % (os.path.basename(HODNOTA_SOUBOR), len(hodnota)))

    stav, klic = http("https://api.github.com/repos/%s/actions/secrets/public-key" % REPO,
                      token=pat)
    if stav != 200:
        print("CHYBA: veřejný klíč se nepodařilo načíst (HTTP %s): %s" % (stav, klic))
        return 2
    print("veřejný klíč repa: key_id=%s" % klic["key_id"])

    if not zapis:
        print("\nKONTROLNÍ BĚH — nic se nemění. Spusť s --zapis, ať se secret nastaví.")
        return 0

    try:
        from nacl import encoding, public
    except ImportError:
        print("CHYBA: chybí PyNaCl (`python -m pip install pynacl`)")
        return 2

    pk = public.PublicKey(klic["key"].encode("utf-8"), encoding.Base64Encoder())
    sealed = public.SealedBox(pk).encrypt(hodnota.encode("utf-8"))
    zaheslovano = base64.b64encode(sealed).decode("utf-8")

    stav, odpoved = http(
        "https://api.github.com/repos/%s/actions/secrets/%s" % (REPO, NAZEV),
        metoda="PUT", telo={"encrypted_value": zaheslovano, "key_id": klic["key_id"]},
        token=pat)
    if stav in (201, 204):
        print("\nHOTOVO: secret %s nastaven (HTTP %s)." % (NAZEV, stav))
        print("Ověření: příští běh agent.yml už musí projít krokem „Otevři pull request“.")
        return 0
    print("\nCHYBA: HTTP %s — %s" % (stav, odpoved))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
