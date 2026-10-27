from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from djangoapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
    path('fetchDealers', views.get_dealerships, name='fetch_dealers'),
    path('fetchDealers/<str:state>', views.get_dealers_by_state, name='fetch_dealers_by_state'),
    path('fetchDealer/<int:dealer_id>', views.get_dealer_by_id, name='fetch_dealer_by_id'),
    path('fetchReviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='fetch_reviews_dealer'),
    path('analyze/<str:text>', views.sentiment_analyzer, name='analyze_sentiment'),
    path('', TemplateView.as_view(template_name='Home.html')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
