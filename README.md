# Корпус стихов

## Описание корпуса
Корпус состоит из 6787 стихов Серебряного века 125 поэтов.\
Количество токенов: 

Особенность этого корпуса в нестандартном употреблении слов, метафорах, в устаревших словах. Поскольку 

Данные собираются в `scipts/scrape_poems.py`. Результат работы скрипта в `scipts/poems.json` со всеми стихами\

Разделение на предложения реализовано с помощью RuSentTokenizer (DeepPavlov sentence tokenizer).\
Токенизация, лемматизация и определение грамматических значений происходит в `scipts/process.py` с помощью библиотеки Stanza.\
В сравнении на датасете стихов GramEval2020 Stanza показала одни из лучших результатов в морфлологии и токенизации.

