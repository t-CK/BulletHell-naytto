Window(class):
    Window -luokka ikkunan hallintaan. Luokka on staattinen(ohjelman ajon aikana tarvitaan ainoastaan ykjsi instanssi), joten muuttujat on tallennettu class variableina.

        _wnd: pygame.Surface. Pygame ikkuna objekti

    __init__:
        Initialisoi pygame.display:n ja suorittaa virheentarkastuksen.
        Asettaa pygame -ikkunan flagit (locals.FULLSCREEN | locals.DOUBLEBUF | locals.HWACCEL | locals.OPENGL | locals.SHOWN) ja, luo pygame -ikkunan ja tallentaa sen _wnd -muuttujaan

