from django.urls import path
from app.views import *

urlpatterns = [
   path('code/', CreateUserFavouriteCode.as_view(), name='code'),
   path('signup/', Signup.as_view(), name='signup'),
   path('signin/', Signin.as_view(), name='signin'),
   path('favourite/', FavouriteView.as_view(), name='favourite')
]
