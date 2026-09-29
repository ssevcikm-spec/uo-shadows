# Isometric Forge

> **Záměr:** Nova hra podle principu Ultima Online, ale v rozsahu, ktery zvladne maly tym: izometricky fantasy sandbox pro jednoho hrace. Vse v hernim svete je interaktivni a ma dusledek. Skilly se zlepsuji jejich pouzivanim - boj, kovarstvi, alchymie, leceni, tatazstvi. Vyrobni skilly vyrabeji predmety s opravdovym uzitkem a hodnotou: zbran zvysuje poskozeni, zbroj snizuje zraneni, lektvar leci, jidlo doplnuje silu. Predmety maji trvanlivost a daji se opravovat. Suroviny se tezi z prostredi (ruda, drevo, byliny) a daji se mezi sebou smenovat. Izometricky pohled, dlazdicova mapa, fantasy svet, NPC s jednoduchou smysluplnou reakci, denni doba.

> **Vzhled:** varianta `dark`

**Žánr:** Fantasy sandbox RPG  
**Pilíř:** Interaktivní svět s dopadem každého rozhodnutí a progresivními dovednostmi

## Vize

Hráč prochází izometrickým fantasy světem, kde každý předmět, NPC a prostředí ovlivňuje svět. Kromě boje se věnuje sběru surovin, výrobě větších předmětů a výcviku dovedností. NPC mají jednoduché reakce na hráčovy činy, den a noc ovlivňují prostředí a NPC chování, a každý předmět má trvanlivost a užitečnost.

## Mechaniky

- Progresivní dovednosti (boj, kovarství, alchymie, léčení, těžba)
- Sběr surovin a jejich směnění do užitečných předmětů
- Denní cyklus ovlivňující NPC chování a prostředí
- Předměty s trvanlivostí a opravou
- NPC s reakcemi na hráčovy činy

## Jak to má vypadat

- **Grafika:** izometrická 2.5D jako Ultima Online – dlaždicový svět viděný shora,
  detailní 2D sprity s měkkým stínováním a živými postavičkami, ne retro 16bitové
  pixely a ne 3D engine. Dlaždice i postavy se kreslí v projekci 2:1, postavy mají
  stín a plynulou animaci chůze; cíl je dojem „reálný svět viděný shora".
- **Zvuk:** ambientní fantasy hudba s jemnými zvuky přírody, poškození předmětů,
  alchymie a NPC reakcemi

## Rozsah

Implementujeme základní sandboxovou logiku, NPC reakce, denní cyklus, dovednosti a předměty. Vynecháme multiplayer, komplexní questy a fyziku

## Plán prací

| # | Úkol | id |
|---|---|---|
| 1 | Implementace dovedností | `skill-system` |
| 2 | Základní křížek kovářství | `crafting-ui` |
| 3 | Denní cyklus | `day-night-cycle` |
| 4 | Sběr surovin | `resource-gathering` |
| 5 | Základní NPC reakce | `npc-interaction` |
| 6 | Trvanlivost předmětů | `item-durability` |

---

*Tenhle dokument vygeneroval plánovač (`forge plan`) a je zadáním pro orchestr: jednotlivé úkoly jsou v `.forge/roadmap.json`. Slabší modely je plní po jednom; dokument je tu proto, aby se neztratila vize.*
