from blocks.BasicBlock import *
from values.BaseValue import BaseValue


class StateBlock(BasicBlock):
    def __init__(self, name: str, pin_type: int, pin_name: str = "val"):
        super().__init__(name)
        super().add_pin(BaseValue(pin_name, pin_type))

    def get_gui_grid(self) -> ParamGrid:
        result: ParamGrid = ParamGrid([])
        num_cols = 5
        row: ParamGridRow = ParamGridRow([])
        for col_index in range(num_cols):
            row.append(ParamGridElem(("", ParamElem({}))))
        result.append(row)
        result[0][1] = (CODE.BORDER_UP_DOWN_LEFT, {})
        result[0][2] = (CODE.BORDER_UP_DOWN, {"name": self.get_name()})
        result[0][3] = (CODE.BORDER_UP_DOWN_RIGHT, {})
        pin: BaseValue
        [pin] = self.get_all_pins().values()
        if pin.get_pin_type() == PIN_TYPE_INPUT:
            column_index = 0
            column_type = CODE.WIRE_RIGHT
        else:
            column_index = 4
            column_type = CODE.WIRE_LEFT
        result[0][column_index] = (column_type, {"name": pin.get_name()})
        pin.set_original_position(
            original_position=
            (0+ self._position[0],
             column_index+ self._position[1]
         ))
        return result


class GroundBlock(StateBlock):
    def __init__(self, name: str,
                 pin_name: str = "val"):
        pin_type: int = PIN_TYPE_OUTPUT
        super().__init__(name=name, pin_type=pin_type, pin_name=pin_name)

