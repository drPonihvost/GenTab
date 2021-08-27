import pytest
import random

@pytest.fixture(autouse=True)
def clean_file():
    with open('test_file.txt', 'w') as file:
        file.writelines('Sample Name\tRun Name\tPanel\tMarker\tDye\tAllele 1\tAllele 2\tAllele 3\tAllele 4\tAllele 5\tAllele 6\t\n')