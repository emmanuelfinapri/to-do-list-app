from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = context['task'].filter(user=self.request.user)
        context['count'] = context['task'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['task'] = context['task'].filter(title__icontains=search_input)
            context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    # fields = ['title', 'description']
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task')


class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    fields = "__all__"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('task')


class RegisterUser(UserCreationForm):

    def check_user(self):
        pass


class RegisterPage(FormView):
    template_name = 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        print("CHECKING IF FORM IS VALID")
        # Check if the form is valid

        print("FORM", form)

        if form.is_valid():
            user = form.save()
            if user is not None:
                login(self.request, user)
            return super(RegisterPage, self).form_valid(form)
        else:
            print("FORM IS NOT VALID.................")

            response = {
                "form": {
                    "error_messages": "Form is invalid"
                }
            }

        return render(request=self.request, template_name=self.template_name, context=response)


def get(self, *args, **kwargs):
    if self.request.user.is_authenticated:
        return redirect('task')
    return super(RegisterPage, self).get(*args, *kwargs)
#
# def post(self, *args, **kwargs):
#     print("This POST is getting csalled on form submission")
#     # print("ARGS",args)
#     # print("KWARGS",kwargs)
#
#     form = self.get_form()
#
#     print("FORM",form)
#     if form.password1 != form.password2:
#         response = {
#             "form": {
#                 "error_messages": "Form is invalid"
#             }
#         }
#         return render(request=self.request, template_name=self.template_name, context=response)
#
#     return self.form_valid(form)
