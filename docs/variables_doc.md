## variables.py

Nää voisi toki olla muissa tiedostoissa tai classien alla, varsinkin Sprite Groupeille hassu paikka, mutta tiedostojen pilkkominen ja homman rakenne toteutu vähän toisin kuin olin aatellut, joten kävi nyt näin, enkä ole ruvennut suuremmin muuttelemaan.

SCREEN_SIZE ja WIDTH/HEIGHT on täällä nyt vain siksi, että näin myös main.py käynnistyy säätämättä enempää.

SPRITE_SCALE (1):  
Tällä kertoimella kerrotaan mm. Sprite'ien skaalaus. Toiminee kaikilla positiivisilla floateilla.  
Toistaiseksi myös mm. alun satunnaisten esteiden koko kerrotaan tällä.

FPS (60):  
Pygamen Clockille annettava FPS-katto.

DEFAULT_SPEED (3):  
*Pelaajan* aloitusnopeus. Oli alkuun hyödyllinen nopeeseen testailuun, ja aattelin olevan taas kun asioiden kokoja ja nopeuksia lyödään lukkoon. Voisi ehkä poistaa ja pistää luvun suoraan Playeriin.

DEFAULT_PICKUP_DISTANCE (40):  
Etäisyys, jolta XP ja powerupit tms. aktivoituvat. Tämäkin tuntui aluksi hyödylliseltä saada muutettua nopeasti muiden vastaavien kanssa. Voisi "kovakoodata" playeriin.

STARTING_SPAWN_TIME (200):  
Alun tick-määrä, jonka välein vihollinen spawnaa. Pienenee ajan kanssa.

---
#### Sprite Groupit

all_sprites  
Pelaajaa ja UI:tä lukuunottamatta kaikki tarvittavat Spritet lisäävät itsensä tähän initissään.  
Olennaisimpana käyttönä main.py kutsuu tätä kautta Spriten update-funktiota jokaisella kierroksella, ja main.py:n "map scrolling" siirtää kaikkia näitä pelaajan liikkuessa.

bullet_group  
Aseiden group. Näiden collision tarkistetaan enemy_groupin kanssa joka luupilla, ja kutsutaan vihollisen damage():a.

enemy_group  
Vihollisten group. Näiden liika läheisyys aiheuttaa playerille damagea, ja bullettien läheisyys näille. 

world_group  
World-classin group. Oma groupinsa lähinnä asioiden piirtojärjestyksen takia; näyttää oudolta jos osa asioista on esteiden päällä ja osa alla.

items_group  
pickups.py-tiedoston classien, eli toistaiseksi Itemien ja XP:n group. Tämäkin olemassa vain piirtojärjestykseen vaikuttamista varten.

collideable  
"Kiinteiden" objektien group. Movement collision ei anna liikkua näiden asioiden päälle.

ui_group  
UI-classin (tähän mennessä vaan Health- ja XP-barien) group. Näitä ei liikuteta ruudulla pelaajan liikkuessa, mutta update():a kutsutaan silti joka luupilla.

tail_group  
Tämän piti olla väliaikainen group erään idean testausta varten, mutta tein... jotain niin, että ilman tätä Worm-Enemy ei toimi oikein. En ole ehtinyt vielä tutkia, miksi, mutta jos tämä eräs idea ei toteudu, tämän ei mielestäni pitäisi olla välttämätön.