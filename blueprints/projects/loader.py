from datetime import datetime

from .models import db, Project, Object, Marker


def allele_parser(row_data):
    """Собирает список из значений 6 аллелей в словаре переданном в
    row_data, если в словаре менее 6 аллелей, заменяет пустые значения на None.
    Заменяет пустые строки значений на None"""
    allele_list = []
    for i in range(1, 7):
        if row_data.get(f'Allele {i}') is not None:
            if row_data.get(f'Allele {i}') != '':
                allele_list.append(row_data.get(f'Allele {i}'))
            else:
                allele_list.append(None)
        else:
            allele_list.append(None)
    return allele_list


def marker_loader(row_data, g_object):
    """Проверка на наличие маркера с id объекта в базе, при отсутствии возвращает
     экземпляр класса Marker с текущими данными. При наличии в базе маркера с текущим id
     производит перезапись значений аллелей"""
    allele = allele_parser(row_data)
    if Marker.query.filter_by(name=row_data.get('Marker'), object_id=g_object.id).first() is None:
        marker = Marker(name=row_data.get('Marker'),
                        allele_1=allele[0],
                        allele_2=allele[1],
                        allele_3=allele[2],
                        allele_4=allele[3],
                        allele_5=allele[4],
                        allele_6=allele[5],
                        object_id=g_object.id)
        return marker
    else:
        marker = Marker.query.filter_by(name=row_data.get('Marker'), object_id=g_object.id).first()
        marker.allele_1, marker.allele_2, marker.allele_3, marker.allele_4, marker.allele_5, marker.allele_6 =\
            allele[0], allele[1], allele[2], allele[3], allele[4], allele[5]
        return marker


def object_loader(row_data, project):
    """Проверка на наличие объекта с id проекта в базе, при отсутствии возвращает
         экземпляр класса Object с текущими значениями. При наличии в базе объекта с текущим id
         производит перезапись значений id и project_id"""
    if Object.query.filter_by(name=row_data.get('Sample Name'), project_id=project.id).first() is None:
        g_object = Object(name=row_data.get('Sample Name'), project_id=project.id)
        return g_object
    else:
        g_object = Object.query.filter_by(name=row_data.get('Sample Name'), project_id=project.id).first()
        g_object.name, g_object.project_id = row_data.get('Sample Name'), project.id
        return g_object


def data_parser(data, project):
    """Парсинг данных из data. Первой строкой передаются ключи,
    из которых построчно создается словарь. Подключение функций создания объектов,
    загружаемых в БД"""
    rows = data.splitlines()
    keys = rows[0].split('\t')[:-1]
    for row in rows[1:]:
        el = row.split('\t')[:-1]
        row_data = {}
        for index, key in enumerate(keys):
            row_data[key] = el[index]
        g_object = object_loader(row_data, project)
        db.session.add(g_object)
        db.session.flush()
        marker = marker_loader(row_data, g_object)
        db.session.add(marker)
        db.session.flush()


def loader(filename, data):
    """Проверка наличия в базе экземпляра класса Project с текущим значением filename,
    при отсутствии объект создается и запускается процедура парсинга данных для создания
    объектов классов Object, Marker.
    При наличии объекта в БД обновляет значения updated_at, а так же объекты классов Object, Marker
    """
    if Project.query.filter_by(name=filename).first() is None:
        project = Project(name=filename)
        db.session.add(project)
        db.session.flush()
        data_parser(data, project)
    else:
        project = Project.query.filter_by(name=filename).first()
        project.updated_at = datetime.utcnow()
        db.session.add(project)
        db.session.flush()
        data_parser(data, project)
    db.session.commit()
