import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.core.exceptions import ObjectDoesNotExist

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, popup, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
        popup=popup
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon)
        for pokemon_entity in pokemon_entities:
            popup = pokemon_entity.get_popup_for_map()
            add_pokemon(
                folium_map, pokemon_entity.lat, pokemon_entity.lon,
                pokemon.title, popup, request.build_absolute_uri(pokemon.image.url))
    pokemons_on_page = []
    for pokemon in pokemons:
        img_url = pokemon.get_image_path()
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
        })
    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(pokemon=requested_pokemon)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            requested_pokemon.title, request.build_absolute_uri(requested_pokemon.image.url))
    img_url = requested_pokemon.get_image_path()
    pokemon = {
        'pokemon_id': requested_pokemon.id,
        'img_url': img_url,
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
    }

    previous_evolution = requested_pokemon.previous_evolution
    if previous_evolution:
        previous_evolution_img_url = previous_evolution.get_image_path()
        pokemon['previous_evolution'] = {
            'pokemon_id': previous_evolution.id,
            'img_url': previous_evolution_img_url,
            'title_ru': previous_evolution.title,
        }

    next_evolutions = requested_pokemon.next_evolutions.all()
    if next_evolutions:
        next_evolution = next_evolutions[0]
        next_evolution_img_url = next_evolution.get_image_path()
        pokemon['next_evolution'] = {
            'pokemon_id': next_evolution.id,
            'img_url': next_evolution_img_url,
            'title_ru': next_evolution.title,
        }

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon})
