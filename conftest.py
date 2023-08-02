import pytest
import random
import string
from datetime import datetime
from checkout import checkout, OUT_FOLDER, TST_FOLDER, FOLDER_FOLDER, COUNT, FILE_SIZE, ARC_TYPE
from pathlib import Path


@pytest.fixture()
def make_folder():
    return checkout(f'mkdir {TST_FOLDER} {OUT_FOLDER} {FOLDER_FOLDER}', "")


@pytest.fixture()
def clean_folder():
    return checkout(f'rm -rf {TST_FOLDER}/* {OUT_FOLDER}/* {FOLDER_FOLDER}/*', "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(COUNT):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        if checkout(f'cd {TST_FOLDER}; dd if=/dev/urandom of={filename} bs={FILE_SIZE} count=1 iflag=fullblock', ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    if not checkout(f'cd {TST_FOLDER}; mkdir {subfoldername}', ""):
        return None, None
    if not checkout(f'cd {TST_FOLDER}/{subfoldername}; dd if=/dev/urandom of={testfilename} bs={FILE_SIZE} count=1 iflag=fullblock', ""):
        return subfoldername, None
    return subfoldername, testfilename


@pytest.fixture()
def make_bad_archive():
    checkout(f'cd {TST_FOLDER}; 7z a -t{ARC_TYPE} {OUT_FOLDER}/bad', "")
    checkout(f'truncate -s 1 {OUT_FOLDER}/bad.{ARC_TYPE}', "")
    yield
    checkout(f'rm -rf {OUT_FOLDER}/bad.{ARC_TYPE}', "")


@pytest.fixture(autouse=True)
def print_time():
    print(f'Start : {datetime.now().strftime("%H:%M:%S.%f")}')
    yield
    print(f'End : {datetime.now().strftime("%H:%M:%S.%f")}')


@pytest.fixture(autouse=True)
def print_stat():
    yield
    cpu = Path('/proc/loadavg').read_text()
    with open("stat.txt", "a+") as f:
        f.write(f'{datetime.now().strftime("%H:%M:%S.%f")} - {COUNT} - {FILE_SIZE} - {cpu}')
