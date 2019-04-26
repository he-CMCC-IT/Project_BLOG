from django.shortcuts import render, get_object_or_404
from .models import Image


# Create your views here.
def index(request):
    return render(request, 'ziyangroup/functions/index.html')


def about_us(request):
    image = Image.objects.get()
    return render(request, 'ziyangroup/functions/about-us.html', {'image': image})


def services(request):
    return render(request, 'ziyangroup/functions/services.html')


def portfolio(request):
    return render(request, 'ziyangroup/functions/portfolio.html')


def contact(request):
    return render(request, 'ziyangroup/functions/contact.html')


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'ziyangroup/utils/image-detail.html', {'section': 'images',
                                                                  'image': image,
                                                                  })
