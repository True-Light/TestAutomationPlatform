from pydantic import BaseModel


class AllureBase(BaseModel):
    id: int


class SearchAllureReport(BaseModel):
    suite: str | None
    job: str | None
    feature: str | None
    version: str | None
    current: int
    pageSize: int


class CreateAllureReport(BaseModel):
    file: list
    suite: str
    job: str
    feature: str
    version: str


class UploadAllureReport(AllureBase):
    suite: str
    job: str
    feature: str
    version: str


class AllureDelete(AllureBase):
    uuid: str


class CreateParams:
    def __init__(self):
        self.zip_path: str | None = None
        self.extract_path: str | None = None
        self.generate_path: str | None = None
        self.uuid: str | None = None
        self.job: str | None = None
        self.suite: str | None = None
        self.feature: str | None = None
        self.version: str | None = None
        self.size: int = 0
