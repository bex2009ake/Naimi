from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

class CreateUserFavouriteCode(APIView):
    def get(self, req: Request):
        return Response({'msg': 'Create user code favourite'}, status=200)
    
    def post(self, req: Request):
        phone = req.data.get('phone')
        code = req.data.get('code')
        city = City.objects.get(id=req.data.get('city'))
      
        if not User.objects.get(phone=phone):
            user = User.objects.create(phone=phone, city=city)
            Favourite.objects.create(owner_id=user)
            OneTimePassword.objects.create(user_id=user, otp=code)
        else:
            user = User.objects.get(phone=phone)
            for i in OneTimePassword.objects.all().filter(user_id=user):
                i.delete()
            OneTimePassword.objects.create(user_id=user, otp=code)

        return Response({'msg': 'OK'}, status=200)



class Signup(APIView):
    def get(self, req: Request):
        return Response({'msg': 'Singup'}, status=200)
    
    def post(self, req: Request):
        phone = req.data.get('phone')
        code = int(req.data.get('code'))

        try: 
            user = User.objects.get(phone=phone)
            city = City.objects.get(name=req.data.get('city'))
            onepassword = OneTimePassword.objects.get(user_id=user)
        except:
            return Response({'error': 'User or city was not found'}, status=404)
        

        if int(code) == int(onepassword.otp) and not onepassword.finish_at < timezone.now():
            user.city = city
            user.is_active = True
            user.save()
            onepassword.delete()

            token = RefreshToken.for_user(user=user)

            return Response({
                'access_token': str(token.access_token),
                'refresh_token': str(token),
            }, status=200)
        
        else: 
            return Response({'error': 'Wrong code !!!'})
        

class Signin(APIView):
    def get(self, req: Request):
        return Response({'msg': 'Singin'}, status=200)
    
    def post(self, req: Request):
        phone = req.data.get('phone')
        code = int(req.data.get('code'))

        try: 
            user = User.objects.get(phone=phone)
            onepassword = OneTimePassword.objects.get(user_id=user)
        except:
            return Response({'error': 'User or code was not found'}, status=404)
        
        
        if int(code) == int(onepassword.otp) and not onepassword.finish_at < timezone.now():
            user.is_active = True
            user.save()
            onepassword.delete()

            token = RefreshToken.for_user(user=user)

            return Response({
                'access_token': str(token.access_token),
                'refresh_token': str(token),
            }, status=200)
        
        else: 
            return Response({'error': 'Wrong code !!!'})
        

class FavouriteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req: Request):
        user = req.user
        favourites = Favourite.objects.get(owner_id=user)

        return Response({'data': favourites.profiles_id.values()})
    
    def post(self, req: Request):
        try:
            user = req.user
            profile = Profile.objects.get(user_id=req.data.get('profile'))
            favourites = Favourite.objects.get(owner_id=user)
        except:
            return Response({'error': 'Profile was not found'})


        favourites.profiles_id.add(profile)
        favourites.save()

        return Response({'msg': 'OK'}, status=200)
        

