# Frontend Cleanup Report

Usunięte elementy oraz uzasadnienie:

1. `src/pages/Home.jsx`
   - Powód: plik nie jest importowany nigdzie w projekcie; funkcjonalność (UploadAudio, TranscriptViewer, SummaryViewer) jest zduplikowana i obecna w `src/App.jsx`.
   - Ryzyko: bardzo niskie. Możliwe przywrócenie z backup brancha `cleanup/frontend-backup`.

2. `src/assets/react.svg`
   - Powód: plik SVG nie jest nigdzie importowany ani używany.
   - Ryzyko: bardzo niskie.

3. `react-router-dom` (dependency)
   - Powód: pakiet jest zadeklarowany w `package.json`, ale kod nie używa routera (brak importów `BrowserRouter`, `Routes`, `Link` itd.). Zmniejszamy rozmiar `node_modules` i poprawiamy klarowność zależności.
   - Ryzyko: umiarkowane — jeśli planujemy dodać routing wkrótce, pakiet będzie trzeba ponownie zainstalować.

Dodatkowe uwagi:
- W komponentach widoczne są klasy ikon Font Awesome (`fas fa-...`), natomiast nie było importu CDN ani biblioteki. Dodałem CDN do `index.html`, aby zachować wygląd bez instalacji dodatkowej paczki.

Backup:
- Pełna kopia stanu przed zmianami jest dostępna w brancha `cleanup/frontend-backup`.

---

Jeśli chcesz, mogę przywrócić którykolwiek z usuniętych plików z branch-a backupowego.
