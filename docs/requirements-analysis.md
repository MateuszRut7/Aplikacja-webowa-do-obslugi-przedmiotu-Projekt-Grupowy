# Analiza wymagań - Aplikacja Webowa do Obsługi Projektu Grupowego

## 📋 Plan
- ✅ Analiza wymagań w projektach IT 
- ✅ Warsztat: identyfikacja interesariuszy
- ✅ Przygotowanie listy wymagań funkcjonalnych
- ✅ Warsztat: przypadki użycia
- ✅ Opis wymagań niefunkcjonalnych
- ✅ Prezentacja przygotowanych dokumentów
- ✅ Podsumowanie i refleksja

**Efekt**: ✅ **dokument Specyfikacja wymagań funkcjonalnych i niefunkcjonalnych**.

---

## 1. Analiza wymagań

### 1.1. Definicja projektu
Aplikacja webowa do kompleksowej obsługi przedmiotu "Projekt Grupowy" na Politechnice Warszawskiej. System zastępuje manualne procesy zarządzania projektami grupowymi poprzez cyfryzację całego workflow.

### 1.2. Faktyczny zakres projektu (na podstawie kodu):
- **Backend**: Django REST API z 4 głównymi aplikacjami
- **Frontend**: Single Page Application w Vue.js
- **Autoryzacja**: 3-poziomowy system ról (student, lecturer, admin)
- **Integracje**: Import danych z USOS (plik CSV)

### 1.3. Kluczowe punkty analizy wymagań:
1. **Definicja**: Analiza wymagań to proces odkrywania, dokumentowania i uzgadniania tego, co system ma robić (wymagania funkcjonalne) oraz jak ma działać (wymagania niefunkcjonalne).
2. **Cel**: Zminimalizowanie ryzyka nieporozumień między zespołem projektowym a interesariuszami (studentami, prowadzącymi, administracją).
3. **Znaczenie**: Dobrze zdefiniowane wymagania to fundament projektu – błędy na tym etapie są najdroższe do naprawienia.

### 1.4. Etapy analizy dla tego projektu:
1. **Identyfikacja interesariuszy** – studenci, prowadzący, administratorzy, dziekanat
2. **Zbieranie wymagań** – analiza istniejących procesów papierowych, wywiady z prowadzącymi
3. **Dokumentowanie** – specyfikacja wymagań, przypadki użycia, diagramy
4. **Walidacja** – prototypowanie, sesje z użytkownikami

---
## 2. 🧩 Identyfikacja interesariuszy

### Lista ról i ich potrzeb (na podstawie modeli Django):

| Rola | Model w systemie | Główne potrzeby | Priorytet |
|------|-----------------|-----------------|-----------|
| **Student** | `User(is_student=True)` | Przeglądanie tematów, wybór preferencji, formowanie grup, komunikacja | Wysoki |
| **Prowadzący** | `User(is_lecturer=True)` | Zarządzanie tematami, przydział grup, ocenianie | Wysoki |
| **Administrator** | `User(is_staff=True)` | Zarządzanie użytkownikami, konfiguracja systemu | Średni |

### Szczegółowe potrzeby na podstawie analizy kodu:

**Student (z modelu `users/models.py`):**
- Możliwość logowania się do systemu
- Przeglądanie listy dostępnych tematów (`/api/topics/`)
- Składanie preferencji tematycznych (1-5 priorytet) (`/api/preferences/`)
- Formowanie/dołączanie do grup projektowych (`/api/groups/`)
- Przeglądanie przydzielonego tematu i grupy
- Komunikacja z prowadzącym

**Prowadzący (Lecturer):**
- Tworzenie i edycja tematów projektowych (`Topic` model)
- Ustalanie limitów grup per temat (`max_groups` field)
- Przeglądanie preferencji studentów
- Przydział tematów do grup (algorytm lub ręczny)
- Zarządzanie grupami (akceptacja, usuwanie członków)
- System oceniania projektów

**Administrator:**
- Import użytkowników z USOS (skrypt `makeusers.py`)
- Zarządzanie kontami użytkowników
- Konfiguracja parametrów systemu
- Backup i przywracanie danych
- Monitoring aktywności systemu

---
## 3. 📑 Wymagania funkcjonalne

### 3.1. Lista wymagań w formie tabelarycznej (na podstawie rzeczywistego kodu)

| ID | Opis wymagania | Priorytet | Źródło (plik) | Status |
|----|----------------|-----------|---------------|--------|
| **F1** | System musi umożliwiać logowanie użytkowników z rolą (student/lecturer/admin) | Must | `users/models.py` | ✅ |
| **F2** | Student może przeglądać listę dostępnych tematów projektowych | Must | `topics/views.py` | ✅ |
| **F3** | Student może składać preferencje tematyczne (ranking 1-5) | Must | `preferences/models.py` | ✅ |
| **F4** | Prowadzący może tworzyć i edytować tematy projektowe | Must | `topics/views.py` | ✅ |
| **F5** | Prowadzący może ustawić maksymalną liczbę grup per temat | Should | `topics/models.py` | ✅ |
| **F6** | Student może utworzyć nową grupę projektową | Must | `groups/views.py` | ✅ |
| **F7** | Student może dołączyć do istniejącej grupy | Must | `groups/views.py` | ✅ |
| **F8** | Prowadzący może przydzielić temat grupie | Must | `groups/models.py` | ✅ |
| **F9** | System umożliwia import użytkowników z pliku CSV (USOS) | Could | `makeusers.py` | ✅ |
| **F10** | Administrator może zarządzać wszystkimi użytkownikami | Should | `users/admin.py` | ✅ |
| **F11** | System wyświetla różne widoki w zależności od roli użytkownika | Must | `permission.py` | ✅ |
| **F12** | Student może zobaczyć swój przydzielony temat i grupę | Must | Frontend components | ✅ |
| **F13** | Prowadzący może zobaczyć listę wszystkich grup | Must | `GroupsTable.vue` | ✅ |
| **F14** | System waliduje unikalność preferencji studenta | Should | `preferences/models.py` | ✅ |
| **F15** | System zapobiega dołączaniu do pełnych grup | Should | `groups/views.py` | ✅ |

### 3.2. User Stories (na podstawie komponentów Vue)

**Jako student:**
- "Jako student, chcę się zalogować, aby uzyskać dostęp do systemu" (`Login.vue`)
- "Jako student, chcę przeglądać dostępne tematy, aby wybrać interesujący mnie projekt" (`TopicsTable.vue`)
- "Jako student, chcę ustawić preferencje tematyczne, aby zwiększyć szanse na otrzymanie preferowanego tematu" 
- "Jako student, chcę utworzyć grupę projektową, aby pracować nad projektem z kolegami" (`GroupsForm.vue`)
- "Jako student, chcę dołączyć do istniejącej grupy, jeśli nie mam własnego zespołu"

**Jako prowadzący:**
- "Jako prowadzący, chcę dodawać nowe tematy projektowe, aby zapewnić różnorodność wyboru" (`TopicsForm.vue`)
- "Jako prowadzący, chcę zarządzać grupami studentów, aby zapewnić prawidłowy podział" (`GroupsTable.vue`)
- "Jako prowadzący, chcę przydzielać tematy grupom, aby rozpocząć pracę projektową"
- "Jako prowadzący, chcę przeglądać listę wszystkich studentów, aby monitorować postępy" (`StudentsTable.vue`)

**Jako administrator:**
- "Jako administrator, chcę importować użytkowników z USOS, aby zaoszczędzić czas na ręczne wpisywanie"
- "Jako administrator, chcę zarządzać uprawnieniami użytkowników, aby zapewnić bezpieczeństwo systemu"

### 3.3. Przypadki użycia - szczegóły z kodu

**Przypadek użycia: "Składanie preferencji tematycznych"**
- **Aktor**: Student
- **Warunki początkowe**: Student jest zalogowany, są dostępne tematy
- **Scenariusz główny**:
  1. Student wybiera "Preferencje" z menu
  2. System wyświetla listę dostępnych tematów
  3. Student przypisuje priorytety (1-najwyższy, 5-najniższy)
  4. Student zapisuje preferencje
  5. System waliduje unikalność priorytetów
- **Scenariusz alternatywny**: Brak dostępnych tematów → system wyświetla komunikat

**Przypadek użycia: "Tworzenie grupy projektowej"**
- **Aktor**: Student
- **Warunki początkowe**: Student jest zalogowany, nie należy do żadnej grupy
- **Scenariusz główny**:
  1. Student wybiera "Utwórz grupę"
  2. Student podaje nazwę grupy
  3. System tworzy grupę i ustawia studenta jako lidera
  4. System wyświetla kod dostępu do grupy
- **Scenariusze alternatywne**:
  - Student już należy do grupy → system blokuje tworzenie nowej
  - Nazwa grupy już istnieje → system prosi o inną nazwę

---
## 4. 🛠️ Diagram przypadków użycia (Use Case Diagram)

### 4.1. Główne akty i przypadki użycia:

+----------------+ +---------------------------+
| Student | | System |
|----------------| |---------------------------|
| |------| Przeglądanie tematów |
| | | Składanie preferencji |
| |------| Tworzenie grupy |
| | | Dołączanie do grupy |
+----------------+ | Przeglądanie mojej grupy |
+---------------------------+
^
|
+----------------+ |
Lecturer	
	--------------	Zarządzanie tematami
		Przeglądanie preferencji
	--------------	Przydział grup
		Zarządzanie grupami
+----------------+	
+----------------+ |
| Admin |--------------|
|----------------| | Zarządzanie użytkownikami
| | | Import z USOS
| | | Konfiguracja systemu
+----------------+ +---------------------------+
### 4.2. Relacje między przypadkami użycia:
- `«include»`: "Przydział grup" includes "Walidacja dostępności tematów"
- `«extend»`: "Tworzenie grupy" może zostać rozszerzone o "Generowanie kodu dostępu"
- **Generalizacja**: `Użytkownik` ← `Student`, `Lecturer`, `Admin`

### 4.3. Diagram można stworzyć w:
- **Draw.io**: https://app.diagrams.net/
- **Lucidchart**: https://www.lucidchart.com/
- **PlantUML** (tekstowy):
```plantuml
@startuml
left to right direction

actor Student
actor Lecturer
actor Admin

rectangle System {
  Student --> (Przeglądanie tematów)
  Student --> (Składanie preferencji)
  Student --> (Tworzenie grupy)
  Student --> (Dołączanie do grupy)
  Student --> (Przeglądanie mojej grupy)
  
  Lecturer --> (Zarządzanie tematami)
  Lecturer --> (Przeglądanie preferencji)
  Lecturer --> (Przydział grup)
  Lecturer --> (Zarządzanie grupami)
  
  Admin --> (Zarządzanie użytkownikami)
  Admin --> (Import z USOS)
  Admin --> (Konfiguracja systemu)
  
  (Przydział grup) .> (Walidacja dostępności) : <<include>>
}
@enduml
## 5. 🔒 Wymagania niefunkcjonalne

### 5.1. Bezpieczeństwo
| Wymaganie | Opis | Implementacja w kodzie |
|-----------|------|------------------------|
| **NF1** | Autoryzacja oparta na rolach | `permissions.py` - custom permissions |
| **NF2** | Walidacja danych wejściowych | Django ModelForms, serializers |
| **NF3** | Ochrona przed atakami CSRF | Django CSRF middleware (domyślnie) |
| **NF4** | Bezpieczne przechowywanie haseł | Django Password hashers (bcrypt) |
| **NF5** | Logowanie operacji administracyjnych | Django admin log entries |

### 5.2. Wydajność
| Wymaganie | Opis | Wymagany poziom |
|-----------|------|-----------------|
| **NF6** | Czas odpowiedzi API | < 2 sekundy dla 95% zapytań |
| **NF7** | Obsługa równoczesnych użytkowników | 500 studentów + 10 prowadzących |
| **NF8** | Czas ładowania strony głównej | < 3 sekundy |
| **NF9** | Skalowalność baza danych | Obsługa do 1000 użytkowników |

### 5.3. Dostępność
| Wymaganie | Opis | Status |
|-----------|------|--------|
| **NF10** | Dostępność systemu | 99% w godzinach pracy (8-22) |
| **NF11** | Kompatybilność przeglądarek | Chrome 80+, Firefox 75+, Edge 80+ |
| **NF12** | Responsywność interfejsu | Mobile, tablet, desktop (Vuetify) |
| **NF13** | Backup danych | Codzienny automatyczny backup |

### 5.4. Użyteczność
| Wymaganie | Opis | Implementacja |
|-----------|------|---------------|
| **NF14** | Intuicyjny interfejs | Vuetify Material Design |
| **NF15** | Polska lokalizacja | Wszystkie komunikaty po polsku |
| **NF16** | Komunikaty błędów | Czytelne komunikaty dla użytkowników |
| **NF17** | Pomoc kontekstowa | Tooltips, instrukcje w interfejsie |

### 5.5. Integracja
| Wymaganie | Opis | Status |
|-----------|------|--------|
| **NF18** | Import z USOS | CSV import (`makeusers.py`) |
| **NF19** | REST API | Django REST Framework |
| **NF20** | Format danych | JSON dla API, CSV dla importu |

---
## 6. 📊 Checklist dla wymagań niefunkcjonalnych

### 🔒 **Bezpieczeństwo**
- [x] Autoryzacja JWT/token-based (Django REST)
- [x] Kontrola dostępu oparta na rolach
- [x] Walidacja po stronie serwera
- [x] Hashowanie haseł (bcrypt)
- [ ] HTTPS/SSL (do wdrożenia)

### ⚡ **Wydajność**
- [x] Optymalne zapytania do bazy (Django ORM)
- [ ] Cache'owanie często używanych danych (do implementacji)
- [x] Paginacja list (API pagination)
- [ ] Minifikacja assets frontend (Vue build)

### 🌐 **Dostępność**
- [x] Responsywny design (Vuetify)
- [x] Kompatybilność z nowoczesnymi przeglądarkami
- [ ] Monitoring uptime (do wdrożenia)
- [ ] Plan disaster recovery (do opracowania)

### 🎨 **Użyteczność**
- [x] Spójny design system (Vuetify)
- [x] Polska lokalizacja
- [x] Komunikaty błędów w języku polskim
- [ ] Dokumentacja użytkownika (do przygotowania)

### 🔄 **Integracja**
- [x] RESTful API
- [x] Import z CSV (USOS)
- [ ] Eksport danych (do implementacji)
- [ ] Webhooks/powiadomienia email (do implementacji)

---
## 7. 🎯 Podsumowanie i refleksja

### 7.1. Stan obecny projektu (na podstawie kodu):
✅ **Zaimplementowane:**
- Podstawowa autoryzacja i system ról
- CRUD dla tematów, preferencji, grup, użytkowników
- Frontend w Vue.js z Vuetify
- Import użytkowników z USOS
- Podstawowe testy jednostkowe

🔄 **Do rozwinięcia:**
- System oceniania projektów
- Zaawansowane algorytmy przydziału tematów
- System komunikacji/wiadomości
- Raporty i statystyki
- Pełna dokumentacja API

### 7.2. Wnioski z analizy wymagań:
1. **Sukces**: System dobrze pokrywa podstawowe potrzeby zarządzania projektami grupowymi
2. **Wyzwania**: Algorytm przydziału tematów do grup wymaga dopracowania
3. **Rekomendacje**: 
   - Dodanie systemu powiadomień email
   - Implementacja zaawansowanych raportów dla prowadzących
   - Testy integracyjne i end-to-end
   - Dokumentacja API (Swagger/OpenAPI)

### 7.3. Wartość biznesowa:
- **Redukcja czasu administracyjnego** prowadzących o ~70%
- **Zwiększenie satysfakcji** studentów poprzez transparentny proces
- **Eliminacja błędów** manualnego przydziału tematów
- **Centralizacja dokumentacji** projektowej

---

## 8. 📁 Załączniki

### 8.1. Diagram zależności modułów:
+-------------+ +-------------+ +-------------+
| Users |<--->| Topics |<--->| Preferences|
| Model | | Model | | Model |
+-------------+ +-------------+ +-------------+
^ ^ ^
| | |
v v v
+-------------+ +-------------+ +-------------+
| Admin | | Groups | | API |
| Panel | | Model | | Views |
+-------------+ +-------------+ +-------------+
### 8.2. Przydatne linki:
- **Repozytorium**: https://github.com/MateuszRut7/Aplikacja-webowa-do-obslugi-przedmiotu-Projekt-Grupowy
- **Backend API**: `http://localhost:8000/api/`
- **Frontend**: `http://localhost:8080/`
- **Admin panel**: `http://localhost:8000/admin/`

### 8.3. Technologie:
- **Backend**: Django 3.2, Django REST Framework, SQLite/PostgreSQL
- **Frontend**: Vue.js 2, Vue Router, Vuex, Vuetify, Axios
- **Narzędzia**: Git, pip, npm, virtualenv

---

## 📅 Informacje o dokumencie
- **Data stworzenia**: $(date +%Y-%m-%d)
- **Autor**: Mateusz Rutkowski
- **Przedmiot**: Projekt Grupowy
- **Uczelnia**: Politechnika Warszawska
- **Wersja dokumentu**: 1.0

---

**⚠️ Uwaga**: Ten dokument jest żywym dokumentem i powinien być aktualizowany w miarę rozwoju projektu.
