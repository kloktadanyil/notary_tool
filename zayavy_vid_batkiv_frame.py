# vybir_zayavy.py
import tkinter as tk 
import tkinter.ttk as ttk 

def create_zayavy_vid_batkiv_frame(parent_window, on_back_command, on_next_command):
    zayavy_vid_batkiv_frame = ttk.Frame(parent_window)
    label = ttk.Label(zayavy_vid_batkiv_frame, text="Оберіть вид заяви на виїзд за кордон:", font=("Arial", 16))
    label.pack(pady=20)
    next_button = ttk.Button(zayavy_vid_batkiv_frame, text="Заяви на виїзд за кордон від 1 батька", command=on_next_command)
    next_button.pack(pady=10)
    back_button = ttk.Button(zayavy_vid_batkiv_frame, text="< Назад", command=on_back_command)
    back_button.pack(anchor="w", padx=10, pady=10)
    
    return zayavy_vid_batkiv_frame