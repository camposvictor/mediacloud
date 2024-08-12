from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from core.forms import SignUpForm, EditProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from core.models import AudioFile
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from datetime import timedelta
from core.forms import EditAudioForm

@login_required
def delete_audio_view(request, id):
    if request.method == 'POST':
        audio = get_object_or_404(AudioFile, id=id)
        audio.delete()
        messages.success(request, f'Audio "{audio.name}" excluído com sucesso!')
        response = HttpResponse()
        response["HX-Redirect"] = '/audios'
        return response
    return redirect('audios')

@login_required
def edit_audio_view(request, id):
    audio = get_object_or_404(AudioFile, id=id)
    if request.method == 'POST':
        form = EditAudioForm(request.POST, instance=audio)
        if form.is_valid():
            audio = form.save(commit=False)
            audio.user = request.user
            audio.save()
            messages.success(request, 'Audio atualizada com sucesso!')
            return redirect('audios')
    else:
        form = EditAudioForm(instance=audio)

    return render(request, 'edit/edit_audio.html', {'form': form})

class AudioView(View):
    def get(self, request):
        audios = AudioFile.objects.all()
        return render(request, 'audios.html', {'audios': audios})

    def post(self, request):
        if request.FILES.get('file'):
            uploaded_file = request.FILES['file']

            if uploaded_file.size > 5 * 1024 * 1024:
                return HttpResponse("<span id='upload-form-alert-audio' class='alert alert-error my-2'>O arquivo excede o tamanho máximo de 10MB</span>", status=400)

            mime_type = uploaded_file.content_type
            if mime_type not in [choice[0] for choice in AudioFile.AUDIO_MIME_CHOICES]:
                return HttpResponse("<span id='upload-form-alert-audio' class='alert alert-error my-2'>Tipo de arquivo não suportado.</span>", status=400)


            audio_info = File(uploaded_file)
            duration = timedelta(seconds=audio_info.info.length) if audio_info else None
            bitrate = audio_info.info.bitrate if audio_info else None
            sample_rate = audio_info.info.sample_rate if audio_info else None
            channels = audio_info.info.channels if audio_info else None

            file_name = uploaded_file.name

            audio_file = AudioFile.objects.create(
                user=request.user,
                file=uploaded_file,
                mime_type=mime_type,
                duration=duration,
                bitrate=bitrate,
                sample_rate=sample_rate,
                channels=channels,
                name=file_name,
                description=request.POST.get('description', ''),
                genre=request.POST.get('genre', ''),
                tags=request.POST.get('tags', ''),
            )
            messages.success(request, f"{audio_file.get_file_name()} carregado com sucesso")
            response = HttpResponse()
            response["HX-Redirect"] = '/'
            return response

        return HttpResponse("<span id='upload-form-alert-audio' class='alert alert-error my-2'>Ocorreu um erro inesperado.</span>", status=400)
