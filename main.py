import sys

import requests
from bs4 import BeautifulSoup

languages_supported = ["Arabic", "German", "English", "Spanish", "French", "Hebrew", "Japanese", "Dutch", "Polish",
                       "Portuguese", "Romanian", "Russian", "Turkish"]

first_lang = sys.argv[1].capitalize()
if languages_supported.count(first_lang) < 1 and first_lang != "All":
    print(f"Sorry, the program doesn't support {sys.argv[1]}")
    exit()
second_lang = sys.argv[2].capitalize()
if languages_supported.count(second_lang) < 1 and second_lang != "All":
    print(f"Sorry, the program doesn't support {sys.argv[2]}")
    exit()
word = sys.argv[3].lower()

l1 = languages_supported.index(first_lang) + 1
if second_lang != "All":
    l2 = languages_supported.index(second_lang) + 1
else:
    l2 = 0


def translate(lang_1, lang_2, w):
    output = '\n'

    def make_translation(fl, sl):
        nonlocal output
        headers = {'User-Agent': 'Mozilla/5.0'}
        translation = f"{languages_supported[fl - 1].lower()}-{languages_supported[sl - 1].lower()}"
        page = requests.get(f'https://context.reverso.net/translation/{translation}/{w}', headers=headers)

        if page.status_code == 404:
            print(f"Sorry, unable to find {word}")

        if page.status_code != 200:
            print("Something wrong with your internet connection")
            exit()

        output += f"{languages_supported[sl - 1]} Translations:\n"

        soup = BeautifulSoup(page.content, 'html.parser')
        translation_div = soup.find('section', {'id': 'filters-content'})

        s = str(translation_div)[str(translation_div).find('{'):]
        s = s[:s.find('"')]
        translations = s[1:].split('}')[:len(s[1:].split('}')) - 1]

        for i in range(1, len(translations)):
            translations[i] = translations[i].replace(' -{', '')
        output += translations[0]

        output += '\n\n'
        output += f"{languages_supported[sl - 1]} Examples:\n"

        sentence_div = soup.find('section', id="examples-content").find_all('span', class_="text")
        sentences = []
        for j in sentence_div:
            sentences.append(j.text.strip())

        output += sentences[0]
        output += '\n'
        output += sentences[1]

    if lang_2 > 0:
        make_translation(lang_1, lang_2)
    else:
        for n in range(len(languages_supported) + 1):
            if n != lang_1:
                make_translation(lang_1, n)
                if n < len(languages_supported):
                    output += '\n\n'
    with open(f"{w}.txt", 'w', encoding="utf-8") as file:
        file.write(output)
        file.close()
    print(output)


translate(l1, l2, word)
