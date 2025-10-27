from django.http import JsonResponse
from django.utils.timezone import now


def _payload(request, status, message, extra=None):
    return {
        "error": {
            "status": status,
            "message": message,
            "path": request.path,
            "timestamp": now().isoformat(),
            **(extra or {}),
        }
    }


def bad_request_json(request, exception):
    return JsonResponse(_payload(request, 400, "Bad request"), status=400)


def permission_denied_json(request, exception):
    return JsonResponse(_payload(request, 403, "Forbidden"), status=403)


def not_found_json(request, exception):
    return JsonResponse(_payload(request, 404, "Not found"), status=404)


def server_error_json(request):
    return JsonResponse(_payload(request, 500, "Internal server error"), status=500)


def csrf_failure_json(request, reason=""):
    return JsonResponse(
        _payload(request, 403, "CSRF verification failed", {"reason": reason}), status=403
    )
