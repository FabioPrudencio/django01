from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login,
    update_session_auth_hash
    )
from django.contrib.auth.forms import (
    UserChangeForm, 
    UserCreationForm, 
    PasswordChangeForm
    )

from .models import Note, Responsavel
from .forms import (
    NoteForm,
    EditProfileForm,
    RegisterProfileForm,
    ResponsavelForm
    )


#@login_required(login_url='notes:login')
def Lista(request):
    latest_question_list = Note.objects.order_by('data')
    context = {'testeq': latest_question_list}
    return render(request, 'notes/lista.html', context)

def Home(request):
	return render(request, 'notes/home.html', {})

def Cadastra(request):
	if request.method == 'POST':
		form = NoteForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect('notes:lista')

	else:
		form = NoteForm()

	return render(request, 'notes/edita.html', {'form': form})

def Edita(request, pk):	
	NoteEdit = get_object_or_404(Note, pk=pk)
	if request.method == 'POST':
		form = NoteForm(request.POST, instance=NoteEdit)

		if form.is_valid():
			form.save()
			return redirect('notes:detalhe', pk=pk)

	else:
		form = NoteForm(instance=NoteEdit)

	return render(request, 'notes/edita.html', {'form': form})

def Detalhe(request, pk):
    NoteDetail = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/detalhe.html', {'notes': NoteDetail})

def Delete(request, pk):
    note = get_object_or_404(Note, pk=pk)    
    if request.method=='POST':
        note.delete()
        return redirect('notes:lista')


    return render(request, 'notes/delete.html', {'note':note})

def Profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/profile.html', args)

def Edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('notes:profile')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)

def Register(request):
    if request.method == 'POST':
        form = RegisterProfileForm(request.POST)
        if form.is_valid():
            form.save()

            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('notes:profile')            
                
        args = {'form': form}
        return render(request,'accounts/register.html', args)
        
    else:
        form = RegisterProfileForm()
        args = {'form': form}
        return render(request,'accounts/register.html', args)

def Change_Password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('notes:profile')
        else:
            args = {'form': form}
            return render(request,'accounts/change_password.html', args)


    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)

def Add_Responsavel(request):
    if request.method == 'POST':
        form = ResponsavelForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('notes:home')

    else:
        form = ResponsavelForm()

    return render(request, 'notes/responsavel.html', {'form': form})

def Edit_Responsavel(request, pk): 
    ResponsavelEdit = get_object_or_404(Responsavel, pk=pk)
    if request.method == 'POST':
        form = ResponsavelForm(request.POST, instance=ResponsavelEdit)

        if form.is_valid():
            form.save()
            return redirect('notes:home', pk=pk)

    else:
        form = ResponsavelForm(instance=ResponsavelEdit)

    return render(request, 'notes/responsavel.html', {'form': form})