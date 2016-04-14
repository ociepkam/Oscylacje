class Instruction:
    def __init__(self, file_path, instruction_type, time):
        self.file_path = file_path
        self.instruction_type = instruction_type
        self.time = time
        self.type = "instruction"

    def prepare_concrete(self):
        instruction_info = {
            "TYPE": self.type,
            "TIME": self.time,
            "INSTRUCTION_TYPE": self.instruction_type,
            "PATH": self.file_path
        }
        return instruction_info