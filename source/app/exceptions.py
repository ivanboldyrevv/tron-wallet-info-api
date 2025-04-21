class NotFoundException(Exception):
    def __init__(self, page_num: int, per_page: int) -> None:
        self.msg = f"No records on page: {page_num} with per_page: {per_page}"
        super().__init__(self.msg)
