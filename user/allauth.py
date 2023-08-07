import json
import requests
from django.contrib.auth import authenticate, login
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def google_signin_view(request):
    if request.method == 'POST':
        id_token = request.POST.get('idtoken')
        try:
            response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}')
            response.raise_for_status()
            data = json.loads(response.content)
            email = data['email']
            user = authenticate(request, username=email, password=None)
            if user is None:
                user = User.objects.create_user(email, email)
            user.profile_picture = data['picture']
            user.save()
            login(request, user)
            return JsonResponse({'success': True})
        except Exception as e:
            return HttpResponseBadRequest(str(e))


