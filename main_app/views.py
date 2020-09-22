from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic  import DetailView, ListView

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Sneaker, Shoelace, Photo

from .forms import PurchaseForm

import uuid
import boto3


# Create your views here.


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = "Invalid sign up - try again"
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def sneakers_index(request):
    sneakers = Sneaker.objects.all()
    return render(request, 'sneakers/index.html', {'sneakers': sneakers})

@login_required
def sneakers_detail(request, sneaker_id):
    sneaker = Sneaker.objects.get(id=sneaker_id)      
    shoelace_sneaker_doesnt_have = Shoelace.objects.exclude(id__in = sneaker.shoelaces.all().values_list('id'))
    purchase_form = PurchaseForm()
    return render(request, 'sneakers/detail.html', {
        'sneaker': sneaker,
        'purchase_form': purchase_form,
        'shoelaces': shoelace_sneaker_doesnt_have
        })

@login_required
def add_purchase(request, sneaker_id):
  form = PurchaseForm(request.POST)
  if form.is_valid():
    new_purchase = form.save(commit=False)
    new_purchase.sneaker_id = sneaker_id
    new_purchase.save()
  return redirect('detail', sneaker_id=sneaker_id)

@login_required
def add_photo(request, sneaker_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, sneaker_id=sneaker_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', sneaker_id=sneaker_id)


@login_required
def assoc_toy(request, sneaker_id, shoelace_id):
  Sneaker.objects.get(id=sneaker_id).shoelaces.add(shoelace_id)
  return redirect('detail', sneaker_id=sneaker_id)

@login_required
def unassoc_shoelace(request, sneaker_id, shoelace_id):
  Sneaker.objects.get(id=sneaker_id).shoelaces.remove(shoelace_id)
  return redirect('detail', sneaker_id=sneaker_id)


class SneakerCreate(CreateView):
    model = Sneaker
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SneakerUpdate(UpdateView):
  model = Sneaker
  fields = ['name', 'style', 'category', 'description', 'year']

class SneakerDelete(DeleteView):
  model = Sneaker
  success_url = '/sneakers/'

class ShoelaceCreate(LoginRequiredMixin, CreateView):
  model = Shoelace
  fields = '__all__'

class ShoelaceDetail(LoginRequiredMixin, DeleteView):
  model = Shoelace

class ShoelaceList(LoginRequiredMixin, ListView):
  model = Shoelace

class ShoelaceUpdate(LoginRequiredMixin, UpdateView):
  model = Shoelace
  fields = '__all__'


class ShoelaceDelete(LoginRequiredMixin, DeleteView):
  model = Shoelace
  success_url = '/shoelaces/'