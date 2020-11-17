from app.models import Tag, Profile

def rightMenu(request):
    return {
        'popular_tags': Tag.objects.popular()[0:10],
        'popular_users': Profile.objects.popular()[0:10],
    }
