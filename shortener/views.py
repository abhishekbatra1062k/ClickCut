from django.http import JsonResponse
from django.views import View
from django.conf import settings
from .models import URLMapping
from .utils import generate_short_url
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import URLForm


class ShortenURLView(View):
    def post(self, request):
        long_url = request.POST.get("long_url")
        if not long_url:
            return JsonResponse({"error": "Missing long_url"}, status=400)

        # Check Redis cache
        cached_short_url = settings.REDIS_CLIENT.get(long_url)
        if cached_short_url:
            return JsonResponse({"short_url": cached_short_url.decode()})

        # Generate and save short URL
        short_url = generate_short_url()
        URLMapping.save_url_mapping(short_url, long_url)

        # Cache in Redis
        settings.REDIS_CLIENT.set(long_url, short_url)

        return JsonResponse({"short_url": short_url})


class RedirectURLView(View):
    def get(self, request, short_url):
        # Check Redis cache
        cached_long_url = settings.REDIS_CLIENT.get(short_url)
        if cached_long_url:
            return redirect(cached_long_url.decode())

        # Retrieve from MongoDB
        long_url = URLMapping.get_long_url(short_url)
        if not long_url:
            return JsonResponse({"error": "Short URL not found"}, status=404)

        # Cache in Redis
        settings.REDIS_CLIENT.set(short_url, long_url)

        return redirect(long_url)


def home(request):
    if request.method == "POST":
        form = URLForm(request.POST)
        if form.is_valid():
            long_url = form.cleaned_data["long_url"]

            # Check Redis cache
            cached_short_url = settings.REDIS_CLIENT.get(long_url)
            if cached_short_url:
                short_url = cached_short_url.decode()
            else:
                # Generate and save short URL
                short_url = generate_short_url()
                URLMapping.save_url_mapping(short_url, long_url)
                settings.REDIS_CLIENT.set(long_url, short_url)

            return render(request, "shortener/home.html", {"form": form, "short_url": request.build_absolute_uri(short_url)})

    else:
        form = URLForm()

    return render(request, "shortener/home.html", {"form": form})


# def redirect_url(request, short_url):
#     # Check Redis cache
#     cached_long_url = settings.REDIS_CLIENT.get(short_url)
#     if cached_long_url:
#         return redirect(cached_long_url.decode())

#     # Retrieve from MongoDB
#     long_url = URLMapping.get_long_url(short_url)
#     if not long_url:
#         return HttpResponse("URL not found", status=404)

#     # Cache in Redis
#     settings.REDIS_CLIENT.set(short_url, long_url)

#     return redirect(long_url)
