class SqlingsDBException(Exception):
    pass


class SqlingsProjectException(Exception):

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class SqlingsProjectDBExistsException(Exception):

    _template = "A database file for project {project_name} already exists on your system in '$HOME/.sqlings/'"

    def __init__(self, project_name: str):
        self.message: str = eval(f'f"""{self._template}"""')
        super().__init__(self.message)
