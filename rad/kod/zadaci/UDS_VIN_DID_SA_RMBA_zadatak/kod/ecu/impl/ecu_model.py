from ecu_template.model.ecu_model import ECUModel


class ECUModelImpl(ECUModel):
    def __init__(self):
        super().__init__()
        with open("./impl/resources/ecu1_program.elf", "rb") as f:
            self.memory = f.read()
            self.memory_len = len(self.memory)
            self.sa_unlocked = False
            self.vin = "3VWFX7AT2DM604494"

    def get_data_from_memory(self, address: int, size: int) -> bytes:
        return self.memory[address:address + size]
