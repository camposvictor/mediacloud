from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, EditProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MediaFileForm
from .models import MediaFile
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


@login_required
def dashboard(request):
    media_files = MediaFile.objects.all()
    media_type = request.GET.get('type')
    if media_type:
        media_files = media_files.filter(media_type=media_type)
    return render(request, 'dashboard.html', {'media_files': media_files})

@login_required
def videos(request):
    return render(request, 'videos.html')

@login_required
def images(request):
   images = MediaFile.objects.filter(media_type='image')
   print(images)
   return render(request, 'images.html', {'images': images})

@login_required
def audios(request):
    return render(request, 'audios.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'auth/register.html', {'form': form})

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('dashboard')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'auth/edit_profile.html', {'form': form})

def upload_media_view(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        if uploaded_file.size > 5 * 1024 * 1024:
            return HttpResponse("<span id='upload-form-alert' class='alert alert-error my-2'>O arquivo excede o tamanho máximo de 10MB", status=400)
        if uploaded_file.content_type.startswith('image/'):
            media_type = 'image'
        elif uploaded_file.content_type.startswith('audio/'):
            media_type = 'audio'
        elif uploaded_file.content_type.startswith('video/'):
            media_type = 'video'
        else:
            return HttpResponse("<span id='upload-form-alert' class='alert alert-error my-2'>Tipo de arquivo não suportado.</span>", status=400)

        media_file = MediaFile.objects.create(
            user=request.user,
            file=uploaded_file,
            media_type=media_type
        )

        messages.success(request, f"{media_file.get_file_name()} carregado com sucesso")
        response = HttpResponse()
        response["HX-Redirect"] = '/'
        return response

    return HttpResponse("<span id='upload-form-alert' class='alert alert-error my-2'>Ocorreu um erro inesperado.", status=400)


@login_required
def edit_media_view(request, pk):
    media_file = get_object_or_404(MediaFile, pk=pk)
    if request.user != media_file.user:
        messages.error(request, 'Você não tem permissão para editar este arquivo.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES, instance=media_file)
        if form.is_valid():
            form.save()
            messages.success(request, 'Arquivo atualizado com sucesso!')
            return redirect('dashboard')
    else:
        form = MediaFileForm(instance=media_file)
    return render(request, 'edit_media.html', {'form': form})

@login_required
def delete_media_view(request, pk):
    media_file = get_object_or_404(MediaFile, pk=pk)
    if request.user == media_file.user:
        media_file.delete()
        messages.success(request, 'Arquivo excluído com sucesso!')
    else:
        messages.error(request, 'Você não tem permissão para excluir este arquivo.')
    return redirect('dashboard')

@login_required
def view_media_view(request, pk):
    media_file = get_object_or_404(MediaFile, pk=pk)
    if request.user != media_file.user:
        messages.error(request, 'Você não tem permissão para visualizar este arquivo.')
        return redirect('dashboard')
    return render(request, 'view_media.html', {'media_file': media_file})

@login_required
def search_media_view(request):
    query = request.GET.get('q')
    media_type = request.GET.get('type')
    if query:
        media_files = MediaFile.objects.filter(
            Q(description__icontains=query) |
            Q(file__icontains=query) |
            Q(tags__icontains=query)
        )
        if media_type:
            media_files = media_files.filter(media_type=media_type)
    else:
        media_files = MediaFile.objects.all()
        if media_type:
            media_files = media_files.filter(media_type=media_type)

    return render(request, 'search_results.html', {'media_files': media_files})

@login_required
def list_media_view(request):
    media_files = MediaFile.objects.all()
    media_type = request.GET.get('type')
    if media_type:
        media_files = media_files.filter(media_type=media_type)
    return render(request, 'list_media.html', {'media_files': media_files})


