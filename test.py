from blueprints.projects.scripts import parser


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

    def test_parser_ol(self):
        assert self.data

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
        case = {
            'allele_1': '15',
            'allele_2': '16',
            'allele_3': '',
            'allele_4': '',
            'allele_5': '',
            'allele_6': ''
        }
        assert self.data['project'][self.filename]['1']['D3S1358'] == case

    def teardown(self):
        self.file.close()
