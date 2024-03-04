from rest_framework.exceptions import ValidationError


class LinkValidator:
    def __init__(self, allowed_domains=None):
        if allowed_domains is None:
            allowed_domains = ['https://www.youtube.com/']
        self.allowed_domains = allowed_domains

    def __call__(self, value):
        if not any(domain in value for domain in self.allowed_domains):
            raise ValidationError('Запрещено использовать ссылки на ресурсы, кроме разрешенных доменов.')
