# CSG-Fernwartung: eigenes Programm bauen

Dieses Paket baut das RustDesk-Programm (Version 1.5.0) für Windows mit

- Name **CSG-Computer Fernwartung** (Programm/Dienst `CSGFernwartung`),
- CSG-Logo und -Symbol,
- eurem Server **csg-hilfe.de** und dessen Schlüssel fest eingebaut.

Gebaut wird kostenlos bei GitHub (Windows-Rechner von GitHub, ca. 60–90 Minuten).

## Einmalig einrichten

1. Bei <https://github.com> ein Konto anlegen (falls noch keins da ist).
2. Oben rechts **+ → New repository**: Name z. B. `csg-fernwartung`, **Public** (dann sind die Bau-Minuten kostenlos),
   „Add a README file“ ankreuzen → **Create repository**.
3. Im neuen Repository **Add file → Upload files** und den **Inhalt dieses Pakets** hineinziehen
   (den Ordner `.github` und den Ordner `csg` sowie diese Anleitung) → **Commit changes**.
   - Wichtig: Der Ordner `.github` beginnt mit einem Punkt und ist unter Windows/macOS evtl. ausgeblendet.
     Am einfachsten das ZIP entpacken und die Ordner aus dem Explorer in das Browserfenster ziehen.
   - Danach muss es im Repository die Datei `.github/workflows/csg-build.yml` geben.

## Programm bauen

1. Im Repository auf **Actions** klicken (beim ersten Mal „I understand my workflows, go ahead and enable them“ bestätigen).
2. Links **CSG Fernwartung bauen (Windows)** wählen → rechts **Run workflow** → **Run workflow**.
3. Warten, bis alle drei Schritte grün sind (ca. 60–90 Minuten).
4. Die fertige Datei `CSGFernwartung-1.5.0-x86_64.exe` liegt dann
   - unter **Releases** (rechte Seite der Startseite des Repositorys) als `csg-1.5.0`, oder
   - im Lauf unter **Artifacts** als `CSGFernwartung-windows-x64` (ZIP, darin die .exe).

## In der Serviceplattform hochladen

Verwaltung → **Fernwartung** → „Eigenes CSG-Programm bauen“ → Datei wählen, Programmname `CSGFernwartung`, Version z. B. `1.5.0-csg1` → **Hochladen**.

Ab dann bekommen Kunden (QuickSupport, Host-Installation) und Techniker („Programm für meinen PC“) das CSG-Programm.
Auf den Techniker-PCs das neue Programm einmal installieren; der Link `csgfernwartung://` öffnet es aus der Plattform.

## Hinweise

- Lizenz: RustDesk steht unter der AGPL-3.0. Da dieses Repository öffentlich ist, sind eure Änderungen (nur Name, Logo, Server)
  damit veröffentlicht – das erfüllt die Lizenz.
- Neue RustDesk-Version: in `.github/workflows/csg-build.yml` oben `RUSTDESK_REF` und `VERSION` ändern und neu bauen.
  Wenn RustDesk den Bauablauf stark ändert, bitte bei der Serviceplattform ein neues Bau-Paket laden.
- Der Schlüssel in `csg/settings.json` ist der **öffentliche** Schlüssel des Servers – er darf öffentlich sein.
- Das Programm ist nicht signiert; Windows warnt beim ersten Download (wie bisher). Mit einem Code-Signing-Zertifikat kann es später signiert werden.
