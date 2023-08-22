## weapons.py
Aseiden luokka. Sisältää classien lisäksi yhden funktion, joka ei ole minkään classin alla 
(vaikka voisikin olla loogisempi Bullet_Orbitissa). Osa classeista vaatii game-instanssilta
attribuutin ticks, joka voisi tavallaan olla mikä vain kierros kierrokselta kasvava luku.

---
### class Bullet (Pygame Sprite)
Bullettien pääluokka. Itsessään ei järin hyödyllinen, mutta lisää perivät objektit 
groupeihin ja laskee update():ssa `ttl`-muuttujaa yhdellä (ja `kill()`:aa Spriten tarvittaessa).

##### docstring
	Parent class for bullets
---	
##### muuttujat
	ttl
		Time to live, main loop -kierroksina. Jos > 0, vähentyy yhdellä joka 
		update()-kutsulla ja pudotessa nollaan Bullet poistetaan. Jos 0 tai 
		negatiivinen, Bullet ei katoa ajan kanssa.
---
##### funktiot ja parametrit
```
__init__(self):
    Lisää objekti bullet_group ja all_sprites -groupeihin, luo Pygamen Surface 
    ja Rect, ja alusta ttl nollaksi (jotta Bullet yksinään kutsuttuna ei heitä
    erroria, vaikka perivät luokat määrittävätkin omat ttl:nsä)
```
```
update(self):
    Laske ttl:ää yhdellä, ja tarvittaessa kutsu Sprite.kill().
```


---
### class Bullet_Line (perii Bulletin)
Suoraa pitkin kulkeva Bullet. Spawnaa pisteeseen `origin` ja kulkee (suurinpiirtein) pisteen
`target` läpi nopeudella `speed` pikseliä per loop. Molemmat `origin`/`target` voivat olla
myös Pygamen Spriteja, jolloin käytetään tämän Rectin keskipistettä. Parametrien 
puuttuessa (tai ollessa None) otetaan originiksi pelaaja, ja targetiksi originia lähin vihollinen.

##### docstring
	Bullet flying in a straight line

    Takes two points as tuples or Sprites, spawns at [origin] and follows a line going
    through [target]. Flies at [speed] pixels per tick for [ttl] (time to live) ticks.
    A ttl of <= 0 makes the bullet not despawn.

    NOTE: Will not register collision when passing through an enemy in a single tick.
---
##### muuttujat
	origin (None), target (None)
		Lähtöpiste ja kohde, jonka läpi kuljetaan. Voi olla tupleja, Spriteja, tai None (kts. kuvaus).
	ttl (60)
		Time to live. Kts. luokka Bullet. Erona tämä class antaa defaultina ttl:n 60 eikä 0.
	speed (5)
		Nopeus (suurinpiirtein) pikseliä/kierros. Laskutapa ja pyöristykset aiheuttavat epätarkkuutta.
	step
		Askel, jolla Rectiä liikutetaan joka kierroksella. Arvo on suoraan misc.get_step(origin, target, speed)
---
##### funktiot ja parametrit
```
__init__(self, game, target, origin, ttl, speed):
    Kts. muuttujat yllä
```
```
update(self):
    Kutsu parentin updatea (ttl:n takia) ja liiku yksi step
```
---
##### käyttöesimerkki

Ammu esim. main loopissa 100 kierroksen välein oletusarvoinen Bullet_Line
pelaajasta kohti lähintä vihollista:  
_(olettaen, että self on instanssi pelistä, jolla on attribuutti ticks, ja weapons.py on importattu)_
```
if self.ticks % 100:
    weapons.Bullet_Line(self)
```


---
### class Bullet_Orbit (perii Bulletin)
Pisteen tai toisen Spriten ympärillä kehää kiertävä bullet.

##### docstring
    Bullet object circling a constant point at (x,y) or a Sprite (defaults to player).

    Speed-attribute (inversely) affects time to do a complete circle, thus the velocity of
    the projectile depends on [radius] as well as [speed]. Despawns after [ttl] ticks (unless ttl <= 0).
    Offset is a tuple of (x,y,X,Y), where x/y scale and X/Y skew the circle, allowing for ellipses.
---
##### muuttujat
    radius (100)
        Ympyrän, jota bullet seuraa, säde pikseleissä (ennen offsetia)
    speed (30)
        Käänteinen kiertonopeus, eli suuremmilla luvuilla kierto on hitaampaa.
        Vaikuttaa aikaan, jossa kokonainen kierros tehdään, joten varsinainen hetkellinen
        nopeus riippuu myös säteestä.
    center
        Piste, jota kierretään. Päivitetään update():ssa, jos center_object on Sprite.
        Ei ole päivitetty huomioimaan map scrollingia, joten tuplena käytännössä
        liikkuu pelaajan mukana.
    x_scale (1), y_scale (1)
        Kertoimet ympyrän x- ja y-koordinaateille, eli jos x_scale != y_scale,
        ympyrä onkin ellipsi.
    x_offset (0), y_offset (0)
        Luku, joka lisätään ticks-lukuun, joista otetaan sin (x:ssä) ja cos (y:ssä),
        joilla voi siis tehdä mm. ellipsejä muutenkin kuin x- ja y-akseleiden suuntaisesti.
        
        Jos x_offset == y_offset, kiertää samaa rataa kuin jos molemmat ovat 0 (tai 
        jaollisia 2*pii:llä), mutta eri kohdassa.
---
##### funktiot ja parametrit
```
__init__(self, game, center_object, radius, speed, ttl, offset):
    center_object
        Tuple (x,y) tai Sprite, jota bullet kiertää. Oletuksena None, jolloin muutetaan
        seuraamaan pelaajaa.
    offset (1,1,0,0)
        Neljän alkion tuple tai lista, josta otetaan (järjestyksessä) arvot
        muuttujiin x_scale, y_scale, x_offset ja y_offset
```
```
update(self):
    Jos bullet kiertää Spritea, tarkista Rectin keskipiste ja päivitä center. Päivitä oma Rect.
    
    center
        Koordinaattituple pisteestä, jota kierretään. Tämä tarvitaan erillisenä
        muuttujana siltä varalta, että initin center_object on Sprite.
```
##### käyttöesimerkit
Spawnaa oletusarvoinen bullet kiertämään pelaajaa: `Bullet_Orbit(game)`

Spawnaa bullet, joka lentää pelaajasta vaakasuoraan oikealle, takaisin, ja katoaa
_(`ttl` on enemmänkin arvattu kuin laskettu)_:
`Bullet_Orbit(game, None, 100, 15, 50, (1,0,0,0))`

Spawnaa bulletit lentämään edestakaisin pelaajan läpi sekä vaaka- että pystysuunnassa:
```
Bullet_Orbit(game, offset=(1,0,0,0))
Bullet_Orbit(game, offset=(0,1,0,0))
```


---
### class Bullet_Sine (perii Bullet_Linen)
Ensimmäinen nopea yritys tehdä aaltoliikettä tekevä bullet. Vaatinee viilausta tai toisenlaisen
lähestymistavan.

##### docstring
    Bullet_Line but wavy
---
##### muuttujat, funktiot ym.
```
__init__(self, game, target, origin, ttl, speed, wave_scale):
    Ainoana erona Bullet_Lineen yksi parametri:
    
    wave_scale (1)
        Kerroin sivuttaisliikkeelle
```
```
update(self):
    Kutsu super().update() eteenpäin liikkumiseksi, laske sivuttaisliike ja siirrä Rect
```


---
### class Explosion (Pygame Sprite)
50 framen animaatio, jonka jälkeen jokainen objektin Rectin sisällä oleva vihollinen ottaa vahinkoa.
Piirtää "animaation" sekä tekee damagen omassa update-funktiossaan, lähinnä koska halusin kokeilla
tätä vaihtoehtoa.

Koska damage on updatessa, ei lisätä bullet_groupiin. Koska grafiikka/animaatio on myös, 
ei piirrä mitään, jos taustavärin piirtäminen ikkunaan tapahtuu Sprite-update'ien ja
ikkunan päivittämisen välissä. Taustan .fill() kannattaa siis tehdä vasta ruudun .flip()in
jälkeen.

##### docstring
    Draw an "animation" for 50 frames on a point or (by default a random enemy) Sprite, then deal area damage

    Draws itself and deals damage in own update(), thus doesn't inherit other weapons or isn't added
    to bullet_group. Really no other reason for the different logic than experimenting/practice.
    
    Because the animation is drawn in update(), needs the main loop's rendering to fill
    background AFTER flipping the screen instead of before.
---
##### muuttujat
    game, target (None), dmg (3)
        Kuten muissakin aseissa. Targetin oletus (eli None) valitsee satunnaisen vihollisen.
    diameter (100)
        Räjähdys-grafiikan halkaisija sivuttaissuunnassa. Pystysuunta on puolet tästä.
    animation_frame
        Alkaa 0:sta ja nousee joka update. Käytetään "animaatiossa" ellipsien koon laskemiseen.
        50:n kierroksen jälkeen update() tekee [dmg] vahinkoa kaikille vihollisille alueella
        sekä poistaa objektin.
---
##### käyttöesimerkit
Oletusarvoilla, eli "räjähdykseen" satunnaisen Enemyn päällä riittää `Explosion(game)`.

Tee 1000 vahinkoa kaikille vihollisille ikkunassa _(WIDTH = ikkunan leveys)_:  
`Explosion(game, player, 1000, SCREEN_WIDTH)`


---
### funktio spawn_orbiters(game, n, radius, speed, ttl)
Spawnaa N kpl tasaisin välimatkoin pelaajaa kiertävää Bullet_Orbitia, kaikilla positiivisilla
kokonaisluvuilla N.
    
##### docstring
    Spawns n equidistant Bullet_Orbits around player

    As math.sin() and .cos() use radians (and the formula in Bullet_Orbit divides by speed)
    adding (2/n*pi * speed) to both should make following bullet equally spaced.
---
##### parametrit
    game
        Viittaus peli-instanssiin
    n (2)
        Bulletien kappalemäärä
    radius (100), speed (30), ttl (500)
        Kts. Bullet_Orbit
---
##### käyttöesimerkit
Yksinkertaisimmillaan, spawnaa 5 kiertävää bulletia: `spawn_orbiters(game, 5)`

Koska jokainen Bullet_Orbit ilman offset:iä ottaa sinin ja kosinin samasta luvusta,
on näitä yhdistelemällä helppo tehdä mm. symmetrisiä kuvioita. Speed toimii
myös negatiivisilla luvuilla. Seuraavat esimerkit näillä leikkimisestä löytyy
(kirjoittamisen hetkellä) event_queue.py:n debug-napeista Z, X ja C, eli main.py:ssä
pääsee tahtoessaan kokeilemaan. Sanoin en yritä kuvailla, enkä sotke dokumentaatiota
enempää screenshoteilla.

##### Z
```
spawn_orbiters(game, 2, 50)
spawn_orbiters(game, 4, 70)
spawn_orbiters(game, 6, 90)
spawn_orbiters(game, 8, 110)
spawn_orbiters(game, 10, 130)
```
##### X
```
spawn_orbiters(game, 2, 50, -30)
spawn_orbiters(game, 4, 70)
spawn_orbiters(game, 6, 90, -30)
spawn_orbiters(game, 8, 110)
```
##### C
```
spawn_orbiters(game, 20, 50)
spawn_orbiters(game, 20, 70, -30)
```