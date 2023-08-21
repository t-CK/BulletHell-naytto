## world.py
Ei sisällä vielä paljoa, ajatus oli että tänne olisi saattanut tulla niin levelin taustaa kuin esim. liikkumiseen vaikuttavia tai damagea tekeviä objecteja levelistä. Nyt vasta vain eka testailuclassi, joka blokkaa pelaajan ja tietyt viholliset. Ei suoranaista grafiikkaa, pelkkä punainen suorakulmio.

### class World (Pygame Sprite)
##### docstring
    World object such as an obstacle or a special area of the level
    [pos_x] and [pos_y] are coordinates for the top left corner, sizes are the  
    sides down and right from that point. If [solid] is True, will be impassable.
---
##### muuttujat, funktiot ym.
    __init__:
    pos_x, pos_y, size_x, size_y
        Objektin vasemman yläkulman (x,y), leveys, korkeus
    solid (True)
        Jos solid on True, lisätään groupiin, jota vastaan tsekataan movement collision
---
#### Käyttöesimerkit:

Spawnaa 300x400-pikselinen este, jonka yläkulma on koordinaatissa (100,200):
    
    World(100, 200, 300, 400) 

Spawnaa 50x50-pikselinen este satunnaiseen kohtaan ruudun reunan ulkopuolelle:

    World(*misc.get_spawn(), 50, 50)
    
Spawnaa este playerin päälle ja poista se (Huom. miten playeria kutsutaankaan sieltä, missä käytät. Tällä hetkellä tosin movement collision vain heittäisi pelaajan liikkuessa ulos esteen sisältä, ellei sitä nimenomaan poista heti.)

    obstacle = World(*player.rect.topleft, *player.rect.size)
    obstacle.kill()