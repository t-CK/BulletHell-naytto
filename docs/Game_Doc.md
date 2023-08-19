Game_State:
    Enum luokka pelin statuksen seurantaa varten. Sisältää kolme statusvaihtoehtoa:
        RUNNING = 0
        PAUSED = 1
        IN_MENU = 2

Game(class):
    Staattinen luokka (ainoastaan yksi instanssi tarvitaan ohjelman ajon aikana), eli luokan muuttujat ovat class variableja:
        _wnd:                       Window -luokan instanssi graafisen käyttöliittymän hallintaan
        _state:                     Game_State enumin instanssi pelin statuksen seurantaan. Game -olion luonnin yhteydessä asetettu oletuksena IN_MENU(2) -tilaan
        _is_Running:                Boolean tyyppinen muuttuja game loopin hallintaa varten.
        _game_objects:              Array, johon tallennetaan Game_Object oliot. listaa käydään läpi game loopissa ja päivitetään peliobjektit (pelihahmot ymv)
                                    listasta poistetaan ajon aikana oliot, joita ei enää tarvita
        _prev_tick                  Edellisen tickin arvo. Käytetään laskiessa delta_timea (pygame.get_ticks() - _prev_tick / 1000)
        _delta_time:                Delta time float muodossa
        
        self._none_player_sprites   Array johon tallennetaan tietokoneen ohjaamat ja staattiset spritet
        self._player                Pelaajan kontrolloima sprite-objekti
        self._map                   Kartta -objekti. Edustaa ja hallitsee pelialuetta
        self._camera                Tuple (x, y), joka pitää sisällään kameran x ja y sijaintitiedot. Käytetään laskemaan map scrollingia
        self._sprite_group          Pygame sprite_group. Käytetään renderöimään spritet. Grouppiin lisätään tai poistetaan spritejä game loopissa, riippuen spriten sijainnista kartalla.


    __init__:
        Initialisoidaan Game -luokka: initialisoidaan _wnd -olio, asetetaan _is_running arvoiksi True ja _state tilaksi IN_MENU(2)
        
    add_sprite:
        Funktio lisää tarvittaessa spriten peliin.
        
    add_ui:
        parametrit:
            ui : UI luokan instanssi
        Lisää uuden ui-elementin peliin
        
    update_game:
        parametrit:
            x_val : int
            y_val : int
        Ottaa parametrinä pelaajan liikkeen vastaluvun.
        Päivittää jokaisen (ei pelaaja)spriten sijainnin annetuilla luvuilla map_scrollingia varten.

    game_loop:
        Tarkkailee Game State:a ja hoitaa pelin päivittämisen tai valikot asianmukaisesti.
        päivittää kameran sijainnin kartalla vastaamaan pelaajan sijaintia ja tarkkailee muiden spritejen sijaintia. Tarvittaessa lisää tai poistaa spriten 
        groupista jottei ikkunan ulkopuolella olevia spritejä renderöidä turhaan.
        Laskee delta timen ja tallentaa _delta_time -muuttujaan.

    toggle_state:
        parametrit:
            state : Game_State
        Ottaa parametrinä vastaan Game_State:n.
        Mikäli annettu Game_State vastaa Game._state -muuttujaan tallennettua Game_State:a, vaihtaa Game_State.PAUSED ja Game_State.RUNNING välilllä.
        Muussa tapauksessa Game._state arvoksi asetetaan annettu Game_State.
        
    get_state:
        Antaa palautusarvona Game luokan _state -muuttujan.

    get_delta_time:
        Lähettää palautusarvona _delta_time(float) -muuttujan