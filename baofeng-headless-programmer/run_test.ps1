cd C:\Users\whanusiewicz\.gemini\config\skills\baofeng-headless-programmer
$env:PATH = "$env:PATH;C:\Users\whanusiewicz\.gemini\config\skills\baofeng-headless-programmer"
$env:PYTHONPATH = "C:\Users\whanusiewicz\Documents\antigravity\dazzling-pythagoras\scratch\chirp_src"
.\chirpc.bat -r Baofeng_BF-F8HP --serial=\\.\COM10 --mmap=test.img --download-mmap > test_manual.log 2>&1
