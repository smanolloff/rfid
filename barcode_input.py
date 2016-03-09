import ConfigParser
import re
import time
import os

class InvalidInput(Exception):
    def __init__(self, data, message):
        super(InvalidInput, self).__init__(message)
        self.data = data

class ReservedInput(InvalidInput):
    pass

class BarcodeProcessor:
    def __init__(self, config_file):
        self._config_file = config_file
        self._config_dir = os.path.dirname(config_file)
        self._read_config()
        self._format_map = {
            'never': '',
            'yearly': '%Y%m',
            'monthly': '%Y%m',
            'daily': '%Y%m%d',
            'hourly': '%Y%m%d%H'
        }

    def process(self, barcode):
        self._validate_barcode(barcode)

        self._read_config()
        self._timestamp = time.localtime()

        output_file = self._build_filename()
        line = self._build_line(barcode)

        with open(output_file, 'a') as f:
            f.write(line)

        return line

    def _validate_barcode(self, barcode):
        pattern = r'^(\d)\d{11}$'
        match_data = re.match(pattern, barcode)

        if not match_data:
            raise InvalidInput(barcode, "INVALID DATA")
        elif match_data.group(1) in ('0', '3', '4', '5', '6'):
            msg = self._config.get('errors', 'reserved_%s' % match_data.group(1))
            raise ReservedInput(barcode, msg)

        return re.match(pattern, barcode)

    def _read_config(self):
        ini = ConfigParser.ConfigParser()
        ini.read(self._config_file)

        self.output_rot = ini.get('output', 'rotation')
        self.output_ext = ini.get('output', 'extension')
        self.output_dir = ini.get('output', 'directory')

        map_config = CustomParser(ini.get('general', 'mapfile'))
        id_config = CustomParser(ini.get('general', 'idfile'))

        self.tid = id_config['TERMINAL_ID']
        self.oid = id_config['OPERATION_ID']
        self.wid = id_config['WORKER_ID']

        self.worker = map_config.get(self.wid)

    def _build_filename(self):
        timestamp = time.strftime(self._format_map[self.output_rot], self._timestamp)
        basename = '%s-%s.%s' % (self.tid, timestamp, self.output_ext)

        if os.path.isabs(self.output_dir):
            fullname = os.path.join(self.output_dir, basename)
        else:
            fullname = os.path.join(self._config_dir, self.output_dir, basename)

        return fullname

    def _build_line(self, barcode):
        # TODO:
        # if barcode[1:3] == '00':
        #     oid = read_opfile()     # use operation_id from CONFIG08.TXT
        # else:
        #     oid = self.oid          # use operation_id from CONFIG.TXT

        oid = self.oid

        fields = [
            barcode,
            self.tid,
            oid,
            self.wid,
            time.strftime('%d.%m.%Y', self._timestamp),
            time.strftime('%s', self._timestamp),
            '\n'
        ]

        return ';'.join(fields)


def main():
    config_file = 'config.ini'

    while True:
        try:
            data = raw_input()
            processor = BarcodeProcessor(config_file)
            print 'Wrote: %s' % processor.process(data)
        except InvalidInput as ex:
            print ex.message + '\n'


if __name__ == '__main__':
    main()
