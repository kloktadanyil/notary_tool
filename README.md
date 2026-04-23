# Notary Document Generator

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![python-docx](https://img.shields.io/badge/Library-python--docx-FF7F00?style=flat&logo=pypi&logoColor=white)
![Output](https://img.shields.io/badge/Output-Word_Documents-2B579A?style=flat&logo=microsoft-word&logoColor=white)
![Notary](https://img.shields.io/badge/Notary-Approved-darkgreen?style=flat)

This program for automating the work of a notary. This application with a graphical interface (GUI) allows you to quickly and accurately generate legal documents based on pre-created Word templates (currently supports the generation of "Application for a child to travel abroad").

## Project features

* **Graphical interface:** Step-by-step "wizard" for creating a document, built on the `tkinter` and `ttk` libraries.
* **Dynamic validation:** Built-in validation of input data (regular expressions) for full name, dates (DD.MM.YYYY), UNZR, identification codes (10 digits) and passport types with error highlighting.
* **Document generation:** Preserving the formatting of the original `.docx` template when replacing placeholders (e.g. `{{FULL_NAME}}`, `{{DATE_OF_BIRTH}}`) using the `python-docx` library.
* **Language adaptation (NLP-elements):** Automatic declension of Ukrainian words, correct endings depending on gender (e.g. "son/daughter", "his/her") and conversion of dates and numbers to text (ordinal and genitive cases).
* **Smart Blocks:** The script automatically detects the type of user's passport (old "booklet" or new ID card) and removes unnecessary text blocks from the final document.
* **Dynamic Fields:** Ability to add an unlimited number of children and accompanying persons to the application with automatic grammar correction (for example, "моєї дитини" / "моїх дітей").

## How the application architecture works

The application is divided into logical modules for easy maintenance and scaling:

1. **GUI and Navigation (`main_app.py`, `vybir_zayavy.py`, etc.):** The main file initializes a 1200x1000 window and controls the display of various screens (`Frame`). The user goes from the main menu to selecting the application type and filling in the data of parents and children.
2. **Validation (`validators.py`):** Contains the `create_validator_with_message` function, which creates validation rules for input fields. If the user enters an incorrect UNZR or letters instead of numbers, the status label instantly turns red and displays an error message.
3. **Data processing and logic (`document_logic.py`, `Zayava_Form_1_batko.py`):** This is where the data from the interface is collected. The system analyzes the gender and automatically substitutes the correct endings in the variable (`ending1`, `ending2`, `zaymennyk`). The `convert_digit_to_text_uk` function also works here, which converts system dates into Ukrainian text.
4. **Working with the template and generation (`document_logic.py`, `placeholders.py`):** The program opens the `Templates.docx` file and looks for special labels (placeholders) written in constants (for example, `{{CITY}}`, `{{APARTMENT}}`). The `replace_placeholder_in_document` function goes through all paragraphs and tables, carefully replacing the labels with the entered data without losing font styles.
5. **Saving the result:** The finished document is automatically saved in the created `Generated documents/Applications/Abroad` directory under the name that corresponds to the applicant's full name (for example, `Ivanov_Ivan_Ivanovich.docx`).

## Development plan (To-Do List)

Currently under development. In the near future:
- [ ] Add an option/button "for tourism purposes" for applications.
- [ ] Set up full scrolling on the first frame in the `Zayava_Form_1_batko.py` file.
- [ ] Implement the ability to insert data via copy-paste (clipboard).
- [ ] Add fields for entering "Region" and "District", since they are currently missing from the form.

## Launch the project locally

1. Clone the repository:
```bash
git clone https://github.com/kloktadanyil/notary_tool.git
```
## How to contribute
Would you like to help with the development of the project or add new fields to the documents? Read our instructions in the file [CONTRIBUTING.md](CONTRIBUTING.md)