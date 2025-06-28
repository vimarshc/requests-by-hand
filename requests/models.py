







class RequestEncodingMixin:
    @property
    def path_url(self):
        """
        Build the path URL to use.
        """

        url = []
        p = urlsplit(self.url)

        path = p.path
        if not path:
            path = "/"
        
        url.append(path)

        query = p.query
        if query:
            url.append("?")
            url.append(query)

        return "".join(url)
    
    @staticmethod
    def _encode_params(data):
        """
        Encode parameters in a peice of data 

        Will sucessfully encode parameters when passed as a dict or a list of 
        2-tuples. Order is retained if data is a list of 2 tuples but arbitrary
        if parameters are are supplied as a dict. 
        """


        if isinstance(data,(str,bytes)):
            return data 
        elif hasattr(data, "read"):
            return data 
        elif hasattr(data, "__iter__"):
            result = []
            for k,vs in to_key_val_list(data):
                if isinstance(vs,basestring) or not hasattr(vs, "__iter__"):
                    vs = [vs]
                for v in vs:
                    if v is not None:
                        result.append(
                            (
                                k.encode("utf-8") if isinstance(k, str) else k,
                                v.encode("utf-8") if isinstance(v, str) else v,
                            )
                        )
        else:
            return data


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
        

class Request(RequestHooksMixin):
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


class PreparedRequest(RequestEncodingMixin,RequestHooksMixin):


    def __init__(self):
        self.method = None
        self.url = None
        self.headers=None
        self._cookies = None
        self.body = None
        self.hooks = default_hooks()
        self._body_position=None

    def prepare(
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
        json=None,
    ):
        """Prepares the entire request with the given parameters."""

        self.prepare_method(method)
        self.prepare_url(url)
        self.prepare_headers(headers)
        self.prepare_cookies(cookies)
        self.prepare_body(body)
        self.prepare_auth(auth,url)


        # Note that prepare_auth must be the last to enable authentication schemes
        # such as OAuth to work on a fully prepare request 

        # This must go after prepare_auth. Authenticators could add a hook. 
        self.prepare_hooks(hooks)
    
    def __repr__(self):
        return f"FunYayRooooRoo[{self.method}]"

    
    def prepare_method(self,method):
        self.method = method
        if self.method is not None:
            # TODO: Add support for Native String.
            # self.method = to_native_string(self.method.upper())
            self.method = self.method.upper()
    
    def prepare_url(self):
        pass
    

    def prepare_headers(self):
        pass
    
    def prepare_body(self):
        pass
    
    def prepare_content_length(self):
        pass
    
    def prepare_auth(self):
        pass
    
    def prepare_cookies(self):
        pass
    

    def prepare_hooks(self):
        pass
    
    




