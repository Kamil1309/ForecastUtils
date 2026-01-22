import pandas as pd
import os

def LoadCSVSeries(filePath, columnNames, delimiter=';'):
   """
   Wczytuje jedną lub wiele kolumn z pliku CSV i zwraca:
   - tablicę 1D jeśli wybrano jedną kolumnę,
   - tablicę 2D jeśli wybrano wiele kolumn.
   """
   data = pd.read_csv(filePath, delimiter=delimiter)
   
   # Jeśli podano pojedynczą nazwę — zamień na listę
   if isinstance(columnNames, str):
      columnNames = [columnNames]
   
   missing_cols = [col for col in columnNames if col not in data.columns]
   if missing_cols:
      raise ValueError(f"Nie znaleziono kolumn: {missing_cols}. Dostępne: {list(data.columns)}")
   
   selected = data[columnNames]
   
   if len(columnNames) == 1:
      return selected[columnNames[0]].values.flatten()
   else:
      return selected.values

def SaveCSVResults(results: pd.DataFrame, output_path: str, decimal_places: int = 3):
    """
    Zapisuje wyniki (DataFrame) do pliku CSV.
    Kolumny zaczynające się od 'Actual_' i 'Predicted_' są zaokrąglane.
    """
    if not isinstance(results, pd.DataFrame):
        raise TypeError("results musi być obiektem pandas.DataFrame")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    results_rounded = results.copy()

    for col in results_rounded.columns:
        if col.startswith(("Actual_", "Predicted_")):
            results_rounded[col] = results_rounded[col].round(decimal_places)

    results_rounded.to_csv(output_path, index=False)
    print(f"✅ Wyniki zapisano do: {output_path}")


# ======= PRZYKŁAD UŻYCIA =======

if __name__ == "__main__":
   data_array = LoadCSVSeries('Data/Bukowsko_total_sum.csv', 'Energy (kWh)') # jedna kolumna

   print(data_array.shape)
   print(data_array[:5], '\n')

   # wiele kolumn
   columns = ['Average power (kW)','Energy (kWh)']
   data_array = LoadCSVSeries('Data/Bukowsko_total_sum.csv', columns)

   print(data_array.shape)
   print(data_array[:5])
