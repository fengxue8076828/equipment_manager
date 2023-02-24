from django.contrib.auth.forms import AuthenticationForm

class CustomedAuthenticationForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        


