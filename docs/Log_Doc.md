Log tiedosto on tarkoitettu auttamaan debuggauksessa:
käyttö on suhteellisen helppoa, sisältää Log_Error, Log_Warning, Log_Info ja Log_Fatal -metodit

Metodit tulostavat annetun viestin värikoodattuna:
Log_Fatal:   Punainen tausta + laukaisee brakepointin
Log_Error:   Punainen
Log_Warning: Keltainen
Log_Info:    Vihreä

käyttö esim:

display.init()
        if not display.get_init():
            Log_Fatal("Failed to initialize pygame.display")
            sys.exit()
        Log_Info("Initialized pygame.display")