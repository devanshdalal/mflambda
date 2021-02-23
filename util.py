from concurrent.futures import ThreadPoolExecutor

def Pool(function, params, use_threads=True, max_workers=5):
    if use_threads:
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            dfs = ex.map(function, *zip(*params))
    else:
        dfs = []
        for param in params:
            try:
                r = function(*param)
            except:
                raise 
            dfs.append(r)
    return dfs
