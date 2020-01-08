from module.config import TASKS
from module.scheduler import run_schedule
from module.utils import Store


class Monitor:

    # 启动收集器
    def __init__(self):
        self.name = 'ShopPy'
        self.tasks = []

    def add_task(self,task):
        self.tasks.append(task)
    # initializing, setting up parameter for store to monitor & keywords

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            return True
        else:
            return False

    class Task:
        def __init__(self, store, keyword):
            if store in Store.storeDict.keys():
                self.store = Store(store)
                self.keyword = keyword
            else:
                self.store = None
                self.keyword = None


if __name__ == '__main__':
    monitor = Monitor()
    tasks = []
    for t in TASKS:
        tasks.append(monitor.Task(t.key(), t.value()))
    monitor.add_task(tasks)
    run_schedule(tasks[0])
    #monitor = Monitor(['tdco'])
    #monitor.run()

    # with concurrent.futures.ProcessPoolExecutor as executor:
    #
    #     assert isinstance(executor, concurrent.futures.Executor)
    #     future = executor.submit(run_schedule(tasks[0]))
    #     future.result()