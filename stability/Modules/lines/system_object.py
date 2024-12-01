import numpy as np
from types import SimpleNamespace

def system_object(D, Dtw, ht, hu, hb, lu, lb, philu, philb, phiru, phirb):
    return SimpleNamespace( ** {
        "D": D,
        "Dtw": Dtw,
        "ht": ht,
        "hu": hu,
        "hb": hb,
        "lu": lu,
        "lb": lb,
        "philu": np.deg2rad(philu),
        "philb": np.deg2rad(philb),
        "phiru": np.deg2rad(phiru),
        "phirb": np.deg2rad(phirb),
        "ycc" : (hu+lu*np.cos(phiru)+hb+lb*np.cos(phirb))/2,
        "theta" : 0,
        "omegaR" : 0,
        "omegaL" : 0
    })