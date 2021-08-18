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

    def test_parser_valid_status(self):
        assert self.data['validation_data']['status'] == 'partial_valid'

    def test_parser(self):
        assert self.data['project'][self.filename]['1']['D3S1358'] == init_case(allele_1='15', allele_2='16')


    def test_parser_ol(self):
        assert self.data['project'][self.filename]['2']['D3S1358'] == init_case(allele_1='15', allele_2='OL')
        assert self.data['validation_data']['OL_detect']['2'][0] == 'D3S1358'

    def test_parser_merge(self):
        assert self.data['project'][self.filename]['3']['D3S1358'] == init_case(allele_1='14', allele_2='15')
        assert not self.data['validation_data']['merge_error'][0]['sample_name'] == '3'



        # assert self.data['project'][self.filename]['4']['D3S1358'] == init_case(allele_1='15', allele_2='16')
        # assert self.data['project'][self.filename]['5']['D3S1358'] == init_case(allele_1='16', allele_2='17', allele_3='18')
        # assert self.data['project'][self.filename]['6']['D3S1358'] == init_case(allele_1='15')
        # assert self.data['project'][self.filename]['7']['D3S1358'] == init_case(allele_1='15', allele_2='16', allele_3='OL')
        # assert self.data['project'][self.filename]['8']['D3S1358'] == init_case(allele_1='16', allele_2='OL', allele_3='17')
        # assert self.data['project'][self.filename]['9']['D3S1358'] == init_case(allele_1='16', allele_2='17')
        # assert self.data['project'][self.filename]['10']['D3S1358'] == init_case(allele_1='16', allele_2='17', allele_3='OL')

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
        assert self.data['project'][self.filename]['1']['D3S1358'] == init_case(allele_1='15', allele_2='16')

    def teardown(self):
        self.file.close()
