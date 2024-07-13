# logic.py

import requests
from collections import defaultdict
from translate import Translator


qwestions = {'как тебя зовут': "Я супер-крутой-бот и мое предназначение помогать тебе!",
             "сколько тебе лет": "Это слишком философский вопрос"}

class TextAnalysis():   
    memory = defaultdict(list)

    def __init__(self, text, owner):
        self.text = text
        self.translation = self.__translate(self.text, "ru", "en")
        TextAnalysis.memory[owner].append(self)

        # Задание №6
        if self.text.lower() in qwestions.keys():
            self.response = qwestions[self.text.lower()]
        else:
            self.response = self.get_answer()

    
    def get_answer(self):
        res = self.__translate(self.__deep_pavlov_answer(), "en", "ru")
        return res

    def __translate(self, text, from_lang, to_lang):
        try:
            
            translator = Translator(from_lang=from_lang, to_lang=to_lang)
            translation = translator.translate(text)
            return translation
        except:
            return "Перевод не удался"

    def __deep_pavlov_answer(self):
        try:
            API_URL = "https://7038.deeppavlov.ai/model"
            data = {"question_raw": [ self.translation ]}
            res = requests.post(API_URL, json=data).json()
            res = res[0][0]
        except:
            res = "I don't know how to help"
        return res 