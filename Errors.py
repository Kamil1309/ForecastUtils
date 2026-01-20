import numpy as np
import math

def CalculateErrors(realTimeSeries, predictedTimeSeries, printData=False, decimalPlaces= 2):
   # Konwersja na tablice NumPy
   real = np.array(realTimeSeries, dtype=float)
   pred = np.array(predictedTimeSeries, dtype=float)

   # Sprawdzenie zgodności długości
   if real.shape != pred.shape:
      raise ValueError(f"realTimeSeries i predictedTimeSeries muszą mieć ten sam rozmiar a mają {real.shape} vs {pred.shape}.")

   # Uniknięcie dzielenia przez zero
   mask = real != 0
   if not np.any(mask):
      raise ValueError("Wszystkie wartości zerowe w realTimeSeries — nie można obliczyć błędów względnych.")

   # Obliczenia tylko dla niezerowych wartości rzeczywistych
   real = real[mask]
   pred = pred[mask]

   # Różnice
   diff = pred - real
   mean_real = np.mean(real)

   # Metryki
   MPE   = np.mean(diff / real) * 100
   MAPE  = np.mean(np.abs(diff / real)) * 100
   MSE   = np.mean(diff**2)
   RMSE  = np.sqrt(MSE)
   rRMSE = RMSE / mean_real * 100
   MAE   = np.mean(np.abs(diff))
   MBE   = np.mean(diff)
   rMBE  = MBE / mean_real * 100

   # R² = 1 - SSR/SST
   SSR = np.sum(diff**2)
   SST = np.sum((real - mean_real)**2)
   R2  = 1 - SSR / SST if SST != 0 else np.nan

   # Zaokrąglenia
   results = {
      "MPE": round(MPE, decimalPlaces),     #Mean Percentage Error
      "MAPE": round(MAPE, decimalPlaces),   #Mean Absolute Percentage Error
      "MSE": round(MSE, decimalPlaces),     #Mean Squared Error
      "RMSE": round(RMSE, decimalPlaces),   #Root Mean Squared Error
      "rRMSE": round(rRMSE, decimalPlaces), #Relative RMSE
      "MAE": round(MAE, decimalPlaces),     #Mean Absolute Error
      "MBE": round(MBE, decimalPlaces),     #Mean Bias Error
      "rMBE": round(rMBE, decimalPlaces),   #Relative Mean Bias Error
      "R2 Score": round(R2, decimalPlaces)  #R2 Score
   }


   if printData:
      for k, v in results.items():
         suffix = "%" if k in ["MPE", "MAPE", "rRMSE", "rMBE"] else ""
         print(f"{k}: {v}{suffix}")

   return tuple(results.values())

def CalculateMAPE(realTimeSeries, predictedTimeSeries, printData=False, decimalPlaces=2):
   """
   Oblicza Mean Absolute Percentage Error (MAPE) pomiędzy danymi rzeczywistymi a przewidywanymi.
   
   Parametry:
      realTimeSeries (list/array): wartości rzeczywiste
      predictedTimeSeries (list/array): wartości przewidywane
      decimalPlaces (int): liczba miejsc po przecinku w wyniku
   
   Zwraca:
      MAPE w procentach (float)
   """
   real = np.array(realTimeSeries, dtype=float)
   pred = np.array(predictedTimeSeries, dtype=float)
   
   if real.shape != pred.shape:
      raise ValueError(f"realTimeSeries i predictedTimeSeries muszą mieć ten sam rozmiar ({real.shape} vs {pred.shape})")
   
   # Uniknięcie dzielenia przez zero
   mask = real != 0
   if not np.any(mask):
      raise ValueError("Wszystkie wartości zerowe w realTimeSeries — nie można obliczyć MAPE.")
   
   real = real[mask]
   pred = pred[mask]
   
   diff = np.abs(pred - real) / real
   MAPE = np.mean(diff) * 100
   
   if printData:
      print(f"MAPE: {MAPE}%")

   return round(MAPE, decimalPlaces)


# ----------------------------------------------
# Kod uruchomieniowy (test)
# ----------------------------------------------

# # Przykładowe dane
# real = np.array([10, 20, 30, 40, 50])
# pred = np.array([12, 19, 29, 43, 48])

# # Uruchomienie funkcji i wypisanie wyników
# metrics = CalculateErrors(real, pred, printData=True)

# # Wyświetlenie zwracanych wartości
# print("\nZwracane wartości jako krotka:")
# print(metrics)
