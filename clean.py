import sys
import shutil
import os
from pathlib import Path

CATEGORIES = {
    'archives': ['.rar', '.zip'],
    'audio': ['.mp3', '.wav'],
    'documents': ['.docx', '.pptx'],
    'video': ['.avi', '.mp4'],
    'images': ['.jpeg', '.png']
}


def move_file(path: Path, root_dir: Path, cat: str) -> None:
    target_dir = root_dir.joinpath(cat)
    if not target_dir.exists():
        target_dir.mkdir()
    new_name = target_dir.joinpath(f"{(path.stem)}{path.suffix}")
    path.replace(new_name)


def get_categories(path: Path) -> str:
    ext = path.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return 'Other'


def sort_folder(path: Path) -> None:
    ignore_path = []

    for i in CATEGORIES:
        path_to_ignore = path.joinpath(i)
        ignore_path.append(path_to_ignore)

    for item in path.glob('**/*'):
        need_to_ignore = False
        if item.is_file():
            cat = get_categories(item)
            for check in ignore_path:
                if check not in list(item.parents):
                    continue
                else:
                    need_to_ignore = True
                    break
            if need_to_ignore is False:
                move_file(item, path, cat)
    for item in path.glob('**/*'):
        if item.is_dir():
            new_path = item.parent.joinpath((item.name))
            item.replace(new_path)


def unpack_archive(path: Path):
    for item in path.glob('**/*'):
        if item.is_file():
            cat = get_categories(item)
            if cat == 'archives':
                new_path = path.joinpath(cat).joinpath(item.stem)
                shutil.unpack_archive(item, new_path)


def removeEmptyFolders(path: Path, removeRoot=True):
    if not os.path.isdir(path):
        return

    # remove empty subfolders
    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                removeEmptyFolders(fullpath)

    # if folder empty, delete it
    files = os.listdir(path)
    if len(files) == 0 and removeRoot:
        print("Removing empty folder:", path)
        os.rmdir(path)


def get_results(path: Path):
    know_suffix = []
    unknown_suffix = []
    for item in path.glob('*'):
        print(item.name)
        for inner in item.glob('**/*'):
            if inner.is_file():
                get_suf = inner.suffix.lower()
                print(inner.name)
                if get_suf not in know_suffix:
                    for cat, exts in CATEGORIES.items():
                        if get_suf in exts:
                            know_suffix.append(get_suf)
                    if get_suf not in unknown_suffix and get_suf not in know_suffix:
                        unknown_suffix.append(get_suf)

    print(f'Known suffix: {know_suffix}')
    print(f'Unknown suffix: {unknown_suffix}')


def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return 'No path to folder'

    if not path.exists():
        return f'Folder with path {path} doesn"t exist'
    sort_folder(path)
    removeEmptyFolders(path, removeRoot=True)
    unpack_archive(path)
    get_results(path)
    return 'All ok'


if __name__ == "__main__":
    removeRoot = True
    print(main())
