import commands

def run(cmd):
    return commands.getstatusoutput(cmd)


class InfiniteLoopError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Inifinte Loop in ' + repr(self.value)
