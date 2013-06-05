#This will store all our utility functions

# _____________--- CORE CHECK FUNCTION ---______________#
def core_check (user):
    return user.get_profile().status == 2

def core_or_supercoord_check (user):
    return user.get_profile().status == 2 or user.get_profile().status == 1

