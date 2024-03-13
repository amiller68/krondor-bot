from .config import Config

class Bot():
    def __init__(self, config: Config):
        # Set the Telegram token
        self.tg_token = os.getenv("TG_TOKEN")
        if self.tg_token is None:
            raise Exception("Setting `TG_TOKEN` is required")
        
        # Set the Database URL. Default to in-memory for now
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///:memory:")
        
        # Set the log path
        self.log_path = os.getenv("LOG_PATH")

        # Determine if the DEBUG mode is set
        debug = os.getenv("DEBUG", "true")
        self.debug = debug == "true"

        # Read the agent configuration at the path
        agent_config_path = os.getenv("AGENT_CONFIG_PATH", "agent.yaml")

        # Open the configration file for the model
        with open(agent_config_path) as f:
            # Load the config file
            self.agent_config = yaml.safe_load(f)