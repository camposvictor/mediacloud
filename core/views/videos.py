from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from core.forms import SignUpForm, EditProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from core.models import VideoFile
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from moviepy.editor import VideoFileClip
from datetime import timedelta
import ffmpeg

@method_decorator(login_required, name='dispatch')
class VideoView(View):
    def get(self, request):
        return render(request, 'videos.html')

    def post(self, request):
        if request.FILES.get('file'):
            uploaded_file = request.FILES['file']

            # Verifica o tipo MIME permitido
            allowed_mime_types = [choice[0] for choice in VideoFile.VIDEO_MIME_CHOICES]
            if uploaded_file.content_type not in allowed_mime_types:
                return HttpResponse("<span id='upload-form-alert-video' class='alert alert-error my-2'>Tipo de arquivo não suportado.</span>", status=400)

            # Verifica o tamanho do arquivo
            if uploaded_file.size > 5 * 1024 * 1024:  # 5MB
                return HttpResponse("<span id='upload-form-alert-video' class='alert alert-error my-2'>O arquivo excede o tamanho máximo de 5MB.</span>", status=400)

            try:
                # Usando moviepy para extrair propriedades do vídeo
                clip = VideoFileClip(uploaded_file.temporary_file_path())
                duration = clip.duration  # Duração em segundos (float)
                resolution = f"{clip.size[0]}x{clip.size[1]}"
                frame_rate = clip.fps

                # Convertendo duração para timedelta
                duration_timedelta = timedelta(seconds=duration)


                # Criação da instância de VideoFile
                media_file = VideoFile.objects.create(
                    user=request.user,
                    file=uploaded_file,
                    description=request.POST.get('description', ''),  # Obtém a descrição se disponível
                    tags=request.POST.get('tags', ''),  # Obtém as tags se disponíveis
                    mime_type=uploaded_file.content_type,
                    duration=duration_timedelta,  # Armazena como timedelta
                    resolution=resolution,
                    frame_rate=frame_rate,
                    video_codec='unknown',
                    audio_codec='unknown',
                    bitrate=0,
                    genre=request.POST.get('genre', '')  # Obtém o gênero se disponível
                )
                messages.success(request, f"{media_file.get_file_name()} carregado com sucesso.")
                response = HttpResponse()
                response["HX-Redirect"] = '/'
                return response

            except Exception as e:
                return HttpResponse(f"<span id='upload-form-alert-video' class='alert alert-error my-2'>Erro ao processar o vídeo: {str(e)}</span>", status=500)

        return HttpResponse("<span id='upload-form-alert-video' class='alert alert-error my-2'>Ocorreu um erro inesperado.</span>", status=400)
