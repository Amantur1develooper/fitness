from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CashOperation, CashRegister, Client, MembershipType, Membership, Visit, Payment

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    Client, MembershipType, Membership, 
    Visit, Payment, Debt, CardSale
)
admin.site.register(Payment)
# Расширяем стандартную админку User
class ClientInline(admin.StackedInline):
    model = Client
    can_delete = False
    verbose_name_plural = 'Доп. информация'
    fk_name = 'user'
    fields = ('phone', 'email', 'birth_date', 'gender', 'photo', 'card_id', 'is_active')

class CustomUserAdmin(UserAdmin):
    inlines = (ClientInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone', 'get_card_id')
    list_select_related = ('client', )

    def get_phone(self, instance):
        return instance.client.phone
    get_phone.short_description = 'Телефон'

    def get_card_id(self, instance):
        return instance.client.card_id
    get_card_id.short_description = 'ID карты'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# Регистрируем расширенную админку User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Админка для клиентов
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'card_id', 'is_active', 'created_at')
    list_filter = ('is_active', 'gender', 'created_at')
    search_fields = ('full_name', 'phone', 'email', 'card_id')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('user', 'full_name', 'phone', 'email', 'photo')
        }),
        ('Доп. информация', {
            'fields': ('birth_date', 'gender', 'card_id', 'is_active', 'discount_balance')
        }),
        ('Системные', {
            'fields': ('notes', 'created_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

# Админка для типов абонементов
@admin.register(MembershipType)
class MembershipTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'visits_number', 'validity_days', 'price')
    list_filter = ('visits_number',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'name': ('name',)}

# Админка для абонементов
class VisitInline(admin.TabularInline):
    model = Visit
    extra = 0
    readonly_fields = ('visit_time', 'success', 'reason')
    can_delete = False

# class PaymentInline(admin.TabularInline):
#     model = Payment
#     extra = 0
#     readonly_fields = ('payment_date',)
#     fields = ('amount', 'payment_date', 'payment_method', 'receipt_number', 'is_debt_payment')

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('client', 'membership_type', 'start_date', 'end_date', 
                   'remaining_visits', 'is_active', 'is_frozen')
    list_filter = ('is_active', 'is_frozen', 'membership_type', 'start_date')
    search_fields = ('client__full_name', 'client__phone', 'client__card_id')
    readonly_fields = ('purchase_date',)
    # inlines = [VisitInline, PaymentInline]
    inlines = [VisitInline, ]
    fieldsets = (
        (None, {
            'fields': ('client', 'membership_type', 'purchase_date')
        }),
        ('Срок действия', {
            'fields': ('start_date', 'end_date', 'is_active', 'is_frozen', 'frozen_days')
        }),
        ('Посещения', {
            'fields': ('remaining_visits',)
        }),
        ('Финансы', {
            'fields': ('original_price', 'discount_amount', 'paid_amount', 'debt_amount'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # При создании
            obj.remaining_visits = obj.membership_type.visits_number
        super().save_model(request, obj, form, change)

# Админка для посещений
@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('membership', 'visit_time', 'success', 'reason')
    list_filter = ('success', 'visit_time')
    search_fields = ('membership__client__full_name', 'reason')
    readonly_fields = ('visit_time',)

# Админка для платежей
# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('membership', 'amount', 'payment_date', 'payment_method', 'is_debt_payment')
#     list_filter = ('payment_method', 'is_debt_payment', 'payment_date')
#     search_fields = ('membership__client__full_name', 'receipt_number')
#     readonly_fields = ('payment_date',)
#     date_hierarchy = 'payment_date'
admin.site.register(CashOperation)
admin.site.register(CashRegister)
# Админка для долгов
@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ('client', 'amount', 'created_at', 'is_paid')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('client__full_name', 'description')
    readonly_fields = ('created_at',)

# Админка для продаж карт
@admin.register(CardSale)
class CardSaleAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'client', 'sale_date', 'price', 'sold_by')
    list_filter = ('sale_date',)
    search_fields = ('card_number', 'client__full_name')
    readonly_fields = ('sale_date',)