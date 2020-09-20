import json
import io


class JsonFile:

    def __init__(self, _json_file_name):
        self.file_name = _json_file_name

    def json_img_txt_details_conversion(self, _file_quantity, _current_number, _current_dir):
        percent = (_current_number / _file_quantity) * 100  # percent calc
        current_dir = _current_dir.replace("\\\\", "\\")
        # Define data
        data = {'%': percent,
                'range': _file_quantity,
                'current': _current_number,
                'dir': current_dir}
        # Write JSON file
        with io.open(self.file_name + '.json', 'w', encoding='utf8') as outfile:
            str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
            outfile.write(str_)

    def root_persist(self, _root):
        # Define data
        data = {'root': _root}
        # Write JSON file
        with io.open(self.file_name + '.json', 'w', encoding='utf8') as outfile:
            str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
            outfile.write(str_)

    def json_details_read(self):
        with open(self.file_name + '.json') as f:
            data = json.load(f)
            return data