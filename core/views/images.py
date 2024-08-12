from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from core.forms import SignUpForm, EditProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from core.models import MediaFile
from django.db.models import Q
from django.http import HttpResponse, QueryDict
from django.urls import reverse
from core.models import ImageFile
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from PIL import Image
from io import BytesIO

@login_required
def edit_image_view(request, id):
    if request.method == 'PATCH':
        # troca por form de imagem;
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Imagem atualizada com sucesso!')
            return redirect('images')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'edit/edit_image.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class ImageView(View):
    def get(self, request):
        images = ImageFile.objects.all()
        return render(request, 'images.html', {'images': images})
    def put(self, request):
        try:
            # Converte o corpo da requisição PUT para um QueryDict
            put_data = QueryDict(request.body)
            print(put_data)

            # Obtém os dados do formulário
            image_id = put_data.get('id')
            description = put_data.get('description')
            tags = put_data.get('tags')

            # Busca a imagem pelo ID
            image = ImageFile.objects.get(id=image_id)

            # Atualiza os campos
            image.description = description
            image.tags = tags
            image.save()

             # Adiciona a mensagem de sucesso
            messages.success(request, 'Imagem atualizada com sucesso!')

            response = HttpResponse()
            response["HX-Redirect"] = '/images'
            return response
        except Exception as e:
            return HttpResponse(f"<span id='upload-form-alert-image' class='alert alert-error my-2'>Erro ao processar a imagem: {str(e)}</span>", status=500)
    def post(self, request):
        if request.FILES.get('file'):
            uploaded_file = request.FILES['file']

            allowed_mime_types = [choice[0] for choice in ImageFile.IMAGE_MIME_CHOICES]
            if uploaded_file.content_type not in allowed_mime_types:
                return HttpResponse("<span id='upload-form-alert-image' class='alert alert-error my-2'>Tipo de arquivo não suportado.</span>", status=400)

            if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
                return HttpResponse("<span id='upload-form-alert-image' class='alert alert-error my-2'>O arquivo excede o tamanho máximo de 10MB.</span>", status=400)

            try:
                image = Image.open(uploaded_file)
                width, height = image.size
                color_depth = image.info.get('bits', 8)
                resolution = f"{width}x{height}"
                exif_data = image.getexif() or None

                media_file = ImageFile.objects.create(
                    user=request.user,
                    file=uploaded_file,
                    description=request.POST.get('description', ''),
                    tags=request.POST.get('tags', ''),
                    mime_type=uploaded_file.content_type,
                    width=width,
                    height=height,
                    color_depth=color_depth,
                    resolution=resolution,
                    exif_data=exif_data
                )
                messages.success(request, f"{media_file.file.name} carregado com sucesso.")
                response = HttpResponse()
                response["HX-Redirect"] = '/'
                return response
            except Exception as e:
                return HttpResponse(f"<span id='upload-form-alert-image' class='alert alert-error my-2'>Erro ao processar a imagem: {str(e)}</span>", status=500)

        return HttpResponse("<span id='upload-form-alert-image' class='alert alert-error my-2'>Ocorreu um erro inesperado.</span>", status=400)
