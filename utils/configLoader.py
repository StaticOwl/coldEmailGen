from configparser import ConfigParser as cp


def load_config(filename, section):
    with open(filename) as f:
        f.readline()
    parser = cp()
    parser.read(filename)
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return config
