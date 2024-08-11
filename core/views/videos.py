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
from io import BytesIO
from django.core.files.base import ContentFile
import random
from PIL import Image
import numpy as np


@method_decorator(login_required, name="dispatch")
class VideoView(View):
    def get(self, request):
        videos = VideoFile.objects.all()
        return render(request, 'videos.html', {'videos': videos})

    def post(self, request):
        if request.FILES.get("file"):
            uploaded_file = request.FILES["file"]

            # Verifica o tipo MIME permitido
            allowed_mime_types = [choice[0] for choice in VideoFile.VIDEO_MIME_CHOICES]
            if uploaded_file.content_type not in allowed_mime_types:
                return HttpResponse(
                    "<span id='upload-form-alert-video' class='alert alert-error my-2'>Tipo de arquivo não suportado.</span>",
                    status=400,
                )

            # Verifica o tamanho do arquivo
            if uploaded_file.size > 5 * 1024 * 1024:  # 5MB
                return HttpResponse(
                    "<span id='upload-form-alert-video' class='alert alert-error my-2'>O arquivo excede o tamanho máximo de 5MB.</span>",
                    status=400,
                )

            try:
                clip = VideoFileClip(uploaded_file.temporary_file_path())
                duration = clip.duration  # Duração em segundos
                resolution = f"{clip.size[0]}x{clip.size[1]}"
                frame_rate = clip.fps

                # Convertendo duração para timedelta
                duration_timedelta = timedelta(seconds=duration)

                # Gerando a thumbnail de um frame aleatório
                frame_time = random.uniform(0, duration)
                frame = clip.get_frame(frame_time)

                # Converte o frame em uma imagem e salva como thumbnail
                thumbnail_image = Image.fromarray(
                    np.uint8(frame)
                )  # Converte o frame para uint8
                thumbnail_io = BytesIO()
                thumbnail_image.save(thumbnail_io, format="JPEG")
                thumbnail_file = ContentFile(
                    thumbnail_io.getvalue(), name=f"{uploaded_file.name}_thumbnail.jpg"
                )

                # Criação da instância de VideoFile
                media_file = VideoFile.objects.create(
                    user=request.user,
                    file=uploaded_file,
                    description=request.POST.get(
                        "description", ""
                    ),  # Obtém a descrição se disponível
                    tags=request.POST.get("tags", ""),  # Obtém as tags se disponíveis
                    mime_type=uploaded_file.content_type,
                    duration=duration_timedelta,  # Armazena como timedelta
                    resolution=resolution,
                    frame_rate=frame_rate,
                    video_codec="unknown",
                    audio_codec="unknown",
                    bitrate=0,
                    genre=request.POST.get("genre", ""),  # Obtém o gênero se disponível
                    thumbnail_file=thumbnail_file,
                )
                messages.success(
                    request, f"{media_file.get_file_name()} carregado com sucesso."
                )
                response = HttpResponse()
                response["HX-Redirect"] = "/"
                return response

            except Exception as e:
                return HttpResponse(
                    f"<span id='upload-form-alert-video' class='alert alert-error my-2'>Erro ao processar o vídeo: {str(e)}</span>",
                    status=500,
                )

        return HttpResponse(
            "<span id='upload-form-alert-video' class='alert alert-error my-2'>Ocorreu um erro inesperado.</span>",
            status=400,
        )
