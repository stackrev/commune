
import commune as c
from functools import partial


class VirtualClient:
    def __init__(self, module: str ='ReactAgentModule',):
        if isinstance(module, str):
            import commune
            self.module_client = c.connect(module)
            self.success = self.module_client.success
        else:
            self.module_client = module
        self.module_client.name = self.module_name()
    
    def remote_call(self, remote_fn: str, *args, return_future= False, timeout=None, **kwargs):
        if return_future:
            return self.module_client.async_forward(fn=remote_fn, args=args, kwargs=kwargs, timeout=timeout)
        else:
            return self.module_client.forward(fn=remote_fn, args=args, kwargs=kwargs, timeout=timeout)
            
    def __str__(self):
        return f'<VirtualClient(name={self.module_client.name}, address={self.module_client.address})>'

    def __repr__(self):
        return self.__str__()
        
    protected_attributes = [ 'module_client', 'remote_call']
    def __getattr__(self, key):

        if key in self.protected_attributes :
            return getattr(self, key)
        else:
            return lambda *args, **kwargs : partial(self.remote_call, (key))( *args, **kwargs)

