import re
from django.core import exceptions
from django.utils.translation import gettext as _


class SanityValidator:

    def validate(self, password, user=None):
        upper_reg = r'\w*[A-Z]\w*'
        lower_reg = r'\w*[a-z]\w*'
        if not ((len(password) >= 8) and
            (bool(re.match(upper_reg, password))) and
            (bool(re.match(lower_reg, password)))):
            raise exceptions.ValidationError(_("Password should contain atleast 1 uppercase, 1 lowercase and "
                                             "comprise of 8 in length."), code='password_not_accepted')

        def get_help_text(self):
            return _("Password should contain atleast 1 uppercase, 1 lowercase and "
                                             "comprise of 8 in length.")
