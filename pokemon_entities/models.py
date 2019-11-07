from django.db import models


class Pokemon(models.Model):
    title = models.CharField('название', max_length=200)
    title_en = models.CharField('название на английском', max_length=200, blank=True, null=True)
    title_jp = models.CharField('название на японском', max_length=200, blank=True, null=True)
    image = models.ImageField('картинка', blank=True, null=True)
    description = models.TextField('описание', blank=True, null=True)
    previous_evolution = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='из кого жволюционировал',
                                           blank=True, null=True, related_name='next_evolutions')
    element_type = models.ManyToManyField("PokemonElementType", verbose_name='стихия', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_image_path(self):
        img_url = ''
        if self.image:
            img_url = self.image.url
        return img_url


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='покемон', )
    lat = models.FloatField('широта')
    lon = models.FloatField('долгота')
    appeared_at = models.DateTimeField('появился', default=None, blank=True, null=True)
    disappeared_at = models.DateTimeField('исчезнет', default=None, blank=True, null=True)
    level = models.PositiveIntegerField('уровень', blank=True, null=True)
    health = models.PositiveIntegerField('здоровье', blank=True, null=True)
    strength = models.PositiveIntegerField('сила', blank=True, null=True)
    defence = models.PositiveIntegerField('защита', blank=True, null=True)
    stamina = models.PositiveIntegerField('выносливость', blank=True, null=True)

    def __str__(self):
        return f'{self.pokemon.title} появился на широте {self.lat} и долготе {self.lon}'

    def get_popup_for_map(self):
        popup = ''
        if self.level:
            popup += f'Уровень:{self.level} \n'
        else:
            popup += f'Уровень: неизвестен \n'
        if self.health:
            popup += f'Здоровье:{self.health} \n'
        else:
            popup += f'Здоровье: неизвестно \n'
        if self.strength:
            popup += f'Сила:{self.strength} \n'
        else:
            popup += f'Сила: неизвестна \n'
        if self.defence:
            popup += f'Защита:{self.defence} \n'
        else:
            popup += f'Защита: неизвестна \n'
        if self.stamina:
            popup += f'Выносливость:{self.stamina} \n'
        else:
            popup += f'Выносливость: неизвестна \n'
        return popup


class PokemonElementType(models.Model):
    title = models.CharField('название', max_length=200)

    def __str__(self):
        return self.title
