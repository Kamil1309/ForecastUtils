import matplotlib.pyplot as plt
import numpy as np

def plot_series(
   series_list: list[dict],
   x_label: str = "Indeks",
   y_label: str = "Wartość",
   title: str = None,
   grid_step: int = None,
   show_legend: bool = True,
   figsize: tuple = (10, 5),
   save_path: str = None
):
   """
   Rysuje wiele serii danych o różnych długościach i punktach startowych.

   Parametry:
   -----------
   series_list : lista słowników
      Każdy słownik opisuje jedną serię danych, np.:
      {
         "values": [lista wartości],
         "start_index": 0,
         "label": "Rzeczywiste wartości",
         "color": "blue",
         "linestyle": "-",
         "marker": None
      }
   x_label, y_label : str
      Opisy osi.
   title : str
      Tytuł wykresu.
   grid_step : int
      Co ile punktów na osi X wstawić pionową linię (siatkę).
   show_legend : bool
      Czy wyświetlić legendę.
   figsize : tuple
      Rozmiar wykresu w calach.
   save_path : str (opcjonalne)
      Jeśli podano, zapisze wykres do pliku (np. "plot.png" lub "plot.pdf").
   """

   plt.figure(figsize=figsize)

   # Narysuj każdą serię
   for i, s in enumerate(series_list):
      values = np.array(s.get("values", []))
      start = s.get("start_index", 0)
      label = s.get("label", f"Seria {i+1}")
      color = s.get("color", None)
      linestyle = s.get("linestyle", "-")
      marker = s.get("marker", None)

      plt.plot(
         np.arange(start, start + len(values)),
         values,
         label=label,
         color=color,
         linestyle=linestyle,
         marker=marker
      )

   # Opisy osi
   plt.xlabel(x_label)
   plt.ylabel(y_label)

   # Tytuł
   if title:
      plt.title(title)

   # Siatka
   plt.grid(True, linestyle="--", alpha=0.6)

   # Linie pionowe co grid_step
   if grid_step:
      max_length = max(s["start_index"] + len(s["values"]) for s in series_list)
      plt.xticks(np.arange(0, max_length + 1, step=grid_step))

   # Legenda
   if show_legend:
      plt.legend()

   plt.tight_layout()

   # Zapis do pliku
   if save_path:
      plt.savefig(save_path, dpi=300, bbox_inches="tight")
      print(f"✅ Wykres zapisano do pliku: {save_path}")

   plt.show()



