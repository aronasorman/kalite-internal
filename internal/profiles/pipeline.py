# used to associate extra_data from github to the user, mainly
# for the gravatar

def set_user_gravatar(backend, details, response, uid,
                      user, social_user, *args, **kwargs):
    avatar = social_user.extra_data['avatar']
    user.avatar = avatar
    user.save()
