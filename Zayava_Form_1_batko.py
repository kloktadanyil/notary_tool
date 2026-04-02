import tkinter as tk  # tk все ще потрібен для Toplevel, StringVar, etc.
import tkinter.ttk as ttk  # Імпортуємо ttk як ttk
from document_logic import *
from placeholders import *
from validators import create_validator_with_message
from datetime import date
app_data = {
    "selected_countries": [],
    "user_data": {}
}

# --- Функції для створення фреймів ---

def create_country_frame_frame(parent_window, app_data, on_back_command): 
    country_frame = ttk.Frame(parent_window)
    max_columns = 5
    
    # ----------------------------------------------------
    # БЛОК 1: НАЛАШТУВАННЯ ПРОКРУТКИ ТА ВИЗНАЧЕННЯ ФУНКЦІЙ
    # ----------------------------------------------------
    
    # 1. Створюємо Scrollbar, Canvas та inner_frame
    scrollbar = ttk.Scrollbar(country_frame, orient="vertical")
    canvas = tk.Canvas(country_frame, yscrollcommand=scrollbar.set)
    
    # Використовуємо grid для country_frame, щоб canvas і scrollbar займали ВЕСЬ доступний простір
    canvas.grid(row=0, column=0, columnspan=max_columns, sticky="nsew")
    scrollbar.grid(row=0, column=max_columns, sticky="ns")
    
    # Фрейм, що містить весь прокручуваний контент
    inner_frame = ttk.Frame(canvas)
    
    # Встановлюємо, що canvas і country_frame можуть розширюватися
    country_frame.grid_rowconfigure(0, weight=1)
    for i in range(max_columns + 1): # +1 для scrollbar
        country_frame.grid_columnconfigure(i, weight=1 if i < max_columns else 0)
    
    # inner_frame повинен мати ту ж конфігурацію стовпців
    for i in range(max_columns):
        inner_frame.columnconfigure(i, weight=1)
        
    window_item_id = canvas.create_window((0, 0), window=inner_frame, anchor='nw')
    scrollbar.config(command=canvas.yview)

    # Функція, яка оновлює scrollregion, коли inner_frame змінює розмір
    def on_frame_configure(event):
        """Оновлює прокручувану область при зміні розміру inner_frame."""
        canvas.config(scrollregion=canvas.bbox("all"))

    # Функція, яка змушує inner_frame розтягуватися по ширині canvas
    def on_canvas_resize(event):
        """Оновлює ширину inner_frame, щоб вона відповідала ширині canvas."""
        canvas.itemconfigure(window_item_id, width=event.width)
     # --- ЗМІННІ ДЛЯ КОНТРОЛЮ ШВИДКОСТІ СКРОЛІНГУ ---
    # Кількість одиниць скролінгу за один клік коліщатка (Windows/macOS)
    # ЗНАЧЕННЯ ПОВИННО БУТИ ЦІЛИМ ЧИСЛОМ (1 для найповільнішого)
    SCROLL_UNITS_DELTA = 1 
    # Кількість одиниць скролінгу для подій <Button-4>/<Button-5> (Linux/X11)
    SCROLL_UNITS_BUTTON = 5 
    # Функція обробки прокрутки колесом миші
    def _on_mousewheel(event):
        """Обробник прокрутки колесом миші з надійною крос-платформною логікою."""
        
        # 1. Linux/X11 <Button-4> (Scroll Up)
        if event.num == 4:
            canvas.yview_scroll(-SCROLL_UNITS_BUTTON, "units")
        # 2. Linux/X11 <Button-5> (Scroll Down)
        elif event.num == 5:
            canvas.yview_scroll(SCROLL_UNITS_BUTTON, "units")
        # 3. Windows/macOS <MouseWheel> (використовує 'delta')
        elif hasattr(event, 'delta'):
            # event.delta / 120 дає +/- 1 (напрямок скролінгу).
            # Множимо на SCROLL_UNITS_DELTA для встановлення бажаної швидкості.
            # На відміну від *0.5, тут результат гарантовано буде цілим числом або 0.
            scroll_direction = int(-1 * (event.delta / 120))
            scroll_amount = scroll_direction * SCROLL_UNITS_DELTA
            canvas.yview_scroll(scroll_amount, "units")
            
    # Прив'язуємо функції до подій
    inner_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_canvas_resize)
    
    # **********************************************
    # КРИТИЧНИЙ РЯДОК: ПРИВ'ЯЗКА ДО ВСЬОГО ВІКНА
    # **********************************************
    parent_window.bind_all("<MouseWheel>", _on_mousewheel) 
    parent_window.bind_all("<Button-4>", _on_mousewheel) 
    parent_window.bind_all("<Button-5>", _on_mousewheel)
    
    # ----------------------------------------------------
    # КІНЕЦЬ БЛОКУ 1: ФУНКЦІЇ ТА НАЛАШТУВАННЯ СКРОЛІНГУ
    # ----------------------------------------------------
    
    
    # 1. Ініціалізація кнопок ОК/Назад та якірної мітки
    ok_button = ttk.Button(inner_frame, text="ОК")
    back_button = ttk.Button(inner_frame, text="< Назад", command=on_back_command)
    anchor_widget = ttk.Label(inner_frame, text="")
    # ... (весь подальший код функції залишається без змін)
    
    # --- Створюємо status_label для загальних повідомлень ---
    status_label = ttk.Label(inner_frame, text="")
    
    # Списки для динамічних полів
    country_frame.children_entries = []
    country_frame.companion_entries = []
    
    # --- Створюємо окремі status_label та валідатори (без змін) ---
    status_label_period_z = ttk.Label(inner_frame, text="", style="Red.TLabel")
    status_label_period_po = ttk.Label(inner_frame, text="", style="Red.TLabel")
    status_label_countries = ttk.Label(inner_frame, text="", style="Red.TLabel")

    # Припускаємо, що create_validator_with_message визначено поза цією функцією
    vcmd_date_z = parent_window.register(create_validator_with_message(status_label_period_z, "date"))
    vcmd_date_po = parent_window.register(create_validator_with_message(status_label_period_po, "date"))
    
    # --- Розміщення чекбоксів ---
    label = ttk.Label(inner_frame, text="Оберіть країни:", font=("Arial", 12), justify='center')
    label.grid(row=0, column=0, columnspan=max_columns, padx=0, pady=5)
    
    options = ["Республіки Польща", "Словацької Республіки", "Угорщини", "Румунії", "Республіки Молдова", "Австрійської Республіки", "Королівства Бельгія", "Республіки Болгарія", "Грецької Республіки", "Королівства Данія", "Естонської Республіки", "Республіки Ісландія", "Королівства Іспанія", "Італійської Республіки", "Республіки Кіпр", "Латвійської Республіки", "Князівства Ліхтенштейн", "Литовської Республіки", "Великого Герцогства Люксембург", "Республіки Мальти", "Королівства Нідерланди", "Федеративної Республіки Німеччина", "Королівство Норвегії", "Португальської Республіки", "Фінляндської Республіки", "Французької Республіки", "Республіки Хорватії", "Чеської Республіки", "Швейцарської Конфедерації", "Королівства Швеція"]
    checkbox_vars = {option: tk.BooleanVar(value=False) for option in options}
    
    current_row = 1 
    current_column = 0
    for option in options:
        checkbox = ttk.Checkbutton(
            inner_frame, 
            text=option, 
            variable=checkbox_vars[option],
            onvalue=True,
            offvalue=False
        )
        checkbox.grid(row=current_row, column=current_column, padx=5, pady=5, sticky='w')
        current_column += 1 
        if current_column >= max_columns:
            current_column = 0
            current_row += 1
            
    status_label_countries.grid(row=current_row + 1, column=0, columnspan=max_columns, padx=0, pady=5)
    
    # Визначаємо рядок, з якого почнеться динамічний контент
    dynamic_start_row = current_row + 2 

    # --- Функція для переміщення якоря та кнопок в самий низ ---
    def relocate_buttons(last_added_row):
        """Переміщує якірний віджет та кнопки ОК/Назад на нові позиції в кінці контенту."""
        # Переміщуємо якір на один рядок нижче від останнього доданого елемента
        anchor_widget.grid(row=last_added_row + 1, column=0, columnspan=max_columns, sticky='ew')
        # Розміщуємо кнопки ОК/Назад після якоря
        ok_button.grid(row=last_added_row + 2, column=0, columnspan=max_columns, pady=10)
        back_button.grid(row=last_added_row + 3, column=0, columnspan=max_columns, pady=10)
        status_label.grid(row=last_added_row + 4, column=0, columnspan=max_columns, pady=10)
        # Обов'язкове оновлення прокручуваної області
        inner_frame.event_generate('<Configure>')


    # --- Новий блок: функція для динамічного додавання дітей ---
    def add_child_fields():
        child_number = len(country_frame.children_entries) + 1
        child_frame = ttk.LabelFrame(inner_frame, text=f"Дані дитини #{child_number}")
        
        current_anchor_row = anchor_widget.grid_info()['row']
        child_frame.grid(row=current_anchor_row, column=0, columnspan=max_columns, padx=10, pady=10, sticky='ew')
        
        # -----------------------------------------------------
        # 1. СТВОРЕННЯ ПОЛІВ 
        # ...
        label_pib = ttk.Label(child_frame, text="ПІБ дитини:")
        entry_pib = ttk.Entry(child_frame, width=50)
        label_dob = ttk.Label(child_frame, text="Дата народження:")
        entry_dob = ttk.Entry(child_frame, width=50)
        label_gender = ttk.Label(child_frame, text="Стать дитини:")
        gender_var = tk.StringVar(value="хлопець")
        radio_boy = ttk.Radiobutton(child_frame, text="Хлопець", variable=gender_var, value="хлопець")
        radio_girl = ttk.Radiobutton(child_frame, text="Дівчина", variable=gender_var, value="дівчина")

        # Лейбли для валідації
        status_label_pib = ttk.Label(child_frame, text="", style="Red.TLabel")
        status_label_dob = ttk.Label(child_frame, text="", style="Red.TLabel")

        # Валідатори
        # Валідатори мають бути створені з новими status_label для уникнення перетину
        vcmd_pib = parent_window.register(lambda p: create_validator_with_message(status_label_pib, "pib_format")(p))
        vcmd_dob = parent_window.register(lambda p: create_validator_with_message(status_label_dob, "date")(p))

        # Конфігуруємо валідацію для полів
        entry_pib.config(validate="focusout", validatecommand=(vcmd_pib, '%P'))
        entry_dob.config(validate="focusout", validatecommand=(vcmd_dob, '%P'))

        # 2. РОЗМІЩЕННЯ ПОЛІВ У ФРЕЙМІ 
        label_pib.grid(row=0, column=0, columnspan=5, padx=5, pady=2)
        entry_pib.grid(row=1, column=0, columnspan=5, padx=5, pady=2)
        status_label_pib.grid(row=2, column=0, columnspan=5, padx=5, pady=2, sticky="ew")
        label_dob.grid(row=3, column=0, columnspan=5, padx=5, pady=2)
        entry_dob.grid(row=4, column=0, columnspan=5, padx=5, pady=2)
        status_label_dob.grid(row=5, column=0, columnspan=5, padx=5, pady=2, sticky="ew")
        label_gender.grid(row=6, column=2, padx=5, pady=2)
        radio_boy.grid(row=7, column=2, padx=5, pady=2)
        radio_girl.grid(row=8, column=2, padx=5, pady=2)
        
        # -----------------------------------------------------

        # 3. Переміщення якоря та кнопок
        relocate_buttons(child_frame.grid_info()['row'])
        
        # 4. Зберігаємо посилання
        new_child = {
            'pib_entry': entry_pib,
            'dob_entry': entry_dob,
            'gender_var': gender_var,
            'pib_status_label': status_label_pib,
            'dob_status_label': status_label_dob
        }
        country_frame.children_entries.append(new_child)


    # --- Функція для динамічного додавання супроводжуючих ---
    def add_companion_fields():
        companion_number = len(country_frame.companion_entries) + 1
        companion_frame = ttk.LabelFrame(inner_frame, text=f"Дані супроводжуючого #{companion_number}")
        
        # 3. Використовуємо якір:
        current_anchor_row = anchor_widget.grid_info()['row']
        companion_frame.grid(row=current_anchor_row, column=0, columnspan=max_columns, padx=10, pady=10, sticky='ew')
        
        # Поля для вводу (ПІБ та Дата народження)
        label_pib = ttk.Label(companion_frame, text="ПІБ супроводжуючого:")
        entry_pib = ttk.Entry(companion_frame, width=50)
        label_dob = ttk.Label(companion_frame, text="Дата Народження:")
        entry_dob = ttk.Entry(companion_frame, width=50)
        label_gender = ttk.Label(companion_frame, text="Стать супроводжуючого:")
        gender_var_suprov = tk.StringVar(value="Чоловік")
        radio_suprov_boy = ttk.Radiobutton(companion_frame, text="Чоловік", variable=gender_var_suprov, value="Чоловік")
        radio_suprov_girk = ttk.Radiobutton(companion_frame, text="Дівчина", variable=gender_var_suprov, value="дівчина")
        # Лейбли для валідації
        status_label_pib = ttk.Label(companion_frame, text="", style="Red.TLabel")
        status_label_dob = ttk.Label(companion_frame, text="", style="Red.TLabel")

        # Валідатори 
        # Валідатори мають бути створені з новими status_label для уникнення перетину
        vcmd_pib = parent_window.register(create_validator_with_message(status_label_pib, "pib_format"))
        vcmd_dob = parent_window.register(create_validator_with_message(status_label_dob, "date"))

        # Конфігуруємо валідацію
        entry_pib.config(validate="focusout", validatecommand=(vcmd_pib, '%P'))
        entry_dob.config(validate="focusout", validatecommand=(vcmd_dob, '%P'))

        # Розміщуємо віджети у фреймі
        label_pib.grid(row=0, column=0, padx=5, pady=2, sticky='w')
        entry_pib.grid(row=0, column=1, padx=5, pady=2, sticky='w')
        status_label_pib.grid(row=1, column=0, columnspan=2, padx=5, pady=2, sticky="ew")
        label_dob.grid(row=2, column=0, padx=5, pady=2, sticky='w')
        entry_dob.grid(row=2, column=1, padx=5, pady=2, sticky='w')
        status_label_dob.grid(row=3, column=0, columnspan=2, padx=5, pady=2, sticky="ew")
        label_gender.grid(row=6, column=2, padx=5, pady=2)
        radio_suprov_boy.grid(row=7, column=2, padx=5, pady=2)
        radio_suprov_girk.grid(row=8, column=2, padx=5, pady=2)
        # Зберігаємо посилання 
        new_companion = {
            'pib_entry': entry_pib,
            'dob_entry': entry_dob,
            'gender_var_suprov': gender_var_suprov,
            'pib_status_label': status_label_pib,
            'dob_status_label': status_label_dob
        }
        country_frame.companion_entries.append(new_companion)
        
        # Переміщення якоря та кнопок
        relocate_buttons(companion_frame.grid_info()['row'])
        
        
    # --- Статичні елементи ---
    
    # 4. Розміщення кнопок додавання
    button_add_child = ttk.Button(inner_frame, text="Додати ще одну дитину", command=add_child_fields)
    button_add_child.grid(row=dynamic_start_row, column=0, columnspan=max_columns, padx=0, pady=5)
    
    button_add_companion = ttk.Button(inner_frame, text="Додати ще одного супроводжуючого", command=add_companion_fields)
    button_add_companion.grid(row=dynamic_start_row + 1, column=0, columnspan=max_columns, padx=0, pady=5)
    
    # 5. Розміщення полів періоду
    period_row = dynamic_start_row + 2
    label_period_z = ttk.Label(inner_frame, text="Період з")
    label_period_z.grid(row=period_row, column=0, padx=0, pady=5)
    entry_period_z = ttk.Entry(inner_frame, width=10, validate="focusout", validatecommand=(vcmd_date_z, '%P'))
    entry_period_z.grid(row=period_row, column=1, padx=0, pady=5)
    status_label_period_z.grid(row=period_row, column=2, padx=0, pady=5, sticky="nswe")
    
    label_period_po = ttk.Label(inner_frame, text="Період по")
    label_period_po.grid(row=period_row, column=3, padx=0, pady=5)
    entry_period_po = ttk.Entry(inner_frame, width=10, validate="focusout", validatecommand=(vcmd_date_po, '%P'))
    entry_period_po.grid(row=period_row, column=4, padx=0, pady=5)
    status_label_period_po.grid(row=period_row, column=5, padx=0, pady=5, sticky="nswe")

    # 6. Початкове розміщення якоря та кнопок
    relocate_buttons(period_row)

    # ----------------------------------------------------
    ## 7. Функції Валідації та Збору Даних (Об'єднаний Код)
    # ----------------------------------------------------
    
    def validate_country_data(checkbox_vars):
        nonlocal status_label # Доступ до status_label
        all_valid = True
        
        # Перевірка, чи обрана хоча б одна країна
        selected_count = sum(1 for var in checkbox_vars.values() if var.get())
        if selected_count == 0:
            status_label_countries.config(text="Оберіть хоча б одну країну!", style="Red.TLabel")
            all_valid = False
        else:
            status_label_countries.config(text="")
        
        # Перевірка, чи додано хоча б одну дитину
        if not country_frame.children_entries:
            status_label.config(text="Додайте хоча б одну дитину!", style="Red.TLabel")
            all_valid = False
        else:
             status_label.config(text="") # Скидаємо, якщо діти є
        
        # Валідація для всіх динамічно доданих полів дітей
        for child_data in country_frame.children_entries:
            pib_val = child_data['pib_entry'].get()
            dob_val = child_data['dob_entry'].get()
            pib_label = child_data['pib_status_label']
            dob_label = child_data['dob_status_label']

            # Перевірка ПІБ
            if not pib_val:
                pib_label.config(text="Це поле обов'язкове!", style="Red.TLabel")
                all_valid = False
            elif not create_validator_with_message(pib_label, 'pib_format')(pib_val):
                all_valid = False
            else:
                pib_label.config(text="")

            # Перевірка Дати Народження
            if not dob_val:
                dob_label.config(text="Це поле обов'язкове!", style="Red.TLabel")
                all_valid = False
            elif not create_validator_with_message(dob_label, 'date')(dob_val):
                all_valid = False
            else:
                dob_label.config(text="")
        
        # !!! ВАЛІДАЦІЯ ДЛЯ СУПРОВОДЖУЮЧИХ !!!
        for comp_data in country_frame.companion_entries:
            pib_suprov_val = comp_data['pib_entry'].get()
            date_suprov_val = comp_data['dob_entry'].get()
            status_label_pib_suprov = comp_data['pib_status_label']
            status_label_date_suprov = comp_data['dob_status_label']
            
            # Логіка "обидва або жодного"
            if (pib_suprov_val and not date_suprov_val) or (not pib_suprov_val and date_suprov_val):
                status_label_pib_suprov.config(text="Заповніть обидва поля або залиште порожніми!", style="Red.TLabel")
                status_label_date_suprov.config(text="Заповніть обидва поля або залиште порожніми!", style="Red.TLabel")
                all_valid = False
            else:
                # Скидаємо статус-мітки, якщо логіка "обидва/жодного" виконана
                status_label_pib_suprov.config(text="")
                status_label_date_suprov.config(text="")
                
                # Додаткова валідація формату, якщо поля заповнені
                if pib_suprov_val:
                    is_valid_pib = create_validator_with_message(status_label_pib_suprov, 'pib_format')(pib_suprov_val)
                    if not is_valid_pib: all_valid = False
                
                if date_suprov_val:
                    is_valid_date = create_validator_with_message(status_label_date_suprov, 'date')(date_suprov_val)
                    if not is_valid_date: all_valid = False

        # ! Валідація полів періоду
        # Перевіряємо, чи викликана валідація на focusout
        period_z_val = entry_period_z.get()
        period_po_val = entry_period_po.get()
        
        if not period_z_val or not period_po_val:
            if not period_z_val: status_label_period_z.config(text="Обов'язкове поле!", style="Red.TLabel")
            if not period_po_val: status_label_period_po.config(text="Обов'язкове поле!", style="Red.TLabel")
            all_valid = False
        else:
            # Якщо поля заповнені, перевіряємо формат ще раз (на випадок, якщо focusout не спрацював)
            if not create_validator_with_message(status_label_period_z, 'date')(period_z_val):
                 all_valid = False
            if not create_validator_with_message(status_label_period_po, 'date')(period_po_val):
                 all_valid = False
                 
            if all_valid: # Якщо обидві дати валідні
                status_label_period_z.config(text="")
                status_label_period_po.config(text="")

        return all_valid
    
    def on_ok_command(selected_vars, app_data):
        if not validate_country_data(selected_vars):
            status_label.config(text="Будь ласка, заповніть всі поля правильно!", style="Red.TLabel")
            return
            
        status_label.config(text="")
        
        # 1. ЗБІР ДАНИХ ПРО ВСІХ ДІТЕЙ
        children_list = []
        for child_data in country_frame.children_entries:
            try:
                pib = child_data['pib_entry'].get()
                dob = child_data['dob_entry'].get()
                gender_var = child_data['gender_var'].get()
                
                # Обчислення віку (припускаємо, що date імпортовано з datetime)
                day, month, year = map(int, dob.split('.'))
                birth_date = date(year, month, day)
                age = date.today().year - birth_date.year - ((date.today().month, date.today().day) < (birth_date.month, birth_date.day))
                
                age_status = "малолітнь" if age < 14 else "неповнолітнь"
                gender_ending = "сина" if gender_var == "хлопець" else "доньки"
                ending_1 = "го" if gender_ending == "сина" else "єї"
                ending_2 = "ого" if gender_ending == "сина" else "ої"
                
                children_list.append({
                    'pib': pib, 'dob': dob, 'age_status': age_status, 'gender_ending': gender_ending, 
                    'ending_1': ending_1, 'ending_2': ending_2
                })
            except:
                child_data['dob_status_label'].config(text="Некоректний формат дати!", style="Red.TLabel")
                return
            
        # 2. ЗБІР ДАНИХ ПРО ВСІХ СУПРОВОДЖУЮЧИХ
        companion_list = []
        for comp_data in country_frame.companion_entries:
            pib = comp_data['pib_entry'].get()
            dob = comp_data['dob_entry'].get()
            gender_var_suprov = comp_data['gender_var_suprov'].get()
            gender_ending_suprov = "який" if gender_var_suprov == "Чоловік" else "яка"       
            if pib and dob:
                companion_list.append({
                    'pib': pib,
                    'dob': dob,
                    'gender_ending_suprov':gender_ending_suprov
                })
        
        # 3. ЗБЕРЕЖЕННЯ В APP_DATA
        # Припускаємо, що константи COUNTRIES, PERIOD_Z, PERIOD_PO, CHILDREN_DATA, COMPANIONS_DATA імпортовано з placeholders.py
        app_data["user_data"]["companions"] = companion_list 
        app_data["user_data"]["children"] = children_list 
        
        selected_countries = [country for country, var in selected_vars.items() if var.get()]
        app_data["user_data"][COUNTRIES] = " та/або до ".join(selected_countries)
        app_data["user_data"][PERIOD_Z] = entry_period_z.get()
        app_data["user_data"][PERIOD_PO] = entry_period_po.get()
        
        # 4. ГЕНЕРАЦІЯ
        if status_label:
            status_label.config(text="Генерація документа...")
        
        # Припускаємо, що generate_document_from_data визначено поза цією функцією
        generate_document_from_data(app_data["user_data"], status_label)

    # Кнопка "ОК" тепер викликає функцію, яка збереже дані та згенерує документ
    ok_button.config(command=lambda: on_ok_command(checkbox_vars, app_data))
    
    # 7. Фінальний return фрейму
    return country_frame

def create_zayava_1_batko_frame(parent_window, on_back_command, on_next_command):
    
    

    document_form_frame = ttk.Frame(parent_window)
    
    # Створюємо status_label для загальних повідомлень
    status_label = ttk.Label(document_form_frame, text="")

    # Створюємо окремі status_label для кожного поля
    status_label_pib = ttk.Label(document_form_frame, text="", style="Red.TLabel")
    status_label_pib_kogo = ttk.Label(document_form_frame, text="", style="Red.TLabel")
    status_label_dob = ttk.Label(document_form_frame, text="", style="Red.TLabel")
    status_label_idn = ttk.Label(document_form_frame, text="", style="Red.TLabel")
    status_label_misto = ttk.Label(document_form_frame, text="", style="Red.TLabel")
    status_label_street = ttk.Label(document_form_frame, text="", style="Red.TLabel")
    status_label_house = ttk.Label(document_form_frame, text="", style="Red.TLabel")
    status_label_appartament = ttk.Label(document_form_frame, text="", style="Red.TLabel")
    status_label_passport = ttk.Label(document_form_frame, text="", style="Red.TLabel")

    # Реєстрація валідаторів, прив'язаних до цього фрейма
    vcmd_pib = parent_window.register(create_validator_with_message(status_label_pib, "pib_format"))
    vcmd__kogo = parent_window.register(create_validator_with_message(status_label_pib_kogo, "pib_format"))
    vcmd_date = parent_window.register(create_validator_with_message(status_label_dob, "date"))
    vcmd_idn = parent_window.register(create_validator_with_message(status_label_idn, "idn"))
    vcmd_text_misto = parent_window.register(create_validator_with_message(status_label_misto, "text"))
    vcmd_text_street = parent_window.register(create_validator_with_message(status_label_street, "number and letters"))
    vcmd_number_house = parent_window.register(create_validator_with_message(status_label_house, "number and letters"))
    vcmd_number_appartament = parent_window.register(create_validator_with_message(status_label_appartament, "number and letters"))
    

    # Створення віджетів Entry
    entry_pib = ttk.Entry(document_form_frame, width=50, validate="focusout", validatecommand=(vcmd_pib, '%P'))
    entry_pib_kogo = ttk.Entry(document_form_frame, width=50, validate="focusout", validatecommand=(vcmd__kogo, '%P'))
    entry_dob = ttk.Entry(document_form_frame, width=50, validate="focusout", validatecommand=(vcmd_date, '%P'))
    entry_nomer = ttk.Entry(document_form_frame, width=50, validate="focusout", validatecommand=(vcmd_idn, '%P'))
    entry_passport_number = ttk.Entry(document_form_frame, width=50)
    entry_misto = ttk.Entry(document_form_frame, width=50, validate="focusout", validatecommand=(vcmd_text_misto, '%P'))
    entry_street = ttk.Entry(document_form_frame, width=50, validate="focusout", validatecommand=(vcmd_text_street, '%P'))
    entry_house = ttk.Entry(document_form_frame, width=50, validate="focusout", validatecommand=(vcmd_number_house, '%P'))
    entry_appartament = ttk.Entry(document_form_frame, width=50, validate="focusout", validatecommand=(vcmd_number_appartament, '%P'))
    
    gender_var = tk.StringVar(value="чоловік")

    # Словники для зручної валідації
    entries_to_validate = {
        'pib': entry_pib,
        'pib_kogo': entry_pib_kogo,
        'dob': entry_dob,
        'idn': entry_nomer,
        'misto': entry_misto,
        'street': entry_street,
        'house': entry_house,
        'appartament': entry_appartament
    }
    
    status_labels_map = {
        'pib': status_label_pib,
        'pib_kogo': status_label_pib_kogo,
        'dob': status_label_dob,
        'idn': status_label_idn,
        'misto': status_label_misto,
        'street': status_label_street,
        'house': status_label_house,
        'appartament': status_label_appartament
    }
    
    validators_map = {
        'pib': 'pib_format',
        'pib_kogo': 'pib_format',
        'dob': 'date',
        'idn': 'idn',
        'misto': 'text',
        'street': "number and letters",
        'house': "number and letters",
        'appartament': "number and letters"
    }

    def open_old_passport_window(passport_number):
        new_window = tk.Toplevel(parent_window)
        new_window.title("Дані старого паспорта")
        new_window.geometry("400x200")
        
        label_wydan = ttk.Label(new_window, text="Ким виданий та дата:")
        label_wydan.pack(pady=5)
        entry_wydan = ttk.Entry(new_window, width=50)
        entry_wydan.pack(pady=5)

        def on_ok():
            issued_by = entry_wydan.get()
            passport_block_text = OLD_PASSPORT_TEXT_TEMPLATE.format(
                passport_number=passport_number,
                issued_by=issued_by
            )
            app_data["user_data"][PASSPORT_BLOCK] = passport_block_text

            
            new_window.destroy()
            on_next_command()

        ok_button = ttk.Button(new_window, text="OK", command=on_ok)
        ok_button.pack(pady=10)

    def open_new_passport_window(passport_number):
        new_window = tk.Toplevel(parent_window)
        new_window.title("Дані нового паспорта")
        new_window.geometry("600x400")
        
        status_label_unzr = ttk.Label(new_window, text="", style="Red.TLabel")
        status_label_organ = ttk.Label(new_window, text="", style="Red.TLabel")
        status_label_data = ttk.Label(new_window, text="", style="Red.TLabel")
        status_label_dijsny = ttk.Label(new_window, text="", style="Red.TLabel")

        vcmd_unzr = parent_window.register(create_validator_with_message(status_label_unzr, "unzr"))
        vcmd_organ = parent_window.register(create_validator_with_message(status_label_organ, "organ"))
        vcmd_date = parent_window.register(create_validator_with_message(status_label_data, "date"))
        vcmd_date_dijsny = parent_window.register(create_validator_with_message(status_label_dijsny, "date"))

        label_unzr = ttk.Label(new_window, text="Запис № (УНЗР):")
        label_unzr.pack(pady=5)
        entry_unzr = ttk.Entry(new_window, width=50, validate="focusout", validatecommand=(vcmd_unzr, '%P'))
        entry_unzr.pack(pady=5)
        status_label_unzr.pack(pady=2)

        label_organ = ttk.Label(new_window, text="Орган, що видав:")
        label_organ.pack(pady=5)
        entry_organ = ttk.Entry(new_window, width=50, validate="focusout", validatecommand=(vcmd_organ, '%P'))
        entry_organ.pack(pady=5)
        status_label_organ.pack(pady=2)
        
        label_data = ttk.Label(new_window, text="Дата видачі:")
        label_data.pack(pady=5)
        entry_data = ttk.Entry(new_window, width=50, validate="focusout", validatecommand=(vcmd_date, '%P'))
        entry_data.pack(pady=5)
        status_label_data.pack(pady=2)
        
        label_dijsny = ttk.Label(new_window, text="Дійсний до:")
        label_dijsny.pack(pady=5)
        entry_dijsny = ttk.Entry(new_window, width=50, validate="focusout", validatecommand=(vcmd_date_dijsny, '%P'))
        entry_dijsny.pack(pady=5)
        status_label_dijsny.pack(pady=2)

        def on_ok():
            unzr = entry_unzr.get()
            organ = entry_organ.get()
            data_vidachi = entry_data.get()
            dijsny_do = entry_dijsny.get()
            
            passport_block_text = NEW_PASSPORT_TEXT_TEMPLATE.format(
                passport_number=passport_number,
                unzr=unzr,
                organ=organ,
                data_vidachi=data_vidachi,
                dijsny_do=dijsny_do
            )
            app_data["user_data"][PASSPORT_BLOCK] = passport_block_text

            new_window.destroy()
            on_next_command()
        
        ok_button = ttk.Button(new_window, text="OK", command=on_ok)
        ok_button.pack(pady=10)

    def validate_all_entries():
        """Перевіряє валідацію всіх полів введення."""
        # Фу нкція використовує цикл for для перевірки більшості полів введення, які зберігаються у словнику entries_to_validate.

        # Отримання даних: У кожній ітерації циклу, код отримує значення (value) поточного поля (entry).

        
        # Вибір валідатора: Потім, використовуючи відповідні словники (status_labels_map і validators_map), він динамічно створює потрібний валідатор за допомогою create_validator_with_message.
        
        # Виконання валідації: Створений валідатор (is_valid = create_validator_with_message(...)) перевіряє значення.

        # Встановлення статусу: Якщо перевірка не пройшла (if not is_valid:), змінна all_valid стає False. Функція продовжує перевіряти інші поля, але вже "знає", що загальний результат буде негативним.
        all_valid = True
        for key, entry in entries_to_validate.items():
            value = entry.get()
            label = status_labels_map[key]
            validator_type = validators_map[key]
            
            is_valid = create_validator_with_message(label, validator_type)(value)
            
            if not is_valid:
                all_valid = False
        
        passport_number = entry_passport_number.get().strip()
        if not ((len(passport_number) == 9 and passport_number.isdigit()) or \
                (len(passport_number) == 8 and passport_number[:2].isalpha() and passport_number[2:].isdigit())):
            status_label_passport.config(text="Формат: 9 цифр або 2 букви + 6 цифр")
            all_valid = False
            
        return all_valid

    def on_button_click():
        """Обробник натискання кнопки "Далі"."""
        if not validate_all_entries():
            status_label.config(text="Будь ласка, заповніть всі поля правильно!", style="Red.TLabel")
            return

        status_label.config(text="")
             
        pib = entry_pib.get()
        pib_kogo = entry_pib_kogo.get()
        date_of_birth = entry_dob.get()
        nomer = entry_nomer.get()
        passport_number = entry_passport_number.get().strip()
        misto = entry_misto.get()
        street = entry_street.get()
        house = entry_house.get()
        appartament = entry_appartament.get()
        
        user_gender_choice = gender_var.get()
        ending1, ending2, ending3 = '', '', ''
        if user_gender_choice == 'чоловік':
            ending1 = 'ин'
            ending2 = 'ий'
            ending3 = 'батько'
            zaymennyk = 'його'
            ending4 = 'в'
        elif user_gender_choice == 'жінка':
            ending1 = 'ка'
            ending2 = 'а'
            ending3 = 'мати'
            zaymennyk = 'її'
            ending4 = 'ла'
            
        app_data["user_data"][PIB] = pib
        app_data["user_data"][PIB_KOGO] = pib_kogo
        app_data["user_data"][DATE_OF_BIRTH] = date_of_birth
        app_data["user_data"][REGISTRATION_NUMBER] = nomer
        app_data["user_data"][CITY] = misto
        app_data["user_data"][STREET] = street
        app_data["user_data"][HOUSE] = house
        app_data["user_data"][APARTMENT] = appartament
        app_data["user_data"][ENDING_1] = ending1
        app_data["user_data"][ENDING_2] = ending2
        app_data["user_data"][ENDING_3] = ending3
        app_data["user_data"][ZAYMENNYK] = zaymennyk
        app_data["user_data"][ENDING_4] = ending4
        # app_data["Bold_formatting"] = {
        # PIB: True,  # Вказуємо, що ПІБ  має бути жирним
        # DATA_OF_BIRTH_DYTYNY: True, 
        
        if len(passport_number) == 9 and passport_number.isdigit():
            open_new_passport_window(passport_number)
        elif len(passport_number) == 8 and passport_number[:2].isalpha() and passport_number[2:].isdigit():
            open_old_passport_window(passport_number)

    # --- Розміщення віджетів у фреймі ---
    button_back = ttk.Button(document_form_frame, text="< Назад", command=on_back_command)
    button_back.pack(anchor="w", padx=10, pady=10)

    label_pib = ttk.Label(document_form_frame, text="ПІБ:")
    label_pib.pack(pady=5)
    entry_pib.pack(pady=5)
    status_label_pib.pack(pady=2)
    
    label_pib_kogo = ttk.Label(document_form_frame, text="ПІБ в родовому відмінку:")
    label_pib_kogo.pack(pady=5)
    entry_pib_kogo.pack(pady=5)
    status_label_pib_kogo.pack(pady=2)

    label_dob = ttk.Label(document_form_frame, text="Дата народження:")
    label_dob.pack(pady=5)
    entry_dob.pack(pady=5)
    status_label_dob.pack(pady=2)

    label_nomer = ttk.Label(document_form_frame, text="ІДН:")
    label_nomer.pack(pady=5)
    entry_nomer.pack(pady=5)
    status_label_idn.pack(pady=2)

    label_misto = ttk.Label(document_form_frame, text="Місто:")
    label_misto.pack(pady=5)
    entry_misto.pack(pady=5)
    status_label_misto.pack(pady=2)

    label_street = ttk.Label(document_form_frame, text="Вулиця чи шось інше:")
    label_street.pack(pady=5)
    entry_street.pack(pady=5)
    status_label_street.pack(pady=2)

    label_house = ttk.Label(document_form_frame, text="Будинок:")
    label_house.pack(pady=5)
    entry_house.pack(pady=5)
    status_label_house.pack(pady=2)

    label_appartament = ttk.Label(document_form_frame, text="Квартира:")
    label_appartament.pack(pady=5)
    entry_appartament.pack(pady=5)
    status_label_appartament.pack(pady=2)

    label_passport_number = ttk.Label(document_form_frame, text="Паспорт:")
    label_passport_number.pack(pady=5)
    entry_passport_number.pack(pady=5)
    status_label_passport.pack(pady=2)

    label_gender = ttk.Label(document_form_frame, text="Стать:")
    label_gender.pack()
    
    radio_male = ttk.Radiobutton(document_form_frame, text="Чоловік", variable=gender_var, value="чоловік")
    radio_male.pack()
    radio_female = ttk.Radiobutton(document_form_frame, text="Жінка", variable=gender_var, value="жінка")
    radio_female.pack()

    generate_button = ttk.Button(document_form_frame, text="Далі", command=on_button_click)
    generate_button.pack(pady=20)
    status_label.pack(pady=5)

    return document_form_frame