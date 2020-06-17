from blocks.LogicalBlock import LogicalBlock
from values.BaseValue import BaseValue, PIN_TYPE_INPUT, PIN_TYPE_OUTPUT


class D_LATCH(LogicalBlock):

    def __init__(self, block_name: str):
        super().__init__(block_name)
        super().add_pin(BaseValue("D", PIN_TYPE_INPUT))
        super().add_pin(BaseValue("C", PIN_TYPE_INPUT))
        super().add_pin(BaseValue("R", PIN_TYPE_INPUT))
        super().add_pin(BaseValue("Q", PIN_TYPE_OUTPUT))
        super().add_pin(BaseValue("NQ", PIN_TYPE_OUTPUT))

    def calculate(self) -> None:
        # the data pin provides the data that will be saved in the latch
        d: BaseValue
        # clock signal
        clk: BaseValue
        # reset signal - when kept high clears the data - when kept low
        # provides the data stored inside
        reset: BaseValue
        q: BaseValue
        [d, clk, reset] = self.get_all_pins_with_type(PIN_TYPE_INPUT).values()
        [q, nq] = self.get_all_pins_with_type(PIN_TYPE_OUTPUT).values()
        if reset.is_low():
            if clk.is_posedge():
                if d.is_high():
                    q.set_high()
                    nq.set_low()
                elif d.is_low():
                    q.set_low()
                    nq.set_high()
        elif reset.is_high():
            q.set_low()
            nq.set_high()

