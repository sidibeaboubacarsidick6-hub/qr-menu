from django.contrib import admin
from django.utils.html import format_html
from .models import Restaurant, QRCode
from .utils import generate_qr_code


class QRCodeInline(admin.TabularInline):
    model = QRCode
    extra = 0
    max_num = 1
    readonly_fields = ['uuid', 'qr_image_preview', 'created_at']
    fields = ['uuid', 'is_active', 'qr_image_preview', 'created_at']

    def qr_image_preview(self, obj):
        if obj.qr_image:
            return format_html(
                '<img src="{}" width="150" height="150" style="background:white;"/>',
                obj.qr_image.url
            )
        return "Pas encore généré"
    qr_image_preview.short_description = "Aperçu QR Code"


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'subscription_end', 'is_active', 'qr_code_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'owner__username', 'owner__email']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [QRCodeInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('owner', 'name', 'slug', 'logo', 'address', 'phone', 'description')
        }),
        ('Personnalisation du menu', {
            'fields': ('primary_color', 'secondary_color', 'background_color', 'text_color', 'header_opacity'),
        }),
        ('Abonnement', {
            'fields': ('subscription_end', 'is_active'),
            'description': 'Gérez l\'abonnement du restaurant.'
        }),
    )
    
    def qr_code_count(self, obj):
        return obj.qr_codes.count()
    qr_code_count.short_description = "QR Codes"
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.qr_codes.exists():
            qr = QRCode.objects.create(restaurant=obj)
            generate_qr_code(qr)
            qr.save()


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'uuid', 'is_active', 'qr_image_preview', 'created_at']
    list_filter = ['is_active']
    search_fields = ['restaurant__name', 'uuid']
    readonly_fields = ['uuid', 'qr_image_preview', 'created_at']
    actions = ['regenerate_qr']

    def qr_image_preview(self, obj):
        if obj.qr_image:
            return format_html(
                '<img src="{}" width="100" height="100" style="background:white;"/>',
                obj.qr_image.url
            )
        return "Pas d'image"
    qr_image_preview.short_description = "QR Code"

    @admin.action(description="Régénérer les QR codes sélectionnés")
    def regenerate_qr(self, request, queryset):
        for qr in queryset:
            generate_qr_code(qr)
            qr.save()
        self.message_user(request, f"{queryset.count()} QR code(s) régénéré(s).")
