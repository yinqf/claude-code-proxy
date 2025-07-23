from src.core.config import config
import logging

logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self, config):
        self.config = config
        # 默认模型配置，当客户端模型名称为空时使用
        self.default_model = "gpt-4o"
        self.default_small_model = "gpt-4o-mini"
    
    def map_claude_model_to_openai(self, claude_model: str) -> str:
        """Map Claude model names to OpenAI model names based on BIG/SMALL pattern"""
        # 如果客户端模型名称为空，使用默认大模型
        if not claude_model or claude_model.strip() == "":
            logger.warning("Empty model name received from client, using default model")
            # 如果配置了big_model，使用配置的大模型，否则使用默认模型
            return self.config.big_model or self.default_model
            
        # If it's already an OpenAI model, return as-is
        if claude_model.startswith("gpt-") or claude_model.startswith("o1-"):
            return claude_model

        # If it's other supported models (ARK/Doubao/DeepSeek), return as-is
        if (claude_model.startswith("ep-") or claude_model.startswith("doubao-") or 
            claude_model.startswith("deepseek-")):
            return claude_model
        
        # Map based on model naming patterns
        model_lower = claude_model.lower()
        
        # 使用haiku模型
        if 'haiku' in model_lower:
            # 如果没有配置small_model，直接使用客户端模型名称
            if self.config.small_model is None or self.config.small_model.strip() == "":
                logger.info(f"No small_model configured, using client model: {claude_model}")
                return claude_model
            return self.config.small_model
            
        # 使用sonnet模型
        elif 'sonnet' in model_lower:
            # 如果没有配置middle_model，直接使用客户端模型名称
            if self.config.middle_model is None or self.config.middle_model.strip() == "":
                logger.info(f"No middle_model configured, using client model: {claude_model}")
                return claude_model
            return self.config.middle_model
            
        # 使用opus模型
        elif 'opus' in model_lower:
            # 如果没有配置big_model，直接使用客户端模型名称
            if self.config.big_model is None or self.config.big_model.strip() == "":
                logger.info(f"No big_model configured, using client model: {claude_model}")
                return claude_model
            return self.config.big_model
            
        else:
            # 默认使用big_model，如果没有配置，则直接使用客户端模型名称
            if self.config.big_model is None or self.config.big_model.strip() == "":
                logger.info(f"No big_model configured for unknown model type, using client model: {claude_model}")
                return claude_model
            return self.config.big_model

model_manager = ModelManager(config)