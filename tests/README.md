# Tesztelés

## Mi van itt?

- `input/`: fájlok, amik bemenetül szolgálnak az emtsv-nek
- `gold/`: fájlok, amik az inputfájlok elvárt elemzéseit tartalmazzák.
- `test.py`: A fő tesztelő szkript. 5 esetet vizsgál:
    1. emtsv importálása lib-ként
    1. emtsv parancssori használata
    1. emtsv futtatása szerverként
    1. emtsv docker parancssori használata
    1. emtsv docker futtatása szerverként

  Mind az öt esetben lefut az összes `input/` beli fájlra az emtsv. A kimenet minden fájlnál össze lesz vetve a `gold/`-beli megfelelőjével.

- esetleg még egy-két segéd-szkript

## Megcélzott fejlesztési menet

1. Fejlesztgetünk (xtsv-t, modult, mindegy, a végén magában az emtsv repóban kell ezeket érvényesíteni).
1. Futtatjuk a `make test`-et. Ez egy venv-ben teszteli a python-os felhasználási módokat (lib, cli, api).
1. Futtatjuk a `make dbuildtest`-et. Ez egy *teszt* címkével ellátott docker image-et hoz létre (`emtsv:test`).
1. Futtatjuk a `make dtest`-et, ami a `emtsv:test` docker image-et fogja tesztelni.
1. Ha minden rendben, akkor a `make build` gyártaná le a pypi-ra feltölthető python csomagot és a `make dbuild` pedig a dockerhub-ra feltölthető docker image-et (`emtsv:latest` és `emtsv:<verzio>`). Ha valahol valamelyik teszt bukik, akkor GOTO 1.

## Tesztfájlelnevezési konvenciók

A `test.py` az összes input-gold párra lefut. Új fájlokra is, kódhoz nyúlni nem kell. A fájnevek három mezőkből épülnek fel:

1. alapnév, pl. `kutya`
1. futtatott modulok, alulvonással elválasztva, pl. `tok_morph_pos`
1. kiterjesztés, `txt`, vagy `tsv`

A mezőket pont (`.`) választja el egymástól. Az elemzetlen (txt) fájloknál nem kell két pont egymás után.

Példák:
- `kutya.txt`: elemzetlen plain text fájl
- `kutya.tok_morph_pos.tsv`: elemzett TSV fájl, ami a tokenizáló, morfológiai elemző és az egyértelműsítő kiemenetét tartalmazza.

## `input/` és `gold/` fájlok megfeleltetése

Alapszabály: egy `input/`-beli fájl minden, vele azonos nevű, nála több elemzést tartalmazó `gold`-beli fájlal egy-egy párt fog alkotni.

Példák:

1. *egy input -- egy gold*:
    - Az `input/`-ban egy `kutya.txt` van, a `gold/`-ban egy `kutya.tok_morph.tsv` --> Egy elemzés fog lesz, az `emtsv tok,morph` fog lefutni az input fájlon és a kimenet a golddal lesz összehaszonlítva. (Beszállás az elemzőlánc elején.)
    - Az `input/`-ban egy `kutya.tok.tsv` van, a `gold/`-ban egy `kutya.tok_morph.tsv` --> Egy elemzés fog lesz, az `emtsv morph` fog lefutni az input fájlon. (Beszállás az elemzőlánc közepén.)
1. *egy input -- több gold*:
    - Az `input/`-ban egy `kutya.txt` van, a `gold/`-ban egy `kutya.tok_morph.tsv` és egy `kutya.tok_morph_pos.tsv`--> Két elemzés lesz: az `emtsv tok,morph` és az `emtsv tok,morph,pos`, mindkettő ugyanazon az inputfájlon. 
    - Az `input/`-ban egy `kutya.tok.tsv` van, a `gold/`-ban egy `kutya.tok_morph.tsv` és egy `kutya.tok_morph_pos.tsv`--> Két elemzés lesz: az `emtsv morph` és az `emtsv morph,pos`, mindkettő ugyanazon a tokenizált inputfájlon. 
1. *több input -- egy gold*:
    - Az `input/`-ban egy`kutya.txt` és egy `kutya.tok_morph.tsv` van, a `gold/`-ban egy `kutya.tok_morph_pos.tsv` --> Két elemzés lesz: az `emtsv tok,morph,pos` fog lefutni a TXT-n és az `emtsv pos` fog lefutni a morfológiailag elemzett input fájlon. Mindkét elemzés eredménye ugyanazzal a gold fájllal lesz összehasonlítva.
1. *több input -- több gold*:
    - Az `input/`-ban egy`kutya.txt` és egy `kutya.tok_morph.tsv` van, a `gold/`-ban egy `kutya.tok_morph.tsv` és egy `kutya.tok_morph_pos.tsv` van --> Három elemzés lesz: a TXT-n le fog futni az `emtsv tok,morph` és az `emtsv tok,morph,pos`, a morfológiailag elemzett input fájlon csak az `emtsv pos` fog lefutni.

Rossz példák:

- Az `input/`-ban egy `kutya.tok_morph_pos` van, a `gold/`-ban egy `kutya.tok_morph_pos.tsv` --> Nem lesz egy elemzése sem, ha a gold-ban kevesebb vagy ugyan annyi modul kimenete található, mint az inputban.
- Az `input/`-ban egy `kutya.tok_morph_pos` van, a `gold/`-ban egy `kutya.tok_morph_ner.tsv` --> Nem lesz egy elemzése sem, ha a gold-ban nincs meg minden elemzés, ami az inputban megvan.
