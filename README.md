
# Prosjektnavn: Database‐analyse av store datasett

Dette repoet inneholder kun kildekoden (skriptene) for prosjektet. Selve datasettene (store filer) er IKKE inkludert av plasshensyn. Følg stegene under for å laste ned og bruke data:

1. **Last ned datasettene fra Google Drive** (eller annet sted):
   - Gå til https://drive.google.com/file/d/1lPZ6aDk1rAKSGpaZiHQLz7O9Gwe84e9h/view?usp=sharing   
   - Last ned filene og pakk dem ut i mappen `dataset/` i prosjektroten. Dermed vil strukturen din se slik ut:
     ```
     ProsjektRoot/
     ├── dataset/
     │   ├── 000/
     │   ├── 001/
     │   ├── 002/
     │   └── … (flere mapper)
     ├── db_utils.py
     ├── DbConnector.py
     ├── main.py
     ├── part2.py
     ├── requirements.txt
     └── README.md
     ```

2. **Installer avhengigheter**:
   ```bash
   pip install -r requirements.txt
# Prosjektnavn: Database-analyse av store datasett

Dette repoet inneholder kun koden som brukes til å analysere og behandle data. Selve datasettene (store filer) ligger i en delt Google Drive-mappe. Følg instruksjonene under for å få alt på plass.

## Prosjektstruktur

```
ProsjektRoot/
├── dataset/              # Mappen der dataene skal ligge (IGNORERT av Git)
├── db_utils.py           # Hjelpefunksjoner for databaseoperasjoner
├── DbConnector.py        # Kobler til databasen og henter data
├── main.py               # Hovedskript som kjører hele analysen
├── part2.py              # Ekstra moduler eller scripts for spesifikke deler
├── requirements.txt      # Liste over Python-avhengigheter
├── download_data.py      # Skript for å laste ned data fra Google Drive (valgfritt)
├── .gitignore            # Ignorerer dataset-mappen og andre midlertidige filer
└── read.me               # Denne filen
```

## Kom i gang steg for steg

1. Klon repoet
   Åpne Terminal og kjør:
   ```
   git clone https://github.com/DITT_BRUKERNAVN/ProsjektRepo.git
   cd ProsjektRepo
   ```
   Bytt ut `DITT_BRUKERNAVN` med ditt GitHub-brukernavn.

2. Installer avhengigheter
   Sørg for at du har Python 3.8 eller nyere installert. Kjør:
   ```
   pip install -r requirements.txt
   ```

3. Last ned datasettene
   Datasettene er for store til å ligge i dette repoet. De ligger offentlig tilgjengelig på Google Drive:
   - Åpne nettleseren og gå til denne lenken:
     ```
     https://drive.google.com/drive/folders/DIN_GOOGLE_DRIVE_LINK
     ```
     (Erstatt `DIN_GOOGLE_DRIVE_LINK` med den faktiske delte lenken.)
   - Last ned hele mappen som en ZIP-fil, pakk ut ZIP-filen, og flytt den utpakkede mappen til prosjektroten med navnet `dataset`. Strukturen skal se slik ut:
     ```
     ProsjektRoot/
     ├── dataset/
     │   ├── 000/
     │   ├── 001/
     │   ├── 002/
     │   └── …
     └── (resten av prosjektfiler)
     ```

4. Kjør nedlastingsskriptet (valgfritt)
   Dersom du har laget `download_data.py`, kan du kjøre:
   ```
   python download_data.py
   ```
   Skriptet laster da ned en ZIP-fil fra Google Drive og pakker ut dataene til `dataset/`.

5. Kjør analysen
   Når du har `dataset/`-mappen på plass, kan du kjøre koden:
   ```
   python main.py
   ```
   eller for del 2:
   ```
   python part2.py
   ```
   Skriptene vil lese rådata fra `dataset/`, bearbeide dem og skrive resultater til skjerm eller til utdatafiler.

## Beskrivelse av skriptene

- `db_utils.py`
  Inneholder funksjoner for å forenkle databaseoperasjoner som opprettelse av tabeller, innsatte data og spørringer.

- `DbConnector.py`
  Håndterer tilkobling til database (for eksempel SQLite). Leser rådata fra `dataset/` og fyller databasen.

- `main.py`
  Hovedskriptet:
  1. Kaller `DbConnector` for å fylle databasen med rådata.
  2. Kjører analyser som aggregering, filtrering og rapportgenerering.
  3. Skriver ut resultater eller lagrer dem til fil.

- `part2.py`
  Ekstra moduler for spesifikke databehandlingsoppgaver, visualisering eller maskinlæring som del 2-oppgaven krever.

- `download_data.py`
  Skript som laster ned en ZIP-fil fra Google Drive, pakker ut data til `dataset/` og sletter den midlertidige ZIP-filen. Husk å oppdatere nedlastings-URL i skriptet.

## Oppretting av Google Drive-mappen

1. Opprett en mappe i Google Drive (for eksempel “MittDataset”).
2. Last opp alle underkataloger (000, 001, 002, …).
3. Høyreklikk på mappen og velg “Del” (Share). Velg “Hent delbar lenke” (Get link).
4. Sørg for at “Alle med lenken kan se” (Anyone with the link can view). Kopier denne lenken.
5. Erstatt `DIN_GOOGLE_DRIVE_LINK` i denne README-filen med den faktiske lenken.

## Kontaktinformasjon

Hvis noe ikke fungerer eller du har spørsmål, kan du kontakte:
Annika Rangnes  
E-post: annika.rangnes@example.com

# Prosjektnavn: Database-analyse av store datasett

Dette repoet inneholder kun kildekoden (skriptene) for prosjektet. Datasettene er for store til å ligge i dette repoet, men finnes som en ZIP-fil på Google Drive. Følg instruksjonene under for å laste ned og bruke dataene.

## Prosjektstruktur

```
ProsjektRoot/
├── dataset/              # Mappen der dataene skal ligge (ignoreres av Git)
├── db_utils.py           # Hjelpefunksjoner for databaseoperasjoner
├── DbConnector.py        # Kobler til databasen og henter data
├── main.py               # Hovedskript som kjører hele analysen
├── part2.py              # Ekstra moduler eller scripts for spesifikke deler
├── requirements.txt      # Liste over Python-avhengigheter
├── download_data.py      # Skript for å laste ned og pakke ut data fra Google Drive (valgfritt)
├── .gitignore            # Ignorerer dataset-mappen og andre midlertidige filer
└── read.me               # Denne filen
```

## Kom i gang steg for steg

1. Klon repoet:
   ```
   git clone https://github.com/DITT_BRUKERNAVN/assignment2_2024-gruppe12.git
   cd assignment2_2024-gruppe12
   ```
   Bytt ut `DITT_BRUKERNAVN` med ditt GitHub-brukernavn.

2. Installer avhengigheter:
   Sørg for at du har Python 3.8 eller nyere installert. Kjør:
   ```
   pip install -r requirements.txt
   ```

3. Last ned og pakk ut datasettene:
   Datasettene ligger som en ZIP-fil på Google Drive. Åpne nettleseren og gå til denne lenken:
   https://drive.google.com/file/d/1lPZ6aDk1rAKSGpaZiHQLz7O9Gwe84e9h/view?usp=sharing  
   - Last ned ZIP-filen til din maskin.  
   - Pakk ut innholdet; en mappe `dataset/` skal nå være tilgjengelig.  
   - Flytt hele `dataset/`-mappen inn i prosjektroten slik at strukturen blir:
     ```
     ProsjektRoot/
     ├── dataset/
     │   ├── 000/
     │   ├── 001/
     │   ├── 002/
     │   └── … 
     └── (andre prosjektfiler)
     ```

4. Kjør nedlastingsskriptet (valgfritt):
   Hvis du foretrekker å laste ned og pakke ut automatisk, kan du bruke `download_data.py`:
   ```
   python download_data.py
   ```
   Skriptet henter ZIP-filen fra Google Drive, pakker ut dataene i `dataset/`, og sletter den midlertidige ZIP-filen.

5. Kjør analysen:
   Når `dataset/`-mappen er på plass, kan du kjøre koden:
   ```
   python main.py
   ```
   eller for del 2:
   ```
   python part2.py
   ```
   Skriptene leser rådata fra `dataset/`, behandler dem og skriver resultater til skjerm eller utdatafiler.

## Beskrivelse av skriptene

- **db_utils.py**  
  Inneholder funksjoner som forenkler databaseoperasjoner (opprettelse av tabeller, innsatte data, spørringer).

- **DbConnector.py**  
  Håndterer tilkobling til database (for eksempel SQLite). Leser rådata fra `dataset/` og fyller databasen.

- **main.py**  
  Hovedskriptet:  
  1. Kaller `DbConnector` for å fylle databasen med rådata.  
  2. Kjører analyser som aggregering, filtrering og rapportgenerering.  
  3. Skriver ut resultater eller lagrer dem til fil.

- **part2.py**  
  Inneholder ekstra databehandlingsoppgaver, visualisering eller maskinlæring for del 2-oppgaven.

- **download_data.py**  
  Skript som laster ned ZIP-filen fra Google Drive og pakker ut dataene til `dataset/`. Pass på at URL-en i skriptet er oppdatert til riktig Google Drive-lenke.

## Opprettelse av Google Drive-mappen

1. Datasettene er lastet opp som én ZIP-fil med mapper `000`, `001`, `002`, …  
2. Del filen på Google Drive slik at “Alle med lenken kan se”.  
3. Kopier delbar lenke og bruk den i punkt 3 over.  

## .gitignore

Sørg for at `.gitignore` inneholder minst:
```
/dataset/
/*.log
```
slik at dataset-mappen og eventuelle loggfiler ikke spores.
