import re

def create_validator_with_message(status_label, validator_type):
    """Validatin function for status label."""
    def validate_function(text):
        # empty string
        if text == "":
            status_label.config(text="")
            return True

        # type validation
        if validator_type == "text":
            if re.fullmatch(r"^[а-яА-ЯёЁЇїІіЄєҐґ' -]*$", text):
                status_label.config(text="")
                return True
            else:
                status_label.config(text="Тут можна вводити лише літери!", style="Red.TLabel")
                return False

        elif validator_type == "number and letters":
            if re.fullmatch(r"^[0-9а-яА-ЯёЁЇїІіЄєҐґ/\-\s.,]*$", text):
                status_label.config(text="")
                return True
            else:
                status_label.config(text="Тут можна вводити і цифри і букви!", style="Red.TLabel")
                return False
        
        elif validator_type == "number":
            if re.fullmatch(r"^\d*$", text):
                status_label.config(text="")
                return True
            else:
                status_label.config(text="Тут можна вводити лише цифри!", style="Red.TLabel")
                return False

        elif validator_type == "pib_format":
            if re.fullmatch(r"^(?:[А-ЯЁЇІЄҐ][а-яёїієґ'-]*)(?: [А-ЯЁЇІЄҐ][а-яёїієґ'-]*){1,2}$", text):
                status_label.config(text="")
                return True
            else:
                status_label.config(text="Неправильна форма ПІБ!", style="Red.TLabel")
                return False

        elif validator_type == "idn":
            if re.fullmatch(r"^\d{10}$", text):
                status_label.config(text="")
                return True
            else:
                status_label.config(text="ІДН має складатися з 10 цифр!", style="Red.TLabel")
                return False

        elif validator_type == "unzr":
            if re.fullmatch(r"^\d{8}-\d{5}$", text):
                status_label.config(text="")
                return True
            else:
                status_label.config(text="Невірний формат УНЗР! Приклад: 12345678-12345", style="Red.TLabel")
                return False

        elif validator_type == "date":
            if re.fullmatch(r"^\d{2}\.\d{2}\.\d{4}$", text):
                status_label.config(text="")
                return True
            else:
                status_label.config(text="Невірний формат дати (ДД.ММ.РРРР)!", style="Red.TLabel")
                return False

        elif validator_type == "organ":
            if re.fullmatch(r"^\d{4}$", text):
                status_label.config(text="")
                return True
            else:
                status_label.config(text="Орган, що видав - 4 цифри!", style="Red.TLabel")
                return False
                
        return True
    return validate_function