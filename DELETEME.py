import os


ROOT_DIR='.'
INCLUDE_DIRS=['.github']


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


if __name__ == "__main__":
    files = replaceable_files()
    for file in files:
        print(file)
