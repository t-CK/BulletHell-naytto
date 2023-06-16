Game_State:
    Enum luokka pelin statuksen seurantaa varten. Sisältää kolme statusvaihtoehtoa:
        RUNNING = 0
        PAUSED = 1
        IN_MENU = 2

Game(class):
    Staattinen luokka (ainoastaan yksi instanssi tarvitaan ohjelman ajon aikana), eli luokan muuttujat ovat class variableja:
        _wnd:          Window -luokan instanssi graafisen käyttöliittymän hallintaan
        _state:        Game_State enumin instanssi pelin statuksen seurantaan. Game -olion luonnin yhteydessä asetettu oletuksena IN_MENU(2) -tilaan
        _is_Running:   Boolean tyyppinen muuttuja game loopin hallintaa varten.
        _game_objects: Lista, johon tallennetaan Game_Object oliot. listaa käydään läpi game loopissa ja päivitetään peliobjektit (pelihahmot ymv)
                       listasta poistetaan ajon aikana oliot, joita ei enää tarvita
        _delta_time:   Delta time float muodossa


    __init__:
        Initialisoidaan Game -luokka: initialisoidaan _wnd -olio, asetetaan _is_running arvoiksi True ja _state tilaksi IN_MENU(2)

    add_game_object:
        Lisätään Game_Object _game_objects -listaan. Pitää kutsua joka kerta, kun uusi peliobjekti luodaan.
        Ottaa parametrina Game_Object -olion ja suorittaa virheentarkastuksen (Käyttää Log_error -metodia tulostamaan virheilmoituksen, mikäli annetun parametrin tyyppi on vääränlainen)

    game_loop:
        Laskee _delta_timen ja suorittaa peliobjektien, komponenttien ja ikkunan päivittämisen while(_is_running) loopissa.

    get_delta_time:
        Lähettää palautusarvona _delta_time(float) -muuttujan