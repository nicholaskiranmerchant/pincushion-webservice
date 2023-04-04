from flask import Flask, request, redirect

app = Flask(__name__)

## UTILITY FUNCTIONS ##

class resource:
    def __init__(self, path, method):
        self.path = path
        self.method = method

        self.route = f'/{self.path}'

    def reference(self, relation : str):
        return {
            'rel': relation,
            'method': self.method,
            'href': f'{request.url_root}{self.path}'
        }

    def response(self, data, *links):
        return {
            'data': data, 
            'links': [
                self.reference('self'),
                resources.root.reference('root'),
                *links
            ]
        }

    def redirect(self):
        return redirect(self.reference('')['href'])

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
            links.append(resource(self.item_path(index - 1), 'GET').reference('prev'))
        
        if index != self.len - 1:
            links.append(resource(self.item_path(index + 1), 'GET').reference('next'))

        
        return resource(self.item_path(index), 'GET').response(
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
    root = resource('', 'GET')
    stats = resource('stats', 'GET')
    posts = index('posts', root, temp_posts)



## ROUTES ##
@app.get(resources.stats.route)
def get_stats():
    data = {
        'message': 'TODO: implement some stats about the server'
    }

    return resources.stats.response(data)

@app.get(resources.posts.route)
def get_post(index):
    return resources.posts.response(index)

@app.get("/")
def get_root_resource():
    data = {
        'message': 'Yo what\'s popping kings and kingesses'
    }

    return resources.root.response(
        data,
        resources.stats.reference('stats'),
        resources.posts.reference('posts', 0)
    )

if __name__ == '__main__':
    app.run(debug=False)
