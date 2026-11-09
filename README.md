# 📈 WallStreet Analyzer

**WallStreet Analyzer** to aplikacja do analizy rynku akcji, stworzona w języku **Python** z wykorzystaniem biblioteki **Streamlit**.

Projekt umożliwia analizowanie wyników wybranych spółek giełdowych, porównywanie ich zachowania na rynku oraz ocenę trendów za pomocą wskaźników analizy technicznej.

Aplikacja prezentuje dane w formie interaktywnych wykresów i czytelnych zestawień, ułatwiając obserwację zmian cen oraz aktywności rynkowej.

---

## 🚀 Funkcjonalności

### 1. Przegląd rynku (Market Overview)

- Analiza 10 wybranych spółek giełdowych.
- Porównanie zmian cen akcji.
- Wizualizacja znormalizowanych wyników spółek.
- Analiza zmienności stóp zwrotu.
- Porównanie średniego dziennego wolumenu obrotu.
- Wybór okresu analizy: **3 miesiące, 6 miesięcy lub 1 rok**.

### 2. Szczegółowa analiza spółki (Stock Details)

- Wybór spółki do indywidualnej analizy.
- Wykres cen zamknięcia.
- Średnie kroczące **SMA 20 i SMA 50**.
- Wskaźnik **RSI (Relative Strength Index)**.
- Wskaźnik **MACD (Moving Average Convergence Divergence)**.
- Analiza dziennych stóp zwrotu.
- Kluczowe wskaźniki efektywności (KPI):
  - Ostatnia cena zamknięcia.
  - Zmiana ceny w wybranym okresie.
  - Dzienna zmienność.
  - Średni dzienny wolumen obrotu.

### 3. Interaktywne wykresy

- Wizualizacja danych z wykorzystaniem **Plotly**.
- Możliwość zmiany analizowanego okresu.
- Czytelne wykresy w ciemnym motywie.

---

## 🛠️ Wykorzystane technologie

| Technologia | Zastosowanie |
|---|---|
| **Python** | Główny język programowania |
| **Pandas** | Przetwarzanie i analiza danych |
| **Streamlit** | Budowa interfejsu aplikacji |
| **Plotly** | Tworzenie interaktywnych wykresów |
| **NumPy** | Operacje numeryczne |
| **Git i GitHub** | Kontrola wersji i przechowywanie kodu |

---

## 💻 Instalacja i uruchomienie

### 1. Sklonowanie repozytorium

```bash
git clone https://github.com/janlickindorf7-pixel/wallstreet-analyzer.git
```

### 2. Przejście do folderu projektu

```bash
cd wallstreet-analyzer
```

### 3. Instalacja wymaganych bibliotek

```bash
pip install streamlit pandas plotly numpy
```

### 4. Uruchomienie aplikacji

```bash
streamlit run app.py
```

Aplikacja zostanie uruchomiona lokalnie i będzie dostępna w przeglądarce pod adresem:

**http://localhost:8501**

> **Uwaga:** Powyższe instrukcje zakładają, że Python i pip są już zainstalowane.