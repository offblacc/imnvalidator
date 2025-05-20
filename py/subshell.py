import pexpect
from constants import AWAITS_PROMPT
import traceback
import config
from abc import ABC, abstractmethod
from typing import Tuple

class Subshell(ABC):
    def __init__(self):
        self.child = None
        self.last_cmd_status = None
        command = self._get_command()
        self.child = pexpect.spawn(command, encoding="utf-8", timeout=10)
        try:
            self.child.expect(AWAITS_PROMPT)
        except Exception:
            print("Could not start subshell. Details:")
            print(traceback.format_exc())
    
    @abstractmethod
    def _get_command(self) -> str:
        """Return the command string to spawn subshell"""
        pass

    @abstractmethod
    def send(self, command: str):
        """Sends command to the subshell and returns its output.
        Modifies self.last_cmd_status

        Args:
            command (str): The command to run
        """
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.child and self.child.isalive():
            self.child.close()
        self.child = None

class HostSubshell(Subshell):
    def _get_command(self) -> str:
        return '/bin/bash'
    
    def send(self, command: str) -> str:
        self.child.sendline(command)
        self.child.expect(AWAITS_PROMPT)
        output = '\n'.join(self.child.before.strip().split('\r\n')[1:-1])
        self.child.sendline("echo $?")
        self.child.expect(r"\d+\r?\n")
        self.last_cmd_status = self.child.match.group(0).strip()
        return output

class NodeSubshell(Subshell):
    def __init__(self, node: str):
        self.node = node
        super().__init__()
    
    def _get_command(self) -> str:
        return f'himage {self.node}@{config.state.eid}'

    def send(self, command: str) -> str:
        self.child.sendline(command)
        self.child.expect(AWAITS_PROMPT)
        output = '\n'.join(self.child.before.strip().split('\r\n')[1:-1])
        output = output[output.find('\r') + 1:] # skip ANSI garbage, ended with \r always during testing
        self.child.sendline("echo $?")
        self.child.expect(r"\d+\r?\n")
        self.last_cmd_status = self.child.match.group(0).strip()
        return output
