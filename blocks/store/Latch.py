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

class JK_LATCH(LogicalBlock):

    def __init__(self, block_name: str):
        super().__init__(block_name)
        super().add_pin(BaseValue("J", PIN_TYPE_INPUT))
        super().add_pin(BaseValue("K", PIN_TYPE_INPUT))
        super().add_pin(BaseValue("CLK", PIN_TYPE_INPUT))
        super().add_pin(BaseValue("PR", PIN_TYPE_INPUT))
        super().add_pin(BaseValue("CLR", PIN_TYPE_INPUT))
        super().add_pin(BaseValue("Q", PIN_TYPE_OUTPUT))
        super().add_pin(BaseValue("NQ", PIN_TYPE_OUTPUT))

    def __high_impedance(self, Q, NQ):
        Q.set_high_impedance()
        NQ.set_high_impedance()

    def __inactive_clear_preset(self, J, K, Q, NQ):
        if J.is_low():
            if K.is_low():
                # keep the previous values of the Q and NQ
                pass
            elif K.is_high():
                Q.set_low()
                NQ.set_high()
            else:
                self.__high_impedance(Q, NQ)
        elif J.is_high():
            if K.is_low():
                Q.set_high()
                NQ.set_low()
            elif K.is_high():
                Q.toggle()
                NQ.toggle()
            else:
                self.__high_impedance(Q, NQ)
        else:
            self.__high_impedance(Q, NQ)

    def calculate(self) -> None:
        J = self.get_pin_with_name("J")
        K = self.get_pin_with_name("K")
        CLK = self.get_pin_with_name("CLK")
        # preset and clear are negated
        PR = self.get_pin_with_name("PR")
        CLR = self.get_pin_with_name("CLR")
        # outputs
        Q = self.get_pin_with_name("Q")
        NQ = self.get_pin_with_name("NQ")
        if PR.is_low():
            if CLR.is_low():
                Q.set_high()
                NQ.set_high()
            elif CLR.is_high():
                Q.set_high()
                NQ.set_low()
            else:
                self.__high_impedance(Q, NQ)
        elif PR.is_high():
            if CLR.is_low():
                Q.set_low()
                NQ.set_high()
            elif CLR.is_high():
                if CLK.is_negedge():
                    self.__inactive_clear_preset(J, K, Q, NQ)
            else:
                self.__high_impedance(Q, NQ)
        else:
            self.__high_impedance(Q, NQ)

