from selenium import webdriver
from django.test import LiveServerTestCase


class RegistrationTest(LiveServerTestCase):
    # Pan Kanapka postanowil zarejestrowac sie w nowym systemie do rezerwacji kanapek
    # otworzyl przegladarke internetowa
    def setUp(self):
        self.browser = webdriver.Firefox()

    #wpisal adres nowego serwisu
    def test_get_registration_site(self):
        self.browser.get("%s/%s"%(self.live_server_url, 'clients/add'))
    # na stronie internetowej zauwazyl tytul "Rejestracja"
        page_title = self.browser.find_element_by_tag_name('title')
        self.assertIn(page_title.text.upper(), 'REJESTRACJA')
    # ukazal się formularz z naglowkiem Rejestracja nowego uzytkownika

    def tearDown(self):
        self.browser.close()




#ukazal się formularz z naglowkiem Rejestracja nowego uzytkownika
#w pole imie wpisal: Pan
#w pole nazwisko wpisal: Kanapka
#w pole login wpisal: PanKanapka
#w pole mail wpisal: pankanpka@pankapka.pl
#w pole haslo wpisal: 0000
#w pole nr telefonu wpisal 666777888
# pole organizacja wpisal: moja firma
#nie pozostalo mu juz nic innego wiec kliknal przycisk rejestracja
#wszystkie pola zostaly wypelnione prawidlowo
#dlatego wyswietlil sie komunikat o poprawnej rejestracji
#a pod nim widnialo pole do wpisania loginu i hasla

#dobra robota pomyślał -  na dzisiaj wystarczy
#zamknął przeglądarkę i poszedł spać