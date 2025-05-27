from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

from pprint import pprint

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_question = data.get("question", "")
        system_prompt = data.get("system_prompt", None)
        previous_prompt = None
        
        if 'chat_history' not in request.session:
            request.session['chat_history'] = []
        else:
            previous_prompt = request.session['chat_history'][-1]

        request.session['chat_history'].append({'role': 'user', 'content': user_question})
        ai_response = ask_ai(user_question, system_prompt, previous_prompt)
        request.session['chat_history'].append({'role': 'assistant', 'content': ai_response})
        request.session.modified = True

        return JsonResponse({"answer": ai_response, "chat_history": request.session['chat_history']})
    elif request.method == 'GET':
        chat_history = request.session.get('chat_history', [])
        return JsonResponse({"chat_history": chat_history})
    

def ask_ai(question, system_prompt=None, previous_prompt=None):
    url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.IOINTELLIGENCE_API_KEY}",
    }

    instructions = """
    Ти є помічником на українському сайті для продажу авто 'DriveHub'. Твоя мета — допомагати користувачам знайти автомобілі для покупки. 
    Ти маєш бути ввічливим, професійним, давати корисні та стислі відповіді українською мовою до 1-2 дуже коротких стислих речень.
    Якщо користувач запитує про автомобілі, дай стислу інформацію, або дуже короткі стислі поради щодо покупки.
    """

    initial_greeting = """Привіт! 👋 Вітаю на DriveHub :) Чим можу допомогти?"""

    messages = []
    
    messages.append({"role": "system", "content": instructions})
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if previous_prompt:
        messages.append(previous_prompt)
    else:
        messages.append({"role": "assistant", "content": initial_greeting})
    messages.append({"role": "user", "content": question})

    json = {
        "model": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        # "model": "Qwen/Qwen3-235B-A22B-FP8",
        "messages": messages,
        "temperature": 0.7,
        # "max_completion_tokens": 100
    }

    print(messages)

    response = requests.post(url, json=json, headers=headers)
    response_data = response.json()
    # pprint(response_data)

    return response_data['choices'][0]['message']['content']