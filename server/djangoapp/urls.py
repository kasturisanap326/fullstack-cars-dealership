@"
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "djangoapp"

urlpatterns = [
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("get_dealers", views.get_dealerships, name="get_dealers"),
    path("get_dealer/<int:dealer_id>", views.get_dealer_by_id, name="get_dealer"),
    path("get_dealers/<str:state>", views.get_dealers_by_state, name="get_dealers_by_state"),
    path("get_car_make", views.get_car_make, name="get_car_make"),
    path("get_cars", views.get_car_make, name="get_cars"),
    path("reviews/dealer/<int:dealer_id>", views.get_dealer_reviews, name="get_dealer_reviews"),
    path("add_review", views.add_review, name="add_review"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"@ | Set-Content -Path "server/djangoapp/urls.py" -Encoding UTF8