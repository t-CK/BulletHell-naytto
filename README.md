# Näyttötyö v0.1

## Käyttö
- Käynnistä .exe tai **Game.py**
- Liiku nuolinäppäimillä tai paina M liikkuaksesi hiirellä
- Yritä selvitä hengissä ja tappaa mahdollisimman paljon vihollisia
- Paina F10 sulkeaksesi pelin. ESC pausettaa.

Pelaajahahmo ampuu jatkuvasti sekä lähintä vihollista kohti lentäviä, että itseään kiertäviä luoteja.
Kuolleilta vihollisilta putoavat XP-neliöt nostavat pelaajan kokemuspisteitä ja kun näitä on tarpeeksi,
pelaajan aseet vahvistuvat ja seuraavalle tasolle nouseminen vaatii aiempaa enemmän pisteitä. 

Toisinaan vihollisen kuollessa nämä pudottavat myös pienen mustan neliön, pommin, jonka kerääminen
aiheuttaa kolmen satunnaisesti valitun vihollisen päällä kaikille lähialueella oleville vihollisille
vahinkoa tekevän räjähdyksen.

Ajan kuluessa viholliset syntyvät useammin, ja kestävämpinä.

Vaikka seuraavat näppäinkomennot eivät kuulu osaksi suunniteltua peliä, testausta varten on olemassa myös
seuraavat näppäimet:  
*(en jaksa kääntää suomeksi, sori)*
```
1 = Spawn 3 orbiters
2 = Spawn 9 orbiters
3 = Spawn bullet orbiting player (with ugly random offset)
4 = Spawn bullet orbiting previous bullet spawned with 3
5 = Despawn bullets
6 = Spawn bullet towards closest enemy
7 = Spawn bullet towards random enemy
8 = Spawn (WIP) sine bullet
9 = Spawn (WIP) sine enemy
0 = Kill enemies
P = Spawn Enemy_Follow
O = Spawn Worm (very WIP)
I = Spawn a bomb pickup

Z, X, C = Some patterns made with weapons.Orbiters()
```
## Image Generator
Alihakemistosta `./image_generator` löytyy tiedosto **imagegen.py** (tai .exe), jolla voit vaihtaa
pelissä ohjaamasi hahmon kuvaketta. Kuvat rakennetaan siellä olevissa alikansioissa olevista kuvatiedostoista.
Näppäimillä Q/E, A/D ja Z/C voit valita hahmon pään, vartalon ja jalat. F5 tallettaa valinnat ja F8 lataa.
Enter tallettaa lopullisen kuvan kansioon, josta peli tämän käynnistyessään lataa.
