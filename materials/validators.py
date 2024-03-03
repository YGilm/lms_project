from rest_framework.serializers import ValidationError


class LinkValidator:
    """Проверяем вхождения сторонних ссылок в поля"""

    def __init__(self, allowed_domain):
        if not allowed_domain:
            raise ValueError("Необходимо указать домен для валидации")
        self.allowed_domain = allowed_domain

    def __call__(self, value):
        if not value:
            return

        if isinstance(value, str) and self.allowed_domain not in value:
            raise ValidationError(f"Ссылка должна принадлежать домену {self.allowed_domain}")
