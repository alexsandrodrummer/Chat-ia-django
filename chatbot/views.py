import os 
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from langchain_groq import ChatGroq
from markdown import markdown


from chatbot.models import Chat

# Set the GROQ API key from environment variables
os.environ['GROQ_API_KEY'] = settings.GROQ_API_KEY

def ask_ai(message):
    model = ChatGroq(model='llama-3.2-90b-vision-preview')
    messages = [
        (
        'system',
        'Você é um assistente responsavel por tirar duvidas sobre programação python.'
        'Responda em formato markdown.',
        ),
        (
        'human',
        message,

        ),
    ]
    response = model.invoke(messages)
    return markdown(response.content, output_format='html')


def chatbot(request):
    chats = Chat.objects.all()

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_ai(message)
        return JsonResponse({
            'message': message,
            'response': response
        })

    
    return render(request, 'chatbot.html', {'chats': chats})