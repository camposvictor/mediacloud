from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from core.forms import SignUpForm, EditProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.forms import MediaFileForm
from core.models import MediaFile
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


