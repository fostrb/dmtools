import readline
import string
import programs
from programs.program import DMProgram


class DMShell(object):
    identchars = string.ascii_letters + string.digits + '_'

    def __init__(self):
        self.name = ''
        self.programs = []
        self.load_programs()

        self.command_loop()

    def load_programs(self):
        for name, cls in programs.__dict__.items():
            if isinstance(cls, type):
                iprog = cls()
                if isinstance(iprog, DMProgram):
                    self.programs.append(iprog)

    def parseline(self, line):
        line = line.strip()
        if not line:
            return None, None, line
        elif line[0] == '?':
            line = 'help ' + line[1:]
        i, n = 0, len(line)
        while i < n and line[i] in self.identchars: i = i+1
        cmd, arg = line[:i], line[i:].strip()
        return cmd, arg, line

    def command_loop(self):
        while True:
            line = input(">")
            cmd, arg, line = self.parseline(line)
            output = ""
            #try:
            found = False
            if cmd is not None:
                for program in self.programs:
                    if cmd.lower() == program.name or cmd.lower() in program.aliases:
                        found = True
                        output = program.run(arg)
                if not found:
                    print("command not found")

            #except:
                #output = "Failure"
            #print(output)





if __name__ == '__main__':
    DMShell()
