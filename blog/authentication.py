from django.contrib.auth.models import User

class EmailAuthbackend(object):
    print('yahan bhi ok hai')
    def authenticate(self, request, username=None , password=None, **kwargs):
        try:
            print('yahan ok hai')
            user=User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None


    def get_user(self,user_id):
        print('get_user ke andar')
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            print('yeh waala none')
            return None
