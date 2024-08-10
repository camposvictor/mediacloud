from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from core.forms import SignUpForm, EditProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from core.forms import MediaFileForm
from core.models import MediaFile
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class ImageView(View):
   def get(self, request):
    images = MediaFile.objects.filter(media_type='image')
    print(images)
    return render(request, 'images.html', {'images': images})
   
   def post(self, request):
    if request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        if uploaded_file.size > 5 * 1024 * 1024:
            return HttpResponse("<span id='upload-form-alert-image' class='alert alert-error my-2'>O arquivo excede o tamanho máximo de 10MB", status=400)
        if uploaded_file.content_type.startswith('image/'):
            media_type = 'image'
        else:
            return HttpResponse("<span id='upload-form-alert-image' class='alert alert-error my-2'>Tipo de arquivo não suportado.</span>", status=400)

        media_file = MediaFile.objects.create(
            user=request.user,
            file=uploaded_file,
            media_type=media_type
        )
        messages.success(request, f"{media_file.get_file_name()} carregado com sucesso")
        response = HttpResponse()
        response["HX-Redirect"] = '/'
        return response
    return HttpResponse("<span id='upload-form-alert-image' class='alert alert-error my-2'>Ocorreu um erro inesperado.", status=400)