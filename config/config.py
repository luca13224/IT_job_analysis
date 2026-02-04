"""
Configuration file for Job Market Crawler project
"""
import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data_raw"
CLEAN_DATA_DIR = BASE_DIR / "data_clean"
MODELS_DIR = BASE_DIR / "models"
OUTPUTS_DIR = BASE_DIR / "outputs"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if not exist
for dir_path in [DATA_DIR, CLEAN_DATA_DIR, MODELS_DIR, OUTPUTS_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Crawler settings
CRAWLER_CONFIG = {
    "itviec": {
        "base_url": "https://itviec.com/it-jobs",
        "login_url": "https://itviec.com/sign_in",
        "max_pages": 50,
        "delay_range": (1, 3),
    },
    "topcv": {
        "base_url": "https://www.topcv.vn/tim-viec-lam-it",
        "max_pages": 30,
    },
    "vietnamworks": {
        "base_url": "https://www.vietnamworks.com/it-software-jobs",
        "max_pages": 30,
    }
}

# Data file paths
CSV_PATH = DATA_DIR / "ITViec_data.csv"
CLEAN_CSV_PATH = CLEAN_DATA_DIR / "clean_data.csv"
CURRENT_PAGE_FILE = BASE_DIR / "current_page.txt"
ERROR_LOG_FILE = BASE_DIR / "error_log.txt"

# NLP settings
STOP_WORDS_VI = ["và", "của", "có", "được", "cho", "với", "trong", "tại", "về"]
SKILL_CATEGORIES = {
    "programming_languages": ["python", "java", "javascript", "c++", "c#", "go", "rust", "kotlin", "swift"],
    "frameworks": ["react", "vue", "angular", "django", "flask", "spring", "laravel", "express"],
    "tools": ["git", "docker", "kubernetes", "jenkins", "aws", "azure", "gcp"],
    "databases": ["mysql", "postgresql", "mongodb", "redis", "elasticsearch"],
}

# ML Model settings
ML_CONFIG = {
    "salary_prediction": {
        "models": ["random_forest", "xgboost", "lightgbm"],
        "test_size": 0.2,
        "cv_folds": 5,
    },
    "job_clustering": {
        "n_clusters": 8,
        "algorithms": ["kmeans", "dbscan", "hierarchical"],
    }
}

# Visualization settings
VIZ_CONFIG = {
    "default_style": "seaborn",
    "color_palette": "Set2",
    "figure_size": (12, 8),
    "dpi": 300,
}

# Salary ranges (VND per month)
SALARY_RANGES = {
    "junior": (5_000_000, 15_000_000),
    "mid": (15_000_000, 30_000_000),
    "senior": (30_000_000, 60_000_000),
    "lead": (60_000_000, 100_000_000),
}

# Job level mapping
JOB_LEVELS = ["fresher", "junior", "mid", "senior", "lead", "manager", "director"]

# City mapping
CITIES = ["Ha Noi", "Ho Chi Minh", "Da Nang", "Can Tho", "Hai Phong"]
