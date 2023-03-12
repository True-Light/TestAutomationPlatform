import os
import sys

from typing import Any, Dict, Optional

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, validator


class Settings(BaseSettings):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_FILES_DIR = os.path.join(BASE_DIR, "upload-files")
    if not os.path.exists(UPLOAD_FILES_DIR):
        os.makedirs(UPLOAD_FILES_DIR)
    ALLURE_RESULTS_DIR = os.path.join(BASE_DIR, "allure-results")
    if not os.path.exists(ALLURE_RESULTS_DIR):
        os.makedirs(ALLURE_RESULTS_DIR)
    ALLURE_REPORTS_DIR = os.path.join(BASE_DIR, "allure-reports")
    if not os.path.exists(ALLURE_REPORTS_DIR):
        os.makedirs(ALLURE_REPORTS_DIR)
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    PLUGINS_DIR = os.path.join(BASE_DIR, 'plugins')
    LOG_LEVEL: str = "INFO"
    LOGURU_LEVEL: str = "INFO"
    PRIVATE_KEY_FILE = os.path.join(BASE_DIR, "automation_private_key.pem")
    API_V1_STR: str = "/api/v1"
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    AES_TYPE: str = "pkcs7"
    # 60 minutes * 24 hours * 7 days = 7 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    SERVER_NAME: str = "TestAutomation"
    SERVER_HOST: AnyHttpUrl = "http://0.0.0.0:8888"
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    # BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["*"]

    # @validator("BACKEND_CORS_ORIGINS", pre=True)
    # def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
    #     if isinstance(v, str) and not v.startswith("["):
    #         return [i.strip() for i in v.split(",")]
    #     elif isinstance(v, (list, str)):
    #         return v
    #     raise ValueError(v)

    PROJECT_NAME: str = "TestAutomation"
    SENTRY_DSN: Optional[HttpUrl] = None

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if len(v) == 0:
            return None
        return v

    ALLURE_REPORT_SERVER: str
    UPLOAD_ZIP_SERVER: str

    REDIS_SERVER: str
    REDIS_PORT: str
    REDIS_PASSWORD: str

    MYSQL_SERVER: str
    MYSQL_ROOT: str = 'root'
    MYSQL_USER: str
    MYSQL_ROOT_PASSWORD: str
    MYSQL_PORT: str
    MYSQL_DB: str
    MYSQL_DATABASE_URI: str

    REDIS_URI: str
    RABBITMQ_URI: str

    # POSTGRES_SERVER: str
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: str
    # POSTGRES_DB: str
    # POSTGRES_DATABASE_URI: Optional[AnyUrl] = None
    #
    # @validator("POSTGRES_DATABASE_URI", pre=True)
    # def assemble_postgres_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
    #     if isinstance(v, str):
    #         return v
    #     return AnyUrl.build(
    #         scheme="postgresql",
    #         user=values.get("POSTGRES_USER"),
    #         password=values.get("POSTGRES_PASSWORD"),
    #         host=values.get("POSTGRES_SERVER"),
    #         path=f"/{values.get('POSTGRES_DB') or ''}",
    #     )

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/server/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: str = "admin"
    FIRST_SUPERUSER_PASSWORD: str = "123456"
    FIRST_SUPERUSER_EMAIL: EmailStr = "test@example.com"  # type:
    FIRST_SUPERUSER_FULL_NAME: str = "管理员"
    FIRST_SUPERUSER_ROLE_CODE: str = "super"
    FIRST_SUPERUSER_ROLE_NAME: str = "超级管理员"
    USERS_OPEN_REGISTRATION: bool = False

    ALLURE_REPORT_LIFECYCLE = 31  # days

    class Config:
        if sys.platform.startswith("win"):
            env_file = r"D:\workspace\TestAutomationVM\.env"
        case_sensitive = True


settings = Settings()
