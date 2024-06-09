import numpy as np


def suma_wektora(wektor):
    return sum(wektor)

def stworz_macierz(ile_dostawcow,ile_odbiorcow,koszty_dostawy,koszty_zakupu,za_ile_sprzeda):
    macierz = np.zeros((ile_dostawcow,ile_odbiorcow),dtype=int)
    for i in range(ile_dostawcow):
        for j in range(ile_odbiorcow):
            if za_ile_sprzeda[j] <= 0:
                macierz[i][j] = koszty_dostawy[i][j] + koszty_zakupu[i]
            else:
                macierz[i][j]= za_ile_sprzeda[j] - ( koszty_dostawy[i][j] + koszty_zakupu[i] )

    return macierz



def dodaj_Fikcyjnego_Odbiorce(macierz,ewentualne_koszty_magazynowania):
    for i in range(macierz):
        macierz[i].append(ewentualne_koszty_magazynowania[i])

    return macierz

def dodaj_Fikcyjnego_Dostawce(macierz):
    macierz = macierz.tolist()
    liczba_kolumn = len(macierz[0])
    macierz.append([0] * liczba_kolumn)
    return macierz




def zwroc_zysk_lub_koszt(macierz, rozwiazanie):
    suma = 0
    for i in range(len(macierz)):
        for j in range(len(macierz[i])):
            suma += macierz[i][j] * rozwiazanie[i][j]
    return suma



def oblicz_koszty_transportu(rozwiazanie, koszty_transportu):
    koszty = 0
    for i in range(len(koszty_transportu)):
        for j in range(len(rozwiazanie[i])):
            koszty += rozwiazanie[i][j] * koszty_transportu[i][j]
    return koszty


def oblicz_przychod(rozwiazanie, ceny_sprzedazy):
    przychod = 0
    for j in range(len(rozwiazanie[0])):
        for i in range(len(rozwiazanie)):
            przychod += rozwiazanie[i][j] * ceny_sprzedazy[j]
    return przychod

def oblicz_koszty(rozwiazanie, koszty_zakupu):
    koszty = 0
    for i in range(len(koszty_zakupu)):
        for j in range(len(rozwiazanie[i])):
            koszty += rozwiazanie[i][j] * koszty_zakupu[i]
    return koszty

