def index(request):
    """profile settings screen
       User can adjust all profile fields
    """
    user = request.user
    userprofile = UserProfile.objects.get(user=user)
    profile = request.user.get_profile()                #get profile profile data
    form = UserProfileForm(instance=profile)
    userform = UserForm(instance=user)    
    createprofileform = UserCreateProfileForm()
    registerform = UserRegisterForm()
    member = Members()                                # To list out authorized members
    member_list = Members.objects.filter(user=user).select_related("member")
    
    list = []
    is_member_screen = False
    # save
    member_save_msg = ''
    profile_save_msg = ''
    pwd_error = ''
    form_error = False
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('setting.views.index')
        if 'delete' in request.POST:
            Members.objects.filter(id=request.POST['delete']).delete()
            User.objects.filter(id=request.POST['delete']).delete()
            UserProfile.objects.filter(id=request.POST['delete']).delete()                            
        if 'password' in request.POST:
            registerform = UserRegisterForm(request.POST)
            createprofileform = UserCreateProfileForm(request.POST)                            
            if registerform.is_valid() and createprofileform.is_valid():
                username = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10)) #To create random string
                result = registerform.save(commit=False)
                result.set_password(request.POST['password'])        #set member password
                result.username = username               
                result.save()
                member.user_id = user.id
                member.member_id = result.id
                member.save()                                        #new member registration
                member_profile = UserProfile.objects.get(user=result.id)
                createprofileform = UserCreateProfileForm(request.POST, instance=member_profile)
                createprofileform.save()                             #create member profile                
                createprofileform = UserCreateProfileForm()
                registerform = UserRegisterForm()
                member_save_msg = 'New member has been added.'           
            is_member_screen = True                   
        elif 'reset_password' in request.POST:
            try:
                check_user = authenticate(username=user, password=request.POST['old_password'])
                if request.POST['reset_password'].strip() and check_user.id:
                    saveuser = User.objects.get(id=user.id)
                    saveuser.set_password(request.POST['reset_password'])
                    saveuser.save()
                    userform = UserForm(instance=saveuser)
                    profile_save_msg = "Your password has been updated."
                else:
                    pwd_error = "Please enter valid password."
            except:
                pwd_error = "Please enter valid password."
        else:
            form = UserProfileForm(request.POST, instance=profile)
            userform = UserForm(request.POST, instance=user)
            if form.is_valid() and userform.is_valid():
                form.save()
                saveuser = userform.save(commit=False)
                saveuser.save()
                profile_save_msg = 'Your details have been saved.'
            else:
                form_error = True
    for members in member_list:
        try:
            member_profile = UserProfile.objects.get(user=members.member.id)
            list.append((members.member, member_profile))       
        except UserProfile.DoesNotExist:
            pass
    form = UserProfileForm(instance=profile)    
    return render(request, 'setting/index.html',
        {'body_class': 'overall-sec-report',
         'layout': 'cols_content_full_width',
         'about_menu': True,
         'security_tab': True,
         'user': user,
         'profile': profile,
         'userprofile':userprofile, 
         'form': form,
         'registerform': registerform,
         'createprofile': createprofileform,
         'userform': userform,
         'profile_save_msg': profile_save_msg,
         'member_save_msg': member_save_msg,
         'member_list': list,
         'form_error': form_error,
         'is_member_screen': is_member_screen,
         'pwd_error': pwd_error
        })
