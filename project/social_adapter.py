from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def new_user(self, request, sociallogin):
        User = get_user_model()
        email = sociallogin.email_addresses[0]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = super().new_user(request, sociallogin)

        return user

    # def populate_user(self, request, sociallogin, data):
    #     email = data.get('email')
    #     data['username'] = email[0: email.index('@')]
    #     return super().populate_user(request, sociallogin, data)

    def is_auto_signup_allowed(self, request, sociallogin):
        '''
        Since all emails that are registered on Labrary are from Labcodes
        All of then, by definition, are verified
        '''
        return True

class CustomAccountAdapter(DefaultAccountAdapter):
    def populate_username(self, request, user):
        """
        Fills in a valid username, if required and missing.  If the
        username is already present it is assumed to be valid
        (unique).
        """
        from allauth.account.utils import user_email, user_username

        email = user_email(user)
        user_username(
                user, email[0: email.index('@')]
            )
