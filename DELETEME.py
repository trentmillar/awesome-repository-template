import os


ROOT_DIR='.'
INCLUDE_DIRS=['.github']

PROPERTY_SPLITER='='

TOKEN_FILE='DELETEME.txt'
TOKEN = '@'
TOKEN_GROUP = '{{' + TOKEN + '}}'


def build_include_dirs():
    full_include_dirs = []
    for dir in INCLUDE_DIRS:
        full_include_dirs.append(os.path.join(ROOT_DIR, dir))

    return full_include_dirs


def can_walk(path, walkable_dirs):
    path = os.path.relpath(path, ROOT_DIR)
    for walkable in walkable_dirs:
        walkable = os.path.basename(walkable)
        if path.startswith(walkable):
            return True
    return False


def replaceable_files():
    replaceables = []
    walkable_dirs = build_include_dirs()

    for path, dirnames, filenames in os.walk(ROOT_DIR):
        if not can_walk(path, walkable_dirs):
            continue

        for file in filenames:
            replaceables.append(os.path.join(path, file))

    return replaceables


def build_token_pairs():
    try:
        pairs = {}
        with open(os.path.join(ROOT_DIR, TOKEN_FILE), 'r') as file:
            for line in file.read().splitlines():
               kv = line.split(PROPERTY_SPLITER)
               key = TOKEN_GROUP.replace(TOKEN, kv[0])
               pairs[key] = kv[1]
        return pairs

    except IOError:
        print('This script must be executed in the root of the repo and %s must exist' % TOKEN_FILE)


def substitute_tokens(files_to_replace, key_values):
    try:
        for file_path in files_to_replace:
            with open(file_path, 'r') as file:
                content = file.read()

            for (key, value) in key_values.items():
                content = content.replace(key, value)

            with open(file_path, 'w') as file:
                file.write(content)

    except IOError as error:
        print('Unable to substitute, %e', error)


if __name__ == "__main__":
    files = replaceable_files()
    pairs = build_token_pairs()
    substitute_tokens(files, pairs)

