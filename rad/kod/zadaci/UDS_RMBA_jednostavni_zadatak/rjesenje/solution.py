from scapy.contrib.isotp.isotp_native_socket import ISOTPNativeSocket
from scapy.contrib.automotive.uds import *

# rx_id i tx_id je potrebno saznati pomocu caringcariboua,
# kao i dostupnost ReadMemoryByAddress servisa

sock = ISOTPNativeSocket("dcan0", rx_id=0x101, tx_id=0x100, basecls=UDS)

# duljinu size polja treba pogoditi (opcije su 1-4 okteta)
# duljina adrese se moze pogoditi iz teksta zadatka (32 bitna rijec)

# za pogresan format dobiva se negativni odgovor s kodom koji to naglasava

memorySizeLen = 1
memoryAddressLen = 4

data = b""
addr = 0x0
size = 0xFF

print()
while True:
    pckt = sock.sr1(UDS() / UDS_RMBA(memorySizeLen=memorySizeLen,
                                     memoryAddressLen=memoryAddressLen,
                                     memorySize1=size,
                                     memoryAddress4=addr),
                    verbose=False)
    if isinstance(pckt.payload, UDS_NR):
        break
    if isinstance(pckt.payload, UDS_RMBAPR):
        data += pckt.dataRecord
    print(f"Addr: {addr}", end="\r")
    addr += size

print('Writing to file "binary"')
with open("binary", "wb") as f:
    f.write(data)
