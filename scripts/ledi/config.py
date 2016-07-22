import vim


class config(object):
    INFLATES = {
        'completion#menu_max_length': int,
    }

    def __init__(self):
        self.cache = {}

    def __get__(self, name, default):
        if name in self.cache:
            return self.cache[name]
        self.cache[name] = self.inflate(name, vim.eval('g:ledi#%s' % name))
        return self.cache[name]

    def inflate(self, name, value):
        if name in self.INFLATES:
            return self.INFLATES[name](value)
        else:
            return value

# Hide config class
config = config()

