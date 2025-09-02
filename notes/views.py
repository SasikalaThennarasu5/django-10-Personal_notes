from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Note

class OwnerQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        qs = Note.objects.all()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(owner=self.request.user)

class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_superuser or obj.owner == self.request.user

class NoteListView(OwnerQuerysetMixin, ListView):
    model = Note

class NoteDetailView(OwnerQuerysetMixin, OwnerRequiredMixin, DetailView):
    model = Note

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ["title", "content"]
    success_url = reverse_lazy("notes:list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class NoteUpdateView(OwnerQuerysetMixin, OwnerRequiredMixin, UpdateView):
    model = Note
    fields = ["title", "content"]
    success_url = reverse_lazy("notes:list")

class NoteDeleteView(OwnerQuerysetMixin, OwnerRequiredMixin, DeleteView):
    model = Note
    success_url = reverse_lazy("notes:list")

class AdminAllNotesView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Note
    def test_func(self):
        return self.request.user.is_superuser
