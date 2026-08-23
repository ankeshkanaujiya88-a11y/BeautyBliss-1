from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Product, ProductImage, ProductVariant


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "image_preview", "is_primary")
    readonly_fields = ("image_preview",)

    @admin.display(description=_("Preview"))
    def image_preview(self, instance):
        if instance.image:
            return format_html(
                '<img src="{}" style="max-width: 80px; max-height: 80px; object-fit: cover; border-radius: 4px; border: 1px solid #e0e0e0;" />',
                instance.image.url,
            )
        return format_html('<span style="color: #999;">No image</span>')


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ("size", "color", "sku", "selling_price", "stock", "stock_unit")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "image_preview",
        "name",
        "category",
        "brand",
        "selling_price",
        "original_price",
        "discount_badge",
        "stock",
        "stock_status",
        "is_active",
        "top_featured",
    )
    list_display_links = ("image_preview", "name")
    list_editable = ("selling_price", "stock", "is_active", "top_featured")
    list_filter = (
        "is_active",
        "top_featured",
        "category",
        "brand",
        "stock_unit",
        "is_free_shipping",
        "has_variants",
        "created",
    )
    search_fields = ("name", "sku", "barcode", "brand", "description", "meta_keywords")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("category",)
    inlines = [ProductImageInline, ProductVariantInline]
    list_per_page = 25
    save_on_top = True
    actions = [
        "make_active",
        "make_inactive",
        "toggle_featured",
        "untoggle_featured",
    ]

    fieldsets = (
        (
            _("Basic Information"),
            {
                "fields": (
                    ("name", "slug"),
                    ("category", "brand"),
                    "description",
                    "additional_details",
                )
            },
        ),
        (
            _("Pricing & Inventory"),
            {
                "fields": (
                    ("selling_price", "original_price", "discount_percentage_display"),
                    ("stock", "stock_unit", "minimum_stock"),
                    ("has_variants", "needs_restock_display"),
                )
            },
        ),
        (
            _("Identification & SKU"),
            {
                "fields": (("sku", "barcode"),),
            },
        ),
        (
            _("Shipping & Delivery"),
            {
                "classes": ("collapse",),
                "fields": (("weight", "is_free_shipping"),),
            },
        ),
        (
            _("Visibility & Promotions"),
            {
                "fields": (("is_active", "top_featured"),),
            },
        ),
        (
            _("SEO & Meta Tags"),
            {
                "classes": ("collapse",),
                "fields": (
                    "meta_keywords",
                    "meta_description",
                ),
            },
        ),
    )

    readonly_fields = (
        "discount_percentage_display",
        "needs_restock_display",
    )

    @admin.display(description=_("Image"))
    def image_preview(self, obj):
        primary = obj.primary_image
        if primary and primary.image:
            return format_html(
                '<img src="{}" style="width: 48px; height: 48px; object-fit: cover; border-radius: 6px; border: 1px solid #ddd;" />',
                primary.image.url,
            )
        return format_html(
            '<div style="width: 48px; height: 48px; background: #f0f0f0; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #999; font-size: 10px;">No Img</div>'
        )

    @admin.display(description=_("Discount"))
    def discount_badge(self, obj):
        discount = obj.discount_percentage
        if discount > 0:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 12px; font-weight: bold; font-size: 11px;">-{}%</span>',
                discount,
            )
        return format_html('<span style="color: #bbb;">0%</span>')

    @admin.display(description=_("Discount %"))
    def discount_percentage_display(self, obj):
        return f"{obj.discount_percentage}%"

    @admin.display(description=_("Restock Alert"))
    def stock_status(self, obj):
        if obj.needs_restock:
            return format_html(
                '<span style="background-color: #ffebe9; color: #cf222e; border: 1px solid rgba(255,129,130,0.4); padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: 600;">⚠️ Low Stock</span>'
            )
        return format_html(
            '<span style="background-color: #dafbe1; color: #1a7f37; border: 1px solid rgba(74,194,107,0.4); padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: 500;">In Stock</span>'
        )

    @admin.display(description=_("Needs Restock?"))
    def needs_restock_display(self, obj):
        return _("Yes") if obj.needs_restock else _("No")

    # Custom Admin Actions
    @admin.action(description=_("Mark selected products as Active"))
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} product(s) marked as active.")

    @admin.action(description=_("Mark selected products as Inactive"))
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} product(s) marked as inactive.")

    @admin.action(description=_("Mark selected products as Top Featured"))
    def toggle_featured(self, request, queryset):
        updated = queryset.update(top_featured=True)
        self.message_user(request, f"{updated} product(s) marked as top featured.")

    @admin.action(description=_("Remove Top Featured from selected products"))
    def untoggle_featured(self, request, queryset):
        updated = queryset.update(top_featured=False)
        self.message_user(request, f"{updated} product(s) removed from top featured.")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("image_preview", "product", "is_primary", "created")
    list_filter = ("is_primary", "created")
    search_fields = ("product__name",)
    autocomplete_fields = ("product",)
    readonly_fields = ("image_preview",)

    @admin.display(description=_("Preview"))
    def image_preview(self, instance):
        if instance.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px; object-fit: cover; border-radius: 4px;" />',
                instance.image.url,
            )
        return format_html('<span style="color: #999;">No image</span>')


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "sku",
        "size",
        "color",
        "selling_price",
        "stock",
        "stock_unit",
        "created",
    )
    list_filter = ("size", "stock_unit", "created")
    search_fields = ("product__name", "sku", "color")
    autocomplete_fields = ("product",)

