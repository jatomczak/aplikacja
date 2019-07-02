
import grequests
import requests
import base64



def pobierz_plany(SNRS : list, user="h0309", password="Honda890"):

    urls = []
    for snr in SNRS:
        urls.append('http://ezis.mn-man.biz/cgi-bin/ezis/suche_znr.pl?Znr='+snr+ \
                    '&Anr=&ListName=Liste&Pet=&Dat=&DatSta=Import&Opt=U&Aktion=SZnr&Lang=en ')


    print('zdobywanie ciasteczek')
    r = requests.get(urls[0], auth=(user, password))
    layer1cookies = r.cookies

    print('wysylanie zapytania na serwer o plany ')

    requests_for_plans = (grequests.get(u, cookies=layer1cookies, auth=(user, password)) for u in urls)
    response_for_plans = grequests.map(requests_for_plans)
    return response_for_plans



def poszukaj_blatow(r1):

    wygenerowane_linki = []
    numer_lini=0
    nowa_linia = 999999
    numer_blatu = 0


    for line in r1.text.splitlines():
        if line[-11:-5] == "tiff A" and line[-4:] == "</A>":
            tresc_linkul = "http://ezis.mn-man.biz" + line[9:]
            tresc_linkur = tresc_linkul[:-28]
            wygenerowane_linki.append(str(tresc_linkur))
            nowa_linia = numer_lini

        if (numer_lini == nowa_linia + 11):
            if (numer_blatu == int(line[-7:-5])):
                wygenerowane_linki[-2] = wygenerowane_linki[-1]
                del wygenerowane_linki[-1]

        if numer_lini == nowa_linia + 11:
            numer_blatu = int(line[-7:-5])

        numer_lini += 1

    return wygenerowane_linki


def poszukaj_pdfow(r1):

    wygenerowane_linki = []
    numer_lini=0
    nowa_linia = 999999
    numer_blatu = 0


    for line in r1.text.splitlines():
        if line[-25:-5] == 'TARGET="_self">pdf A':
            tresc_linkul = "http://ezis.mn-man.biz" + line[9:]
            tresc_linkur = tresc_linkul[:-28]
            wygenerowane_linki.append(str(tresc_linkur))
            nowa_linia = numer_lini

        if (numer_lini == nowa_linia + 11):
            if (numer_blatu == int(line[-7:-5])):
                wygenerowane_linki[-2] = wygenerowane_linki[-1]
                del wygenerowane_linki[-1]

        if numer_lini == nowa_linia + 11:
            numer_blatu = int(line[-7:-5])

        numer_lini += 1

    return wygenerowane_linki



def poszukaj_plikow_cab(r1):

    wygenerowane_linki = []
    numer_lini=0
    nowa_linia = 999999
    numer_blatu = 0


    for line in r1.text.splitlines():
        if line[-22:] == ('TARGET="_self">cab</A>') or line[-22:] == ('TARGET="_self">RIS</A>'):
            tresc_linkur = "http://ezis.mn-man.biz" + line[9:-24]
            # tresc_linkur = tresc_linkul[:-24]
            wygenerowane_linki.append(str(tresc_linkur))
            nowa_linia = numer_lini

        if (numer_lini == nowa_linia + 10):
            if numer_blatu == int(line[-7:-5]):
                wygenerowane_linki[-2] = wygenerowane_linki[-1]
                del wygenerowane_linki[-1]

        if numer_lini == nowa_linia + 10:
            numer_blatu = int(line[-7:-5])

        numer_lini += 1

    return wygenerowane_linki


def poszukaj_plikow_ris(r1):

    wygenerowane_linki = []
    numer_lini=0
    nowa_linia = 999999
    numer_blatu = 0


    for line in r1.text.splitlines():
        if line[-22:] == ('TARGET="_self">RIS</A>'):
            tresc_linkur = "http://ezis.mn-man.biz" + line[9:-24]
            # tresc_linkur = tresc_linkul[:-24]
            wygenerowane_linki.append(str(tresc_linkur))
            nowa_linia = numer_lini

        if (numer_lini == nowa_linia + 10):
            if numer_blatu == int(line[-7:-5]):
                wygenerowane_linki[-2] = wygenerowane_linki[-1]
                del wygenerowane_linki[-1]

        if numer_lini == nowa_linia + 10:
            numer_blatu = int(line[-7:-5])

        numer_lini += 1

    return wygenerowane_linki


def pobieranie_blatow(wygenerowane_linki, user="h0309", password="Honda890"):

    r2 = requests.get(wygenerowane_linki[0], auth=(user, password))
    layer1Cookies1 = r2.cookies

    print('pobieranie planow ' + Sachnumer)

    rs = (grequests.get(u, cookies=layer1Cookies1, auth=(user, password)) for u in wygenerowane_linki)
    out = grequests.map(rs)
    return out

def pobieranie_blatow1(wygenerowane_linki, user="h0309", password="Honda890"):

    r2 = requests.get(wygenerowane_linki[0], auth=(user, password))
    layer1Cookies1 = r2.cookies

    rs = (grequests.get(u, cookies=layer1Cookies1, auth=(user, password)) for u in wygenerowane_linki)
    out = grequests.map(rs)
    return out



def podziel_na_paczki(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def html_to_tiff(out, Sachnumer):
    i=1
    nazwy_plikow=[]

    for plan in out:
        filename = glowna_sciezka + 'tiff\\'+Sachnumer+'_'+str(i)+'.tiff'
        with open(filename, 'wb') as f:
            for data in plan.iter_content(1024):
                f.write(data)
        nazwy_plikow.append(filename)
        print('zapisano plan ' +Sachnumer+'_'+str(i)+'.tiff')
        i=i+1
    return nazwy_plikow

def html_to_tiff1(out, filename):

    nazwy_plikow=[]

    for i in range(out.__len__()):
        file = filename[i][filename[i].rfind('\\')+1:]
        with open(filename[i], 'wb') as f:
            for data in out[i].iter_content(1024):
                f.write(data)
        nazwy_plikow.append(filename[i])
        print('zapisano plan ' +file)
        i += 1
    return nazwy_plikow

def tiff_to_pdf(nazwy_plikow, Sachnumer, nazwa):

    if nazwy_plikow.__len__()>1:
        with open(nazwa+".pdf","wb") as f1:
            f1.write(img2pdf.convert(nazwy_plikow))
            print('zapisano plan ' + Sachnumer+".pdf")

    return nazwy_plikow.__len__()