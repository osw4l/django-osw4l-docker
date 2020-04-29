__author__ = 'osw4l'


from django.shortcuts import render


def error400(request):
    return render(request, '400.html', status=400)


def error403(request):
    return render(request, '403.html', status=403)


def error404(request):
    return render(request, '404.html', status=404)


def error500(request):
    return render(request, '500.html', status=500)
