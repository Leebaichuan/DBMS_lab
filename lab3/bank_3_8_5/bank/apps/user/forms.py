# apps/user/forms.py: stores the form class for User Append 
#                       and User UpdateProfile
from django import forms
from .models import User

# the form to record the info to append user
# requires: User,ModelForm
class UserAppendForm(forms.ModelForm):
    
    # the User model
    class Meta:
        model = User
        fields = ( 'ID', 'Name', 'PhoneNum', 'Address', \
        'Contact_Name', 'Contact_PhoneNum', 'Contact_Email' )

    # save this form
    def save(self, commit = True):
        # Save the provided password in hashed format
        user = super().save(commit = False)
        if commit:
            user.save()
        return user
