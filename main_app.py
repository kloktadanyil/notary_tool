import tkinter as tk
import tkinter.ttk as ttk  # Імпортуємо ttk
from Zapovnenya_documenta import create_zapovnenya_documenta_frame
from vybir_zayavy import create_vybir_zayavy_frame
from zayavy_vid_batkiv_frame import create_zayavy_vid_batkiv_frame
from Zayava_Form_1_batko import *
from Zayava_Form_1_batko import create_country_frame_frame

def hide_all_frames():
    """Hiding all frames."""
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
def setup_styles():
    style = ttk.Style()
    style.configure("TButton", font=("Arial",10))
    style.configure("MainMenu.TButton", font=("Arial", 14))
# --- Main window ---
root = tk.Tk()
root.title("Нотаріус")
root.geometry("1200x1000")
style = ttk.Style()
style.configure("Green.TLabel", foreground="green")
style.configure("Red.TLabel", foreground="red")
setup_styles()
#main_menu
main_menu_frame = ttk.Frame(root)
label_menu = ttk.Label(main_menu_frame, text="Оберіть тему яка вас цікавить: ", font=("Arial", 18))
label_menu.pack(pady=20)
button_Zapovnenya_documenta = ttk.Button(main_menu_frame, text="Заповнення документа",style="MainMenu.TButton",width=60, command=show_Zapovnenya_documenta_frame)
button_Zapovnenya_documenta.pack(pady=40)
#create new Frames
Zapovnenya_documenta_frame = create_zapovnenya_documenta_frame(root, on_back_command=show_main_menu_frame, on_next_command=show_vybir_zayavy_frame)
vybir_zayavy_frame = create_vybir_zayavy_frame(root, on_back_command=show_Zapovnenya_documenta_frame, on_next_command=show_zayavy_vid_batkiv_frame)
zayavy_vid_batkiv_frame = create_zayavy_vid_batkiv_frame(root, on_back_command=show_vybir_zayavy_frame, on_next_command=show_zayava_1_batko_frame)
zayava_1_batko_frame = create_zayava_1_batko_frame(root, on_back_command=show_zayavy_vid_batkiv_frame,on_next_command=show_country_frame)
country_frame = create_country_frame_frame (root, app_data, on_back_command=show_main_menu_frame)
main_menu_frame.pack(fill="both", expand=True)
root.mainloop()
