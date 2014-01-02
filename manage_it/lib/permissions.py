 
def user_in_groups(user, groups_names):
    return user.groups.filter(name__in=groups_names)
