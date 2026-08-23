from categories.models import Category
from core.models import SiteSettings


def common_data(request):
    return {
        "categories": Category.objects.filter(status=Category.StatusChoices.ACTIVE),
        "settings": SiteSettings.load(),
    }
