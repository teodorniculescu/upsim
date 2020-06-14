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
        d: BaseValue
        clk: BaseValue
        r: BaseValue
        q: BaseValue
        [d, clk, r] = self.get_all_pins_with_type(PIN_TYPE_INPUT).values()
        [q, nq] = self.get_all_pins_with_type(PIN_TYPE_OUTPUT).values()
        if r.is_high():
            if clk.is_posedge():
                if d.is_high():
                    q.set_high()
                    nq.set_low()
                elif d.is_low():
                    q.set_low()
                    nq.set_high()
        elif r.is_low():
            q.set_low()
            nq.set_high()

