def Log_Error(msg :str):
    """Tulostaa terminaaliin punaiseksi värjätyn virheilmoituksen"""
    print(f"\033[0;31;40m ERROR: {msg} \033[0;0m")

def Log_Warning(msg :str):
    """Tulostaa tetrminaaliin keltaiseksi värjätyn varoituksen"""
    print(f"\033[0;33;40m WARNING: {msg} \033[0;0m")

def Log_Info(msg :str):
    """Tulostaa terminaaliin vihreäksi värjätyn viestin"""
    print(f"\033[0;32;40m INFO: {msg} \033[0;0m")

def Log_Fatal(msg :str):
    """Tulostaa terminaaliin fatal error virheilmoituksen ja laukaisee breakpointin"""
    print(f"\033[0;30;41m FATAL ERROR: {msg} \033[0;0m")
    breakpoint()

if __name__ == "__main__":
    Log_Error("testi error")
    Log_Warning("testi Warning")
    Log_Info("testi info")
    Log_Fatal("testi fatal")
    print("testi", 2*5)