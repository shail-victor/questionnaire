import os, configparser, io


def read_properties_file(file_path):
    """
    Reading the property file as passed in the file_path

   :param file_path: path of the file/filename
   :return: dict

   """
    with open(file_path) as f:
        config = io.StringIO()
        config.write('[dummy_section]\n')
        config.write(f.read().replace('%', '%%'))
        config.seek(0, os.SEEK_SET)

        cp = configparser.SafeConfigParser()
        cp.readfp(config)

        return dict(cp.items('dummy_section'))