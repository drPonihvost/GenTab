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


def find_sample_in_array(array, sample_name):
    n = 0
    for i in array:
        if i.get('sample_name') == sample_name:
            return True, n
        n += 1
    return False, n - 1


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


def total_validator(*args):
    if False in args:
        return False
    return True


def merge(old_alleles, new_alleles):
    merge_validate = True
    allele_list = [j for i, j in old_alleles.items()]
    if len(set(allele_list)) == 1:
        return new_alleles, merge_validate
    for allele, value in new_alleles.items():
        if old_alleles[allele] != value:
            merge_validate = False
    return old_alleles, merge_validate


def form_result(status, ol_detect, merge_error, project, object_list):
    return {
        'validation_data': {
            'status': status,
            'OL_detect': ol_detect,
            'merge_error': merge_error
        },
        'project': project,
        'object_list': object_list
    }


def parser(data, filename):
    status = 'valid'
    ol_detect = []
    merge_error = []
    project = {filename: {}}
    object_list = []

    keys_line, *rest = data.splitlines()
    header = line_to_array(keys_line)
    if validate_fields(header) == 'invalid':
        status = 'invalid'
        return form_result(status, ol_detect, merge_error, project, object_list)

    header = get_dict(header)

    for row in rest:
        merge_validate = True
        row = line_to_array(row)
        sample_name = row[header['Sample Name']]
        marker = row[header['Marker']]
        alleles, ol_validate = allele_in_dict(row, header)

        if not project[filename].get(sample_name):
            project[filename][sample_name] = {marker: alleles}
            object_list.append(
                {
                    'sample_name': sample_name,
                    'status': 'valid'
                }
            )
        else:
            if project[filename][sample_name].get(marker):
                old_alleles = project[filename][sample_name][marker]
                new_alleles, new_ol_validate = allele_in_dict(row, header)
                alleles, merge_validate = merge(old_alleles, new_alleles)
                ol_validate = total_validator(ol_validate, new_ol_validate)

            project[filename][sample_name][marker] = alleles

        total_validate = total_validator(ol_validate, merge_validate)

        if not total_validate and status == 'valid':
            status = 'partial_valid'

        sample_in_object_list, sample_index = find_sample_in_array(object_list, sample_name)

        sample_containing_ol, object_index = find_sample_in_array(ol_detect, sample_name)

        if not sample_containing_ol and not ol_validate:
            ol_detect.append({'sample_name': sample_name, 'marker': [marker]})
        elif not ol_validate and not sample_containing_ol:
            ol_detect[object_index]['marker'].append(marker)

        sample_containing_merge_error, object_index = find_sample_in_array(merge_error, sample_name)

        if not sample_containing_merge_error and not merge_validate:
            merge_error.append({'sample_name': sample_name, 'marker': [marker]})
        elif not merge_validate:
            merge_error[object_index]['marker'].append(marker)

        object_in_list = object_list[sample_index]

        if object_in_list['status'] == 'valid' and not ol_validate and merge_validate:
            object_in_list['status'] = 'partial_valid'
        elif not merge_validate:
            object_in_list['status'] = 'invalid'

    return form_result(status, ol_detect, merge_error, project, object_list)


def create_object_list(data):
    return [i['sample_name'] for i in data['object_list'] if i['status'] == 'valid']


def form_objects_only_base(object_list, object_in_base):
    return [i for i in object_in_base if i not in object_list]


def create_markers(sample):
    return [Marker(name=marker, **alleles) for marker, alleles in sample.items()]


def upload_to_base(data, user_id):
    object_list = create_object_list(data=data)
    filename = [i for i in data['project']][0]
    project = Project.get_by_user(filename, user_id)
    if project:
        update_record(data, user_id, filename, object_list)
        return {'msg': f'Проект {filename} обновлен'}
    else:
        create_record(data, user_id, filename, object_list)
        return {'msg': f'Проект {filename} загружен'}


def create_record(data, user_id, filename, object_list):
    projects = []
    project = Project(
        name=filename,
        user_id=user_id,
        load_at=datetime.utcnow()
    )
    samples = []
    for item in data['project'][filename]:
        if item not in object_list:
            continue
        sample = Object(name=item)
        sample.marker = create_markers(data['project'][filename][item])
        samples.append(sample)
    project.object = samples
    projects.append(project)
    Project.bulk_save(projects)


def update_record(data, user_id, filename, object_list):
    project = Project.get_by_user(filename, user_id)
    object_in_base = Object.get_name_by_project_id(project_id=project.id)
    only_base = form_objects_only_base(object_list, object_in_base)
    projects = []
    project.load_at = datetime.utcnow()
    samples = []
    for item in data['project'][filename]:
        sample = Object.get_by_name(name=item, project_id=project.id)
        if not sample and item not in object_list:
            continue
        elif not sample and item in object_list:
            sample = Object(name=item)
            sample.marker = create_markers(data['project'][filename][item])
            samples.append(sample)
        elif sample and item in object_list:
            sample.marker = create_markers(data['project'][filename][item])
            samples.append(sample)
    if only_base:
        for item in only_base:
            sample = Object.get_by_name(name=item, project_id=project.id)
            samples.append(sample)
    project.object = samples
    projects.append(project)
    Project.bulk_save(projects)
