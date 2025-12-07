# Karta projektu

Karta projektu to pierwszy oficjalny dokument projektowy, który opisuje jego podstawowe założenia: dlaczego projekt powstaje, co ma osiągnąć, jakie są ograniczenia, kto za co odpowiada i jak będzie mierzony sukces.

## Struktura karty projektu

| Sekcja | Co zawiera | Przykładowe treści |
|--------|------------|-------------------|
| 1. Tytuł projektu | Nazwa projektu i akronim | "AW-PG – Aplikacja Webowa do Obsługi Projektu Grupowego" |
| 2. Cel projektu | Co projekt ma osiągnąć i dlaczego | "Umożliwienie zarządzania projektami grupowymi online dla studentów i prowadzących" |
| 3. Uzasadnienie edukacyjne | Dlaczego projekt jest potrzebny | "Obecnie proces jest manualny. System zautomatyzuje przydział tematów i formowanie grup." |
| 4. Zakres projektu | Co wchodzi w zakres i co jest poza zakresem | "W zakresie: tematy, preferencje, grupy; poza zakresem: integracja z USOS w czasie rzeczywistym" |
| 5. Główne wymagania | Wstępna lista funkcjonalności | "Student może wybrać preferencje, utworzyć grupę; Prowadzący może dodawać tematy" |
| 6. Zespół projektowy i role | Lista członków i ich funkcji | "Product Owner – M. Cybulski, Scrum Master – A. Harasimiuk, Frontend – M. Rutkowski, Backend – A. Szewczyk" |
| 7. Zasoby i narzędzia | Technologie, środowisko, repozytorium | "GitHub, Django, Vue.js, SQLite/PostgreSQL" |
| 8. Harmonogram wstępny | Etapy realizacji projektu | "Analiza wymagań (1-2 tyg.), Implementacja (3-20 tyg.), Testy (21-22 tyg.), Prezentacja (23 tydz.)" |
| 9. Ryzyka i działania zapobiegawcze | Potencjalne zagrożenia i sposoby ich ograniczenia | "Brak doświadczenia w Vue.js → tutoriale i przykłady" |
| 10. Oczekiwane rezultaty | Co powstanie na koniec | "Działająca aplikacja webowa + pełna dokumentacja" |
| 11. Kryteria sukcesu | Jak zostanie oceniony sukces projektu | "Aplikacja działa, dokumentacja kompletna, kod na GitHubie" |
| 12. Akceptacja projektu | Podpisy | "Zatwierdza: prowadzący, kierownik projektu" |

---

## KARTA PROJEKTU - Aplikacja Webowa do Obsługi Projektu Grupowego

### 1. Informacje ogólne

**Tytuł projektu:**  
Aplikacja Webowa do Obsługi Przedmiotu "Projekt Grupowy"

**Akronim projektu:**  
AW-PG

**Data utworzenia:** 7.10.2021
**Wersja dokumentu:** 1.0  

**Zespół projektowy:**

| Imię i nazwisko | Rola w projekcie | Zakres odpowiedzialności |
|-----------------|------------------|--------------------------|
| Michał Cybulski | Product Owner / Kierownik projektu | Definiowanie wymagań, priorytetyzacja, komunikacja z interesariuszami, planowanie |
| Aleksandra Harasimiuk | Scrum Master | Organizacja spotkań, notatki z daily, usuwanie przeszkód, monitorowanie postępów |
| Mateusz Rutkowski | Programista Frontend | Implementacja interfejsu użytkownika (Vue.js), integracja z API, UI/UX |
| Adam Szewczyk | Programista Backend | Implementacja logiki biznesowej (Django), baza danych, REST API |

**Prowadzący:** dr inż. Przemysław Korpas  
**Jednostka dydaktyczna:** Politechnika Warszawska, Wydział Elektroniki i Technik Informacyjnych

---

### 2. Cel projektu

Celem projektu jest opracowanie i wdrożenie webowej aplikacji do kompleksowej obsługi przedmiotu "Projekt Grupowy", umożliwiającej:

- **Studentom:** przeglądanie dostępnych tematów, składanie preferencji (ranking 1-3), formowanie grup projektowych, śledzenie przydzielonych tematów
- **Prowadzącym:** zarządzanie pulą tematów, przeglądanie preferencji studentów, przydział tematów do grup, monitorowanie postępów
- **Administratorom:** import użytkowników z systemu USOS, zarządzanie kontami, konfiguracja systemu

Projekt ma zautomatyzować i usprawnić proces zarządzania projektami grupowymi, zastępując dotychczasowe rozwiązania manualne.

---

### 3. Uzasadnienie projektu

Obecnie proces zarządzania projektami grupowymi na przedmiotach projektowych opiera się na:

- Ręcznym przydziale tematów przez prowadzących (często przez e-mail)
- Braku systemu preferencji studentów
- Manualnym formowaniu grup (komunikatory, spotkania)
- Braku scentralizowanej platformy do komunikacji i dokumentacji

Projekt rozwiązuje te problemy poprzez:

- **Automatyzację** procesu przydziału tematów na podstawie preferencji
- **Cyfryzację** całego workflow zarządzania projektami
- **Centralizację** komunikacji i dokumentacji
- **Zwiększenie transparentności** procesu dla wszystkich uczestników

---

### 4. Zakres projektu

#### W zakresie projektu:
- Analiza wymagań i projektowanie systemu
- Implementacja backendu w Django REST Framework (Python 3.9+)
- Implementacja frontendu w Vue.js 2 z Vuetify
- System autoryzacji z 3 rolami: Student, Prowadzący (Lecturer), Administrator
- Moduł zarządzania tematami projektowymi (CRUD)
- System preferencji tematycznych studentów (ranking 1-3)
- System formowania i zarządzania grupami projektowymi
- Podstawowy system komunikacji (widoki przydzielonych tematów/grup)
- Import użytkowników z pliku CSV (z systemu USOS)
- Dokumentacja techniczna i użytkownika
- Testy funkcjonalne i prezentacja

#### Poza zakresem projektu:
- Integracja z systemem USOS w czasie rzeczywistym (API)
- Zaawansowany system oceniania z rubrykami
- Mobilna aplikacja natywna
- System wideokonferencji i czatu w czasie rzeczywistym
- Zaawansowane raporty analityczne i statystyki
- System powiadomień e-mail/SMS

---

### 5. Wymagania

| Typ | Opis |
|-----|------|
| **Funkcjonalne** | Logowanie z rolami, zarządzanie tematami (CRUD), składanie preferencji (1-3 priorytet), formowanie/dołączanie do grup, przydział tematów przez prowadzących, import użytkowników z CSV |
| **Niefunkcjonalne** | Wydajność: czas odpowiedzi API < 2s, czas ładowania strony < 3s; Dostępność: 99% w godzinach pracy; Responsywność: mobile/tablet/desktop |
| **Interfejsowe** | Nowoczesny interfejs webowy (Vue.js + Vuetify Material Design), polska lokalizacja, intuicyjna nawigacja |
| **Bezpieczeństwo** | Autoryzacja JWT, kontrola dostępu oparta na rolach, hashowanie haseł (bcrypt), ochrona przed CSRF |

---

### 6. Zespół projektowy i role

| Rola | Osoba odpowiedzialna | Główne zadania |
|------|----------------------|----------------|
| **Product Owner** | Michał Cybulski | Definiowanie wymagań, priorytetyzacja backlogu, akceptacja funkcji, reprezentowanie interesariuszy |
| **Scrum Master** | Aleksandra Harasimiuk | Organizacja Scrum (daily, sprint review, retrospective), usuwanie przeszkód, monitorowanie postępów, dokumentacja spotkań |
| **Programista Frontend** | Mateusz Rutkowski | Implementacja interfejsu użytkownika w Vue.js, komponenty Vuetify, integracja z REST API, responsywność, UX |
| **Programista Backend** | Adam Szewczyk | Implementacja Django REST API, modele danych, logika biznesowa, baza danych, bezpieczeństwo, optymalizacja |

---

### 7. Zasoby i narzędzia

| Kategoria | Narzędzie / Technologia | Cel zastosowania |
|-----------|-------------------------|------------------|
| **Metodologia** | Scrum | Organizacja pracy, planowanie sprintów, śledzenie postępów |
| **Zarządzanie projektem** | GitHub, Discord | Planowanie zadań, komunikacja, dokumentacja zespołowa |
| **Repozytorium kodu** | GitHub | Kontrola wersji kodu źródłowego i dokumentacji |
| **Analiza i projektowanie** | Draw.io, Miro, PlantUML | Diagramy przypadków użycia, diagramy UML, mapy procesów |
| **Programowanie backend** | Python 3.9, Django 3.2, Django REST Framework, SQLite/PostgreSQL | Implementacja REST API, baza danych, logika aplikacji |
| **Programowanie frontend** | Vue.js 2, Vue Router, Vuex, Vuetify, Axios | Implementacja interfejsu użytkownika, zarządzanie stanem |
| **Środowisko developerskie** | VS Code, Git, virtualenv, npm, pip | Rozwój, testowanie, zarządzanie zależnościami |
| **Dokumentacja** | Markdown, VS Code | Tworzenie i przechowywanie dokumentacji |
| **Komunikacja** | Discord, Microsoft Teams, e-mail uczelniany | Spotkania daily, konsultacje, przekazywanie informacji |

---

### 8. Harmonogram realizacji (zgodny z metodyką Scrum)

| Sprint | Zakres | Czas realizacji | Cel sprintu |
|--------|--------|-----------------|-------------|
| **Sprint 1** | Inicjacja projektu, analiza wymagań, wybór technologii | styczeń (tydzień 1-2) | Określenie wymagań, wybór stacku (Django, Vue.js), utworzenie repozytorium GitHub |
| **Sprint 2** | Planowanie architektury, definicja ról, wstępna makieta | styczeń (tydzień 3-4) | Przydział ról (Product Owner, Developer), pierwsze makiety interfejsu, decyzje dot. hostingu |
| **Sprint 3** | Modelowanie bazy danych, logowanie, autoryzacja | luty (tydzień 5-6) | Modele Django (tematy, użytkownicy, grupy), mechanizm logowania (bez USOS) |
| **Sprint 4** | Budowa frontendu – widoki listy tematów i szczegółów | luty–marzec (tydzień 7-8) | Widok listy tematów, szczegółów tematu, nawigacja, podstawowy UI w Vue |
| **Sprint 5** | System zapisów na tematy, preferencje grup | marzec (tydzień 9-10) | Mechanizm składania 3 preferencji, tworzenie grup, dołączanie do istniejących |
| **Sprint 6** | Panel administracyjny, zarządzanie użytkownikami | marzec (tydzień 11-12) | CRUD tematów z poziomu admina, dodawanie użytkowników, role prowadzącego/studenta |
| **Sprint 7** | Integracja backendu z frontendem, endpointy API | marzec–kwiecień (tydzień 13-14) | Połączenie Vue z Django REST, wystawienie endpointów, autoryzacja |
| **Sprint 8** | Testy funkcjonalne, poprawki bezpieczeństwa | kwiecień (tydzień 15-16) | Testy manualne, zabezpieczenia dostępu, walidacja danych |
| **Sprint 9** | Hosting, wdrożenie na Heroku, migracje bazy | maj (tydzień 17-18) | Konfiguracja Heroku, migracje Django, automatyzacja deploy z GitHub |
| **Sprint 10** | Finalizacja funkcjonalności, poprawki UI/UX | maj (tydzień 19-20) | Ostateczne poprawki frontendu, responsywność, komunikaty błędów |
| **Sprint 11** | Testy integracyjne i akceptacyjne | maj–czerwiec (tydzień 21-22) | Testy z udziałem prowadzącego, weryfikacja wymagań "must have" |
| **Sprint 12** | Dokumentacja projektu, przygotowanie prezentacji | czerwiec (tydzień 23-24) | Raport końcowy, dokumentacja techniczna, przygotowanie demo |
| **Sprint 13** | Prezentacja wyników, podsumowanie projektu | czerwiec (tydzień 25) | Prezentacja przed komisją, zebranie feedbacku, zamknięcie projektu |

---

### 9. Analiza ryzyka

| Nr | Ryzyko | Prawdopodobieństwo | Skutek | Działanie zapobiegawcze |
|----|---------|-------------------|--------|-------------------------|
| 1 | Konflikty w zespole z powodu różnych harmonogramów | Średnie | Wysoki | Regularne spotkania online, elastyczne godziny pracy, komunikacja asynchroniczna |
| 2 | Brak doświadczenia w Vue.js w zespole frontendowym | Wysokie | Średni | Tutoriale, wykorzystanie Vuetify dla gotowych komponentów, wzajemna pomoc |
| 3 | Problemy z integracją Django REST z Vue.js | Średnie | Średni | Rozpoczęcie od prostego API, dokumentacja CORS, testy integracyjne |
| 4 | Opóźnienia w implementacji z powodu innych obowiązków studenckich | Wysokie | Wysoki | Realistyczny harmonogram sprintów, priorytetyzacja zadań, komunikacja o problemach |
| 5 | Niekompletne dane z USOS do importu | Niskie | Średni | Uproszczony format CSV, skrypt walidacji danych, opcja ręcznego dodawania |
| 6 | Błędy w algorytmie przydziału tematów do grup | Średnie | Wysoki | Testy na danych przykładowych, opcja przydziału ręcznego przez prowadzącego |
| 7 | Problemy z deploymentem lub konfiguracją środowiska | Niskie | Średni | Dockerizacja aplikacji, szczegółowa instrukcja instalacji |

---

### 10. Kryteria sukcesu projektu

- [ ] Aplikacja uruchamia się lokalnie (backend: localhost:8000, frontend: localhost:8080)
- [ ] Wszystkie podstawowe wymagania funkcjonalne zaimplementowane
- [ ] System autoryzacji z 3 rolami działa poprawnie
- [ ] Student może składać preferencje i formować grupy
- [ ] Prowadzący może zarządzać tematami i przydzielać je grupom
- [ ] Kod źródłowy dostępny w repozytorium GitHub
- [ ] Dokumentacja zawiera analizę wymagań i kartę projektu
- [ ] Projekt został zaprezentowany i oddany w terminie

---

### 11. Rezultaty projektu

1. **Działająca aplikacja webowa** z backendem w Django i frontendem w Vue.js
2. **Dokumentacja wymagań** analiza interesariuszy, wymagania funkcjonalne/niefunkcjonalne, przypadki użycia
3. **Karta projektu** z harmonogramem, zespołem, zakresem i analizą ryzyk
4. **Repozytorium GitHub** z kodem źródłowym i dokumentacją
5. **Instrukcja uruchomienia** i konfiguracji środowiska developerskiego
6. **Prezentacja końcowa** projektu z demonstracją działania systemu

---

### 12. Akceptacja projektu

| Funkcja | Imię i nazwisko | Data | Podpis |
|---------|----------------|------|--------|
| Product Owner / Kierownik projektu | Michał Cybulski | 7.12.2025 | __________ |
| Scrum Master | Aleksandra Harasimiuk | 7.12.2025 | __________ |
| Programista Frontend | Mateusz Rutkowski | 7.12.2025 | __________ |
| Programista Backend | Adam Szewczyk | 7.12.2025 | __________ |
| Prowadzący | dr inż. Przemysław Korpas | [Data akceptacji] | __________ |

---

## Uwagi końcowe:

- Dokument przechowywany w repozytorium projektu: `docs/karta-projektu.md`
- Aktualizacja wersji dokumentu wymaga odnotowania zmian w historii wersji
- Każdy członek zespołu ma obowiązek zapoznać się z treścią karty projektu
- Projekt podlega ocenie zgodnie z kryteriami ustalonymi przez prowadzącego
- Wszystkie decyzje projektowe dokumentowane są w notatkach ze spotkań zespołowych

---
**Wersja dokumentu:** 1.0  
**Data ostatniej aktualizacji:** 7.12.2025
**Status:** W trakcie realizacji  
**Metodologia:** Scrum  
**Cykl sprintów:** 2-tygodniowe iteracje
