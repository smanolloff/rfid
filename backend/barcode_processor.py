import ConfigParser
import re
import time
import os
import pdb

class BarcodeProcessor:
    def __init__(self, master_config):
        self._master_config = master_config
        self.output_rot = master_config.get('output', 'rotation')
        self.output_ext = master_config.get('output', 'extension')
        self.output_dir = master_config.get('output', 'directory')
        self._config_dir = master_config.get('general', 'mountpoint')

        self.map_config_file = self.subconf_path('mapping')
        self.general_config_file = self.subconf_path('general')
        self.alt_config_file = self.subconf_path('operation')
        self._file_timestamp = time.localtime()
        self._read_config()

    def subconf_path(self, subconf):
      return os.path.join(
          self._config_dir,
          self._master_config.get('config', subconf)
      )

    def process(self, barcode):
        if not self._validate_barcode(barcode):
            return self._process_invalid_input(barcode)
        elif barcode[0] in ('1', '2'):
            return self._process_regular_input(barcode)
        elif barcode[0] in ('7', '8', '9'):
            return self._process_special_input(barcode)
        else:
            return self._process_reserved_input(barcode)

    def _process_regular_input(self, barcode):
        self._read_config()
        self._timestamp = time.localtime()
        line = self._build_line(barcode)
        file = self._build_filename()

        with open(file, 'a') as f:
            f.write(line)

        return ('normal', line)

    def _process_invalid_input(self, barcode):
        return ('invalid', barcode)

    def _process_reserved_input(self, barcode):
        return ('reserved', barcode)

    def _process_special_input(self, barcode):
        self._read_config()
        if barcode[0] == '7':
            new_value = ('terminal', barcode[-3:])
        elif barcode[0] == '8':
            new_value = ('operation', barcode[-2:])
        elif barcode[0] == '9':
            new_value = ('worker', barcode[-3:])

        self.general_config.set('ids', *new_value)
        with open(self.general_config_file, 'w') as f:
            self.general_config.write(f)


        self._read_config() # update with written values
        return ('configure', new_value)

    def _validate_barcode(self, barcode):
        pattern = r'^(\d)\d{11}$'
        match_data = re.match(pattern, barcode)
        return re.match(pattern, barcode)

    def _read_config(self):
        self.map_config = ConfigParser.ConfigParser()
        self.map_config.read(self.map_config_file)

        self.general_config = ConfigParser.ConfigParser()
        self.general_config.read(self.general_config_file)

        self.alt_config = ConfigParser.ConfigParser()
        self.alt_config.read(self.alt_config_file)

        self.tid = self.general_config.get('ids', 'terminal')
        self.oid = self.general_config.get('ids', 'operation')
        self.wid = self.general_config.get('ids', 'worker')
        self.alt_oid = self.alt_config.get('ids', 'operation')

        try:
            self.worker = self.map_config.get('workers', str(self.wid))
        except ConfigParser.NoOptionError, e:
            self.worker = ''

        try:
            self.operation = self.map_config.get('operations', str(self.oid))
        except ConfigParser.NoOptionError, e:
            self.operation = ''

    def _build_filename(self, recursive=False):
        formatted_time = time.strftime('%s', self._file_timestamp)
        basename = '%s-%s.%s' % (self.tid, formatted_time, self.output_ext)

        if os.path.isabs(self.output_dir):
            fullname = os.path.join(self.output_dir, basename)
        else:
            fullname = os.path.join(self._config_dir, self.output_dir, basename)

        if not recursive and not os.access(fullname, os.W_OK):
            self._file_timestamp = self._timestamp
            fullname = self._build_filename(True)


        return fullname

    def _build_line(self, barcode):
        if barcode[1:3] == '00':
            oid = self.alt_oid      # use operation_id from CONFIG08.TXT
        else:
            oid = self.oid          # use operation_id from CONFIG.TXT

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
