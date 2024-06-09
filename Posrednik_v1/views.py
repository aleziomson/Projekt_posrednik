
from django.shortcuts import render, redirect
from .forms import InputForm
from .Funkcje_do_budowania_macierzy import stworz_macierz, zwroc_zysk_lub_koszt, oblicz_koszty_transportu, oblicz_przychod, oblicz_koszty
from .Funkcje_do_rozwiazywania_zagadnienia import solver_maksymalny_zysk, solver_minimalny_koszt
import numpy as np

def initial_input(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            liczba_dostawcow = form.cleaned_data['liczba_dostawcow']
            liczba_odbiorcow = form.cleaned_data['liczba_odbiorcow']
            wybor = request.POST.get('wybor')
            request.session['liczba_dostawcow'] = liczba_dostawcow
            request.session['liczba_odbiorcow'] = liczba_odbiorcow
            request.session['wybor'] = wybor
            return render(request, 'Posrednik_v1/dynamic_input.html', {
                'liczba_dostawcow': liczba_dostawcow,
                'liczba_odbiorcow': liczba_odbiorcow,
                'dostawcy_range': range(liczba_dostawcow),
                'odbiorcy_range': range(liczba_odbiorcow)
            })
    else:
        form = InputForm()
    return render(request, 'Posrednik_v1/initial_input.html', {'form': form})

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        content = file.read().decode('utf-8').splitlines()
        liczba_dostawcow, liczba_odbiorcow = map(int, content[0].split(','))
        wybor = content[1].strip()
        koszty_dostawy = [list(map(int, line.split(','))) for line in content[2:2+liczba_dostawcow]]
        koszty_zakupu = list(map(int, content[2+liczba_dostawcow].split(',')))
        ceny_sprzedazy = list(map(int, content[3+liczba_dostawcow].split(',')))
        popyt = list(map(int, content[4+liczba_dostawcow].split(',')))
        podaz = list(map(int, content[5+liczba_dostawcow].split(',')))
        ewentualne_koszty_magazynowania = list(map(int, content[6+liczba_dostawcow].split(',')))

        context = {
            'liczba_dostawcow': liczba_dostawcow,
            'liczba_odbiorcow': liczba_odbiorcow,
            'wybor': wybor,
            'koszty_dostawy': koszty_dostawy,
            'koszty_zakupu': koszty_zakupu,
            'ceny_sprzedazy': ceny_sprzedazy,
            'popyt': popyt,
            'podaz': podaz,
            'ewentualne_koszty_magazynowania': ewentualne_koszty_magazynowania
        }

        return calculate(request, context)
    return render(request, 'Posrednik_v1/initial_input.html')

def calculate(request, context=None):
    if request.method == 'POST' or context:
        if context:
            liczba_dostawcow = context['liczba_dostawcow']
            liczba_odbiorcow = context['liczba_odbiorcow']
            wybor = context['wybor']
            koszty_dostawy = context['koszty_dostawy']
            koszty_zakupu = context['koszty_zakupu']
            ceny_sprzedazy = context['ceny_sprzedazy']
            popyt = context['popyt']
            podaz = context['podaz']
            ewentualne_koszty_magazynowania = context['ewentualne_koszty_magazynowania']
        else:
            liczba_dostawcow = int(request.POST.get('liczba_dostawcow'))
            liczba_odbiorcow = int(request.POST.get('liczba_odbiorcow'))
            wybor = request.session.get('wybor')
            koszty_dostawy = [
                [int(request.POST.get(f'koszty_dostawy_{i}_{j}')) for j in range(liczba_odbiorcow)]
                for i in range(liczba_dostawcow)
            ]
            koszty_zakupu = [int(request.POST.get(f'koszty_zakupu_{i}')) for i in range(liczba_dostawcow)]
            ceny_sprzedazy = [int(request.POST.get(f'ceny_sprzedazy_{j}')) for j in range(liczba_odbiorcow)]
            popyt = [int(request.POST.get(f'popyt_{j}')) for j in range(liczba_odbiorcow)]
            podaz = [int(request.POST.get(f'podaz_{i}')) for i in range(liczba_dostawcow)]
            ewentualne_koszty_magazynowania = [
                int(request.POST.get(f'ewentualne_koszty_magazynowania_{j}')) for j in range(liczba_dostawcow)
            ]

        zamkniete = False
        dodano = ""

        macierz_zysku = stworz_macierz(liczba_dostawcow, liczba_odbiorcow, koszty_dostawy, koszty_zakupu, ceny_sprzedazy)

        if sum(popyt) == sum(podaz):
            nowa_macierz = macierz_zysku
            zamkniete = True
            if wybor == "MAX":
                rozwiazanie = solver_maksymalny_zysk(nowa_macierz, podaz, popyt)
            elif wybor == "MIN":
                rozwiazanie = solver_minimalny_koszt(nowa_macierz, podaz, popyt)
        elif sum(popyt) > sum(podaz):
            nowa_macierz = np.vstack([macierz_zysku, [0]*liczba_odbiorcow])
            koszty_dostawy.append([0] * liczba_odbiorcow)
            podaz.append(sum(popyt) - sum(podaz))
            koszty_zakupu.append(0)
            ewentualne_koszty_magazynowania.append(0)
            dodano = "Dostawca"
            if wybor == "MAX":
                rozwiazanie = solver_maksymalny_zysk(nowa_macierz, podaz, popyt)
            elif wybor == "MIN":
                rozwiazanie = solver_minimalny_koszt(nowa_macierz, podaz, popyt)
        else:
            nowa_macierz = np.hstack([macierz_zysku, np.array(ewentualne_koszty_magazynowania).reshape(-1, 1)])
            for i in range(len(koszty_dostawy)):
                koszty_dostawy[i].append(ewentualne_koszty_magazynowania[i])
            ceny_sprzedazy.append(0)
            popyt.append(sum(podaz) - sum(popyt))
            dodano = "Odbiorca"
            if wybor == "MAX":
                rozwiazanie = solver_maksymalny_zysk(nowa_macierz, podaz, popyt)
            elif wybor == "MIN":
                rozwiazanie = solver_minimalny_koszt(nowa_macierz, podaz, popyt)

        zysk = zwroc_zysk_lub_koszt(nowa_macierz, rozwiazanie)
        koszt_transportu = oblicz_koszty_transportu(rozwiazanie, koszty_dostawy)
        przychod = oblicz_przychod(rozwiazanie, ceny_sprzedazy)
        koszt_zakupu = oblicz_koszty(rozwiazanie, koszty_zakupu)
        wszystkie_koszty = koszt_zakupu + koszt_transportu

        context = {
            'macierz_zysku': macierz_zysku,
            'rozwiazanie': rozwiazanie,
            'zysk': zysk,
            'koszt_transportu': koszt_transportu,
            'przychod': przychod,
            'koszt_zakupu': koszt_zakupu,
            'wszystkie_koszty': wszystkie_koszty,
            'wybor': wybor,
            'zamkniete': zamkniete,
            'dodano': dodano,
            'nowa_macierz': nowa_macierz,
            'liczba_dostawcow': liczba_dostawcow,
            'liczba_odbiorcow': liczba_odbiorcow,
        }
        return render(request, 'Posrednik_v1/results.html', context)
    else:
        return redirect('initial_input')


