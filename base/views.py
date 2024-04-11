from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response


class RegisterAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.create_user(username=username, password=password)
                return Response({'success': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'success': 'User logged in successfully'})
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
class ProductViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from . models import Product
from django.core.files.base import ContentFile
import base64

class AddProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def create(self, request, *args, **kwargs):
        # Decode base64-encoded image data
        product_image_data = request.data.get('product_image')
        decoded_image_data = base64.b64decode(product_image_data)

        # Create file object
        product_image_file = ContentFile(decoded_image_data, name='product_image.jpg')

        # Update request data with file object
        request.data['product_image'] = product_image_file

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

from django.http import JsonResponse
from rest_framework.decorators import api_view
@api_view(['GET'])
def list_all_products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_user_products(request):
    if request.method == 'GET':
        user = request.user  # Retrieve the user associated with the token
        products = Product.objects.filter(user=user)  # Filter products by user
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            print("Login in successfuly🎉🏆🙌")
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# views.pyythonm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        token = RefreshToken.for_user(user)

        return Response({'token': str(token.access_token)}, status=status.HTTP_201_CREATED)
    

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token  



from django.http import JsonResponse

@csrf_exempt
def get_user_info(request):
    if request.method == 'GET':
        # Check if Authorization header exists
        if 'Authorization' in request.headers:
            # Extract token from the Authorization header
            token_parts = request.headers['Authorization'].split()
            if len(token_parts) == 2:
                token_key = token_parts[1]
                # Retrieve the token object from the database
                try:
                    token = Token.objects.get(key=token_key)
                except Token.DoesNotExist:
                    return JsonResponse({'error': 'Token not found'}, status=404)

                # Retrieve the associated user
                user = token.user

                # Response containing user information
                response_data = {
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email
                }

                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'Invalid Authorization header format'}, status=400)
        else:
            return JsonResponse({'error': 'Authorization header is missing'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

from django.contrib.auth import logout
@csrf_exempt
def logout_user(request):
    logout(request)
    return JsonResponse({'message': 'User logged out successfully'})

@csrf_exempt
def get_user_info_(request):
    if request.method == 'GET':
        # Extract token from the Authorization header
        token_key = request.headers.get('Authorization').split()[1]
        
        # Retrieve the token object from the database
        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Token not found'}, status=404)
        
        # Retrieve the associated user
        user = token.user
        
        # Response containing user information
        response_data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }
        
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
from django.middleware.csrf import get_token

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})


from django.shortcuts import render
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def mpesa_(request):
    cl = MpesaClient()
    if 'phone_number' in request.GET:
        phone_number = request.GET['phone_number']
        # Use the extracted phone number in your logic
        amount = 1
        account_reference = 'Unisell'
        transaction_desc = 'Description'
        callback_url = 'https://api.darajambili.com/express-payment'
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
        return HttpResponse(response)
    else:
        # Handle the case where phone_number is not provided in the request
        return HttpResponse("Phone number not provided in the request.")
    
@csrf_exempt
def mpesa(request):
    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '0746727592'
    amount = 1
    account_reference = 'Unisell'
    transaction_desc = 'Description'
    callback_url = 'https://api.darajambili.com/express-payment'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)

# class GetUserInfo(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         print(request.headers)
#         user = request.user
#         response_data = {
#             'user_id': user.id,
#             'username': user.username,
#         }
#         return Response(response_data, status=status.HTTP_200_OK)

# views.py
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User
# from django.http import JsonResponse
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# @api_view(['POST'])
# def register(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     if username and password:
#         if User.objects.filter(username=username).exists():
#             return Response({'error': 'Username already exists'}, status=400)
#         else:
#             user = User.objects.create_user(username=username, password=password)
#             return Response({'success': 'User registered successfully'}, status=201)
#     else:
#         return Response({'error': 'Username and password are required'}, status=400)

# @api_view(['POST'])
# def user_login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     user = authenticate(request, username=username, password=password)

#     if user is not None:
#         login(request, user)
#         return Response({'success': 'User logged in successfully'})
#     else:
#         return Response({'error': 'Invalid username or password'}, status=400)
