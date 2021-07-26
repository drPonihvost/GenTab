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
        return False
    return True


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
    ol_validate = True
    for i in range(ALLELE_COUNT):
        base_key = f'allele_{i + 1}'
        file_key = f'Allele {i + 1}'
        if file_key in header:
            value = row[header.get(file_key)]
            alleles[base_key] = value
            if ol_validate:
                ol_validate = validator(value)
        else:
            alleles[base_key] = ''
    return alleles, ol_validate


def merge_validator(comparison_data):
    if len(comparison_data) > 0:
        return False
    return True


def total_validator(*args):
    if False in args:
        return False
    return True


def merge(old_alleles, new_alleles):
    alleles = {**old_alleles, **new_alleles}
    return alleles


def comparison(old_alleles, new_alleles):
    comparison_validate = []
    for allele, value in new_alleles.items():
        if old_alleles[allele] != value:
            comparison_validate.append({
                'allele': allele,
                'allele_old': old_alleles[allele],
                'allele_new': value
            })
    alleles = merge(old_alleles, new_alleles)
    return alleles, comparison_validate


def parser(data, filename):
    result = {
        'validation_data': {
            'status': 'valid',
            'OL_detect': {},
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
        merge_validate = True
        row = line_to_array(row)
        sample_name = row[header['Sample Name']]
        marker = row[header['Marker']]
        alleles, ol_validate = allele_in_dict(row, header)

        if not data[filename].get(sample_name):
            data[filename][sample_name] = {marker: alleles}
        else:
            if data[filename][sample_name].get(marker):
                old_alleles = data[filename][sample_name][marker]
                new_alleles, ol_validate = allele_in_dict(row, header)
                alleles, comparison_data = comparison(old_alleles, new_alleles)
                merge_validate = merge_validator(comparison_data)
            data[filename][sample_name][marker] = alleles

        total_validate = total_validator(ol_validate, merge_validate)

        if not total_validate and result['validation_data']['status'] == 'valid':
            result['validation_data']['status'] = 'partial_valid'

        if result['validation_data']['OL_detect'].get(sample_name) and ol_validate:
            if result['validation_data']['OL_detect'].get(sample_name).count(marker) > 0:
                x = result['validation_data']['OL_detect'].get(sample_name)
                x.pop(x.index(marker))
                if len(x) == 0:
                    result['validation_data']['OL_detect'].pop(sample_name)

        if not result['validation_data']['OL_detect'].get(sample_name) and not ol_validate:
            result['validation_data']['OL_detect'][sample_name] = [marker]
        elif not ol_validate:
            result['validation_data']['OL_detect'][sample_name].append(marker)

        if not merge_validate:
            result['validation_data']['merge_error'].append({'sample_name': sample_name,
                                                             'marker': marker,
                                                             'data': comparison_data})

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
        samples = []
        for item in data['project'][file]:
            markers = []
            sample = Object(name=item)
            for mark, al in data['project'][file][item].items():
                markers.append(Marker(name=mark, **al))
            sample.marker = markers
            samples.append(sample)
        project.object = samples
        projects.append(project)
    Project.bulk_save(projects)
