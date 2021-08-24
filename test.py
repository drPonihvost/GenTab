from blueprints.projects.scripts import parser


def init_case(allele_1='', allele_2='', allele_3='', allele_4='', allele_5='', allele_6=''):
    return {
        'allele_1': allele_1,
        'allele_2': allele_2,
        'allele_3': allele_3,
        'allele_4': allele_4,
        'allele_5': allele_5,
        'allele_6': allele_6
    }


def find_sample(sample, array):
    n = 0
    for i in array:
        if i.get(sample):
            return n
        n += 1


class TestParserInvalid:
    def setup(self):
        self.file = open('test projects/test_invalid.txt', encoding='utf8')
        self.filename = self.file.name
        self.data = parser(data=self.file.read(), filename=self.filename)

    def test_parser_valid_status(self):
        assert self.data['validation_data']['status'] == 'invalid'

    def teardown(self):
        self.file.close()


class TestParserPartialValid:
    def setup(self):
        self.file = open('test projects/test_partial_valid.txt', encoding='utf8')
        self.filename = self.file.name
        self.data = parser(data=self.file.read(), filename=self.filename)
        self.status_file = self.data['validation_data']['status']
        self.ol_detect = self.data['validation_data']['ol_detect'][0]['marker'][0]

    def test_parser_valid_status(self):
        assert self.status_file == 'partial_valid'

    def test_parser_ol(self):
        for i in range(1, 3):
            sample_index = find_sample(sample=str(i), array=self.data['object_list'])
            assert self.data['project'][self.filename][str(i)]['D3S1358'] == init_case(allele_1='15', allele_2='OL')
            assert self.data['object_list'][sample_index]['status'] == 'partial_valid'
            assert self.ol_detect == 'D3S1358'


    def teardown(self):
        self.file.close()


class TestParserValid:
    def setup(self):
        self.file = open('test projects/test_valid.txt', encoding='utf8')
        self.filename = self.file.name
        self.data = parser(data=self.file.read(), filename=self.filename)

    def test_parser_valid_status(self):
        assert self.data['validation_data']['status'] == 'valid'



    def test_parser_alleles(self):
        sample_index = find_sample(sample='1', array=self.data['object_list'])
        assert self.data['project'][self.filename]['1']['D3S1358'] == init_case(allele_1='15', allele_2='16')
        assert self.data['object_list'][sample_index]['status'] == 'valid'

        sample_index = find_sample(sample='2', array=self.data['object_list'])
        assert self.data['project'][self.filename]['2']['D3S1358'] == init_case(allele_1='15', allele_2='15')
        assert self.data['object_list'][sample_index]['status'] == 'valid'

    def teardown(self):
        self.file.close()
