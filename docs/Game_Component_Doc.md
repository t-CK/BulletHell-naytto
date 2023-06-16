Game_Component -tiedosto pitää sisällään pelikomponentti -luokat (periytetty abstraktista Game_Component -luokasta)

Sprite_Component(Class):
    Komponentti on tarkoitettu käsittelemnään renderöitävät kuvar peliobjektissa.

    _wnd: referenssi pygamen ikkunaan, jotta voidaan käyttää sprite_component -luokkaaa kuvien   ymv renderöintiin.
    
    __init__:
        Luo tyhjän listan renderöitäviä kuvia varten ja tallentaa parametrina saadun pygame -ikkunan referenssin luokan muuttujaan.
    
    add_sprite:
        Ottaa parametrina yhden tai useamman string-muotoisen kuvan osoitteen projektikansiossa, lataa kuvan listaan käyttäen pygame.image.load(), muuttaa näytön käyttämään formaattiin convert() -metodilla ja tallentaa pygame.Surface:n _imgs -listaan.

    render_sprite:
        Renderöi kuvan _imgs -listasta, ottaa parametrina kuvan indexipaikan listassa.

Input_Component(class):
    Komponentti user inputin käsittelyä varten.

    _wnd: referenssi pygamen ikkunaan, jotta voidaan käyttää sprite_component -luokkaaa kuvien   ymv renderöintiin.

    __init__:
        Tallentaa pygame -ikkunan referenssin muuttujaan ja asettaa Game_Component objektin _owner muuttujaan, jotta voidaan kutsua oikeaa oliota käyttäjäsyötteen mukaan.

    get_input():
        Kuuntelee käyttäjän syötettä ja kutsuu syötteen mukaisesti tarvittavaa metodia self._owner -oliosta.