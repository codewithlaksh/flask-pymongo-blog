# Flask Pymongo Blog

A simple blog app using flask and mongo db

## !!! Attention !!!
- Please add your api key to this snippet inside ```templates/add.html```
```js 
<script src="https://cdn.tiny.cloud/1/no_api_key/tinymce/6/tinymce.min.js" referrerpolicy="origin"></script>
```

- Add the following to a ```.env``` file
**Change mongo uri in production**
```python
ADMIN_USERNAME=""
ADMIN_PASSWORD=""
APP_SECRET=""
MONGO_URI="mongodb://localhost:27017/flask-blog-app"
```
