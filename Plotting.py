import matplotlib.pyplot as plt
import numpy as np
import os

def create_series_plot(
   series_list: list[dict],
   x_label: str = "Indeks",
   y_label: str = "Wartość",
   title: str = None,
   grid_step: int = None,
   show_legend: bool = True,
   figsize: tuple = (10, 5)
):
   """Tworzy i zwraca obiekt wykresu (Figure) ze wszystkimi ustawieniami."""
   fig, ax = plt.subplots(figsize=figsize)

   # Narysuj każdą serię
   for i, s in enumerate(series_list):
      values = np.array(s.get("values", []))
      start = s.get("start_index", 0)
      ax.plot(
         np.arange(start, start + len(values)),
         values,
         label=s.get("label", f"Seria {i+1}"),
         color=s.get("color", None),
         linestyle=s.get("linestyle", "-"),
         marker=s.get("marker", None)
      )

   # Opisy osi i tytuł
   ax.set_xlabel(x_label)
   ax.set_ylabel(y_label)
   if title:
      ax.set_title(title)

   # Siatka
   ax.grid(True, linestyle="--", alpha=0.6)

   # Linie pionowe co grid_step
   if grid_step:
      max_length = max((s.get("start_index", 0) + len(s.get("values", []))) for s in series_list)
      ax.set_xticks(np.arange(0, max_length + 1, step=grid_step))

   # Legenda
   if show_legend:
      ax.legend()

   fig.tight_layout()
   return fig

def save_plot(fig, path):
   """Tylko zapisuje przekazany wykres i tworzy foldery, jeśli ich nie ma."""
   if path:
      # Wyciągnięcie ścieżki do folderu z pełnej ścieżki pliku
      directory = os.path.dirname(path)
      
      # Tworzenie folderu, jeśli nie istnieje
      if directory and not os.path.exists(directory):
         os.makedirs(directory, exist_ok=True)
         print(f"📁 Utworzono brakujący folder: {directory}")
         
      fig.savefig(path, dpi=300, bbox_inches="tight")
      print(f"✅ Wykres zapisano do pliku: {path}")
