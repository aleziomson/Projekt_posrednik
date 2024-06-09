def znajdz_najmniejsze_dostosowanie(macierz, przypisane):
    min_dostosowanie = float('inf')
    indeks = (-1, -1)

    for i in range(len(macierz)):
        for j in range(len(macierz[i])):
            if macierz[i][j] < min_dostosowanie and not przypisane[i][j]:
                min_dostosowanie = macierz[i][j]
                indeks = (i, j)

    return indeks

def solver_minimalny_koszt(macierz, podaz, popyt):
    rozwiazanie = [[0] * len(macierz[0]) for _ in range(len(macierz))]
    pozostaly_popyt = popyt[:]
    pozostala_podaz = podaz[:]
    przypisane = [[False] * len(macierz[0]) for _ in range(len(macierz))]

    while True:
        indeks = znajdz_najmniejsze_dostosowanie(macierz, przypisane)
        i, j = indeks

        if i == -1 or j == -1:
            break

        ilosc = min(pozostala_podaz[i], pozostaly_popyt[j])
        rozwiazanie[i][j] = ilosc
        pozostala_podaz[i] -= ilosc
        pozostaly_popyt[j] -= ilosc

        przypisane[i][j] = True

        if pozostala_podaz[i] == 0:
            przypisane[i] = [True] * len(macierz[i])
        if pozostaly_popyt[j] == 0:
            for k in range(len(macierz)):
                przypisane[k][j] = True

    return rozwiazanie

def znajdz_najwieksze_dostosowanie(macierz):
    max_dostosowanie = 0
    indeks = (-1, -1)

    for i in range(len(macierz)):
        for j in range(len(macierz[i])):
            if macierz[i][j] > max_dostosowanie:
                max_dostosowanie = macierz[i][j]
                indeks = (i, j)

    return indeks

def solver_maksymalny_zysk(macierz, podaz, popyt):
    rozwiazanie = [[0] * len(macierz[0]) for _ in range(len(macierz))]
    pozostaly_popyt = popyt[:]
    pozostala_podaz = podaz[:]
    przypisane = [[False] * len(macierz[0]) for _ in range(len(macierz))]

    while True:
        max_dostosowanie = 0
        indeks = (-1, -1)

        for i in range(len(macierz)):
            for j in range(len(macierz[i])):
                if macierz[i][j] > max_dostosowanie and not przypisane[i][j]:
                    max_dostosowanie = macierz[i][j]
                    indeks = (i, j)

        if indeks == (-1, -1):
            break

        i, j = indeks

        ilosc = min(pozostala_podaz[i], pozostaly_popyt[j])
        rozwiazanie[i][j] = ilosc
        pozostala_podaz[i] -= ilosc
        pozostaly_popyt[j] -= ilosc

        przypisane[i][j] = True

        if pozostala_podaz[i] == 0:
            przypisane[i] = [True] * len(macierz[i])
        if pozostaly_popyt[j] == 0:
            for k in range(len(macierz)):
                przypisane[k][j] = True

    return rozwiazanie


