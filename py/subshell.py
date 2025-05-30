import pexpect
from constants import AWAITS_PROMPT, AWAITS_FREEBSD_ROOT_PROMPT, OS
import traceback
import config
from abc import ABC, abstractmethod
from typing import Tuple

class Subshell(ABC):
    def __init__(self):
        # self.child = None
        self.last_cmd_status = None
        command = self._get_command()
        self.child = pexpect.spawn(command, encoding="utf-8", timeout=10)
        try:
            self.child.expect(self._get_prompt())
        except Exception:
            print("Could not start subshell. Details:")
            print(traceback.format_exc())
    
    @abstractmethod
    def _get_command(self) -> str:
        """Return the command string to spawn subshell"""
        pass
    
    @abstractmethod
    def _get_prompt(self) -> str:
        """Return prompt to await when starting shell"""
        pass

    def send(self, command: str) -> str:
        self.clear_buffer()
        
        self.child.sendline(command)
        self.child.expect(self.prompt)
        
        output = '\n'.join(self.child.before.strip().split('\r\n')[1:-1]) # cut original command and new prompt
        output = output[output.find('\r') + 1:] # skip additional ANSI garbage
        
        self.child.sendline("echo $?")
        self.child.expect(r"\d+\r?\n")
        
        self.last_cmd_status = self.child.match.group(0).strip()
        
        self.clear_buffer()

        return output

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.child and self.child.isalive():
            self.child.close()
        self.child = None
    
    def clear_buffer(self):
        try:
            while True:
                self.child.expect('.+', timeout=0)
        except pexpect.TIMEOUT:
            pass

class HostSubshell(Subshell):
    def __init__(self, host=OS.LINUX):
        self.prompt = AWAITS_PROMPT if host == OS.LINUX else AWAITS_FREEBSD_ROOT_PROMPT
        super().__init__()
        
    def _get_command(self) -> str:
        return '/bin/bash'
    
    def _get_prompt(self) -> str:
        return self.prompt
    
class NodeSubshell(Subshell):
    def __init__(self, node: str):
        self.node = node
        self.prompt = AWAITS_PROMPT
        super().__init__()
    
    def _get_command(self) -> str:
        return f'himage {self.node}@{config.state.eid}'
    
    def _get_prompt(self) -> str:
        return self.prompt # covers prompts on both freebsd&linux host's nodes