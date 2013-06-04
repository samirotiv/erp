#This will store all our utility functions

# _____________--- CORE CHECK FUNCTION ---______________#
def core_check (user):
    loginuser = user.get_profile()
    if loginuser.status == '2':
        return True
    else:
        return False

def core_or_supercoord_check (user):
    loginuser = user.get_profile()
    if ((loginuser.status == '2') or (loginuser.status == '1')):
        return True
    else:
        return False

