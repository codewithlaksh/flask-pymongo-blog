from project import app

@app.template_filter('get_val')
def get_val_filter(dict, key):
    return dict.get(key)
