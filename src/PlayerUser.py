
class PlayerUser:

    def __int__(self, type, ID):
        self.ID = ID
        self.type = type

    def get_id(self):
        return self.ID

    def get_type(self):
        return self.type

    def request_move(self):
        self.move_sequence.pop()


    # THis is a stub for testing
    def set_moves(self, moves):
        self.move_sequence = moves


# TODO Add Main Loop Logic