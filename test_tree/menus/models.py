from django.db import models


class Menu(models.Model):
    name = models.CharField("Назавание меню", max_length=50)
    description = models.TextField("Описание", blank=True, null=True)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'


class Field(models.Model):
    name = models.CharField("Назавание поля", max_length=50)
    description = models.TextField("Описание", blank=True, null=True)
    menu = models.ForeignKey(
        Menu, verbose_name='Меню', on_delete=models.PROTECT,
        related_name='fields'
    )
    is_head = models.BooleanField(
        verbose_name='Являеться ли это поле самым верхним', default=False
    )
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'


class FieldRelations(models.Model):
    parent = models.ForeignKey(
        Field, verbose_name='Родительское поле', on_delete=models.PROTECT,
        related_name='childs'
    )
    child = models.ForeignKey(
        Field, verbose_name='Дочернее поле', on_delete=models.PROTECT,
        related_name='parents'
    )
    url = models.TextField(blank=True, null=True)

    def save(self):
        """Auto creating field path."""
        field = self
        url = [str(field.child.slug)]
        if field.parent.is_head:
            url.insert(0, str(field.parent.slug))
            url.insert(0, str(field.parent.menu.slug))
        else:
            url.insert(0, str(field.parent.parents.first().url))
        self.url = '_'.join(url)
        return super(FieldRelations, self).save()

    def __str__(self):
        return f'{self.parent.name} -> {self.child.name}'

    class Meta:
        verbose_name = 'Отношениe'
        verbose_name_plural = 'Отношения полей меню друг к другу'
        constraints = [
            models.UniqueConstraint(
                fields=['parent', 'child'], name='unique_relation'
            ),
        ]
