from celery import bootsteps
from kombu.utils.limits import TokenBucket


class MyExtTokenBucket(TokenBucket):
    seen_ids = set()

    def add(self, item):
        return super().add(item)

    def can_consume(self, tokens=1):
        return tokens == 'ok'

    def pop(self):
        item, token = super().pop()

        args = eval(item.argsrepr)

        if args[1] % 2 == 0 and args[1] not in self.seen_ids:
            self.seen_ids.add(args[1])
            return item, 'nope'
        else:
            try:
                self.seen_ids.remove(args[1])
            except KeyError:
                pass

            return item, 'ok'

    def expected_time(self, tokens=1):
        return 1.0


class Step(bootsteps.StartStopStep):
    requires = {'celery.worker.consumer.tasks:Tasks'}

    def bucket_for_task(type, Bucket=TokenBucket):
        return super().bucket_for_task(type, Bucket=Bucket)

    def start(self, c):
        self.consumer = c
        c.task_buckets['scm.tasks.bs_test'] = MyExtTokenBucket(1, 1)

        return super().start(c)

    def stop(self, *args, **kwargs):
        return super().stop(*args, **kwargs)
