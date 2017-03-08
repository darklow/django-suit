from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render


@staff_member_required
def custom_admin_view(request):
    """
    If you're using multiple admin sites with independent views you'll need to set
    current_app manually and use correct admin.site
    # request.current_app = 'admin'
    """
    context = admin.site.each_context(request)
    context.update({
        'title': 'Custom view',
    })

    template = 'admin/custom_view.html'
    return render(request, template, context)


def home(request):
    return HttpResponse("""<html><head>
    <style>body {font-family: sans-serif; margin: 5rem; text-align: center; line-height: 1.7; font-size: 18px;}</style>
    </head>
    <body>
     Welcome to Django Suit demo app.<br>
     Go to <a href="/admin/">admin</a> to explore all the features.
    </body></html>""")
