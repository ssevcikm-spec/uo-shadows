"""rozdel-shell-coins.py — jednorázový zásah do plánu (15. 10. 2026).

CO DĚLÁ A PROČ (naměřeno, ne odhad):
  1. `world.bodies` → `done: true`: kód vyrobil agent orchestry v běhu #374 a prošel
     v CI parsováním i testy; PR nevzniklo, protože krok „Otevři pull request" nemá
     v repu hry funkční secret FORGE_PAT (`fatal: could not read Username`).
     Patch byl integrován ručně a ověřen (`[test] 113 kontrol, 0 selhání`).
  2. `shell.coins` → ROZDELENA na `shell.nocoins` (game.gd) a `shell.save` (save.gd).
     Důvod: aider si do chatu přidá každý vlastněný soubor CELÝ (game.gd ~3 940 t,
     save.gd ~1 894 t) a request měl **40 537 t proti limitu 8 000** (Groq
     `gpt-oss-120b`) → model zadání NIKDY neviděl (3× „agent nic nezměnil").
  3. `sim.wire` přepojeno na nové id (záviselo na `shell.coins`).

POUŽITÍ: python _analyza/PRACE-2026-10-15/rozdel-shell-coins.py
"""

import io
import json
import os

PLAN = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                    ".forge", "roadmap.json")

DONE_NOTE_BODIES = (
    "HOTOVO 15. 10. 2026: kód vyrobil agent orchestry v běhu #374 (19:14 UTC) a prošel "
    "v CI parsováním i testy. PR nevzniklo — krok „Otevři pull request“ v repu hry nemá "
    "fungující secret FORGE_PAT (`fatal: could not read Username for https://github.com`). "
    "Patch jsem proto stáhl z artefaktu běhu a integroval ručně (commit 2faed29); ověřeno: "
    "[test] 113 kontrol, 0 selhání; check-wiring 102 funkcí v 17 souborech. "
    "Artefakt: _analyza/PRACE-2026-10-15/patchy/run374.zip."
)

SPOLECNE = (
    "POZOR (naměřeno 15. 10. 2026): tahle granule vznikla ROZDELENÍM původní `shell.coins`, "
    "která vlastnila DVA soubory. Aider si do chatu přidá každý soubor celý (game.gd ~3 940 t, "
    "save.gd ~1 894 t) a request pak měl 40 537 t proti limitu 8 000 (Groq) → model zadání "
    "NIKDY neviděl (3× „agent nic nezměnil“). Granule proto vlastní JEDEN soubor."
)

PROMPT_NOCOINS = (
    "V scripts/game.gd ODSTRAŇ logiku mincí a skóre: proměnné `score` a `coin_total`, hledání "
    "uzlů ve skupině `coin`, text „Skóre“ v `_update_hud()` a obsluhu sběru mincí — design je "
    "sandbox, ne sběračka mincí. HUD nech existovat, ale ať zobrazuje hodnoty z registru "
    "(`get_parent().get_node_or_null(\"Registry\")`); když je null, napiš „—“ (dlouhá pomlčka). "
    "NIC JINÉHO neměň (ukládání ani hráče). Soubor začíná `extends Node` — zachovej to. "
    "Pozor na parsování: `:=` jen u hodnot se známým typem; `Vector2.ZERO` typ nemá, piš "
    "`var v: Vector2 = Vector2.ZERO`; typy jako `Level` v anotaci NEEXISTUJÍ (piš `Node`). "
    "Testy: `python .forge/check-wiring.py .` a Godot smoke bez nové chyby v logu. " + SPOLECNE
)

PROMPT_SAVE = (
    "V scripts/save.gd ZACHOVEJ veřejné rozhraní `save() -> bool` a `load() -> bool` a přepiš "
    "cestu z `user://sandbox.cfg` na `user://save.cfg` (smlouva docs/TDD.md §3.16). Když není "
    "co uložit, vrať `false` a ohláš to přes `push_error` — TICHÝ ÚSPĚCH JE ZAKÁZANÝ (dřívější "
    "verze uložila 35 bajtů a vrátila `true`). Ukládej pozici hráče, atributy, dovednosti, "
    "zlato a inventář. Soubor `scripts/game.gd` v téhle granuli NEMĚŇ (patří granuli "
    "`shell.nocoins`). Pozor na parsování: `:=` jen u známého typu; `Vector2.ZERO` typ nemá → "
    "`var v: Vector2 = Vector2.ZERO`; typy komponent (`Player`, `Level`) v anotaci NEEXISTUJÍ "
    "→ piš `Node`. Testy: ověř, že `save()` bez komponent vrátí `false`, a že `load()` vrátí "
    "pozici. " + SPOLECNE
)


def main():
    with io.open(PLAN, encoding="utf-8") as f:
        d = json.load(f)

    nove = []
    for x in d["grains"]:
        if x["id"] == "world.bodies":
            x["done"] = True
            x["done_note"] = DONE_NOTE_BODIES
            nove.append(x)
        elif x["id"] == "shell.coins":
            nove.append({
                "id": "shell.nocoins",
                "title": "Kostra: pryč s mincemi a skóre (M0 — monolit se zbavuje slepé uličky)",
                "done": None, "kind": "code",
                "owns": ["scripts/game.gd"], "depends_on": ["engine.shell"],
                "acceptance": ["tests", "wiring", "smoke"],
                "size_lines": 60, "model": "strong", "milestone": "M0",
                "prompt": PROMPT_NOCOINS,
            })
            nove.append({
                "id": "shell.save",
                "title": "Ukládání z monolitu do komponenty Save (M0 — jedna cesta k souboru)",
                "done": None, "kind": "code",
                "owns": ["scripts/save.gd"], "depends_on": ["engine.shell"],
                "acceptance": ["tests", "wiring", "smoke"],
                "size_lines": 60, "model": "strong", "milestone": "M0",
                "prompt": PROMPT_SAVE,
            })
        else:
            nove.append(x)

    for x in nove:
        if x["id"] == "sim.wire":
            x["depends_on"] = ["engine.shell", "shell.nocoins", "shell.save"]

    d["grains"] = nove
    d["_popis"].append(
        "ZMĚNA 15. 10. 2026 (večer): world.bodies HOTOVÁ (patch z orchestry #374, integrováno ručně — "
        "krok PR nemá funkční FORGE_PAT). `shell.coins` ROZDELENA na `shell.nocoins` (game.gd) a "
        "`shell.save` (save.gd), protože dva vlastněné soubory v jednom zadání vyrobily request "
        "40 537 t proti limitu 8 000 a model zadání neviděl."
    )

    with io.open(PLAN, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("granulí po změně:", len(d["grains"]))
    for x in d["grains"]:
        print("  %-22s done=%-6s owns=%s" % (x["id"], str(x.get("done")), x.get("owns")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
