from django.contrib import admin
from .models import ClaimTableEducation, ClaimTableOSP, Transaction

@admin.register(ClaimTableEducation)
class ClaimTableEducationAdmin(admin.ModelAdmin):
    list_display = ('claim_designation', 'impact', 'gdpr_compliance')

@admin.register(ClaimTableOSP)
class ClaimTableOSPAdmin(admin.ModelAdmin):
    list_display = ('claim_designation', 'impact', 'gdpr_compliance')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'transaction')
