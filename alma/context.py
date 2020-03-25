class Context:
    def __init__(self, api_key, options):
        self.api_key = api_key
        self.options = options

        self.user_agent_components = []

    @property
    def logger(self):
        return self.options["logger"]

    @property
    def api_root(self):
        return self.options["api_root"]

    @property
    def mode(self):
        return self.options["mode"]

    def url_for(self, path):
        root = self.api_root[self.mode].rstrip("/")

        return "{root}/{path}".format(root=root, path=path.lstrip("/"))

    def add_user_agent_component(self, component, version):
        self.user_agent_components.append(
            "{component}/{version}".format(component=component, version=version)
        )

    def user_agent_string(self):
        return "; ".join(self.user_agent_components[::-1])
