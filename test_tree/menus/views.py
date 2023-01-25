from django.shortcuts import render


from django.http import HttpResponse
from .models import Menu, Field



def menu(request, slug):
    """"""
    menu = slug.split('_')
    #if '_' not in slug:
        #menu = Menu.objects.get(slug=slug)
    #else:
        #splited_slug = slug.split('_')
        #
    return HttpResponse(render(
        template_name='menu.html',
        request=request,
        context={'menu': menu}
        ))
