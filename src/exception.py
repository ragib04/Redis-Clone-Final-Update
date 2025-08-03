class NoStringValueError(Exception):
    def _init_(self, msg):
        self.msg = msg

    def _repr_(self):
        return self.msg


class SyntaxError(Exception):
    def _init_(self, msg):
        self.msg = msg

    def _repr_(self):
        return self.msg


class InvalidRequest(Exception):
    def _init_(self, msg):
        self.msg = msg

    def _repr_(self):
        return self.msg


class InvalidDataType(Exception):
    def _init_(self, msg):
        self.msg = msg

    def _repr_(self):
        return self.msg


class InvalidFormat(Exception):
    def _init_(self, msg):
        self.msg = msg

    def _repr_(self):
        return self.msg