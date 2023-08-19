High_Score(class): 
    Käsittelee SQL tietokantaa ja pitää kirjaa pelaajien high scoresta
    
    Luokan muuttujat:
        _table  : String                : SQL table nimi
        _conn   : sqlite connection     : sqlite yhteys SQL tietokantaan
        _cursor : sqlite cursor object  : sqlite connectionin cursor
    
    Funktiot:
        __init__:
            Avaa SQL tietokantayhteyden.
            Jos score.db tiedostoa ei löydy, luodaan se ja initialisoidaan arvoilla table: score, pname(player name)(string), score(int),
            kills(int) ja time(real/float)
        
        get_score:
            Hakee tietokannasta kaikki pelaajatiedot ja pisteet.
            Palauttaa haetut tiedot listinä.
        
        get_score:
            parametrit:
                pName : string
            Hakee tietokannasta yksittäisen pelaajan tiedot ja palauttaa ne listana.
            Ottaa parametrinä pelaajan nimen.
            
        add_score:
            parametrit:
                pName   : str
                score   : int
                kills   : int
                time    : float
            Lisää uuden pelaajan pelitulokset tietokantaan.
            Mikäli annetulla nimellä löytyy jo kenttä tietokannasta, kutsutaan update_score -funktiota.
        
        update_score:
            parametrit:
                pName   : str
                score   : int
                kills   : int
                time    : float
            Päivittää tietokantaan pelaajan tuloksen annetuilla parametreillä.