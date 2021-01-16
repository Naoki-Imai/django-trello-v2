from django.shortcuts import render,redirect, resolve_url, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import DetailView, UpdateView, CreateView, ListView, DeleteView

from .forms import UserForm, ListForm, CardForm, CardCreateFromHomeForm
from .models import List, Card
from .mixins import OnlyYouMixin


# Create your views here.
def index(request):
  return render(request, "trello_app/index.html")

#ログインしたらhomeへリダイレクトする
class HomeView(LoginRequiredMixin, ListView):
  model = List
  template_name = 'trello_app/home.html'

def signup(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user_instance = form.save()
      login(request, user_instance)
      return redirect('trello_app:home')
  else:
    form = UserCreationForm()

  context = {
    "form":form
  }
  return render(request, 'trello_app/signup.html', context)

class UserDetailView(LoginRequiredMixin, DetailView):
  model = User
  template_name = "trello_app/users/detail.html"

class UserUpdateView(OnlyYouMixin,SuccessMessageMixin, UpdateView):
  model = User
  template_name = "trello_app/users/update.html"
  form_class = UserForm
  success_url = reverse_lazy('trello_app:home')
  success_message = 'ユーザー情報を更新しました'

class ListCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
  model = List
  template_name = 'trello_app/lists/create.html'
  form_class = ListForm
  success_url = reverse_lazy('trello_app:home')
  success_message = 'リストを作成しました'
  def form_valid(self,form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class ListListView(LoginRequiredMixin, ListView):
  model = List
  template_name = 'trello_app/lists/list.html'

class ListDetailsView(LoginRequiredMixin, DetailView):
  model = List
  template_name = 'trello_app/lists/detail.html'

class ListUpdateView(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
  model = List
  template_name = "trello_app/lists/update.html"
  form_class = ListForm
  success_url = reverse_lazy('trello_app:home')
  success_message = 'リストを更新しました'

class ListDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
  model = List
  template_name = 'trello_app/lists/delete.html'
  form_class = ListForm
  success_url = reverse_lazy('trello_app:home')
  success_message = 'リストを削除しました'

class CardCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
  model = Card
  template_name = 'trello_app/cards/create.html'
  form_class = CardForm
  success_url = reverse_lazy('trello_app:home')
  success_message = 'カードを作成しました'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class CardListView(LoginRequiredMixin, ListView):
  model = Card
  template_name = 'trello_app/cards/list.html'
  

class CardDetailView(LoginRequiredMixin, DetailView):
  model = Card
  template_name = 'trello_app/cards/detail.html'

class CardUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
  model = Card
  template_name = "trello_app/cards/update.html"
  form_class = CardForm
  success_url = reverse_lazy('trello_app:home')
  success_message = 'カードを更新しました'

class CardDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
  model = Card
  template_name = 'trello_app/cards/delete.html'
  form_class = CardForm
  success_url = reverse_lazy('trello_app:home')
  success_message = 'カードを削除しました'

class CardCreateFromHomeView(LoginRequiredMixin, SuccessMessageMixin , CreateView):
  model = Card
  template_name = 'trello_app/cards/create.html'
  form_class = CardCreateFromHomeForm
  success_url = reverse_lazy('trello_app:home')
  success_message = 'カードを作成しました'

  def form_valid(self, form):
    list_pk = self.kwargs['list_pk']
    list_instance = get_object_or_404(List, pk=list_pk)
    form.instance.list = list_instance
    form.instance.user = self.request.user
    return super().form_valid(form)