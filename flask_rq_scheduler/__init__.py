from flask.ext.rq import get_connection, get_queue
from rq_scheduler import Scheduler


def get_scheduler(queue='default'):
    return Scheduler(get_queue(queue), connection=get_connection(queue))


def scheduled_job(func_or_queue=None):
    if callable(func_or_queue):
        func = func_or_queue
        queue = 'default'
    else:
        func = None
        queue = func_or_queue

    def wrapper(fn):
        def delay_at(scheduled_time, *args, **kwargs):
            s = get_scheduler(queue)
            return s.enqueue_at(scheduled_time, fn, *args, **kwargs)

        def delay_in(time_delta, *args, **kwargs):
            s = get_scheduler(queue)
            return s.enqueue_in(time_delta, fn, *args, **kwargs)

        def schedule(scheduled_time, args=None, kwargs=None, interval=None, repeat=None):
            s = get_scheduler(queue)
            return s.schedule(scheduled_time, fn, args, kwargs, interval, repeat)

        fn.delay_at = delay_at
        fn.delay_in = delay_in
        fn.schedule = schedule
        return fn

    if func is not None:
        return wrapper(func)

    return wrapper


class RQScheduler(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        pass
