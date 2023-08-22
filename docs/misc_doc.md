## misc.py
Sekalaisia apufunktioita, joita muut classit käyttävät, ja joille en keksinyt parempaa tiedostonimeä tai classia.

---
### get_closest_enemy(position):
> Return enemy Sprite closest to passed point or Sprite (or player by default)

Parametri position voi olla kokonaislukupari (x,y) tuplena, tai Sprite. Spriten tapauksessa koordinaatit otetaan Rect:in keskipisteestä. Jos parametria ei anneta tai se on None, otetaan siihen pelaajan keskipisteen koordinaatit.

Funktio palauttaa enemy_groupista Spriten, jonka Rectin keskipiste on lähimpänä annettua pistettä. Jos enemy_group on tyhjä, palautuu None.

#### Käyttöesimerkit:
Palauta pelaajaa lähimpänä oleva vihollis-Sprite:  
`get_closest_enemy()`

Tuhoa ruudun vasenta yläkulmaa lähin vihollis-Sprite:  
`get_closest_enemy((0,0)).kill()`

---
### get_random_enemy():
> Return a random enemy Sprite (or None)

Palauttaa satunnaisen Spriten enemy_groupista. Jos group on tyhjä, palauttaa None.

---
### get_distance(point1, point2):
> Return distance between two tuples or Sprites' centers

Ottaa parametreinä 1-2 tuplea (x,y) tai Spritea. Spritejen tapauksessa käytetään Rectin keskipistettä. Palauttaa pisteiden välisen etäisyyden.

---
### get_step(origin, target, speed):
> Return a tuple for movement from [origin] to [target] at [speed] pixels per tick

Parametrit origin ja target voivat olla tupleja (x,y) tai Spriteja. Speedin oletusarvo on 1. Palauttaa vektorin v, jolla vektori `origin + v` on `speed` pikseliä lähempänä vektoria `target` kuin vektori `origin`. _(Ainakin noin teoriassa näin. Koska pygamen Rectit käyttävät kokonaislukuja, varsinkin pienellä speedillä suunta on epätarkka, ja alle 1:n speedillä ei varmasti toimi ainakaan toivotusti, jos ollenkaan)_

#### Käyttöesimerkit:  
Siirrä pygame-Spritea sprite oletusarvon eli 1 pikselin verran kohti pelaajaa:  
`sprite.rect.move_ip(get_step(sprite, player))`

Tallenna muuttujaan foo piste, joka on pelaajasta 30 pikseliä kohti ruudun vasenta yläreunaa:  
`foo = get_step(player, (0,0), 30)`

---
### get_step_p(vector, speed, inverse):
> Take a vector and return a perpendicular vector of length speed. 
    
Ottaa parametrinä tuplen (x,y), nopeuden (oletus 1) ja booleanin inverse (oletuksena False). Palauttaa get_step:in tapaan "liikevektorin" nopeudella `speed`, mutta parametrinä annetulle vektorille poikkisuuntaisena, eli käännettynä 90 asteella. Poikkisuuntaisia vektoreitahan on 2-ulotteisessa avaruudessa aina kaksi, ja jos `inverse` on True, palautetaan toinen niistä.

#### Käyttöesimerkit:
Käännä vektoria (1, 0) 90 astetta oikealle (eli palauta tuple (0, -1)):  
`get_step_p((1, 0))`

Siirrä Spritea `s` noin 10 pikseliä oikealle pelaajaan `player` nähden:  
`s.rect.move_ip(get_step_p(get_step(s, player), 10)`

Siirrä Spritea `s` noin 10 pikseliä vasemmalle pelaajaan `player` nähden:  
`s.rect.move_ip(get_step_p(get_step(s, player), 10, True)`

---
### get_spawn(side, distance):
> Returns a tuple of a random point a bit off-screen.

Palauttaa satunnaisen tuplen (x,y), `distance` (oletuksena 50) pikseliä ruudun reunojen ulkopuolella. Parametri `side` on kokonaisluku väliltä 0-3 (tai oletusarvolla None valitaan satunnaisesti), ja vastaa ikkunan reunoja seuraavasti:

	0: Yläreuna
	1: Oikea
	2: Alareuna
	3: Vasen

#### Käyttöesimerkit:
Spawnaa Enemy_Follow satunnaiselle puolelle _(tämä on tosin oletusarvo, joten pelkkä `Enemy_Follow(game)` riittää)_:  
`Enemy_Follow(game, get_spawn())`