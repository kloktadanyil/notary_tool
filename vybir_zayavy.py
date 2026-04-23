# vybir_zayavy.py
import tkinter as tk
import tkinter.ttk as ttk 

def create_vybir_zayavy_frame(parent_window, on_back_command, on_next_command):
    vybir_zayavy_frame = ttk.Frame(parent_window)
    label = ttk.Label(vybir_zayavy_frame, text="Оберіть вид заяви:", font=("Arial", 16))
    label.pack(pady=20)
    next_button = ttk.Button(vybir_zayavy_frame, text="Заяви на виїзд за кордон", command=on_next_command)
    next_button.pack(pady=10)
    back_button = ttk.Button(vybir_zayavy_frame, text="< Назад", command=on_back_command)
    back_button.pack(anchor="w", padx=10, pady=10)
    
    return vybir_zayavy_frame