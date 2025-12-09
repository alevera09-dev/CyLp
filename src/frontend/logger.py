from time import strftime, gmtime

class LogMessage:
    def __init__(self, level:str, text:str, col:str, line:str):
        self.col = col
        self.line = line
        self.level = level
        self.text = text
        
class FileFormatter:
    def format(self, log_message: LogMessage):
        return f"[{log_message.level}] {log_message.text}"
    
class ColorConsoleFormatter:
    COLORS = {
        "DEBUG": "\033[96m",
        "INFO": "\033[92m",
        "WARN": "\033[93m",
        "ERROR": "\033[91m"
        }
    
    RESET = "\033[0m"

    def format(self, log_message: LogMessage):
        color = self.COLORS.get(log_message.level)
        return f"{color}[{log_message.level}] {log_message.text} col: {log_message.col}, line: {log_message.line}{self.RESET}"
    
           
class Logger:
    def __init__(self, min_level="INFO"):
        self.messages_list = []
        self.min_level = min_level
        self.levels = {"DEBUG":0, "INFO":1, "WARN":2, "ERROR":3}
        self.timestamp_file = strftime("%Y-%m-%d", gmtime())
    
    def set_level(self, new_level):
        self.min_level = new_level
        
    def log(self, level:str, text:str, col:int, line:int):
        if self.levels[level] >= self.levels[self.min_level]:
            log_message = LogMessage(level, text, str(col), str(line))
            self.messages_list.append(log_message)
    
    def write_to_files(self, formatter:FileFormatter):
        with open(f"{self.timestamp_file}-application.log", "a") as application_log:
            
            with open(f"{self.timestamp_file}-errors", "a") as errors_log:
                for msg in self.messages_list:
                    
                    application_log.write(formatter.format(msg) + "\n")
                    if self.levels[msg.level] >= self.levels["WARN"]:
                        errors_log.write(formatter.format(msg) + "\n")
        
        self.messages_list.clear()
        
    def print_logs(self, formatter:ColorConsoleFormatter | FileFormatter):
        for msg in self.messages_list:
            print(formatter.format(msg))