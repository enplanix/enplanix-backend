from django.db import connection
import time
import functools

def observe_queries(view_func):
    @functools.wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        connection.queries_log.clear()
        start_queries = len(connection.queries)
        start_time = time.time()

        response = view_func(request, *args, **kwargs)

        total_time = time.time() - start_time
        queries_count = len(connection.queries) - start_queries

        print(f'[{view_func.__name__}] Tempo: {total_time:.3f}s - Queries: {queries_count}')
        for q in connection.queries:
            print(f"SQL ({q['time']}s): {q['sql']}")

        return response
    return _wrapped_view


def is_float(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False