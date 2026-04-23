# Contributing Guide

Thank you for your interest in the **Notary Document Generator** project! We welcome any help: from fixing bugs to adding new templates and features.

This document describes exactly how you can extend the functionality of the program without breaking its architecture.

## How to add a new field to a document

The program architecture is built in such a way that the document generation function (`replace_placeholder_in_document`) is universal. It automatically processes all the data passed to it in the dictionary.

To add a new replaceable field to an existing document, you **don't** need to change the logic of working with `.docx` files. Just follow 4 simple steps:

### Step 1. Add a label to the Word template
Open the `Templates.docx` file and insert the new placeholder in the desired place. Use double curly braces in uppercase, for example: `{{NEW_FIELD}}`.

### Step 2. Register the variable in the code
Open the file `placeholders.py` and add a constant to avoid typos when used in other files:
```python
NEW_FIELD = '{{NEW_FIELD}}'
```
### Step 3. Create the input field (GUI)
In the file of the desired screen (for example, `Zayava_Form_1_batko.py`), create widgets for data entry using tkinter.ttk:
```python
label_new = ttk.Label(document_form_frame, text="New field name:")
entry_new = ttk.Entry(document_form_frame, width=50)

# Tip: Don't forget to add the new field to the validation dictionaries
# (entries_to_validate, validators_map) if it needs validation!
```
### Step 4. Pass data to generator
Find the function that handles the generation button (for example, `on_button_click())`. Read the text from your new field and save it to the main dictionary `app_data`
```python
# Read data from the interface
new_value = entry_new.get()
# Write to the dictionary under the key of our placeholder
app_data["user_data"][NEW_FIELD] = new_value
```
## How to make a Pull Request
If you want to propose your changes to the main repository, please follow this process:

1. Fork this repository.

2. Create a new branch for your feature `(git checkout -b feature/AmazingFeature)`.

3. Commit your changes `(git commit -m 'feat: Add new amazing feature')`. Be sure to write clear commit messages in English.

4. Push your changes to your fork `(git push origin feature/AmazingFeature)`.

5. Open a Pull Request.

Before creating a PR, make sure your code is free of commented garbage (dead code) and follows the general writing style (PEP 8).