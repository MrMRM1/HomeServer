

def run_as_current_user(self, function, *args, **kwargs):
    """Execute a function impersonating the current logged-in user."""
    self.authorizer.impersonate_user(self.username, self.password)
    args = list(args)
    if self.username == 'anonymous':
        args.append('guest')
    else:
        args.append(self.username)
    args = tuple(args)
    try:
        return function(*args, **kwargs)
    finally:
        self.authorizer.terminate_impersonation(self.username)
