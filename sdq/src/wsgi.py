from flask import Flask, request, redirect
import json

app = Flask(__name__)

## UTILITY FUNCTIONS ##
class methods:
    get = 'GET'
    post = 'POST'

class resource:
    def __init__(self, path):
        self.path = path

        self.route = f'/{self.path}'

    def reference(self, relation='', method=''):
        return {
            'rel': relation,
            'method': method,
            'href': f'{request.url_root}{self.path}'
        }

    def response(self, data, *links):
        return {
            'data': data, 
            'links': [
                self.reference('self', request.method),
                resources.root.reference('root', methods.get),
                *links
            ]
        }

    def redirect(self):
        return redirect(self.reference()['href'])

class index:
    def __init__(self, path : str, fallback : resource, source):
        self.path = path
        self.fallback = fallback
        self.source = source
        self.len = len(source)

        self.route = f'/{path}/<int:index>'

    def item_path(self, index):
        return f'{self.path}/{index}'

    def reference(self, relation : str, index):
        return {
            'rel': relation,
            'method': 'GET',
            'href': f'{request.url_root}{self.item_path(index)}'
        }

    def response(self, index):
        # Fall back on an index-out-of-bounds
        if index < 0 or index >= self.len:
            return self.fallback.redirect()

        links = []
        if index != 0:
            links.append(resource(self.item_path(index - 1)).reference('prev', methods.get))
        
        if index != self.len - 1:
            links.append(resource(self.item_path(index + 1)).reference('next', methods.get))

        
        return resource(self.item_path(index)).response(
            self.source[index],
            *links
        )

temp_posts = [
    "This is my first post! I am so happy",
    "This is my second post! I'm starting to feel weird",
    "This is my third post- what's happening to me?",
    "This is my fourth po....."
]
class resources:
    root = resource('')
    stats = resource('stats')
    posts = index('posts', root, temp_posts)
    about = resource('about')



temp_stats = []
## ROUTES ##
@app.get(resources.stats.route)
def get_stats():
    data = {
        'message': 'TODO: implement some stats about the server',
        'temp_stats': temp_stats
    }

    return resources.stats.response(data)

@app.post(resources.stats.route)
def post_stats():
    data = {'temp_stats': temp_stats}
    if len(json.dumps(request.json)) > 1e3:
        data['success'] = False
        data['message'] = f'Did not post entry, payload size exceeded'
    else:
        if len(temp_stats) >= 3:
            temp_stats.pop(0)

        temp_stats.append(request.json)

        data['success'] = True
        data['message'] = f'New statistics entry {request.json} posted'

    return resources.stats.response(data)

@app.get(resources.posts.route)
def get_post(index):
    return resources.posts.response(index)

@app.get(resources.about.route)
def get_about():
    data = {
        "name": "nicholas kiran merchant",
        "occupation": "big chef dog",
        "hometown": "ketchum, id"
    }

    return resources.about.response(
        data,
        resources.posts.reference('posts', 0)
    )

@app.get("/")
def get_root_resource():
    data = {
        'message': 'Yo what\'s popping kings and kingesses'
    }

    return resources.root.response(
        data,
        resources.stats.reference('view', methods.get),
        resources.stats.reference('add', methods.post),
        resources.posts.reference('view', 0),
        resources.about.reference('about', methods.get)
    )

if __name__ == '__main__':
    app.run(debug=False)
