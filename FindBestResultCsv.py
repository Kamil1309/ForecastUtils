import pandas as pd
from itertools import product


def select_best_rows(csv_file, column_name, n_best=5, ascending=True):
   """
   Wybiera najlepsze wiersze z pliku CSV według wskazanej kolumny.

   Parametry:
      csv_file (str): ścieżka do pliku CSV
      column_name (str): nazwa kolumny, po której sortujemy
      n_best (int): ile najlepszych wierszy wypisać
      ascending (bool): 
         True  -> najmniejsze wartości są najlepsze (np. MAPE, Score)
         False -> największe wartości są najlepsze (np. R2_Score)

   Zwraca:
      pandas.DataFrame z najlepszymi wierszami
   """

   # Wczytaj dane
   df = pd.read_csv(csv_file)

   # Sprawdź, czy kolumna istnieje
   if column_name not in df.columns:
      raise ValueError(f"Kolumna '{column_name}' nie istnieje w pliku CSV. "
                        f"Dostępne kolumny: {list(df.columns)}")

   # Posortuj dane i wybierz n najlepszych
   best_rows = df.sort_values(by=column_name, ascending=ascending).head(n_best)

   print(f"\nNajlepsze {n_best} wierszy wg kolumny '{column_name}' "
         f"({'rosnąco' if ascending else 'malejąco'}):\n")
   print(best_rows.to_string(index=False))

   return best_rows

def CheckDuplicates(fileName):
   # Wczytaj plik
   df = pd.read_csv(fileName)

   # Znajdź wszystkie duplikaty (keep=False)
   dupes = df[df.duplicated(keep=False)]

   print("Liczba wszystkich wierszy:", len(df))
   print("Liczba wierszy powtarzających się:", len(dupes))

   if dupes.empty:
      print("\nBrak duplikatów.")
      return dupes

   print("\n=== Duplikaty w formacie CSV (pełne wiersze z numerem wiersza) ===")
   
   # Wypisz każdy wiersz jako CSV z numerem wiersza z pliku
   for idx, row in dupes.iterrows():
      line_values = []
      for x in row.values:
         # Jeśli liczba całkowita w float, wypisz jako int
         if isinstance(x, float) and x.is_integer():
               line_values.append(str(int(x)))
         else:
               line_values.append(str(x))
      line = ",".join(line_values)
      print(f"{idx + 1}   {line}")

   return dupes


def generate_param_combinations(param_grid):
   """Generuje wszystkie możliwe kombinacje parametrów."""
   keys = list(param_grid.keys())
   values = list(param_grid.values())
   return [dict(zip(keys, combo)) for combo in product(*values)]

def find_missing_combinations(param_grid, results_file):
   """
   Sprawdza, które kombinacje parametrów z param_grid NIE występują w pliku wynikowym.

   Zwraca:
      pandas.DataFrame z brakującymi kombinacjami.
   """
   print("\n=== ANALIZA BRAKUJĄCYCH KOMBINACJI ===")

   # Wczytaj plik wynikowy
   df = pd.read_csv(results_file)

   # Kolumny parametrów
   param_columns = list(param_grid.keys())

   # Wszystkie możliwe kombinacje
   all_combos = generate_param_combinations(param_grid)
   df_all = pd.DataFrame(all_combos)

   # Parametry z pliku
   df_params = df[param_columns].drop_duplicates()

   # Wyszukiwanie brakujących
   merged = df_all.merge(df_params, on=param_columns, how="left", indicator=True)
   missing = merged[merged["_merge"] == "left_only"].drop(columns=["_merge"])

   # Ustawienia pandas — pełne kolumny bez "..."
   pd.set_option('display.max_columns', None)
   pd.set_option('display.width', 200)
   pd.set_option('display.max_colwidth', None)

   print(f"Liczba brakujących kombinacji: {len(missing)}")
   print(missing.to_string(index=False))

   return missing


# ======= PRZYKŁAD UŻYCIA =======

if __name__ == "__main__":
   # ====================== Znalezienie najlepszych wyników ======================
   csv_file = "Wyniki_Holt_3.txt"  # Twój plik z wynikami
   csv_file = "LSTM_GridSearch_Results.txt"  # Twój plik z wynikami
   csv_file = "Hybrid_GridSearch_Results.txt"  # Twój plik z wynikami

   # Wybierz metrykę, sposób sortowania i liczbę wyników
   column = "MAPE"     # np. "Score", "MAPE", "R2_Score"
   n = 5               # ile najlepszych wierszy chcesz zobaczyć
   smallest = True     # True jeśli mniejsze = lepsze, False jeśli większe = lepsze

   select_best_rows(csv_file, column, n_best=n, ascending=smallest)

   # # ====================== Sprawdzenie duplikatów ======================

   CheckDuplicates(csv_file)

   # # ====================== Znalezienie najlepszych wyników ======================

   param_grid = {
      "n_steps": [1, 6, 12],
      "epochs": [40, 60, 100],
      "batch_size": [8, 16, 24],
      "lstm1_units": [128, 256, 512],
      "lstm2_units": [64, 128, 256],
      "dense1_units": [40, 80],
      "dense2_units": [20],
      "dropout1": [0, 0.1],
      "dropout2": [0, 0.1]
   }

   # uruchomienie funkcji
   missing = find_missing_combinations(param_grid, csv_file)
