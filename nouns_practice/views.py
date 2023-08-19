import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from nouns_practice.utils import extract_cases, extract_words, get_soup, remove_accent

# Create your views here.

def index(request):
    word = "машина"
    soup = get_soup(word)
    words = extract_words(soup)
    cases = extract_cases(words)
    print(cases)
    context = { 'cases': cases, 'word': word}
    return render(request, "nouns/index.html", context)

def practice(request, word_chosen):
    if not "correct_answer_num" in request.session:
        request.session["correct_answer_num"] = 0

    if request.method == "POST":
        user_answer = request.POST.get("user_answer")
        if remove_accent(request.session.get("answer")) == user_answer:
            request.session["correct_answer_num"] += 1

    word = word_chosen
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

def reset_session(request):
    request.session.flush()
    return redirect("practice")
