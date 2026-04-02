import tkinter as tk
import tkinter.ttk as ttk  # Імпортуємо ttk
from Zapovnenya_documenta import create_zapovnenya_documenta_frame
from vybir_zayavy import create_vybir_zayavy_frame
from zayavy_vid_batkiv_frame import create_zayavy_vid_batkiv_frame
from Zayava_Form_1_batko import *
from Zayava_Form_1_batko import create_country_frame_frame

def hide_all_frames():
    """Приховує всі існуючі фрейми."""
    for frame in [main_menu_frame, Zapovnenya_documenta_frame, vybir_zayavy_frame, zayavy_vid_batkiv_frame, zayava_1_batko_frame,country_frame]:
        if frame.winfo_ismapped():
            frame.pack_forget()

def show_main_menu_frame():
    hide_all_frames()
    main_menu_frame.pack(fill="both", expand=True)

def show_Zapovnenya_documenta_frame():
    hide_all_frames()
    Zapovnenya_documenta_frame.pack(fill="both", expand=True)

def show_vybir_zayavy_frame():
    hide_all_frames()
    vybir_zayavy_frame.pack(fill="both", expand=True)
    
def show_zayavy_vid_batkiv_frame():
    hide_all_frames()
    zayavy_vid_batkiv_frame.pack(fill="both", expand=True)
    
def show_zayava_1_batko_frame():
    hide_all_frames()
    zayava_1_batko_frame.pack(fill="both", expand=True)
    
def show_country_frame():
    hide_all_frames()
    country_frame.pack(fill="both", expand=True)
# Ця функція централізовано налаштовує всі стилі
def setup_styles():
    style = ttk.Style()
    
    # "TButton" - це базовий стиль для всіх ttk.Button
    style.configure("TButton", font=("Arial",10))
    
    # "MainMenu.TButton" - це власний стиль, що успадковує від TButton
    # і може мати додаткові або змінені властивості.
    style.configure("MainMenu.TButton", font=("Arial", 14))
# --- Створення головного вікна та його налаштування ---
root = tk.Tk()
root.title("Нотаріус")
root.geometry("1200x1000")
style = ttk.Style()
style.configure("Green.TLabel", foreground="green")
style.configure("Red.TLabel", foreground="red")
# Викликаємо функцію, щоб налаштувати стилі для всього додатку
setup_styles()
# Головне меню
# ЗАМІНЕНО: tk.Frame на ttk.Frame
main_menu_frame = ttk.Frame(root)
# ЗАМІНЕНО: tk.Label на ttk.Label
label_menu = ttk.Label(main_menu_frame, text="Оберіть тему яка вас цікавить: ", font=("Arial", 18))
label_menu.pack(pady=20)
# ЗАМІНЕНО: tk.Button на ttk.Button
button_Zapovnenya_documenta = ttk.Button(main_menu_frame, text="Заповнення документа",style="MainMenu.TButton",width=60, command=show_Zapovnenya_documenta_frame)
button_Zapovnenya_documenta.pack(pady=40)

# Створюємо фрейми. Код їх створення залишається без змін,
# оскільки в них вже використовуються функції, які повертають ttk.Frame.
Zapovnenya_documenta_frame = create_zapovnenya_documenta_frame(root, on_back_command=show_main_menu_frame, on_next_command=show_vybir_zayavy_frame)
vybir_zayavy_frame = create_vybir_zayavy_frame(root, on_back_command=show_Zapovnenya_documenta_frame, on_next_command=show_zayavy_vid_batkiv_frame)
zayavy_vid_batkiv_frame = create_zayavy_vid_batkiv_frame(root, on_back_command=show_vybir_zayavy_frame, on_next_command=show_zayava_1_batko_frame)
zayava_1_batko_frame = create_zayava_1_batko_frame(root, on_back_command=show_zayavy_vid_batkiv_frame,on_next_command=show_country_frame)
country_frame = create_country_frame_frame (root, app_data, on_back_command=show_main_menu_frame)
main_menu_frame.pack(fill="both", expand=True)
root.mainloop()
