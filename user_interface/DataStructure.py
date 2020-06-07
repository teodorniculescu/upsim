from typing import List, Dict, NewType, Tuple

ParamElem = NewType("ParamElem", Dict[str, str])
ParamGridElem = NewType('ParamGridElem', Tuple[str, ParamElem])
ParamGridRow = NewType('ParamGridRow', List[ParamGridElem])
ParamGrid = NewType('ParamGrid', List[ParamGridRow])
