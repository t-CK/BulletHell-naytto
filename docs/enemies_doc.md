## enemies.py
Vihollistyyppeihin liittyvät luokat. Ajatus oli, että kaikki periytyisivät ensimmäisestä Enemy-luokasta, 
mutta uudemmissa kokeilin asioita, joiden jäljiltä ainakaan vielä kaikkien kohdalla näin ei ole.
Osa classeista vaatii game-instanssilta attribuutin ticks, joka voisi tavallaan olla mikä vain
kierros kierrokselta kasvava luku.

---
### class Enemy (Pygame Sprite)
Vihollisten kattoluokka (lukuunottamatta ainakin Worm_Tailia). Lisätään groupeihin enemy_group ja 
all_sprites. Jos solid == True, myös groupiin collideable.

##### docstring
    Rudimentary enemy sprite object (probably gonna move much of this to a child class)

    Variables: (in addition to pygame's Sprite stuff)
        hp, speed: Self-explanatory
        dmg: Damage the enemy deals when bumping into player
        solid: If False, can pass through world obstacles / other solid enemies
        invulnerable: Ticks of invulnerability (i-frames)

    Methods:
        update(): Pygame's Sprite-update. Decrease i-frames and move towards player. (+ collision)
        damage(): Decrease HP (if not invulnerable) and set i-frames. Call death() if needed.
        death(): Drop XP and kill sprite.

---
##### muuttujat
    hp, speed
        Vihollisen hitpointit ja etäisyys, kuinka monta pikseliä yhdellä loopilla liikutaan
    game, player
        Viittaukset App- tai Game-luokan objektiin, sekä pelaajaobjektiin
    surf, rect
        Pygamen Surface ja Rect -objektit
    color
        Tuple (r, g, b) kuvaamaan väriä, jolla Surface täytetään, jos tälle ei ole imagea
    dmg
        Vahinko, jonka vihollinen tekee pelaajalle osuessaan
    solid
        Boolean. Jos True, estää vihollisen liikkeen toisten "kiinteiden" vihollisten/esteiden läpi
    invulnerable
        Looppien (= update-kutsujen) määrä, joiden aikana vahinkoa ei oteta

---
##### funktiot ja parametrit

```
__init__(self, game, position, hp, speed, dmg, solid):
    game, hp (3), speed (1), dmg (1), solid (True)
        Kts. muuttujat yllä
    position (misc.get_spawn)
        Tuple koordinaateista (x,y), joiden mukaan Spriten Rectin keskipiste määräytyy.
        Voi ottaa parametrina myös metodin, jota kutsuu, kuten oletusarvonaan.
```
```
update(self):
    Laske invulnerable-muuttujaa yhdellä, jos > 1
```
```
damage(self, amount):
    amount (1)
        Hp-määrä, joka vahinkoa otetaan
    
    Jos invulnerable > 0, ei tehdä mitään. Muulloin vähennetään self.hp:tä,
    pienennetään Spriten Surfacen kokoa (ja ilman imagea väriä), ja asetetaan
    invulnerable-muuttujan arvoksi 5. Tarvittaessa kutsutaan self.death()
```
```
death(self):
    Spawnaa satunnaisen arvoinen XP-pickup ja tuhoa self
```
 
---
### class Enemy_Follow (perii Enemyn)

Vihollinen, joka liikkuu joka updatella sekä x-, että y-akselilla kohteensa suuntaan. Kohde on 
oletusarvoisesti pelaaja, mutta voi olla muutakin. Tämä target ei tosin vielä liiku ruudulla pelaajan 
liikkuessa, eli ei noudata "map-scrollingia".

##### docstring
    Enemy moving in a straight line towards player

---
##### muuttujat
    target (player)
        Kohde, jota enemy lähestyy tuplena (x,y). Jos parametrina annetaan Sprite, 
        otetaan sen Rectin keskipisteestä koordinaatit (suhteessa ruutuun, eli 
        kohde ei vielä liiku mapilla pelaajan liikkuessa)

---
##### funktiot ja parametrit
```
__init__():
    Target-parametria (kts. muuttujat) lukuunottamatta toimii kuten ylempi class (kts. Enemy)
```
```
update(self):
    Kutsu super().update() i-frame'ien takia, liiku kohti targetia, ja jos solid == True,
    liiku takaisin kunnes ei collisionia. Palauttaa True, jos collision tapahtui, muuten False
```

---
### class Enemy_Sine (perii Enemy_Follow:n)
Sivuttain aaltoillen liikkuva versio Enemy_Followista. Ainoana erona siihen liikkuu joka updatella sivuttain 
pelaajaan nähden. Koska tämä suunta katsotaan joka kierroksella, ei suoranaisesti tee sivuttaista 
aaltoliikettä, vaan seuraa edestakaisin spiraalin sektoria pitkin. Tästä seuraa varsinkin lyhyillä 
etäisyyksillä jotain melko rumaa, mutta tulipa kokeiltua.

##### docstring
    Enemy_Follow but with some added circling


---
### class Enemy_Worm_Head (perii Enemyn)
Keskeneräinen kokeilu useammasta Spritesta koostuvasta "madosta". Pyrkimys oli, että mato voi katketa ja häntä 
jää elämään, vaikka ei liiku. Koska ajattelin, että päätä ei saa pystyä tuhoamaan yksinään liian helposti, 
pään ottama vahinko siirtyy kiinni olevan "hännän" viimeiseen Spriteen, ja vasta yksinäinen pää 
ottaa vahingon itse.

##### docstring
    Worm type enemy head
    
---
##### muuttujat
    turn_rate (7)
        Vaikuttaa **käänteisesti** aaltoliikkeen frekvenssiin
    turn_speed (7)
        Vaikuttaa aallon leveyteen. (Hämäävä muuttujannimi, tiedän)
    target
        Tuple (x,y), jonka läpi kuljetaan. Otetaan joka ohituksella satunnaisesti pelaajan lähistöltä.
    last_position
        Viimeinen sijainti, johon häntä seuraa. Jos liike ei onnistu (esim.
        collisionin takia, jota ei ole vielä implementoitu), laitetaan arvoksi None.
    child
        Enemy_Worm_Tail -luokan objekti, joka seuraa päätä, ja jota pitkin damage "lähetetään".
    size
        Surfacen koko. Lähetetään child-objektille yhtä pienempänä.

##### funktiot ja parametrit
```
__init__(self, game, tail_length, position, 
        turn_rate, turn_speed, target, hp, speed, dmg, solid):
    tail_length (20)
        Seuraavien häntä-objektien lukumäärä. Jos > 0, init luo moisen, ja lähettää  
        tälle parametreina (itsensä lisäksi) tail_length-1:n ja size-1:n
    size (20)
        Surfacen koko. Lähetetään child-objektille yhtä pienempänä.
```
```
update(self):
    Liiku kohti `target`ia kiemurrellen. Päivitä last_position. Jos sijainti on 
    sama kuin ennen liikettä, aseta arvoksi None.
```
```
damage(self, amount):
    Jos `child` == None, ota damagea. Muuten kutsu childin pass_damage():a.
```

---
### class Enemy_Worm_Tail (Pygame Sprite)
Mato-enemyn ei-pää. Siirtyy liikkeessään päätä kohti seuraavan Spriten last_positioniin. Ei peri muita 
Enemy-classeja, vaan on oma Sprite-luokkansa

##### docstring
    Child object following Enemy_Worm_Head (and other Tails)
    
---
##### muuttujat
    hp, dmg, invulnerable
        Kuten muilla Enemyillä. Hp ja dmg -arvot otetaan suoraan parentilta.
    child, size
        Kuten Enemy_Worm_Head:illä. Size on minimissään 5.
    color
        Tuple (r,g,b), vastaamaan Enemyn väriä. Tummenee/punertuu damagesta.
    parent
        Viittaus objektiin, joka tämän objektin loi, eli jonka objektin child self on.
    dead
        Boolean siitä, onko olion hp 0. Tällä hetkellä käytännössä turha.
        Liittyy lähinnä graafiseen ideaan, jota ehkä testailen vielä.

---
##### funktiot ja parametrit
```
__init__(self, parent, tail_length):
    Luo itsensä kuin yksinkertaisempi Enemy_Worm_Head, lisää itsensä groupeihin 
    ja jos tail_length > 0, luo oman Enemy_Worm_Tail-childin.
```
```
update(self):
    Laske invulnerablea, liiku parentin last_positioniin (ellei None), ja päivitä
    oma last_position
```
```
damage(self, amount):
    Laske hp:tä, kutsu tarvittaessa self.death(), muuta väriä ja aseta vulnerable
```
```
pass_damage(self, amount):
    Ota päältä tullut damage, jos self.child == None, muuten lähetä eteenpäin.
```
```
death(self):
    Yritin ideoida tänne jotain erikoisempaa, mutta nyt asettaa sekä omansa
    että parent'insa childin Noneksi (varmistukseksi ettei muu aiheuta erroreita)
    ja toistaiseksi kuolee suoraan, jonka takia edellinen askel lienee turha.
```