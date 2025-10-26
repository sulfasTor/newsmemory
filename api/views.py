from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(["GET"])
def health(_request):
    return JsonResponse({"status": "ok"})


@api_view(["GET", "POST"])
def orders(request):
    if request.method == "POST":
        data = request.data or {}
        # TODO: persist to DB (add model/migration)
        return JsonResponse({"created": data}, status=201)
    return JsonResponse({"items": []})
