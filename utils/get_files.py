import os
import magic
mime = magic.Magic(mime=True)


def get_files(root_path):
    tree = {}
    for path, a, files, in os.walk(root_path):
        temp = path
        path = path.split('/')[4:]
        path.insert(0, 'root')
        curr = tree
        for elem in path[:-1]:
            curr = curr[elem]
        curr[path[-1]] = {}
        curr = curr[path[-1]]
        for item in files:
            curr[item] = mime.from_file(os.path.join(temp, item))
    return tree
