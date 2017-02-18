import os
import json
from pprint import pprint


def clean_file(file_path):
    data = ''
    file = open(file_path, 'r')
    line = file.readline()
    while line:
        if not line.startswith('# '):
            data += line
        line = file.readline()

    return data


def browse_structure(categories_scene, parent_id, elements, scene_name):
    child_id = None
    for element in elements:
        if type(element) == list:
            browse_structure(categories_scene, child_id, element, scene_name)
        else:
            child_id = element
            for entry in categories_scene['entries']:
                if parent_id is None and entry['id'] == child_id:
                    entry['metadata'].update({'initial': 1})
                elif entry['id'] == parent_id:
                    entry['children'].append(child_id)


dir_path = ''

"""Get file"""
project_path = dir_path + 'project.ttp'
characters_path = dir_path + 'characters.ttp'
categories_path = dir_path + 'categories'

languages = []
project_data = json.loads(clean_file(project_path))
languages = project_data['languages']

characters = []
characters_data = json.loads(clean_file(characters_path))
characters = characters_data['characters']

categories_files = [categories_path + '/' + f for f in os.listdir(categories_path) if os.path.isfile('{0}/{1}'.format(categories_path, f))]

"""Get categories locales files"""
categories_scene = {}
for categories_file in categories_files:
    categories_data = json.loads(clean_file(categories_file))
    scene_name = os.path.splitext(os.path.basename(categories_file))[0]
    categories_scene.update({
            'entries': categories_data['entries'],
            'structure': categories_data['structure'],
        })

    for entry in categories_scene['entries']:
        entry.update({'children': []})

    browse_structure(categories_scene, None, categories_scene['structure'], scene_name)

    del(categories_scene['structure'])

    with open('output/'+scene_name+'.json', 'w') as file:
        json.dump(categories_scene, file)


    """Locales files"""
    for language in languages:
        categories_local_path = '{0}/{1}/{2}'.format(categories_path, language, os.path.basename(categories_file))
        categories_local_data = json.loads(clean_file(categories_local_path))
        categories_local_data = categories_local_data['entries']
        with open('output/'+scene_name+'_'+language+'.json', 'w') as file:
            json.dump(categories_local_data, file)


# print(languages)
# print(characters)
# print(categories_files)
# print(categories_scene)


"""Import data"""

"""Organise data"""

"""Save new file"""
