import os
from pathlib import Path
from dotenv import load_dotenv

# 加载.env配置文件
env_path = Path(__file__).parent / 'config.env'
load_dotenv(env_path)

# 获取项目根目录
PROJECT_ROOT = os.getenv('PROJECT_ROOT', str(Path(__file__).parent))

class Config:
    """Centralized configuration sourced from config.env."""

    # API access (Qwen / OpenAI-compatible)
    API_BASE_URL = os.getenv("API_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

    # OpenAI / LangChain legacy fields kept for compatibility
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

    # Database configuration
    DATABASE_URL = os.getenv("DATABASE_URL")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER = os.getenv("MYSQL_USER", "braven")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "innerecho_chat")

    # Vector store configuration (absolute path under project root)
    CHROMA_PERSIST_DIRECTORY = os.getenv(
        "CHROMA_PERSIST_DIRECTORY", os.path.join(PROJECT_ROOT, "chroma_db")
    )

    # Model defaults
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen-plus")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))

    # Server configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"