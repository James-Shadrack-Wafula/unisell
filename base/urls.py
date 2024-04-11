
from django.urls import path
from . import views
urlpatterns = [
    # path('', views.home),
    path('register/', views.RegisterAPIView.as_view() ),
    path('login/', views.LoginAPIView.as_view()),
    path('add_product/', views.ProductViewSet.as_view(actions={'post': 'create'})), 
    path('new_products/', views.AddProductViewSet.as_view(actions={'post': 'create'})),
    path('products/', views.list_all_products,),
    path('api/login/', views.LoginView.as_view()),
    path('api/register/', views.RegisterView.as_view()),
    path('api/get_user_info/', views.get_user_info, name='get_user_info'),
    path('api/my_products/', views.list_user_products),
    path('api/logout/', views.logout_user),
    path('pay/', views.mpesa),
    path('getCsrf/', views.get_csrf_token)
    # pushing files
]

