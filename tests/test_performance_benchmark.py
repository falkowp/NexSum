"""
Test wydajności i jakości systemu NexSum.

Generuje dane potrzebne do dokumentacji:
- Test "Przed i Po" (surowy vs. oczyszczony tekst)
- Pomiary czasu przetwarzania
- Statystyki zbioru badawczego
"""

import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.transcription.transcriber import process_audio_pipeline


class PerformanceBenchmark:
    """Narzędzie do testowania wydajności i jakości NexSum."""
    
    def __init__(self, output_dir: str = "test_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = []
        
    def test_single_file(self, audio_path: str, label: str = None) -> Dict[str, Any]:
        """
        Testuje jeden plik audio i zwraca szczegółowe wyniki.
        
        Args:
            audio_path: Ścieżka do pliku audio
            label: Opcjonalna etykieta (np. "Krótki", "Średni", "Długi")
        
        Returns:
            Dict z wynikami testu
        """
        audio_file = Path(audio_path)
        
        if not audio_file.exists():
            raise FileNotFoundError(f"Plik nie istnieje: {audio_path}")
        
        print(f"\n{'='*60}")
        print(f"Testowanie: {audio_file.name}")
        if label:
            print(f"Kategoria: {label}")
        print(f"{'='*60}")
        
        # Odczytaj plik
        with open(audio_file, "rb") as f:
            audio_bytes = f.read()
        
        file_size_mb = len(audio_bytes) / (1024 * 1024)
        print(f"Rozmiar pliku: {file_size_mb:.2f} MB")
        
        # Oszacuj długość audio (jeśli możliwe)
        try:
            from pydub import AudioSegment
            import io
            audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
            duration_sec = len(audio) / 1000.0
            duration_min = duration_sec / 60.0
            print(f"Długość nagrania: {duration_min:.2f} minut ({duration_sec:.1f} sekund)")
        except Exception as e:
            duration_sec = None
            duration_min = None
            print(f"Nie udało się określić długości: {e}")
        
        # POMIAR CZASU TRANSKRYPCJI
        print("\nRozpoczynanie transkrypcji...")
        start_time = time.time()
        
        try:
            raw_text, polished_text = process_audio_pipeline(audio_bytes)
            processing_time = time.time() - start_time
            
            print(f"✓ Transkrypcja zakończona w {processing_time:.2f} sekund")
            
            # Statystyki tekstu
            raw_words = len(raw_text.split())
            polished_words = len(polished_text.split())
            raw_chars = len(raw_text)
            polished_chars = len(polished_text)
            
            print(f"\nStatystyki tekstu:")
            print(f"  Surowy tekst: {raw_words} słów, {raw_chars} znaków")
            print(f"  Oczyszczony tekst: {polished_words} słów, {polished_chars} znaków")
            
            # Oblicz wydajność
            if duration_sec:
                realtime_factor = duration_sec / processing_time
                print(f"\nWydajność: {realtime_factor:.2f}x czasu rzeczywistego")
                print(f"  (Na 1 min audio = {60/realtime_factor:.1f}s przetwarzania)")
            
            result = {
                "filename": audio_file.name,
                "label": label,
                "timestamp": datetime.now().isoformat(),
                "file_size_mb": round(file_size_mb, 2),
                "duration_seconds": round(duration_sec, 1) if duration_sec else None,
                "duration_minutes": round(duration_min, 2) if duration_min else None,
                "processing_time_seconds": round(processing_time, 2),
                "realtime_factor": round(realtime_factor, 2) if duration_sec else None,
                "raw_text": raw_text,
                "polished_text": polished_text,
                "stats": {
                    "raw_words": raw_words,
                    "raw_chars": raw_chars,
                    "polished_words": polished_words,
                    "polished_chars": polished_chars,
                    "chars_removed": raw_chars - polished_chars,
                    "chars_removed_percent": round((raw_chars - polished_chars) / raw_chars * 100, 2) if raw_chars > 0 else 0
                },
                "success": True
            }
            
            self.results.append(result)
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"✗ Błąd podczas przetwarzania: {e}")
            
            result = {
                "filename": audio_file.name,
                "label": label,
                "timestamp": datetime.now().isoformat(),
                "file_size_mb": round(file_size_mb, 2),
                "processing_time_seconds": round(processing_time, 2),
                "error": str(e),
                "success": False
            }
            
            self.results.append(result)
            return result
    
    def save_before_after_comparison(self, result: Dict[str, Any]) -> None:
        """Zapisuje porównanie 'Przed i Po' do pliku tekstowego."""
        if not result.get("success"):
            print("Pomijam zapis - test nieudany")
            return
        
        filename = result["filename"].rsplit(".", 1)[0]
        output_file = self.output_dir / f"before_after_{filename}.txt"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("TEST 'PRZED I PO' - SKUTECZNOŚĆ CZYSZCZENIA TEKSTU\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Plik: {result['filename']}\n")
            if result.get('label'):
                f.write(f"Kategoria: {result['label']}\n")
            f.write(f"Data testu: {result['timestamp']}\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("1. SUROWY TEKST Z WHISPERA (przed czyszczeniem)\n")
            f.write("-" * 80 + "\n\n")
            f.write(result["raw_text"])
            f.write("\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("2. OCZYSZCZONY TEKST Z NEXSUM (po czyszczeniu)\n")
            f.write("-" * 80 + "\n\n")
            f.write(result["polished_text"])
            f.write("\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("STATYSTYKI CZYSZCZENIA\n")
            f.write("-" * 80 + "\n\n")
            stats = result["stats"]
            f.write(f"Surowy tekst:      {stats['raw_words']} słów, {stats['raw_chars']} znaków\n")
            f.write(f"Oczyszczony tekst: {stats['polished_words']} słów, {stats['polished_chars']} znaków\n")
            f.write(f"Usunięto:          {stats['chars_removed']} znaków ({stats['chars_removed_percent']}%)\n")
        
        print(f"\n✓ Zapisano porównanie 'Przed i Po': {output_file}")
    
    def save_summary_report(self) -> None:
        """Generuje zbiorczy raport ze wszystkich testów."""
        if not self.results:
            print("Brak wyników do zapisania")
            return
        
        report_file = self.output_dir / f"summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        successful_results = [r for r in self.results if r.get("success")]
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("RAPORT WYDAJNOŚCI NEXSUM\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Data testu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Liczba testowanych plików: {len(self.results)}\n")
            f.write(f"Testy zakończone sukcesem: {len(successful_results)}\n\n")
            
            # ZADANIE 2: Test wydajności
            f.write("=" * 80 + "\n")
            f.write("ZADANIE 2: TEST WYDAJNOŚCI (POMIARY CZASU)\n")
            f.write("=" * 80 + "\n\n")
            
            for result in successful_results:
                f.write(f"Plik: {result['filename']}")
                if result.get('label'):
                    f.write(f" ({result['label']})")
                f.write("\n")
                
                if result.get('duration_minutes'):
                    f.write(f"  • Długość nagrania: {result['duration_minutes']:.2f} minut\n")
                f.write(f"  • Czas przetwarzania: {result['processing_time_seconds']:.2f} sekund\n")
                
                if result.get('realtime_factor'):
                    f.write(f"  • Wydajność: {result['realtime_factor']:.2f}x czasu rzeczywistego\n")
                f.write("\n")
            
            # ZADANIE 3: Opis zbioru badawczego
            f.write("=" * 80 + "\n")
            f.write("ZADANIE 3: OPIS ZBIORU BADAWCZEGO\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"1. Liczba przetestowanych plików: {len(successful_results)}\n\n")
            
            total_duration = sum(r.get('duration_minutes', 0) for r in successful_results if r.get('duration_minutes'))
            f.write(f"2. Łączna długość nagrań: {total_duration:.2f} minut ({total_duration/60:.2f} godzin)\n\n")
            
            formats = set(result['filename'].rsplit('.', 1)[-1].lower() for result in self.results)
            f.write(f"3. Testowane formaty: {', '.join(sorted(formats))}\n\n")
            
            f.write("4. Informacje dodatkowe:\n")
            f.write("   (należy uzupełnić ręcznie - czy to były nagrania jednego głosu,\n")
            f.write("    czy różnych osób, męskie/żeńskie, itp.)\n\n")
            
            # Średnie wartości
            if successful_results:
                avg_processing = sum(r['processing_time_seconds'] for r in successful_results) / len(successful_results)
                f.write("=" * 80 + "\n")
                f.write("ŚREDNIE WARTOŚCI\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Średni czas przetwarzania: {avg_processing:.2f} sekund\n")
                
                if any(r.get('realtime_factor') for r in successful_results):
                    factors = [r['realtime_factor'] for r in successful_results if r.get('realtime_factor')]
                    avg_factor = sum(factors) / len(factors)
                    f.write(f"Średnia wydajność: {avg_factor:.2f}x czasu rzeczywistego\n")
        
        print(f"\n✓ Zapisano zbiorczy raport: {report_file}")
        
        # Zapisz też JSON dla łatwiejszej analizy
        json_file = report_file.with_suffix('.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"✓ Zapisano dane w formacie JSON: {json_file}")


def main():
    """
    Testuje wszystkie pliki audio w katalogu test_data.
    """
    print("=" * 80)
    print("NARZĘDZIE DO TESTOWANIA WYDAJNOŚCI NEXSUM")
    print("=" * 80)
    print("\nTen skrypt przetestuje wszystkie pliki audio w katalogu test_data.\n")
    
    benchmark = PerformanceBenchmark(output_dir="test_results")
    
    # Automatyczne wykrywanie wszystkich plików MP3 w test_data
    test_data_dir = Path(__file__).parent.parent / "test_data"
    mp3_files = sorted(test_data_dir.glob("*.mp3"))
    
    print(f"Znaleziono {len(mp3_files)} plików MP3 do przetestowania.\n")
    
    if not mp3_files:
        print("⚠ Brak plików MP3 w katalogu test_data!")
        return
    
    # Test 1: "Przed i Po" - użyj pierwszego pliku "English in a Minute"
    before_after_file = None
    for f in mp3_files:
        if "English in a Minute" in f.name:
            before_after_file = f
            break
    
    if before_after_file:
        print("=" * 80)
        print("ZADANIE 1: TEST 'PRZED I PO'")
        print("=" * 80)
        
        try:
            result = benchmark.test_single_file(
                str(before_after_file),
                label="Test Przed/Po (Educational)"
            )
            benchmark.save_before_after_comparison(result)
        except Exception as e:
            print(f"\n⚠ Błąd podczas testu 'Przed i Po': {e}")
    
    # Test 2 i 3: Wydajność - testuj wszystkie pliki
    print("\n" + "=" * 80)
    print("ZADANIE 2 i 3: TEST WYDAJNOŚCI WSZYSTKICH PLIKÓW")
    print("=" * 80)
    
    for i, mp3_file in enumerate(mp3_files, 1):
        print(f"\n[{i}/{len(mp3_files)}]")
        try:
            benchmark.test_single_file(str(mp3_file), label=None)
        except Exception as e:
            print(f"\n⚠ Błąd podczas przetwarzania {mp3_file.name}: {e}")
    
    # Generuj zbiorczy raport
    benchmark.save_summary_report()
    
    print("\n" + "=" * 80)
    print("TESTY ZAKOŃCZONE!")
    print("=" * 80)
    print(f"\nWyniki zapisane w katalogu: {benchmark.output_dir.absolute()}")
    print("\nNastępne kroki:")
    print("1. Przeczytaj plik 'before_after_*.txt' dla Zadania 1")
    print("2. Sprawdź 'summary_report_*.txt' dla Zadań 2 i 3")
    print("3. Użyj pliku JSON do stworzenia wykresów w Excelu/Python")


if __name__ == "__main__":
    main()
