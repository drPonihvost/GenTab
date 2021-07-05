from .models import Project, Object, Marker
from datetime import datetime
from functools import reduce

# OBJECT_NAME_INDEX = 0
#
# REQUORED_FIELDS = {
#     'Sample Name': 1,
#     'Marker': 1,
#     'Allele 1': 1,
#     'Allele 2': 1
# }
#
# def validator(value):
#     if not value:
#         return 'invalid'
#     if value and value == 'OL':
#         return 'partial_valid'
#     return 'valid'
#
#
# def line_to_array(line):
#     return line.split('\t')
#
# # def acc(index, value):
# #     acc = {}
# #     if not value:
# #         return acc
# #     acc[index] = value
#
#
# def parser(data, filename):
#     invalid = False
#
#     # result = {
#     #     validation_data: {},
#     #     project: {}
#     # }
#
#
#     keys_line, *rest = data.splitlines()
#     head = line_to_array(keys_line)
#     def index_map()
#     index_map = reduce(lambda acc, value: acc if not value else acc ({head.index(value): value}), head)
#     print(index_map)
#
#
#     for line in rest:
#         line = line_to_array(line)







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
    if not value:
        return 'invalid'
    if value and value == 'OL':
        return 'partial_valid'
    return 'valid'


def validate_fields(header):
    for i in REQUIRED_KEYS[:4]:
        try:
            header.index(i)
        except ValueError:
            return {"message": f"Отсутствует поле {i}, убедитесь в корректности файла импорта"}


def parser(data, filename):
    invalid = False
#
# def get_dict(header):
#     d = {}
#     for key in REQUIRED_KEYS:
#         if key in header:
#             d[key] = header.index(key)
#     return d
#
#
# def allele_in_list(row, d):
#     alleles = []
#     for i in range(ALLELE_COUNT):
#         if f'Allele {i+1}' in d:
#             alleles.append(row[d[f'Allele {i+1}']])
#         else:
#             alleles.append('')
#     return alleles
#
#
# def validate_and_convert(filename, file):
#     rows = file.splitlines()
#     header = rows[0].split('\t')
#     validate = validate_fields(header)
#     if validate:
#         return validate
#     d = get_dict(header)
#     data = {filename: {}}
#     for row in rows[1:]:
#         row = row.split('\t')
#         sample_name = row[d['Sample Name']]
#         marker = row[d['Marker']]
#         alleles = allele_in_list(row, d)
#         if not data[filename].get(sample_name):
#             data[filename][sample_name] = {marker: alleles}
#         else:
#             data[filename][sample_name][marker] = alleles
#     return data
#
#
# def upload_to_base(data, user_id):
#     for file in data:
#         project = Project.get_by_name(file, user_id)
#         if project:
#             project.delete()
#         project = Project(name=file, user_id=user_id, load_at=datetime.utcnow())
#         project.save()
#         for sample in data[file]:
#             g_object = Object(name=sample, project_id=project.id)
#             g_object.save()
#             for mark, al in data[file][sample].items():
#                 marker = Marker(name=mark,
#                                 object_id=g_object.id,
#                                 allele_1=al[0],
#                                 allele_2=al[1],
#                                 allele_3=al[2],
#                                 allele_4=al[3],
#                                 allele_5=al[4],
#                                 allele_6=al[5])
#                 marker.save()
#     return {"message": f"Файл успешно загружен"}
