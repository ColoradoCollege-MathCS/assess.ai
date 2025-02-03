import tkinter as tk
from tkinter import ttk

class ModelSelector(ttk.Frame):
    # Frame for selecting a model
    # Take in the parent variable and callback function for which model was selected
    def __init__(self, parent, on_model_select):
        style = ttk.Style()
        style.configure(
            "ModelSelector.TFrame",
            background="#D2E9FC"
        )
        super().__init__(parent, style="ModelSelector.TFrame")
        
        # Create combobox (ComboBox is a dropdown menu)
        self.combo = ttk.Combobox(
            self,
            state="readonly",
            font=("SF Pro Text", 13),
            width=50
        )
        # Without pack(), the widget exists but isn't visible
        self.combo.pack(pady=0)
        
        # Style the dropdown list
        self.option_add('*TCombobox*Listbox.font', ("SF Pro Text", 13))
        self.option_add('*TCombobox*Listbox.selectBackground', "#0A84FF")
        self.option_add('*TCombobox*Listbox.selectForeground', "white")
        self.option_add('*TCombobox*Listbox.background', "white")

        # Disable text selection
        self.combo.configure(exportselection=False)
        
        # Bind selection event
        self.combo.bind('<<ComboboxSelected>>', self._on_select)
        self.on_model_select = on_model_select

    def set_models(self, models):
        self.combo['values'] = models
        if models:
            self.combo.set(models[0])
        
    def _on_select(self, event):
        self.on_model_select(self.combo.get())