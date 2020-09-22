from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('sneakers/', views.sneakers_index, name='index'),
    path('sneakers/create/', views.SneakerCreate.as_view(), name='sneakers_create'),
    path('sneakers/<int:sneaker_id>/', views.sneakers_detail, name='detail'),
    path('sneakers/<int:sneaker_id>/photo/', views.add_photo, name='add_photo'),
    path('sneakers/<int:sneaker_id>/assoc_shoelace/<int:shoelaceid>/', views.assoc_toy, name='assoc_toy'),
    path('sneakers/<int:pk>/update/', views.SneakerUpdate.as_view(), name='sneakers_update'),
    path('sneakers/<int:pk>/delete/', views.SneakerDelete.as_view(), name='sneakers_delete'),
    path('sneakers/<int:sneaker_id>/add_purchase/', views.add_purchase, name='add_purchase'),
    path('shoelaces/', views.ShoelaceList.as_view(), name='shoeslaces_index'),
    path('shoelaces/create/', views.ShoelaceCreate.as_view(), name='shoelaces_create'),
    path('shoelaces/<int:pk>/', views.ShoelaceDetail.as_view(), name='shoelace_detail'),
    path('shoelaces/<int:pk>/update/', views.ShoelaceUpdate.as_view(), name='shoelaces_update'),
    path('shoelaces/<int:pk>/delete/', views.ShoelaceDelete.as_view(), name='shoelaces_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]