# Fix Covers
KUAL extension to fix missing covers of sideloaded books on Kindle

Requires Jailbroken Kindle, KUAL & Python 3 installed

Reads db directly
If cover is missing or too small to be a "real" cover it will:
 * use a local cover in the documents folder (Naming convention is name of book in lower case with _ instead of spaces .jpg)
 * if no local cover is found it will download the first match on open library for title and author

Log file in base kindle folder

To Run, simply place this entire folder in the extensions folder and then launch KUAL and pick Fix Covers > Fix Covers
