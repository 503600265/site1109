
from django.views import generic, View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Labeling
from .forms import LabelingForm
from cloudinary.forms import cl_init_js_callbacks
import pandas as pd
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group

# Create your views here.
@login_required
def index(request):
    labeling_list = Labeling.objects.filter(user=request.user).all()
    context = {
        'labeling_list': labeling_list
    }
    return render(request, 'labels/index.html', context)
@login_required
def detail(request, labeling_id):
    labeling = get_object_or_404(Labeling, pk=labeling_id)
    return render(request, 'labels/detail.html', {'labeling': labeling})
@login_required
def about(request):
    return render(request, 'labels/about.html')
@login_required
def NameView(request):
        labeling_list = Labeling.objects.filter(user=request.user).all().extra(select={'name_lower': 'LOWER(name)'}).order_by('name_lower')
        context = {
            'labeling_list': labeling_list
        }
        return render(request, 'labels/index.html', context)

# class NameView(ListView):
#     template_name = 'labels/index.html'
#     def get_queryset(self):
#         """
#         sorts by name
#         """
#         return Labeling.objects.filter(user=request.user).all().extra(select={'name_lower': 'LOWER(name)'}).order_by('name_lower')
@login_required
def NameViewZ_A(request):
        labeling_list = Labeling.objects.filter(user=request.user).all().extra(select={'name_lower': 'LOWER(name)'}).order_by('-name_lower')
        context = {
            'labeling_list': labeling_list
        }
        return render(request, 'labels/index.html', context)

# class NameViewZ_A(ListView):
#     template_name = 'labels/index.html'
#     name_lower = Labeling.objects.name.lower()
#
#     def get_queryset(self):
#         """
#         sorts by name
#         """
#         return Labeling.objects.filter(user=request.user).all().extra(select={'name_lower': 'LOWER(name)'}).order_by('-name_lower')
@login_required
def PublishView(request):
        labeling_list = Labeling.objects.filter(user=request.user).all().order_by('publishDate')
        context = {
            'labeling_list': labeling_list
        }
        return render(request, 'labels/index.html', context)
#
# class PublishView(ListView):
#     template_name = 'labels/index.html'
#
#     def get_queryset(self):
#         """
#         sorts by price (low to high)
#         """
#         return Labeling.objects.filter(user=request.user).all().order_by('publishDate')
@login_required
def PublishViewMostRecent(request):
        labeling_list = Labeling.objects.filter(user=request.user).all().order_by('-publishDate')
        context = {
            'labeling_list': labeling_list
        }
        return render(request, 'labels/index.html', context)
# class PublishViewMostRecent(ListView):
#     template_name = 'labels/index.html'
#
#     def get_queryset(self):
#         """
#         sorts by price high to low
#         """
#         return Labeling.objects.filter(user=request.user).all().order_by('-publishDate')
@login_required
def upload(request):
    context = dict( backend_form = LabelingForm())
    if request.method == 'POST':
        form = LabelingForm(request.POST, request.FILES)
        context['posted'] = form.instance
        if form.is_valid():
            obj= form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('/labels')

        if not form.is_valid():
            return render(request=request, template_name="labels/failedsubmit.html")
    return render(request, 'labels/labelingsubmit.html', context)
# @login_required
# def update(request, id):
#     # dictionary for initial data with
#     # field names as keys
#     context ={}
#
#     # fetch the object related to passed id
#     obj = get_object_or_404(Labeling, id = id)
#
#     # pass the object as instance in form
#     form = LabelingForm(request.POST or None, instance = obj)
#
#     # save the data from the form and
#     # redirect to detail_view
#     if form.is_valid():
#         form.save()
#         return HttpResponseRedirect("/",id=Labeling.id)
#
#     # add form dictionary to context
#     context["form"] = form
#
#     return render(request, "labels/update.html", context)
@login_required
def edit(request, id):
    labeling = get_object_or_404(Labeling, id=id)
    context = dict( backend_form = LabelingForm())
    if request.method == 'POST':
        form = LabelingForm(request.POST, request.FILES, instance=labeling)
        if form.is_valid():
            labeling.publishDate=timezone.datetime.now()
            labeling.save()
            return redirect('/labels')
    return render(request, 'labels/edit.html', context)
@login_required
def delete(request, id):
    # dictionary for initial data with
    # field names as keys
    context = dict( backend_form = LabelingForm())
    obj = get_object_or_404(Labeling, id = id)


    # fetch the object related to passed id



    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return redirect('/labels')
    return render(request, "labels/index.html", context)
