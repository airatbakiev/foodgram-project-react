from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import UniqueConstraint


class UserRoles:
    USER = 'user'
    ADMIN = 'admin'
    USER_ROLES = (
        (USER, USER),
        (ADMIN, ADMIN),
    )


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта',
    )
    role = models.CharField(
        max_length=9,
        choices=UserRoles.USER_ROLES,
        default=UserRoles.USER,
        verbose_name='Права доступа',
    )
    confirmation_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Код подтверждения',
    )
    username = models.CharField(
        unique=True,
        max_length=150,
        validators=[RegexValidator(r'^[\w.@+-]')],
        verbose_name='Ник пользователя',
    )
    first_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name='Фамилия',
    )

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'
        constraints = [
            UniqueConstraint(fields=['email', ], name='email'),
            UniqueConstraint(fields=['username', ], name='username')
        ]

    @property
    def is_admin(self):
        return (
            self.role == UserRoles.ADMIN
            or self.is_staff or self.is_superuser
        )

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    def __str__(self):
        return self.username