from __future__ import annotations
from typing import Optional, Any
from rich.console import Console
from logger import FileFormatter, Logger


class CyLpError:
    """Base class for all errors in the CyLp language."""
    
    def __init__(
        self,
        message: str,
        line: int,
        column: int,
        token: Optional[str] = None,
        **extra: Any,
    ) -> None:
        self.message = message
        self.line = line
        self.column = column
        self.token = token
        self.__dict__.update(extra)
    
    def details(self):
        return " "
       
    def format(self) -> str:
        """Returns a pretty string of the error"""
        
        location = f"line: {self.line}, col: {self.column}"
        token_part = f" cerca de '{self.token}'" if self.token else ""
        detail = self.details()
        
        return f"[cyan]{location}[/] [bold red]{self.__class__.__name__}[/]: {self.message}[yellow]{detail}{token_part}[/]"
   
    
    def format_file(self) -> str:
        """Returns a plain string of the error"""
        
        location = f"line: {self.line}, col: {self.column}"
        token_part = f" cerca de '{self.token}'" if self.token else ""
        detail = self.details()
        
        return f"{location} {self.__class__.__name__}: {self.message}{detail}{token_part}"      
            
    def __str__(self):
        """For print(error) to work automatically"""
        return self.format()
    
    def __repr__(self):
        return f"{self.__class__.__name__}('{self.message}', {self.line}, {self.column})"
 
   
class LexerError(CyLpError):
    """Lexical error: prohibited character or sequence.\n
    Extra attributes: bad_char = the incorrect character."""    
    def details(self):
        return f" -> '{self.bad_char}'"
        

class ParserError(CyLpError):
    """Syntax error: the parser expected something different."""
    
    def details(self):
        return f"(Expected: {self.expected}, Get: {self.get})" if isinstance(self.expected, str) else '/'.join(self.expected)
      
        
class TypeErrorCyLp(CyLpError):
    """Type error during semantic analysis."""
    
    def details(self):
        return f" -> esperado: {self.expected_type}, encontrado: {self.got_type}"
     
        
class NameErrorCyLp(CyLpError):
    """Undeclared or out-of-scope identifier."""
    
    def details(self):
        return f" -> '{self.name}' no esta definido"


class RuntimeErrorCyLp(CyLpError):
    """Error during program execution."""
    
    def details(self):
        return f" durante operacion: {self.operation}"
        
    
class ErrorReporter:
    def __init__(self, logger:Logger) -> None:
        self.errors: list[CyLpError] = []
        self.panic_mode: bool = False
        self.max_errors: int = 20
        self.console = Console()
        self.log_formatter = FileFormatter()
        self.logger = logger
    
    def add_error(self, error: CyLpError) -> None:
        if len(self.errors) >= self.max_errors and not self.panic_mode:
            self.errors.append(CyLpError("Demasiados errores, modo pánico activado.", 0, 0))
            self.panic_mode = True
        elif len(self.errors) < self.max_errors and not self.panic_mode:
            self.errors.append(error)
            self.logger.log("ERROR", error.format_file(), error.column, error.line)
            self.logger.write_to_files(self.log_formatter)
        
    def has_errors(self) -> bool:
        return len(self.errors) > 0
            
    def display(self) -> None:
        for error in self.errors:
            self.console.print(f"[white]{error}[/]")
