import matplotlib.pyplot as plt
import numpy as np

def create_series_plot(series_list, x_label="Indeks", y_label="Wartość", title=None, figsize=(10, 5)):
   """Tworzy i zwraca obiekt wykresu (Figure)."""
   fig, ax = plt.subplots(figsize=figsize)
   
   for i, s in enumerate(series_list):
      values = np.array(s.get("values", []))
      start = s.get("start_index", 0)
      ax.plot(np.arange(start, start + len(values)), values, 
               label=s.get("label", f"Seria {i+1}"),
               color=s.get("color"), linestyle=s.get("linestyle", "-"))

   ax.set_xlabel(x_label)
   ax.set_ylabel(y_label)
   if title: ax.set_title(title)
   ax.legend()
   plt.tight_layout()
   
   return fig

def save_plot(fig, path):
   """Zapisuje przekazany wykres."""
   fig.savefig(path, dpi=300, bbox_inches="tight")
   plt.close(fig)
