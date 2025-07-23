import os
import sys
import logging

logger = logging.getLogger(__name__)

# Configuration
class Config:
    def __init__(self):
        self.openai_api_key = self._get_env_value("OPENAI_API_KEY")
        if not self.openai_api_key:
            print("Warning: OPENAI_API_KEY not set. Client API key will be required.")
        
        # Add Anthropic API key for client validation
        self.anthropic_api_key = self._get_env_value("ANTHROPIC_API_KEY")
        if not self.anthropic_api_key:
            print("Warning: ANTHROPIC_API_KEY not set. Client API key validation will be disabled.")
        
        self.openai_base_url = self._get_env_value("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.azure_api_version = self._get_env_value("AZURE_API_VERSION")  # For Azure OpenAI
        self.host = self._get_env_value("HOST", "0.0.0.0")
        
        # 安全地转换整数值，处理空字符串的情况
        port_str = self._get_env_value("PORT")
        self.port = self._safe_int_convert(port_str, 8082)
        
        self.log_level = self._get_env_value("LOG_LEVEL", "INFO")
        
        # Token limits - if not set, no limits will be applied
        if "MAX_TOKENS_LIMIT" in os.environ and os.environ["MAX_TOKENS_LIMIT"].strip():
            max_tokens_str = os.environ["MAX_TOKENS_LIMIT"]
            self.max_tokens_limit = self._safe_int_convert(max_tokens_str, None)
        else:
            self.max_tokens_limit = None  # No limit
            
        if "MIN_TOKENS_LIMIT" in os.environ and os.environ["MIN_TOKENS_LIMIT"].strip():
            min_tokens_str = os.environ["MIN_TOKENS_LIMIT"]
            self.min_tokens_limit = self._safe_int_convert(min_tokens_str, None)
        else:
            self.min_tokens_limit = None  # No limit
        
        # Connection settings
        timeout_str = self._get_env_value("REQUEST_TIMEOUT")
        self.request_timeout = self._safe_int_convert(timeout_str, 300)
        
        retries_str = self._get_env_value("MAX_RETRIES")
        self.max_retries = self._safe_int_convert(retries_str, 1)
        
        # 模型设置 - 如果未设置环境变量或为空，则设为None表示直接透传客户端模型
        self.big_model = self._get_env_value("BIG_MODEL")
        self.middle_model = self._get_env_value("MIDDLE_MODEL", self.big_model)
        self.small_model = self._get_env_value("SMALL_MODEL")
    
    def _get_env_value(self, env_name, default_value=None):
        """获取环境变量值，空字符串视为未设置"""
        value = os.environ.get(env_name, default_value)
        if value is not None and isinstance(value, str) and value.strip() == "":
            return default_value
        return value
    
    def _safe_int_convert(self, value_str, default_value):
        """安全地将字符串转换为整数，出错时返回默认值"""
        if value_str is None or value_str.strip() == "":
            return default_value
        try:
            return int(value_str)
        except ValueError:
            logger.warning(f"Cannot convert '{value_str}' to integer, using default: {default_value}")
            return default_value
        
    def validate_api_key(self):
        """Basic API key validation"""
        if not self.openai_api_key:
            return False
        # Basic format check for OpenAI API keys
        if not self.openai_api_key.startswith('sk-'):
            return False
        return True
        
    def validate_client_api_key(self, client_api_key):
        """Validate client's Anthropic API key"""
        # If no ANTHROPIC_API_KEY is set in the environment, skip validation
        if not self.anthropic_api_key:
            return True
            
        # Check if the client's API key matches the expected value
        return client_api_key == self.anthropic_api_key

try:
    config = Config()
    if config.openai_api_key:
        print(f" Configuration loaded: API_KEY={'*' * 20}..., BASE_URL='{config.openai_base_url}'")
    else:
        print(f" Configuration loaded without OpenAI API key. BASE_URL='{config.openai_base_url}'")
    
    # 显示token限制配置信息
    if config.max_tokens_limit is None:
        print(f" Max Tokens: No limit")
    else:
        print(f" Max Tokens: {config.max_tokens_limit}")
        
    if config.min_tokens_limit is None:
        print(f" Min Tokens: No limit")
    else:
        print(f" Min Tokens: {config.min_tokens_limit}")
    
    # 显示模型配置信息
    print(f" Big Model (opus): {config.big_model if config.big_model else 'Passthrough client model'}")
    print(f" Middle Model (sonnet): {config.middle_model if config.middle_model else 'Passthrough client model'}")
    print(f" Small Model (haiku): {config.small_model if config.small_model else 'Passthrough client model'}")
        
except Exception as e:
    print(f"=4 Configuration Error: {e}")
    sys.exit(1)
