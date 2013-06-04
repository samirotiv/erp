#This will store all our utility functions

# _____________--- CORE CHECK FUNCTION ---______________#
def core_check (user):
    loginuser = user.get_profile()
    return loginuser.status == 2

def core_or_supercoord_check (user):
    loginuser = user.get_profile()
    return ((loginuser.status == 2) or (loginuser.status == 1))

