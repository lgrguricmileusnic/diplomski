# Platforma za obuku stručnjaka kibernetičke sigurnosti u području automobilske industrije

## Motivacija
Za razliku od ostalih područja kibernetičke sigurnosti, postoji nedostatak edukacijskih platformi za kibernetičku sigurnost u autoindustriji.

### Postojeća rješenja
- nepotpune implementacije CAN simulacija 
	- https://github.com/carloop/simulator-program
	- https://github.com/duraki/virtualcar/tree/master/src
	- https://medium.com/@naoumine/vehicle-hacking-with-icsim-part-1-f4bd632cac9e
- Cloudcar CTF
	- https://cloudcar.canbushack.com/
	- https://www.youtube.com/watch?v=0CjFu-K3gNY
	- isključivo hakiranje CAN-a
	- ograničeno na par izazova (situacija)
	- zatvoreni kod
- trenutni automotive CTF-ovi se temelje na reverzanju firmwarea i analizi snimljenog CAN prometa
- iznimke su CTF-ovi gdje organizatori imaju resursa sastaviti stvarnu mrežu ECU-ova i ostale auto elektronike

## Ideja
Platformu koja bi podržavala izazove čija rješenja uključuju ulančavanje CAN, Bluetooth, WiFi (i potencijalno web ranjivosti). Platforma bi se za potrebe diplomskog rada zasnivala na SBC-u poput Raspberry Pi-a.
### Virtualni dio
**Mreža virtualnih ECU-ova** koji mogu biti implementirani kao:
- linux containeri koji komuniciraju putem CAN socketa na temelju snimljenih pcap datoteka
	- stvarni ECU-ovi ne koriste linux, ali nije smisao platforme iskoristiti ranjivosti u samoj implementaciji CAN socketa nego snimati i analizirati promet između ECU-ova te "razgovarati" s njima
- neka druga vrsta softverske implementacije koristeći više procesa/dretvi gdje svaki proces/dretva predstavlja jedan ECU
- mrežu bi bilo moguće konfigurirati kroz neku vrstu konfig datoteka (slično kako IMUNES pohranjuje svoje konfiguracije mreža) ili kroz grafičko sučelje
- ograničenje ovakvog pristupa je što se potencijalno gube neki fizički elementi CAN sabirnice poput arbitraže koja omogućava određene vrste DoS napada

**Bluetooth, WiFi stogovi**
Obzirom da se dio IVI sustava u industriji zasniva na Linuxu (npr. Yocto), takvi sustavi mogu potencijalno koristiti ranjive WiFi i Bluetooth stogove. Platforma bi podržavala konfiguriranje takvih ranjivih stogova, što bi omogućilo simuliranje napada koji foothold ostvaraju kroz IVI.

**Web?**
Neki IVI sustavi imaju pristup webu za što koriste postojeće web rendering engine zajedno s njihovim ranjivostima. Platforma bi podržavala konfiguriranje takvih ranjivih web rendering enginea, što bi omogućilo simuliranje napada koji foothold ostvaraju kroz IVI.
Primjer s AppleWebKit-om u BMW-u:
https://i.blackhat.com/USA-19/Thursday/us-19-Cai-0-Days-And-Mitigations-Roadways-To-Exploit-And-Secure-Connected-BMW-Cars-wp.pdf
### Sklopovski dio
**Single board računalo** poput Raspberry Pi-a ili nekog x86 ekvivalenta. Na računalo bi bio spojen ženski OBD konektor. Spajanje na OBD konektor pomoću drugog računala ili neke vrste CAN analizatora bi omogućilo slanje i primanje poruka iz nekog od ECU-a konfiguriranog u virtualnom dijelu (ili više njih). Obzirom da SBC-ovi imaju i USB portove i oni se mogu koristiti/konfigurirati kao potencijalni vektor napada.
### Platforma
Kompromitiranje određenih ECU-ova, ostvarivanje footholda i slično može nositi bodove kao na HackTheBox i TryHackMe platformama. Korisnik bi mogao preuzeti konfiguracijske datoteke za izazove koje onda može učitati u svoj hardver. Konfiguracijske datoteke bi definirale topologiju virtualne mreže, čvorove kojima može pristupiti putem vanjskog OBD konektora, funkcije USB portova, ciljeve koje mora kompromitirati, Bluetooth/Wi-fi stackove i web rendering engine koji se koristi.
https://downloads.distrinet-research.be/software/sancus/publications/werquin2019.pdf

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

#### Primjer izazova
Inspiriran primjerom iz stvarnog svijeta: https://www.thetruthaboutcars.com/cars/news-blog/thieves-steal-toyota-rav4-by-hacking-into-its-headlights-44500318

**Početna postava izazova**
Napadač (korisnik) se nalazi izvan automobila te ima pristup CAN sabirnici spojenoj na prednji far. Na USB priključku nije onemogućeno spajanje HID uređaja.
**Ciljevi:** kompromitirati ECU koji upravlja otključavanjem/zaključavanjem vrata, kompromitirati IVI

**Tijek rješavanja zadatka**
1. Korisnik spaja drugo računalo na OBD priključak Raspberry Pi "automobila"
2. snimanje CAN prometa iz perspektive CAN priključka prednjeg fara
3. prepoznavanje poruka otključaj/zaključaj poslanih ECU-u za otključvanje/zaključavanje vrata koji nije ispravno separiran na sigurnosno kritičnu CAN sabirnicu
4. otključavanje vrata automobila replay napadom
5. platforma sada omogućava korisniku da se spoji preko USB priključka na Raspberry Pi-u
6. korisnik spaja tipkovnicu u Raspberry Pi i ostvaruje pristup ljuski te izvlači ivi_flag.txt

**Alternativni scenarij**i
- spajanjem "automobila" na isti Wi-fi te skeniranjem portova korisnik otkriva da su developeri zaboravili ugasiti ssh server koji je pogrešno konfiguriran ili ima ranjivosti
- korisnik dobije dio koda koji upravlja Bluetooth vezama, otkriva command injection ranjivost jer se ime BT uređaja ne sanitizira prije korištenja u shell-u

## Sužavanje opsega posla
Obzirom da mi se koncept diplomskog čini pun nepredvidivih problema, kroz diplomski projekt bi se fokusirao samo na virtualnu mrežu ECU-ova i komunikaciju s "vanjskim svijetom" kroz OBD konektor.
Potom bih razmotrio preostalu količinu posla za implementaciju ostatka platforme, odlučio se za neke ili sve od navedenih mogućnosti, implementirao demo izazove.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

### Druge slične jednostavnije ideje 
- izraditi nešto poput [DVWA](https://github.com/digininja/DVWA)
	- simulaciju automobila s puno ranjivih komponenata i različitim načinima pristupa na istom hardveru kao u inicijalnoj ideji, ali bez strukturiranih ciljeva i izazova s nekim smislom, više kao automotive cybersecurity "igralište"
- modificirati IMUNES za stvaranje virtualne mreže ECU-ova
