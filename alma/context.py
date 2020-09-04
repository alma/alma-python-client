class Context:
    def __init__(self, options):
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

    @property
    def credentials(self):
        return self.options["credentials"]

    def url_for(self, path):
        root = self.api_root[self.mode].rstrip("/")

        return f"{root}/{path.lstrip('/')}"

    def add_user_agent_component(self, component, version):
        self.user_agent_components.append(f"{component}/{version}")

    def user_agent_string(self):
        return "; ".join(self.user_agent_components[::-1])
