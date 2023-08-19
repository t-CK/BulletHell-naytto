Window(class):
    Window -luokka ikkunan hallintaan. Luokka on staattinen(ohjelman ajon aikana tarvitaan ainoastaan ykjsi instanssi), joten muuttujat on tallennettu class variableina.

        _wnd: pygame.Surface. Pygame ikkuna objekti

    __init__:
        Initialisoi pygame.display:n ja suorittaa virheentarkastuksen.
        Asettaa pygame -ikkunan flagit (locals.FULLSCREEN | locals.DOUBLEBUF | locals.HWACCEL | locals.SHOWN) ja, luo pygame -ikkunan ja tallentaa sen _wnd -muuttujaan

    draw_background:
        Päivittää ikkunan taustan magneta -värillä
        
    draw_objects:
        Parametrit:
            sprites : pygame.sprite.Group
        Ottaa parametrina vastaan pygame sprite groupin.
        Looppaa groupin jokaisen spriten ja renderöi ikkunaan käyttäen pygame.Surface.blit:tiä.
    
    end_frame:
        Kutsutaan game loopin lopussa, render flown viimeisenä.
        Vaihtaa front ja back bufferit kutsumalla pygame.display.flip -funktiota.
       
    get_size:
        Palauttaa ikkunan koon tuplena (w, h)
    