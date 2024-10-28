import os
import json
import yaml
from markdownify import markdownify
import urllib.request
from datetime import datetime

# import hashnode

export_path = 'p.json'
media_path = 'media'
posts_path = 'articles/'
config = {
}

export = json.load(open(export_path))
# print(export['posts'])

for post in export['posts']:
    cover_image_basename = f"{post['id']}.png"
    cover_image_path = f"{media_path}/{cover_image_basename}"
    post_path = f"{posts_path}/{post['slug']}.md"

    if not os.path.isfile(cover_image_path) and post['coverImage']:
        urllib.request.urlretrieve(
            post['coverImage'], cover_image_path)

    frontmatter = {
        'author': 'Damasukma Trihanandi',
        'pubDatetime': datetime.strptime(post['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ'),
        'modDatetime': datetime.strptime(post['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ'),
        'draft': False,
        'title': post['title'],
        'slug': post['slug'],
        'tags': post['tags'],
        'description': post['brief'],
    }
    frontmatter_yaml = yaml.dump(frontmatter)

    content = f'''---\n{frontmatter_yaml}---\n\n{post['contentMarkdown']}'''
    

    with open(post_path, 'w') as f:
        f.write(content)

    print("Done convert: " + post['slug'])
