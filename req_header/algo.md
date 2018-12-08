```python
    if 'cdn' or 'asset' in url:
        prediction = cacheable
    else if requests url extension is in ['jpeg', 'jpg', 'css', 'png']:
        prediction = cacheable
    else if chrome defined url_type is 'Font':
        prediction = cacheable
    
    if prediction not decided:
        if request method is not 'GET':
            prediction = uncacheable
        else if requests url extension is in ['.gif', '.php', '.aspx', 'ashx', No_Extension]:
            prediction = uncacheable
        else if chrome defined url_type is in ['XHR', 'Document']:
            prediction = uncacheable
        else if request.headers has 'cookies', 'content-type', 'content-length':
            prediction = uncacheable
    
    if prediction not decided:
        prediction = cacheable
    
```

