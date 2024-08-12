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
from core.forms import EditImageForm

@login_required
def delete_image(request, id):
    if request.method == 'POST':
        image = get_object_or_404(ImageFile, id=id)
        image.delete()
        messages.success(request, f'Imagem "{image.get_file_name}" excluída com sucesso!')
        response = HttpResponse()
        response["HX-Redirect"] = '/'
        return response
    return redirect('images') 

@login_required
def edit_image_view(request, id):
    image = get_object_or_404(ImageFile, id=id)
    if request.method == 'POST':
        form = EditImageForm(request.POST, instance=image)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user  # Adicione o usuário ao campo 'user'
            image.save()
            messages.success(request, 'Imagem atualizada com sucesso!')
            return redirect('images')
    else:
        form = EditImageForm(instance=image)

    return render(request, 'edit/edit_image.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class ImageView(View):
    def get(self, request):
        images = ImageFile.objects.all()
        return render(request, 'images.html', {'images': images})

    def post(self, request):
        if request.FILES.get('file'):
            uploaded_file = request.FILES['file']

            allowed_mime_types = [choice[0] for choice in ImageFile.IMAGE_MIME_CHOICES]
            if uploaded_file.content_type not in allowed_mime_types:
                return HttpResponse("<span id='upload-form-alert-image' class='alert alert-error my-2'>Tipo de arquivo não suportado.</span>", status=400)

            if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
                return HttpResponse("<span id='upload-form-alert-image' class='alert alert-error my-2'>O arquivo excede o tamanho máximo de 10MB.</span>", status=400)

            try:
                # Abrir a imagem para obter metadados
                image = Image.open(uploaded_file)
                width, height = image.size
                color_depth = image.info.get('bits', 8)
                resolution = f"{width}x{height}"
                exif_data = image.getexif() or None

                # Obter o nome do arquivo a partir do arquivo carregado
                file_name = uploaded_file.name

                # Criar o objeto ImageFile
                media_file = ImageFile.objects.create(
                    user=request.user,
                    file=uploaded_file,
                    name=file_name,  # Usa o nome do arquivo do objeto `uploaded_file`
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