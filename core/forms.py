from django import forms
from .models import Review, Order, Master, Service

RATING_CHOICES = [
    (1, '1 — Очень плохо'),
    (2, '2 — Плохо'),
    (3, '3 — Нормально'),
    (4, '4 — Хорошо'),
    (5, '5 — Отлично'),
]

class ReviewForm(forms.ModelForm):
    master = forms.ModelChoiceField(queryset=Master.objects.all(), label='Мастер')
    rating = forms.ChoiceField(choices=RATING_CHOICES, label='Оценка')

    class Meta:
        model = Review
        fields = ['master', 'rating', 'client_name', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class OrderForm(forms.ModelForm):
    master = forms.ModelChoiceField(queryset=Master.objects.filter(is_active=True), label='Мастер')
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.none(), label='Услуги', widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Order
        fields = ['master', 'services', 'client_name', 'phone', 'comment', 'appointment_date']
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'master' in self.data:
            try:
                master_id = int(self.data.get('master'))
                master = Master.objects.get(pk=master_id)
                self.fields['services'].queryset = master.services.all()
            except (ValueError, Master.DoesNotExist):
                self.fields['services'].queryset = Service.objects.none()
        elif self.instance.pk and self.instance.master:
            self.fields['services'].queryset = self.instance.master.services.all()
        else:
            self.fields['services'].queryset = Service.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        master = cleaned_data.get('master')
        services = cleaned_data.get('services')
        if master and services:
            allowed_services = set(master.services.values_list('pk', flat=True))
            selected_services = set(s.pk for s in services)
            if not selected_services.issubset(allowed_services):
                raise forms.ValidationError(f"Мастер {master.name} не предоставляет выбранные услуги")
        return cleaned_data
