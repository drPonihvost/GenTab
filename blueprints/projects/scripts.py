from .models import Project, Object, Marker
from datetime import datetime


ALLELE_COUNT = 6
REQUIRED_KEYS = ['Sample Name',
                 'Marker',
                 'Allele 1',
                 'Allele 2',
                 'Allele 3',
                 'Allele 4',
                 'Allele 5',
                 'Allele 6']


def line_to_array(line):
    return line.split('\t')


def validator(value):
    if value == 'OL':
        return 'partial_valid'
    return 'valid'


def validate_fields(header):
    for i in REQUIRED_KEYS[:4]:
        if header.count(i) == 0:
            return 'invalid'


def get_dict(header):
    d = {}
    for key in REQUIRED_KEYS:
        if key in header:
            d[key] = header.index(key)
    return d


def allele_in_dict(row, header):
    alleles = {}
    allele_validate = 'valid'
    for i in range(ALLELE_COUNT):
        base_key = f'allele_{i+1}'
        file_key = f'Allele {i+1}'
        if file_key in header:
            value = row[header.get(file_key)]
            alleles[base_key] = value
            if allele_validate == 'valid':
                allele_validate = validator(value)
        else:
            alleles[base_key] = ''
    return alleles, allele_validate


def parser(data, filename):



    result = {
        "validation_data": {
            "status": 'valid',
            'data':[]
        },
        "project": {}
    }

    keys_line, *rest = data.splitlines()
    header = line_to_array(keys_line)
    if validate_fields(header) == 'invalid':
        result["validation_data"]["status"] = 'invalid'
        return result

    header = get_dict(header)
    data = {filename: {}}
    for row in rest:
        row = line_to_array(row)
        sample_name = row[header['Sample Name']]
        marker = row[header['Marker']]
        alleles, allele_validate = allele_in_dict(row, header)

        if not data[filename].get(sample_name):
            data[filename][sample_name] = {marker: alleles}
        else:
            data[filename][sample_name][marker] = alleles

        if allele_validate == 'partial_valid' and result['validation_data']['status'] == 'valid':
            result['validation_data']['status'] = 'partial_valid'
            result['validation_data']['data'].append({'sample_name': sample_name, 'marker': marker})
        elif allele_validate == 'partial_valid':
            result['validation_data']['data'].append({'sample_name': sample_name, 'marker': marker})

    result['project'] = data
    return result


def upload_to_base(data, user_id):
    for file in data:
        project = Project.get_by_name(file, user_id)
        if project:
            project.delete()
        project = Project(name=file, user_id=user_id, load_at=datetime.utcnow())
        project.save()
        for sample in data[file]:
            g_object = Object(name=sample, project_id=project.id)
            g_object.save()
            for mark, al in data[file][sample].items():
                marker = Marker(object_id=g_object.id, name=mark, **al)
                marker.save()