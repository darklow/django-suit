from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def custom_admin_view(request):
    context = admin.site.each_context(request)
    context.update({
        'title': 'Custom view',
    })

    template = 'admin/custom_view.html'
    return render(request, template, context)
