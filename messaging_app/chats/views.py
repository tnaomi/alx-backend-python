from django.shortcuts import render

def getChats(request):
    return render(request, 'chats/chat_list.html')

def getChat(request, chat_id):
    return render(request, 'chats/chat.html', {'chat_id': chat_id})

