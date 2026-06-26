FileNotFoundError: [Errno 2] No such file or directory: '旅游数据.csv'
Traceback:
File "C:\Users\zjl85\OneDrive\Desktop\24211870238周佳丽\代码\app.py", line 35, in <module>
    df = load_data()
File "C:\Users\zjl85\AppData\Local\Programs\Python\Python314\Lib\site-packages\streamlit\runtime\caching\cache_utils.py", line 281, in __call__
    return self._get_or_create_cached_value(args, kwargs, spinner_message)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\zjl85\AppData\Local\Programs\Python\Python314\Lib\site-packages\streamlit\runtime\caching\cache_utils.py", line 326, in _get_or_create_cached_value
    return self._handle_cache_miss(cache, value_key, func_args, func_kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\zjl85\AppData\Local\Programs\Python\Python314\Lib\site-packages\streamlit\runtime\caching\cache_utils.py", line 385, in _handle_cache_miss
    computed_value = self._info.func(*func_args, **func_kwargs)
File "C:\Users\zjl85\OneDrive\Desktop\24211870238周佳丽\代码\app.py", line 21, in load_data
    df = pd.read_csv("旅游数据.csv", encoding="utf-8-sig")
         ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\zjl85\AppData\Local\Programs\Python\Python314\Lib\site-packages\pandas\io\parsers\readers.py", line 873, in read_csv
    return _read(filepath_or_buffer, kwds)
File "C:\Users\zjl85\AppData\Local\Programs\Python\Python314\Lib\site-packages\pandas\io\parsers\readers.py", line 300, in _read
    parser = TextFileReader(filepath_or_buffer, **kwds)
File "C:\Users\zjl85\AppData\Local\Programs\Python\Python314\Lib\site-packages\pandas\io\parsers\readers.py", line 1645, in __init__
    self._engine = self._make_engine(f, self.engine)
                   ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
File "C:\Users\zjl85\AppData\Local\Programs\Python\Python314\Lib\site-packages\pandas\io\parsers\readers.py", line 1904, in _make_engine
    self.handles = get_handle(
                   ~~~~~~~~~~^
        f,
        ^^
    ...<6 lines>...
        storage_options=self.options.get("storage_options", None),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
File "C:\Users\zjl85\AppData\Local\Programs\Python\Python314\Lib\site-packages\pandas\io\common.py", line 926, in get_handle
    handle = open(
        handle,
    ...<3 lines>...
        newline="",
    )
