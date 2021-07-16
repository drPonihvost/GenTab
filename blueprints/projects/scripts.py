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
        base_key = f'allele_{i + 1}'
        file_key = f'Allele {i + 1}'
        if file_key in header:
            value = row[header.get(file_key)]
            alleles[base_key] = value
            if allele_validate == 'valid':
                allele_validate = validator(value)
        else:
            alleles[base_key] = ''
    return alleles, allele_validate


def merge(old_alleles, new_alleles):
    alleles = {**old_alleles, **new_alleles}
    return alleles


def comparison(old_alleles, new_alleles):
    comparison = []
    for allele, value in new_alleles.items():
        if old_alleles[allele] != value:
            comparison.append({'allele': allele,
                               'allele_old': old_alleles[allele],
                               'allele_new': value})
    alleles = merge(old_alleles, new_alleles)
    return alleles, comparison


def parser(data, filename):
    result = {
        'validation_data': {
            'status': 'valid',
            'OL_detect': [],
            'merge_error': []
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
        comparison_validate = []
        row = line_to_array(row)
        sample_name = row[header['Sample Name']]
        marker = row[header['Marker']]
        alleles, allele_validate = allele_in_dict(row, header)

        if not data[filename].get(sample_name):
            data[filename][sample_name] = {marker: alleles}
        else:
            if data[filename][sample_name].get(marker):
                old_alleles = data[filename][sample_name][marker]
                new_alleles, allele_validate = allele_in_dict(row, header)
                alleles, comparison_validate = comparison(old_alleles, new_alleles)
                if len(comparison_validate) > 0:
                    allele_validate = 'partial_valid'
            data[filename][sample_name][marker] = alleles

        if allele_validate == 'partial_valid' and result['validation_data']['status'] == 'valid':
            result['validation_data']['status'] = 'partial_valid'
            result['validation_data']['OL_detect'].append({'sample_name': sample_name, 'marker': marker})
            if len(comparison_validate) > 0:
                result['validation_data']['merge_error'].append({'sample_name': sample_name,
                                                                 'marker': marker,
                                                                 'data': comparison_validate})
        elif allele_validate == 'partial_valid':
            result['validation_data']['OL_detect'].append({'sample_name': sample_name, 'marker': marker})
            if len(comparison_validate) > 0:
                result['validation_data']['merge_error'].append({'sample_name': sample_name,
                                                                 'marker': marker,
                                                                 'data': comparison_validate})

    result['project'] = data
    return result


def upload_to_base(data, user_id):
    projects = []
    for file in data['project']:
        project = Project.get_by_user(file, user_id)
        if project:
            project.delete()
        project = Project(name=file,
                          user_id=user_id,
                          load_at=datetime.utcnow(),
                          validation_data=data['validation_data'])
        objects = []
        for sample in data['project'][file]:
            markers = []
            object = Object(name=sample)
            for mark, al in data['project'][file][sample].items():
                markers.append(Marker(name=mark, **al))
            object.marker = markers
            objects.append(object)
        project.object = objects
        projects.append(project)
    Project.bulk_save(projects)
