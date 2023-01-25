from django.shortcuts import render

from django.http import HttpResponse


def menu(request, slug):
    """Main view function for show menus. prepared slug via list creating."""
    menu = slug.split('_')
    return HttpResponse(render(
        template_name='menu.html', request=request,
        context={'menu': menu}
    ))
