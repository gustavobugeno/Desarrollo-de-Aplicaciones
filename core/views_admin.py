from django.http import HttpResponse
from django.contrib.auth.models import User

def create_admin(request):
    if User.objects.filter(username="admin").exists():
        return HttpResponse("El superusuario ya existe.")

    User.objects.create_superuser(
        username="admin",
        password="Admin1234!",
        email="admin@example.com"
    )
    return HttpResponse("Superusuario creado correctamente.")