from . import pobieranie_sp_z_ezisa
import os
import zipfile
import mmap
import shutil
from . import sql_emcos


def main(autobus, user='h0309', password='Honda890', root='C:\\Users\\h0309\\PycharmProjects\socket_recognition_v3'
                                                          '\\autobusy\\'):
    # ---------------------------------------------funkcje--------------------------------------------------------------
    def zapis_pliku_z_wtyczkami(root, autobus, glowna_sciezka):
        ebc_files = [os.path.join(root, name)
                     for root, dirs, files in os.walk(glowna_sciezka)
                     for name in files
                     if name.endswith((".kbl", ".BLA", ".XML", ".SYM", ".txt"))]

        important_IBIS_plans = []

        for ebc_file in ebc_files:
            with open(ebc_file, 'rb', 0) as file, \
                    mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
                if s.find(b'X2039') != -1:
                    important_IBIS_plans.append([ebc_file, 'X2039'])
                if s.find(b'XKSW') != -1:
                    important_IBIS_plans.append([ebc_file, 'XKSW'])
                if s.find(b'X1035') != -1:
                    important_IBIS_plans.append([ebc_file, 'X1035'])

        all_sachnumers = []
        for sach in important_IBIS_plans:
            all_sachnumers.append(sach[0][sach[0].find("ch_eb-cable\\") + 12:sach[0].find("ch_eb-cable\\") + 23])

        with open(root + autobus + "\\wazne_blaty_ibis.txt", "w") as f:
            for sach in important_IBIS_plans:
                s1 = str(sach[0][sach[0].find("ch_eb-cable\\") + 24:sach[0].find("ch_eb-cable\\") + 37])
                s2 = str(sach[1])
                f.write(s1 + " " + s2 + "\n")
        return all_sachnumers

    def pobranie_sql(autobus):
        with sql_emcos.UseOracleDb() as cursor:
            _SQL = "select SNR from kass032_view where produktnr like '%" + autobus + "%' AND (bend_snr like '%SCHALTPLAN%' OR bend_snr like '%BELEGUNGSPLAN  IBIS%' OR bend_snr like '%INSTRUMENTEN%')"
            cursor.execute(_SQL)
            result = cursor.fetchall()

        all_plans_in_bus = []
        benelegung_plans = []
        instrumententafels = []

        for i in result:
            if i[0][2:5] == '992' and i[0][:2] in ['33', '34', '83']:
                all_plans_in_bus.append(i[0])
            if i[0][2:7] == '25445' and i[0][:2] in ['33', '34', '83'] and int(i[0][-4:-1]) > 802:
                benelegung_plans.append(i[0])
            if i[0][2:5] == '760' and i[0][:2] in ['33', '34', '83']:
                instrumententafels.append(i[0])
        return all_plans_in_bus, benelegung_plans, instrumententafels

    def pobranie_plikow_zip(batches):
        status_pobrania = 0
        for batch in batches:
            responses_for_batch = pobieranie_sp_z_ezisa.pobierz_plany(batch, user, password)
            wygenerowane_nazwy = []
            href = []
            i = 0

            for response in responses_for_batch:
                linki = pobieranie_sp_z_ezisa.poszukaj_plikow_cab(response)
                if len(linki) > 0:
                    for j in range(linki.__len__()):
                        wygenerowane_nazwy.append(glowna_sciezka + batch[i] + '_' + str(j + 1) + '.zip')
                    href = sum([href, linki], [])
                i += 1

            if href.__len__() > 1:
                blat_html = pobieranie_sp_z_ezisa.pobieranie_blatow1(href, user, password)
                pobieranie_sp_z_ezisa.html_to_tiff1(blat_html, wygenerowane_nazwy)
            status_pobrania += 1
            if (status_pobrania * ilosc_planow_w_paczce * 100) / all_plans_in_bus.__len__() < 100:
                print("pobrano " + str(
                    (status_pobrania * ilosc_planow_w_paczce * 100) / all_plans_in_bus.__len__()) + "%")
            else:
                print("pobrano 100%")
        pass

    def rozpakowywanie_zipow():
        for file in os.listdir(glowna_sciezka):
            master_folder = file[:11]
            try:
                zip_ref = zipfile.ZipFile(glowna_sciezka + file, 'r')
                zip_ref.extractall(glowna_sciezka + master_folder + "\\" + file[:-4])
                zip_ref.close()
                os.remove(zip_ref.filename)
            except:
                print('pliki_juz_istnieja')
        pass

    def usuniecie_zbednych_plikow(sciezka):
        try:
            shutil.rmtree(sciezka)
        except:
            print('nie znaleziono folderu do usuniecia')
        pass

    def pobieranie_tiff(all_sachnumers, folder):
        status_pobrania = 0
        batches = list(pobieranie_sp_z_ezisa.podziel_na_paczki(all_sachnumers, ilosc_planow_w_paczce))

        for batch in batches:
            batch = list(map(str.strip, batch))
            responses_for_batch = pobieranie_sp_z_ezisa.pobierz_plany(batch, user, password)
            wygenerowane_nazwy = []
            href = []
            i = 0

            for response in responses_for_batch:
                linki = pobieranie_sp_z_ezisa.poszukaj_blatow(response)
                if len(linki) > 0:
                    for j in range(linki.__len__()):
                        wygenerowane_nazwy.append(root + autobus + '\\'+folder+'\\' + batch[i] + '_' + str(j + 1) + '.tiff')
                    href = sum([href, linki], [])
                i += 1

            if href.__len__() > 0:
                blat_html = pobieranie_sp_z_ezisa.pobieranie_blatow1(href, user, password)
                pobieranie_sp_z_ezisa.html_to_tiff1(blat_html, wygenerowane_nazwy)
            status_pobrania += 1
            if (status_pobrania * ilosc_planow_w_paczce * 100) / all_sachnumers.__len__() < 100:
                print("pobrano " + str((status_pobrania * ilosc_planow_w_paczce * 100) / all_sachnumers.__len__()) + "%")
            else:
                print("pobrano 100%")
        pass

    def tworzenie_folderow(nazwy_folderow):
        for nazwa_folderu in nazwy_folderow:
            try:
                os.makedirs(root + autobus + '\\'+nazwa_folderu+'\\')
            except:
                p = 1
                # print('path ' + root + autobus + '\\'+nazwa_folderu+'\\' + ' already exists')
        pass

    # ---------------------------------------------koniec funkcji-------------------------------------------------------
    try:
        usuniecie_zbednych_plikow(root + autobus)
    except:
        p=1

    tworzenie_folderow(['plany_w_plikach_eb-cable', 'plany_tiff', 'belegungsplany', 'instrumententafels'])

    ilosc_planow_w_paczce = 40

    glowna_sciezka = root + autobus + '\\plany_w_plikach_eb-cable\\'

    all_plans_in_bus, benelegung_plans, instrumententafels = pobranie_sql(autobus)
    print("znaleziono " + str(all_plans_in_bus.__len__()) + " planow w tym autobusie, rozpoczynam pobieranie:")

    batches = list(pobieranie_sp_z_ezisa.podziel_na_paczki(all_plans_in_bus, ilosc_planow_w_paczce))
    pobranie_plikow_zip(batches)
    rozpakowywanie_zipow()
    all_sachnumers = zapis_pliku_z_wtyczkami(root, autobus, glowna_sciezka)

    all_sachnumers = list(dict.fromkeys(all_sachnumers))
    print("znaleziono " + str(all_sachnumers.__len__()) + " planow, rozpoczynam pobieranie:")
    pobieranie_tiff(all_sachnumers, 'plany_tiff')

    benelegung_plans = list(dict.fromkeys(benelegung_plans))
    print("znaleziono " + str(benelegung_plans.__len__()) + " belegungsplanow, rozpoczynam pobieranie:")
    pobieranie_tiff(benelegung_plans, 'belegungsplany')

    instrumententafels = list(dict.fromkeys(instrumententafels))
    print("znaleziono " + str(instrumententafels.__len__()) + " planow desek, rozpoczynam pobieranie:")
    pobieranie_tiff(instrumententafels, 'instrumententafels')

    usuniecie_zbednych_plikow(glowna_sciezka)
    shutil.move(root+autobus+'\\', 'K:\Kompilacja\IBIS socket finder')

    pass
