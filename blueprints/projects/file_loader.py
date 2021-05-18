from .models import Project, Object, Marker

ALLELE_COUNT = 6


def allele_parser(row_data):
    """Собирает словарь из значений аллелей в количестве указанном в ALLELE_COUNT из словаря переданного в
    row_data, если в словаре менее ALLELE_COUNT аллелей, заменяет пустые значения на None.
    Заменяет пустые строки значений на None"""
    allele_dict = {}
    for i in range(ALLELE_COUNT):
        in_order = row_data.get(f'Allele {i + 1}')
        if in_order:
            allele_dict.update({f'allele_{i + 1}': in_order})
        else:
            allele_dict.update({f'allele_{i + 1}': None})
    return allele_dict


def file_loader(filename, data):
    """Проверка наличия в базе экземпляра класса Project с текущим значением filename,
    при отсутствии объект создается и запускается процедура парсинга данных для создания
    объектов классов Object, Marker.
    При наличии объекта в БД обновляет значения updated_at, удаляет все связанные с проектом
    сущности и записывает новые"""
    project = Project.get_by_name(name=filename)
    if project:
        objects = Object.get_all_name(project_id=project.id)
        for g_object in objects:
            g_object.delete()
    else:
        project = Project(name=filename)
    project.save()
    rows = data.splitlines()
    keys = rows[0].split('\t')[:-1]
    for row in rows[1:]:
        el = row.split('\t')[:-1]
        row_data = {}
        for index, key in enumerate(keys):
            row_data[key] = el[index]
        g_object = Object(name=row_data['Sample Name'], project_id=project.id)
        try:
            g_object.save()
        except:
            continue
        finally:
            g_object = Object.get_by_name(name=row_data['Sample Name'], project_id=project.id)
            alleles = allele_parser(row_data)
            marker = Marker(name=row_data['Marker'],
                            **alleles,
                            object_id=g_object.id
                            )
            marker.save()
