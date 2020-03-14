# undocumented / unknown DNS call 

# author: size_t
#================================================================================================================================================================================


# Import the required module to handle Windows API Calls
import ctypes

# Import Python -> Windows Types from ctypes
from ctypes.wintypes import DWORD,HANDLE,LPWSTR

# getting a handle to kernel32.dll & DNSAPI.dll
k_handle = ctypes.WinDLL("Kernel32.dll")
dns_handle = ctypes.WinDLL("DNSAPI.dll")


# DNS_CACHE_ENTRY Structure
class DNS_CACHE_ENTRY(ctypes.Structure):
	_fields_ = [
	("pNext", HANDLE),
	("recName", LPWSTR),
	("wType", DWORD),
	("wDataLength", DWORD),
	("dwFalgs", DWORD),
	]

print("[INFO] Pulling DNS Cache Data From System...")

# setup a new Base Entry	
DNS_Entry = DNS_CACHE_ENTRY()

# configuring the size of the Entry
DNS_Entry.wDataLength = 1024

# execute the Windows API Call to grab the DNS Entry Cache
response = dns_handle.DnsGetCacheDataTable(ctypes.byref(DNS_Entry))

# handling any errors
if response == 0:
	print("[ERROR] Failed to get DNS Cache Table.. Error Code: {0}".format(k_handle.GetLastError()))

print("[INFO] Got DNS Cache Table, Parsing Data...")

# Getting the first pNext
# Converting a pointer to a structure to ignore the first entry as its 0
DNS_Entry = ctypes.cast(DNS_Entry.pNext, ctypes.POINTER(DNS_CACHE_ENTRY))

while True:
	# Handle try catch for when we dont have any more entries
	try:
		print("[INFO] DNS Entry: {0} - Type: {1}".format(DNS_Entry.contents.recName, DNS_Entry.contents.wType))
		DNS_Entry = ctypes.cast(DNS_Entry.contents.pNext, ctypes.POINTER(DNS_CACHE_ENTRY))
	except:
		break
		
print("[INFO] DNS Cache Table Dumped")


