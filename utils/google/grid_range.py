from utils.other import Container


class GridRange(Container):
    sheetId: int = None
    startRowIndex: int = None
    endRowIndex: int = None
    startColumnIndex: int = None
    endColumnIndex: int = None

    @staticmethod
    def to_grid_range_json(sheet_id: int, cells_range: str):
        start_cell, end_cell = cells_range.split(":")[0:2]
        cells_range = {}
        range_az = range(ord('A'), ord('Z') + 1)
        if ord(start_cell[0]) in range_az:
            cells_range["startColumnIndex"] = ord(start_cell[0]) - ord('A')
            start_cell = start_cell[1:]
        if ord(end_cell[0]) in range_az:
            cells_range["endColumnIndex"] = ord(end_cell[0]) - ord('A') + 1
            end_cell = end_cell[1:]
        if len(start_cell) > 0:
            cells_range["startRowIndex"] = int(start_cell) - 1
        if len(end_cell) > 0:
            cells_range["endRowIndex"] = int(end_cell)
        cells_range["sheetId"] = sheet_id
        return cells_range
