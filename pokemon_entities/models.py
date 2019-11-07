from django.db import models


class Pokemon (models.Model):
    title = models.CharField('название', max_length=200)
    title_en = models.CharField('название на английском', max_length=200, blank=True, null=True)
    title_jp = models.CharField('название на японском', max_length=200, blank=True, null=True)
    image = models.ImageField('картинка', blank=True, null=True)
    description = models.TextField('описание', blank=True, null=True)
    previous_evolution = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='из кого жволюционировал',
                                           blank=True, null=True, related_name='next_evolutions')

    def __str__(self):
        return self.title

    def get_image_path(self):
        img_url = ''
        if self.image:
            img_url = self.image.url
        return img_url


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='покемон',)
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
