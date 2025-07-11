from datetime import timezone
from django import forms
from .models import Client, Debt, Membership, MembershipType, Payment
from django.core.exceptions import ValidationError

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'phone', 'email', 'birth_date', 'gender', 'photo', 'notes', 'card_id']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_card_id(self):
        card_id = self.cleaned_data['card_id']
        if Client.objects.filter(card_id=card_id).exists():
            raise ValidationError('Клиент с таким номером карты уже существует')
        return card_id
# core/forms.py
# class MembershipForm(forms.ModelForm):
#     discount_amount = forms.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         required=False,
#         initial=0,
#         label="Скидка (сом)"
#     )
    
#     paid_amount = forms.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         required=True,
#         label="Оплаченная сумма",
#         min_value=0
#     )
    
#     payment_method = forms.ChoiceField(
#         choices=Payment.PAYMENT_METHODS,
#         initial='cash',
#         label="Способ оплаты"
#     )
    
#     class Meta:
#         model = Membership
#         fields = ['membership_type', 'start_date', 'discount_amount', 'paid_amount', 'payment_method']
#         widgets = {
#             'start_date': forms.DateInput(attrs={'type': 'date'}),
#         }
class MembershipForm(forms.ModelForm):
    discount_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        initial=0,
        label="Скидка (сом)"
    )
    
    paid_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        label="Оплаченная сумма",
        min_value=0
    )
    
    class Meta:
        model = Membership
        fields = ['membership_type', 'start_date', 'discount_amount', 'paid_amount']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paid_amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['discount_amount'].widget.attrs.update({'class': 'form-control'})
# class MembershipForm(forms.ModelForm):
#     discount_amount = forms.DecimalField(
#         max_digits=10, 
#         decimal_places=2, 
#         required=False, 
#         initial=0,
#         label="Скидка (в сомах)"
#     )
#     paid_amount = forms.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         required=True,
#         label="Оплаченная сумма"
#     )
    
#     class Meta:
#         model = Membership
#         fields = ['membership_type', 'start_date', 'discount_amount', 'paid_amount']
#         widgets = {
#             'start_date': forms.DateInput(attrs={'type': 'date'}),
#         }
# class MembershipForm(forms.ModelForm):
#     discount_amount = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0)
    
#     class Meta:
#         model = Membership
#         fields = ['membership_type', 'start_date', 'discount_amount']
        
#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         instance.discount_amount = self.cleaned_data['discount_amount']
#         if commit:
#             instance.save()
#         return instance
    
    
class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = ['amount', 'description']
# class MembershipForm(forms.ModelForm):
#     class Meta:
#         model = Membership
#         fields = ['membership_type', 'start_date']
#         widgets = {
#             'start_date': forms.DateInput(attrs={'type': 'date'}),
#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Просто убираем фильтр is_active
#         self.fields['membership_type'].queryset = MembershipType.objects.all()
        # self.fields['start_date'].initial = timezone.now().date() 
# class MembershipForm(forms.ModelForm):
#     class Meta:
#         model = Membership
#         fields = ['membership_type', 'start_date']
#         widgets = {
#             'start_date': forms.DateInput(attrs={'type': 'date'}),
#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['membership_type'].queryset = MembershipType.objects.filter(is_active=True)
#         self.fields['start_date'].initial = timezone.now().date()
from django import forms
from .models import CardSale, Client
class CardSaleForm(forms.ModelForm):
    class Meta:
        model = CardSale
        fields = ['card_number', 'price', 'client']
        widgets = {
            'card_number': forms.TextInput(attrs={'placeholder': 'Например: 1234567890'}),
            'price': forms.NumberInput(attrs={'min': 0}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.filter(is_active=True)
        self.fields['client'].required = False
# class CardSaleForm(forms.ModelForm):
#     class Meta:
#         model = CardSale
#         fields = ['client', 'card_number', 'price']
#         widgets = {
#             'client': forms.Select(attrs={'class': 'form-control'}),
#             'card_number': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Введите номер карты'
#             }),
#             'price': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Цена карты',
#                 'min': '0',
#                 'step': '0.01'
#             }),
#         }
#         labels = {
#             'client': 'Клиент',
#             'card_number': 'Номер карты',
#             'price': 'Цена'
#         }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CardSaleForm, self).__init__(*args, **kwargs)
        # Можно добавить фильтрацию клиентов при необходимости
        self.fields['client'].queryset = Client.objects.filter(is_active=True)
        
        # Если нужно ограничить выбор клиентов только для текущего пользователя
        # if user and not user.is_superuser:
        #     self.fields['client'].queryset = Client.objects.filter(created_by=user, is_active=True)

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if CardSale.objects.filter(card_number=card_number).exists():
            raise forms.ValidationError('Карта с таким номером уже продана')
        return card_number
    
class WithdrawForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        label="Сумма изъятия"
    )
    reason = forms.CharField(
        max_length=200,
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Причина изъятия",
        required=True
    )
    
# class CardSaleForm(forms.ModelForm):
#     class Meta:
#         model = CardSale
#         fields = ['card_number', 'price', 'client']
#         widgets = {
#             'card_number': forms.TextInput(attrs={'placeholder': 'Например: 1234567890'}),
#             'price': forms.NumberInput(attrs={'min': 0}),
#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['client'].queryset = Client.objects.filter(is_active=True)
#         self.fields['client'].required = False