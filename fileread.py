
import logging

logger = logging.getLogger(__name__)

class ReadFile:
    """
    Readfile class, outputs a mangled file to proces later.
    """
    def __init__(self,*args, **kwargs):
        self.filename = args[0]
        self.delimiter = kwargs.get('delimiter', ' ')
        self.quotechar = kwargs.get('qchar', '|')

    def read(self):
        import csv
        fh = None
        try:
            fh = open(self.filename,'rb')
            reader = csv.DictReader(fh, delimiter=self.delimiter, quotechar=self.quotechar)
            for row in reader:
                self._read(row)
        except:
            print 'Could not read file'

        self.__mangle(self.rows)

    def _read(self, data):
        logger.info('Got row from person: %s %s' % (data['first_name'], data['last_name']))
        if not hasattr(self, 'rows'):
            self.rows = []

        self.rows.append(data)

    def __mangle(self, rows):
        try:
            import csv
            fh = open(self.filename + '.mangled', 'w')
            writer = csv.DictWriter(fh,fieldnames=['first_name', 'last_name'])
            writer.writeheader()
            for row in self.rows:
                row = self.get_mangled_row(row)
                writer.writerow(row)
        except:
            print('write error')

    def get_mangled_row(self, row):
        a = ""
        for i in range(min(len(row['first_name']), len(row['last_name']))):
            a += row['first_name'][i] + row['last_name'][i]
        if len(row['first_name']) > len(row['last_name']):
            a = a + row['first_name'][min(len(row['first_name']),
                len(row['last_name'])):]
        elif len(row['first_name']) < len(row['last_name']):
            a = a + row['last_name'][min(len(row['first_name']),
                len(row['last_name'])):]
        first, last = a[:len(a)/2], a[len(a)/2:]
        return {'first_name': first, 'last_name': last}

rf = ReadFile('test.csv')
rf.read()
