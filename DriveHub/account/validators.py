from django.utils.translation import ngettext
from django.contrib.auth.password_validation import MinimumLengthValidator

class CustomMinimumLengthValidator(MinimumLengthValidator):
    def __init__(self, min_length=8):
        self.min_length = min_length
        super().__init__(min_length=self.min_length)
        

    def get_error_message(self):
        return ngettext(
            "Password must contain at least %(min_length)d character.",
            "Password must contain at least %(min_length)d characters.",
            self.min_length,
        ) % {"min_length": self.min_length}