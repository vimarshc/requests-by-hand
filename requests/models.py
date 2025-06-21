







class RequestEncodingMixin:
    pass



class RequestHooksMixin:
    def register_hook(self,event,hook):
        """Properly register a hook"""

        if event not in self.hooks:
            raise ValueError(f'Unsupported event specified, with even name "{event}"')
        
        if isinstance(hook, Callable):
            self.hooks[event].append(hook)
        elif hasattr(hook,"__iter__"):
            self.hooks[event].extend(h for h in hook if isinstance(h,Callable))
        


        def deregister_hook(self,event,hook):
            """Deregister a previously registered hook. 
            Returns True if hook existed, False if not. 
            """

            try:
                self.hooks[event].remove(hook)
                return True
            except ValueError:
                return False 
        

class Request:
    """

    A user-created :class: `Request <Requests> object. 

    Used to prepare a :class: `PreparedRequest <PreparedRequest>`, which is sent to the server. 

    :param method: HTTP method to use
    :param url: URL to send. 
    :param headers: dictionary of headers to send
    :param files: dictionary of {filename: fileobject} files to multipart upload. 
    :param data: the body to attach to the request. If a dictionary or a
        list of tuples ``[(key, value)]`` is provided, form-encoding will
        take place. 
    :param json: json for the body to attach to the request (if files or data is not specificied)
    :param params: URL parameters to append to URL. if a dictionary or 
        list of tuples is provided ``[(key, value)]`` is provided, form-encoding will take place. 
    :param auth: Auth handler or (user,pass) tuple. 
    :param cookies: dictionary or CookieJar of cookies to attach to this request
    :param hooks: dictionary of callback hooks, for internal usage.
    """

    def __init__(
        self,
        method=None,
        url=None,
        headers=None,
        files=None,
        data=None,
        params=None,
        auth=None,
        cookies=None,
        hooks=None,
        json=None
        )

        # Default empty dicts for dict params
        data = [] if data is None else data
        files = [] if files is None else files
        headers = [] if headers is None else headers
        params = [] if params is None else params
        hooks = [] if params is None else hooks

        self.hooks = default_hooks()
        for k,v in list(hooks.items()):
            self.register_hook(event=k,hook=v)
        

        self.method = method
        self.url = url
        self.headers = headers
        self.files = files
        self.data = data
        self.json = json
        self.params = params
        self.auth = auth
        self.cookies = cookies
    
    def __repr__(self):
        return f"<Request [{self.method}]>"
    
    def prepare(self):
        """
        Constructs a :class: PreparedRequest <PreparedRequest> for transmission and returns it
        """

        p = PrepareRequest()
        p.prepare(
            method=self.method,
            url=self.url,
            headers=self.headers,
            files=self.files,
            data=self.data,

        )



