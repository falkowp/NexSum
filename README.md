# NexSum - Abstractive Text Summarization Model

A from-scratch implementation of a Seq2Seq model with attention for abstractive text summarization.

## Project Structure

## Szybkie uruchomienie (Windows) ✅

Poniżej znajdują się kroki, które pozwolą Ci uruchomić backend i frontend lokalnie.

### 1. Przygotowanie Pythona 📦

- Utwórz i aktywuj wirtualne środowisko:

  ```powershell
  python -m venv .venv
  .venv\Scripts\activate
  ```

- Zainstaluj zależności Pythona:

  ```powershell
  pip install -r requirements.txt
  ```

### 2. Wymagania systemowe dla audio 🔊

- Zainstaluj `ffmpeg` i upewnij się, że jest w PATH. Najprościej przez Chocolatey:

  ```powershell
  choco install ffmpeg
  ```

  Brak `ffmpeg` powoduje błędy przy przetwarzaniu audio (pydub/whisper).

### 3. Modele i dodatkowe zasoby 🧠

- Pobierz model spaCy używany w projekcie:

  ```powershell
  python -m spacy download en_core_web_sm
  ```

- Przy pierwszym uruchomieniu `openai-whisper` pobierze model (np. "base") — może to zająć kilka minut i wymagać miejsca na dysku.

### 4. Uruchomienie backendu (Flask) 🔧

- Z katalogu projektu:

  ```powershell
  python backend/app.py
  ```

- Backend nasłuchuje na `127.0.0.1:5000`. CORS jest skonfigurowany dla frontendu (`5173` i `3000`).

### 5. Uruchomienie frontendu (Vite + React) ⚛️

- Przejdź do katalogu `frontend` i wykonaj:

  ```powershell
  cd frontend
  npm install
  npm run dev
  ```

- Alternatywnie, aby uruchomić backend i frontend równocześnie (z katalogu `frontend`):

  ```powershell
  npm run dev-all
  ```

### 6. Testy 🧪

- Uruchom testy jednostkowe:

  ```powershell
  pytest
  ```

---

### Najczęstsze problemy (i jak je rozwiązać) ⚠️

- Brak `ffmpeg` → błędy przy konwersji/odczycie audio.
- Brak modelu spaCy (`en_core_web_sm`) → błąd `OSError` przy ładowaniu modelu.
- Pierwsze uruchomienie Whisper pobiera model — oczekuj dłuższego czasu i większego zużycia pasma.

---

Jeśli chcesz, mogę dodać skrypt `.bat` lub dopisać `README` po angielsku — daj znać, którą opcję preferujesz.
