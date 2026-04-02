# vybir_zayavy.py
import tkinter as tk # tk все ще потрібен
import tkinter.ttk as ttk # Імпортуємо ttk як ttk

def create_zayavy_vid_batkiv_frame(parent_window, on_back_command, on_next_command):
    # ЗАМІНЕНО: tk.Frame на ttk.Frame
    zayavy_vid_batkiv_frame = ttk.Frame(parent_window)
    
    # ЗАМІНЕНО: tk.Label на ttk.Label
    label = ttk.Label(zayavy_vid_batkiv_frame, text="Оберіть вид заяви на виїзд за кордон:", font=("Arial", 16))
    label.pack(pady=20)
    
    # ЗАМІНЕНО: tk.Button на ttk.Button
    next_button = ttk.Button(zayavy_vid_batkiv_frame, text="Заяви на виїзд за кордон від 1 батька", command=on_next_command)
    next_button.pack(pady=10)
    
    # ЗАМІНЕНО: tk.Button на ttk.Button
    back_button = ttk.Button(zayavy_vid_batkiv_frame, text="< Назад", command=on_back_command)
    back_button.pack(anchor="w", padx=10, pady=10)
    
    return zayavy_vid_batkiv_frame