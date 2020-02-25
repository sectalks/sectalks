from java.util.concurrent import Callable, Executors, TimeUnit
from uaeruntime import Interpreter
from com.adamyi.uae.UaeRuntimeWrapper import runTask


class ReqTask(Callable):
    def __init__(self, safe_eval, code):
        self.safe_eval = safe_eval
        self.code = code

    def call(self):
        self.safe_eval(self.code)
        return self.safe_eval.symtable.get('uae_rsp')


# since we don't have flask request context in java thread
def flattenRequest(request):
    return {
        "method": request.method,
        "cookies": request.cookies,
        "args": request.args,
        "form": request.form,
        "json": request.json,
        "host": request.host,
        "host_url": request.host_url,
        "path": request.path,
        "full_path": request.full_path,
        "url": request.url,
        "base_url": request.base_url,
        "url_root": request.url_root,
        "headers": request.headers.to_list(),
        "remote_addr": request.remote_addr,
        "data": request.data
    }


def runCode(env, code, timeout):
    safe_eval = Interpreter(usersyms=env)
    #es = Executors.newSingleThreadExecutor()
    task = ReqTask(safe_eval, code)
    return runTask(task, timeout)
    #fut = es.submit(task)
    #return fut.get(timeout, TimeUnit.SECONDS)
