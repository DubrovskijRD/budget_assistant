class Amount(float):
    def __init__(self, value):
        super(Amount, self).__init__()
        self.validate(value)

    def validate(self, value: float):
        if value < 0:
            raise ValueError(f'Invalid amount value: {value}')