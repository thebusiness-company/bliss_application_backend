


from django.http import JsonResponse


def error_404(request, exception):
    message = ("The API andpoint is not available.")
    response = JsonResponse(data={'message':message, 'status_code': 404})
    response.status_code = 404
    return response


def error_500(request):
    message = ("There is an server error. Our team is working on it.")
    response = JsonResponse(data={'message': message, 'status_code': 500})
    response.status_code = 500
    return response
# Create your views here.
