import pytest

from blueprints.projects.scripts import parser
import random

CYCLE = 100
SEQUENCE = ['', 'OL', '9', '10', '11', '12', '13', '14', '14.3', '15', '15.3',
            '16', '16.3', '17', '17.3', '18', '18.3', '19', '19.3', '20.3', 'OL']

DECREASE_SEQUENCE = ['', '15', '16', '17', 'OL']


def form_allele_list(sequence):
    alleles = []
    sequence = sequence.copy()
    for i in range(6):
        allele = random.choice(sequence)
        allele_1_index = sequence.index(allele)
        if len(sequence[allele_1_index::]) > 1:
            sequence = sequence[allele_1_index::]
            if allele == '':
                sequence = ['']
            elif alleles.count(allele) > 0 and alleles.index(allele) == 0 and i == 1:
                sequence = ['']
            elif alleles.count(allele) > 0:
                sequence.remove(allele)
                allele = random.choice(sequence)
        alleles.append(allele)
    return alleles


def create_test_data(
        sample_name,
        allele_1,
        allele_2,
        allele_3,
        allele_4,
        allele_5,
        allele_6

):
    return '{}\ttest_run\tPowerPlex_Fusion_6C_Panels_IDX_v1.3\tD1S1656\tB\t{}\t{}\t{}\t{}\t{}\t{}\t\n'.format(
        sample_name,
        allele_1,
        allele_2,
        allele_3,
        allele_4,
        allele_5,
        allele_6
    )


def create_data_array(decrease=False):
    array = []
    sequence = SEQUENCE
    if decrease:
        sequence = DECREASE_SEQUENCE

    for i in range(CYCLE):
        alleles_old = form_allele_list(sequence)
        alleles_new = form_allele_list(sequence)
        alleles_old.insert(0, str(i))
        alleles_new.insert(0, str(i))
        array.append((alleles_old, alleles_new))
    return array


def set_status(alleles):
    if 'OL' in alleles:
        return 'partial_valid'
    return 'valid'


@pytest.mark.parametrize('alleles', [i for i in create_data_array()])
def test_parser(alleles):
    alleles = alleles[0]
    content = create_test_data(*alleles)
    status = set_status(alleles)
    in_file = {'D1S1656': {
        'allele_1': alleles[1],
        'allele_2': alleles[2],
        'allele_3': alleles[3],
        'allele_4': alleles[4],
        'allele_5': alleles[5],
        'allele_6': alleles[6],
    }}

    with open('test_file.txt', 'a') as file:
        file.writelines(content)
    with open('test_file.txt', 'r') as file:
        filename = file.name
        file = file.read()
        data = parser(file, filename)

    sample_in_parser = next(iter(data['project'][filename]))
    alleles_in_parser = in_file['D1S1656']
    status_file_in_parser = data['validation_data']['status']
    status_sample_in_parser = data['object_list'][0]['status']
    ol_validate = None

    assert data['project'][filename][alleles[0]] == in_file
    assert data['validation_data']['status'] == status
    assert data['object_list'][0]['status'] == status
    if status == 'partial_valid':
        ol_validate = data['validation_data']['OL_detect'][0]['marker']
        assert data['validation_data']['OL_detect'][0]['marker'][0] == 'D1S1656'

    print(f'\n Объект {alleles[0]} записан как {sample_in_parser}\n',
          f'Генерируемые значения {alleles[1::]} записаны как:\n{alleles_in_parser}\n'
          f'Статус файла: {status_file_in_parser}\n'
          f'Статус объекта: {status_sample_in_parser}\n'
          f'Параметры валидации: {ol_validate}')


@pytest.mark.parametrize('alleles_old, alleles_new', [i for i in create_data_array(decrease=True)])
def test_parser_merge(alleles_old, alleles_new):
    content_old = create_test_data(*alleles_old)
    content_new = create_test_data(*alleles_new)
    status_old = set_status(alleles_old)
    status_new = set_status(alleles_new)
    merge_status = alleles_old == alleles_new
    in_file_old = {'D1S1656': {
        'allele_1': alleles_old[1],
        'allele_2': alleles_old[2],
        'allele_3': alleles_old[3],
        'allele_4': alleles_old[4],
        'allele_5': alleles_old[5],
        'allele_6': alleles_old[6],
    }}

    with open('test_file.txt', 'a') as file:
        file.writelines(content_old)
        file.writelines(content_new)
    with open('test_file.txt', 'r') as file:
        filename = file.name
        file = file.read()
        data = parser(file, filename)

    sample_in_parser = next(iter(data['project'][filename]))
    alleles_in_parser = [in_file_old['D1S1656'].get(i) for i in in_file_old['D1S1656']]
    status_file_in_parser = data['validation_data']['status']
    status_sample_in_parser = data['object_list'][0]['status']
    ol_validate = None
    merge_validate = None

    assert data['project'][filename][alleles_old[0]] == in_file_old
    if merge_status:
        if status_old == 'partial_valid' or status_new == 'partial_valid':
            ol_validate = data['validation_data']['OL_detect'][0]['marker']
            assert data['validation_data']['status'] == 'partial_valid'
            assert data['object_list'][0]['status'] == 'partial_valid'
        else:
            assert data['validation_data']['status'] == 'valid'
            assert data['object_list'][0]['status'] == 'valid'
    else:
        merge_validate = data['validation_data']['merge_error'][0]['marker']
        if status_old == 'partial_valid' or status_new == 'partial_valid':
            ol_validate = data['validation_data']['OL_detect'][0]['marker']
            assert data['validation_data']['status'] == 'partial_valid'
            assert data['object_list'][0]['status'] == 'invalid'
            assert data['validation_data']['OL_detect'][0]['marker'][0] == 'D1S1656'
            assert data['validation_data']['merge_error'][0]['marker'][0] == 'D1S1656'
        else:
            assert data['validation_data']['status'] == 'partial_valid'
            assert data['object_list'][0]['status'] == 'invalid'
            assert data['validation_data']['merge_error'][0]['marker'][0] == 'D1S1656'

    print(f'\nОбъект {alleles_old[0]} записан как {sample_in_parser}\n'
          f'Генерируемые значения\t{alleles_old[1::]}\n'
          f'\t\t\t\t\t\t{alleles_new[1::]}\n'
          f'записаны как:\t\t\t{alleles_in_parser}\n'
          f'Статус файла: {status_file_in_parser}\n'
          f'Статус объекта: {status_sample_in_parser}\n'
          f'Параметры валидации OL: {ol_validate}\n'
          f'Параметры валидации merge: {merge_validate}')
