from datetime import timedelta
from django.db import models

# Create your models here.
# models.py
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

class Client(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другой'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, verbose_name="ФИО")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    photo = models.ImageField(upload_to='client_photos/', null=True, blank=True, verbose_name="Фото")
    notes = models.TextField(blank=True, verbose_name="Примечания")
    card_id = models.CharField(max_length=50, unique=True, verbose_name="ID карты доступа")
    is_active = models.BooleanField(default=True, verbose_name="Активный клиент")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    created_by = models.ForeignKey(User,blank=True, on_delete=models.SET_NULL, null=True, 
                                 related_name='created_clients', verbose_name="Кто создал")
    discount_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                         verbose_name="Баланс скидки")
    def __str__(self):
        return self.full_name

class MembershipType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    visits_number = models.PositiveIntegerField(verbose_name="Количество посещений")
    validity_days = models.PositiveIntegerField(verbose_name="Срок действия (дней)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    def __str__(self):
        return f"{self.name} ({self.visits_number} посещений)"

class Membership(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='memberships')
    membership_type = models.ForeignKey(MembershipType, on_delete=models.PROTECT)
    purchase_date = models.DateField(auto_now_add=True, verbose_name="Дата покупки")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    remaining_visits = models.PositiveIntegerField(verbose_name="Осталось посещений")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    is_frozen = models.BooleanField(default=False, verbose_name="Заморожен")
    frozen_days = models.PositiveIntegerField(default=0, verbose_name="Дней заморозки")
    original_price = models.DecimalField(max_digits=10, decimal_places=2, 
                                       verbose_name="Исходная цена")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                        verbose_name="Сумма скидки")
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                    verbose_name="Оплаченная сумма")
    debt_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    freeze_start = models.DateField(null=True, blank=True)
    freeze_days = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Кто оформил"
    )
    
    def __str__(self):
        return f"{self.client} - {self.membership_type} (до {self.end_date})"
    #  def save(self, *args, **kwargs):
    #     if not self.pk and not self.created_by:
    #         if hasattr(self, '_current_user'):
    #             self.created_by = self._current_user
    #     super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
        if not self.pk:  # Только при создании нового абонемента
            self.original_price = self.membership_type.price
            self.remaining_visits = self.membership_type.visits_number
            
            # Рассчитываем оплаченную сумму
            if not hasattr(self, 'paid_amount'):
                self.paid_amount = self.original_price - getattr(self, 'discount_amount', 0)
            
            # Рассчитываем долг, если оплачено меньше
            if self.paid_amount < (self.original_price - getattr(self, 'discount_amount', 0)):
                self.debt_amount = (self.original_price - getattr(self, 'discount_amount', 0))-  self.paid_amount
        if self.pk and not self.is_frozen and self.freeze_days > 0:
            self.end_date += timedelta(days=self.freeze_days)
            self.freeze_days = 0
            self.freeze_start = None
        super().save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     if not self.pk:  # При создании
    #         self.remaining_visits = self.membership_type.visits_number
    #         original_price = self.membership_type.price
    #         self.paid_amount = original_price - self.discount_amount
            
    #         # Если оплачено меньше цены - создаем долг
    #         if self.paid_amount < original_price:
    #             self.debt_amount = original_price - self.paid_amount
    #     super().save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.original_price = self.membership_type.price
    #         self.paid_amount = self.original_price - self.discount_amount
    #         self.remaining_visits = self.membership_type.visits_number
    #     super().save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     if not self.pk:  # Если объект создаётся впервые
    #         self.remaining_visits = self.membership_type.visits_number
    #     super().save(*args, **kwargs)

class Visit(models.Model):
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, related_name='visits')
    visit_time = models.DateTimeField(auto_now_add=True, verbose_name="Время посещения")
    success = models.BooleanField(default=True, verbose_name="Успешный вход")
    reason = models.CharField(max_length=200, blank=True, verbose_name="Причина отказа")
    
    def __str__(self):
        return f"{self.membership.client} - {self.visit_time}"

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('card', 'Карта'),
        ('online', 'Онлайн'),
    ]
    
    membership = models.ForeignKey(Membership,null=True, blank=True, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, 
                                      verbose_name="Способ оплаты")
    notes= models.CharField(max_length=100, verbose_name='примечание', null=True, blank=True)
    receipt_number = models.CharField(max_length=50, blank=True, verbose_name="Номер чека")
    is_debt_payment = models.BooleanField(default=False)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Кто внес платеж"
    )
    def __str__(self):
        deb = "Долг"
        return f"{self.membership or deb} - {self.amount} руб."
    
    
class Debt(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='debts')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма долга")
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_paid = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Долг'
        verbose_name_plural = 'Долги'
    
    def clean(self):
        if self.amount <= 0:
            raise ValidationError('Сумма долга должна быть положительной')
    
    def __str__(self):
        return f'Долг {self.client}: {self.amount} сом'
class CardSale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    card_number = models.CharField(max_length=50, unique=True)
    sale_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sold_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    
class CashRegister(models.Model):
    name = models.CharField(max_length=100, default="Основная касса", verbose_name="Название кассы")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Баланс")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление")
    
    class Meta:
        verbose_name = 'Касса'
        verbose_name_plural = 'Кассы'
    
    def __str__(self):
        return f"{self.name} - {self.balance} сом"

class CashOperation(models.Model):
    OPERATION_TYPES = [
        ('income', 'Приход'),
        ('outcome', 'Расход'),
    ]
    
    cash_register = models.ForeignKey(CashRegister, on_delete=models.PROTECT, verbose_name="Касса")
    operation_type = models.CharField(max_length=10, choices=OPERATION_TYPES, verbose_name="Тип операции")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Связанный платеж")
   
    notes = models.TextField(blank=True, verbose_name="Примечание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата операции")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Кто провел операцию")
    
    class Meta:
        verbose_name = 'Операция по кассе'
        verbose_name_plural = 'Операции по кассе'
    
    def __str__(self):
        return f"{self.get_operation_type_display()} - {self.amount} сом"
    
    def save(self, *args, **kwargs):
        # Обновляем баланс кассы при сохранении операции
        if not self.pk:
            if self.operation_type == 'income':
                self.cash_register.balance += self.amount
            else:
                self.cash_register.balance -= self.amount
            self.cash_register.save()
        super().save(*args, **kwargs)