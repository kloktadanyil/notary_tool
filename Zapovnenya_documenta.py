# Zapovnenya_documenta.py
import tkinter as tk
import tkinter.ttk as ttk 

def create_zapovnenya_documenta_frame(parent_window, on_back_command, on_next_command):
    zapovnenya_documenta_frame = ttk.Frame(parent_window)
    label = ttk.Label(zapovnenya_documenta_frame, text="Оберіть вид документа:", font=("Arial", 16))
    label.pack(pady=20)
    next_button = ttk.Button(zapovnenya_documenta_frame, text="Заяви", command=on_next_command)
    next_button.pack(pady=10)
    back_button = ttk.Button(zapovnenya_documenta_frame, text="< Назад", command=on_back_command)
    back_button.pack(anchor="w", padx=10, pady=10)
    
    return zapovnenya_documenta_frame