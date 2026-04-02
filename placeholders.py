# Плейсхолдери для основних даних
PIB = '{{ПІБ}}'
PIB_KOGO = '{{ПІБКОГО}}'
DATE_OF_BIRTH = '{{ДАТА_НАРОДЖЕННЯ}}'
REGISTRATION_NUMBER = '{{РЕЄСТРАЦІЙНИЙ_НОМЕР}}'
CITY = '{{МІСТО}}'
STREET = '{{ВУЛИЦЯ}}'
HOUSE = '{{БУДИНОК}}'
APARTMENT = '{{КВАРТИРА}}'
ENDING_1 = '{{ЗАКІНЧЕННЯ_1}}'
ENDING_2 = '{{ЗАКІНЧЕННЯ}}'
ENDING_3 = '{{БАТЬКО}}'
GENDER_ENDING = '{{СИН_ДОНЬКА}}'
AGE_STATUS = '{{СТАТУС_ВІКУ}}'
ENDING_CHILD_1 = '{{ЗАКІНЧЕННЯ_2}}'
ENDING_CHILD_2 = '{{ЗАКІНЧЕННЯ_3}}'
ZAYMENNYK = '{{ЗАЙМЕННИК}}'
ENDING_4 = '{{ЗАКІНЧЕННЯ_4}}'
CHILDREN_DATA = '{{ДАНІ_ДІТЕЙ}}'
CHILDREN_DATA_2 = '{{DATA_CHILDREN_2}}'
MY_CHILD = '{{МОЮ_ДИТИНУ}}'
MY_CHILD_2 = '{{МО_ДИТИНИ}}'
# Плейсхолдери для старого паспорта
OLD_PASSPORT = '{{ПАСПОРТ}}'
ISSUED_BY = '{{ВИДАНИЙ}}'
COMPANIONS_DATA = '{{ДАНІ_СУПРОВОДЖУЮЧИХ}}'
COMPANIONS_ENDING = '{{ЗАКІНЧЕННЯ_ДЛЯ_СУПРОВОДЖУЮЧИХ}}' 
COMPANIONS_ENDING_2 = '{{ЗОБОВ}}' 
# Плейсхолдери для нового паспорта
NEW_PASSPORT_NUMBER = '{{НОМЕР_КАРТКИ}}'
UNZR = '{{УНЗР}}'
ISSUING_BODY = '{{ОРГАН}}'
ISSUE_DATE = '{{ДАТА_ВИДАЧІ}}'
VALID_UNTIL = '{{ДІЙСНИЙ_ДО}}'

# Єдиний плейсхолдер для всього блоку паспорта
PASSPORT_BLOCK = '{{БЛОК_ПАСПОРТА}}'
OLD_PASSPORT_TEXT_TEMPLATE = "паспорт {passport_number}, виданий {issued_by} року,"
NEW_PASSPORT_TEXT_TEMPLATE = "паспорт {passport_number}, Запис № {unzr}, орган, що видав {organ}, дата видачі {data_vidachi}, дійсний до {dijsny_do},"
#Тут passport_number і issued_by — це іменовані плейсхолдери.
#А у файлі main_app.py ми заповнюємо цей шаблон, вказуючи значення для кожного імені:
COUNTRIES = '{{КРАЇНИ}}'

PERIOD_Z = '{{ПЕРІОД_З}}'
PERIOD_PO = '{{ПЕРІОД_ПО}}'

DATE_PROPYSOM = '{{ДАТА_ПРОПИСОМ}}'