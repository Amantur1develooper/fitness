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
        card_id = self.cleaned_data.get('card_id')
        if not card_id:
            raise ValidationError('Номер карты обязателен')
        if Client.objects.filter(card_id=card_id).exists():
            raise ValidationError('Клиент с таким номером карты уже существует')
        return card_id

    # def clean_card_id(self):
    #     card_id = self.cleaned_data['card_id']
    #     if Client.objects.filter(card_id=card_id).exists():
    #         raise ValidationError('Клиент с таким номером карты уже существует')
    #     return card_id
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
from django.db.models import Q   
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

from django import forms
from django.utils import timezone
from .models import Client, Payment, CashRegister, CashOperation

# class OneTimeMembershipForm(forms.Form):
#     client_full_name = forms.CharField(
#         label='ФИО клиента',
#         max_length=100,
#         widget=forms.TextInput(attrs={'class': 'form-control'}))
    
#     phone = forms.CharField(
#         label='Телефон',
#         max_length=20,
#         widget=forms.TextInput(attrs={'class': 'form-control'}))
    
#     payment_method = forms.ChoiceField(
#         label='Способ оплаты',
#         choices=Payment.PAYMENT_METHODS,
#         widget=forms.Select(attrs={'class': 'form-control'}))
    
#     notes = forms.CharField(
#         label='Примечание',
#         required=False,
#         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    
#     def calculate_price(self):
#         now = timezone.localtime(timezone.now())
#         if now.hour < 14:  # До 14:00
#             return 200
#         return 400
from django import forms
from .models import Client
from django.contrib.auth.models import User


class ClientEditForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'full_name',
            'phone',
            'email',
            'birth_date',
            'photo',
            'notes',
            'card_id',
            'is_active',
            'user'
        ]
        widgets = {
            'birth_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Дополнительная информация о клиенте'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Иванов Иван Иванович'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'client@example.com'
            }),
            'card_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'RFID или номер карты'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'user': forms.Select(attrs={
                'class': 'form-select'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'is_active': 'Активный клиент',
            'card_id': 'ID карты доступа',
            'photo': 'Фотография профиля'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_user = self.instance.user
        self.fields['user'].queryset = User.objects.filter(
            Q(client__isnull=True) | Q(pk=current_user.pk) if current_user else Q()
        )
        self.fields['user'].required = False
        self.fields['user'].label = 'Привязать к учетной записи'
        
        # Добавляем классы Bootstrap для всех полей
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                    field.widget.attrs['class'] = 'form-select'
                elif isinstance(field.widget, forms.CheckboxInput):
                    field.widget.attrs['class'] = 'form-check-input'
                else:
                    field.widget.attrs['class'] = 'form-control'
# class ClientEditForm(forms.ModelForm):
#     class Meta:
#         model = Client
#         fields = [
#             'full_name',
#             'phone',
#             'email',
#             'birth_date',
           
#             'photo',
#             'notes',
#             'card_id',
#             'is_active',
           
#             'user'
#         ]
#         widgets = {
#             'birth_date': forms.DateInput(attrs={'type': 'date'}),
#             'notes': forms.Textarea(attrs={'rows': 4}),
#         }
#         labels = {
#             'is_active': 'Активный статус',
#             'discount_balance': 'Баланс скидки (руб)'
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Фильтруем пользователей: только непривязанные + текущий (если есть)
#         current_user = self.instance.user
#         self.fields['user'].queryset = User.objects.filter(
#             Q(client__isnull=True) | Q(pk=current_user.pk) if current_user else Q()
#         )
#         self.fields['user'].required = False
        
        
        
class OneTimeMembershipForm(forms.Form):
    client_full_name = forms.CharField(label='ФИО клиента', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=20)
    price = forms.DecimalField(
        label='Цена абонемента', 
        max_digits=10, 
        decimal_places=2,
        initial=200  # или другая базовая цена
    )
   
    payment_method = forms.ChoiceField(
        label='Способ оплаты',
        choices=Payment.PAYMENT_METHODS
    )
    notes = forms.CharField(
        label='Примечания',
        required=False,
        widget=forms.Textarea(attrs={'rows': 2}))
    
    def clean_visit_price(self):
        visit_price = self.cleaned_data.get('visit_price')
        price = self.cleaned_data.get('price')
        if not visit_price:
            return price  # Если не указана, равна цене абонемента
        return visit_price
        
        