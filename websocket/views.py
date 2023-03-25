from django.shortcuts import render


def chat_box(request, chat_box_name):
    return render(request, "chat/lobby.html", {"chat_box_name": chat_box_name})
