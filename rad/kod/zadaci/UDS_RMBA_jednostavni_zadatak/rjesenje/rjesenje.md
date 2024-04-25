
# Rješenje

1. Natjecatelj koristi `caringcaribou` alat odnosno njegov `uds discovery` modul za pronalazak ISO-TP adrese na kojoj sluša UDS poslužitelj
2. Potom korištenjem naredbe `caringcaribou uds services` skenira dostupne servise, među kojima se nalazi ReadMemoryByAddress servis
3. Iz teksta zadatka potrebno je zaključiti da je u formatu ReadMemoryByAddress poruke potrebno specificirati 32 bitnu adresu (memoryAddressLen=4). Uz to potrebno je i pogoditi memorySizeLen parametar koji predstavlja duljinu polja za veličinu podataka koje želimo isčitati u oktetima. 
	- parametar memorySizeLen može biti u rasponu \[1, 4\], za pogrešan parametar poslužitelj vraća invalidFormat grešku.
4. Potrebno je napisati Scapy skriptu ili skriptu koja koristi can-utils alate isotprecv, isotpsend kako bi se isčitao cijeli sadržaj memorije ECU-a (solution.py)
5. Pokretanjem naredbe `strings` na dobivenoj binarnoj datoteci natjecatelj pronalazi zastavicu.