import os
import shutil
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

cwd = os.getcwd()
archive_dir = os.path.join(cwd, 'ART_archive')
art_dir = os.path.join(archive_dir, 'atomic-red-team-master')
atomics_dir = os.path.join(art_dir, 'atomics')

# Get latest Atomic Red Team
## Remove stale files
try:
    shutil.rmtree(art_dir)
except OSError as e:
    print("Info: %s : %s" % (art_dir, e.strerror))

## Download & extract Atomic Red Team
art_url = "https://github.com/redcanaryco/atomic-red-team/archive/refs/heads/master.zip"
with urlopen(art_url) as response:
    with ZipFile(BytesIO(response.read())) as zfile:
        zfile.extractall(archive_dir)

exit()

file1 = open('urls.txt', 'r')
Lines = file1.readlines()



for line in Lines:
    url=line.strip()
    fullname = os.path.join(cwd, archive_dir, url.split('//')[-1])
    path = os.path.dirname(fullname)
    if not os.path.exists(path):
        os.makedirs(path)

    # Download the file from `url` and save it locally under `file_name`:
    with urlopen(url) as response, open(fullname, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

 