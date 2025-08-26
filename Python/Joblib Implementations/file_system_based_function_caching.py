import os
import pickle
import hashlib
from functools import wraps
import time
import shutil

class FileCache:
    def __init__(self, cache_location):
        self.location = os.path.abspath(cache_location)
        if not os.path.exists(self.location):
            os.makedirs(self.location)

    def _generate_key(self, func, args, kwargs):
        arg_representation = str(args) + str(sorted(kwargs.items()))
        unique_string = f"{func.__module__}.{func.__name__}:{arg_representation}"
        
        hashed_key = hashlib.sha256(unique_string.encode('utf-8')).hexdigest()
        return os.path.join(self.location, hashed_key)

    def memoize(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_filepath = self._generate_key(func, args, kwargs)

            if os.path.exists(cache_filepath):
                with open(cache_filepath, 'rb') as file_handle:
                    return pickle.load(file_handle)
            
            computed_result = func(*args, **kwargs)
            with open(cache_filepath, 'wb') as file_handle:
                pickle.dump(computed_result, file_handle)
            
            return computed_result
        return wrapper

if __name__ == '__main__':
    cache_directory = "./my_app_cache"
    memory = FileCache(cache_location=cache_directory)

    @memory.memoize
    def fetch_data(source_url):
        print(f"Executing slow function for: {source_url}")
        time.sleep(2)
        return {"data": f"content from {source_url}"}

    print("First call for url1...")
    start1 = time.time()
    print(fetch_data(source_url="api.example.com/data1"))
    print(f"Took {time.time() - start1:.2f}s")
    
    print("\nSecond call for url1 (should be fast)...")
    start2 = time.time()
    print(fetch_data(source_url="api.example.com/data1"))
    print(f"Took {time.time() - start2:.2f}s")

    print("\nFirst call for url2...")
    start3 = time.time()
    print(fetch_data(source_url="api.example.com/data2"))
    print(f"Took {time.time() - start3:.2f}s")

    shutil.rmtree(cache_directory)
    print(f"\nCleaned up cache directory: {cache_directory}")