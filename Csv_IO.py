import pandas as pd

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
