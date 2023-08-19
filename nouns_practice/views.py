import random
from bs4 import BeautifulSoup
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
import requests

# Create your views here.

def index(request):
    word = "машина"
    soup = get_soup(word)
    words = extract_words(soup)
    cases = extract_cases(words)
    print(cases)
    context = { 'cases': cases, 'word': word}
    return render(request, "nouns/index.html", context)

def practice(request):
    if not "correct_answer_num" in request.session:
        request.session["correct_answer_num"] = 0

    if request.method == "POST":
        user_answer = request.POST.get("user_answer")
        if remove_accent(request.session.get("answer")) == user_answer:
            request.session["correct_answer_num"] += 1

    word = "машина"
    soup = get_soup(word)
    words = extract_words(soup)
    cases = extract_cases(words)
    grammatical_cases = [(x, y) for x in ["sing", "plur"] for y in ["nom", "gen", "dat", "acc", "ins", "pre"]]
    chosen_case = random.choice(grammatical_cases)
    request.session["answer"] = cases[chosen_case[0]][chosen_case[1]]
    context = {
        'word': word, 
        'chosen_case': chosen_case,
        'answer': cases[chosen_case[0]][chosen_case[1]],
        'correct_answer_num': request.session["correct_answer_num"]
    }
    return render(request, "nouns/practice.html", context)

def get_soup(chosen_word):
    URL = f"https://en.wiktionary.org/wiki/{chosen_word}"

    resp = requests.get(URL)

    if resp.status_code == 404:
        raise ValueError("Page not found")

    soup = BeautifulSoup(resp.content, "html.parser")
    return soup

def extract_words(soup):
    russian_title = soup.find("span", attrs={"id": "Russian"})

    if russian_title is None:
        raise ValueError("Russian title not found")

    declension_table = soup.find("span", attrs={"id": "Russian"}).find_next("table")
    if declension_table.attrs["class"][0] == "audiotable":
        declension_table = (
            soup.find("span", attrs={"id": "Russian"})
            .find_next("table")
            .find_next("table")
        )

    tds = declension_table.find_all("td")

    if len(tds) != 12:
        raise ValueError("Not enough cells")

    words = []

    for td in tds:
        words.append(td.find("span").get_text())
    return words

def extract_cases(words):
    cases = {}

    cases["sing"] = {}
    cases["plur"] = {}

    cases["sing"]["nom"] = words[0]
    cases["plur"]["nom"] = words[1]
    cases["sing"]["gen"] = words[2]
    cases["plur"]["gen"] = words[3]
    cases["sing"]["dat"] = words[4]
    cases["plur"]["dat"] = words[5]
    cases["sing"]["acc"] = words[6]
    cases["plur"]["acc"] = words[7]
    cases["sing"]["ins"] = words[8]
    cases["plur"]["ins"] = words[9]
    cases["sing"]["pre"] = words[10]
    cases["plur"]["pre"] = words[11]
    return cases

def remove_accent(word):
    accent_dict = {
        "А": "А́",
        "Е": "Е́",
        "И": "И́",
        "О": "О́",
        "У": "У́",
        "Ы": "Ы́",
        "Э": "Э́",
        "Ю": "Ю́",
        "Я": "Я́",
        "а": "á",
        "а": "а́",
        "е": "é",
        "е": "е́",
        "ё": "ё",
        "и": "и́",
        "и": "и́",
        "о": "ó",
        "о": "о́",
        "у": "у́",
        "у": "у́",
        "ы": "ы́",
        "ы": "ы́",
        "э": "э́",
        "э": "э́",
        "ю": "ю́",
        "ю": "ю́",
        "я": "я́",
        "я": "я́",
    }

    for key, value in accent_dict.items():
        word = word.replace(value, key)

    return word

