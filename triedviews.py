def save_reporter(request):
    user = request.POST.get('id')
    print user
    userprofile = UserProfile.objects.get(user=user)
    form = ReporterRegisterForm()
    profileform = ProfilecontactForm(instance=userprofile)

    if request.method == 'POST':        
        form = ReporterRegisterForm(request.POST, instance=user) 
        profileform = ProfilecontactForm(request.POST,instance = userprofile)
        if form.is_valid() and profileform.is_valid(): 
            form.save()
            profilesave = profileform.save(commit=False)            
            profilesave.save()
    return render(request, 'setting/edit_reporter.html',
                   {'form': form,
                     'profile':profileform
                    })
