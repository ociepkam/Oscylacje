# Test integracji relacji

1) Wartości parametrów w pliku xlsx wygenerowanym przez general_experiment.py:
    
    Każdy wiersz oznacza trial, który zostanie wyświetlony na ekranie
    
    A) BLOCK_NUMBER
    - liczba naturalna dodatnia, która określa do którego bloku należy dany trial
    - bloki zostaną wyświetlone kolejno od najniższego numeru do najwyższego
    - triale należące do tego samego bloku nie muszą się znajdować bezpośrednio po sobą
    - kolejność występowania triali w bloku określa kolejność wyświetlenia ich podczas eksperymentu (chyba, że zostanie włączona opcja randomizacji)
    
    B) SAMPLE_TYPE
    - może przyjmować nastepujące wartości
        * instruction (zawiera tylko i wyłącznie informacje w kolumnie A, B, G, Q)
        * letters
        * figures
        * NamesHeightRelations
        * NamesAgeRelations
    
    C) N
    - liczba relacji
        * może przyjmować wartości 2, 3, 4
        * program działa dla dowolnej liczby relacji, lecz powyrzsze wartości są jedynymi dozwolonymi w specyfikacji
    
    D) NR
    - numer kolejnego triala
    
    E) MEMORY
    - okresla typ zadania
    - może przyjmować wartości 1, 0
    
    F) INTEGR
    - okresla typ zadania
    - może przyjmować wartości 1, 0
    
    G) SHOW_TIME
    - liczba naturalna dodatnia
    - czas prezentacji każdej z relacji określony w .........

    H) REST_TIME
    - liczba naturalna dodatnia
    - długośc przerwy pomiędzy relacjami określona w .........
    
    I) MAX__TIME
    - liczba naturalna dodatnia
    - czas na odpowiedź określona w .........
    
    J) FEEDB
    - może przyjmować wartości 0, 1 albo 2
        * 0 (nie wyświetlaj informacji o poprawności rozwiązania tego triala)
        * 1 (wyświetl informację o poprawności rozwiązania tego triala)
        * 2 (na koniec testu podaj całkowity wynik wszystkich rozwiązanych triali)
    
    I) FEEDB_TIME
    - liczba naturalna dodatnia
    - czas wyświetlania FEEDB określona w .........
    
    L) WAIT
    - liczba naturalna
        * 0 ( po trialu wyświetla napis „naciśnij przycisk” i czeka na reakcję badanego- czas na odpoczynek)
        * inne (czas przerwy pomiędzy próbami określony w .........)
    
    M) EXP
    - może przyjmować wartości 0, 1
        * 0 trial testowy
        * 1 trial experymentalny
    
    N) FIX__TIME
    - liczba naturalna dodatnia
    - czas wyświetlania punktu fixacji określona w .........
    
    0) LIST_VIEW
    - może przyjmować wartości 0, 1
        * 1 wyświetla odpowiedzi jedna pod drugę
        * 0 wyświetla odpowiedzi po sobie
    
    P) INSTRUCTION
    - link do pliku
    - plik w formacie txt, bmp, jpg
    - przed trialem wyświetla informację znajdująca się w pliku

    R) Weryfikacja
    - określa czy dane w wierszu zostały poprawnie wprowadzone (przy założeniu, że użytkownik jest inteligentny)
        * 1 (dane wprowadzone poprawnie)
        * 0 (dane wprowadzone błędnie)
    - pierwsza liczba w kolumnie określa ile triali zostało wprowadzonych poprawnie

2) Wartości parametrów w pliku yaml wygenerowanym przez concrete_experiment.py:

    - informacje w pliku są podawane zgodnie z kolejnością wyświetlania
    - struktura ma postać drzewiastą. Spis elementów poczynając od najbardziej ogólnych
        * experiment
            + name (nazwa osoby badanej w postaci ID+SEX+AGE)
            + list_of_blocks (lista występujących kolejno po sobie bloków)
            + eeg
                @ może przyjmować wartości 0, 1
                @ okresla, czy eeg jest włączone podczas badania i nalezy wysyłac triggery
        * experiment_elements (lista elementów w danym bloku)
            + może zawierać trzy typy elementów (TYPE)
        * instruction
            + instruction_type (text, image)
            + path (ścieżka do pliku zawierającego instrukcję, TIP)
            + time (SHOW_TIME)
            + type (SAMPLE_TYPE)
        * trial
            + poza elementami opisanymi w podpunkcie 1 zawiera:
                @ ANSWER (string, zawierajacy odpowiedź)
                @ RELATIONS_LIST (tablica stringów - kolejnych wyswietlanych relacji)
                @ TASK (pytanie, które zostanie zadane na koniec triala)
            
        

