import re
from dataclasses import dataclass


@dataclass
class RuntimeInfo:
    phase: str
    cpu_user: float
    cpu_sys: float
    elapsed: float


class HLSLog:
    RE_RUNTIME = re.compile(
        r"Finished ([^:]+): CPU user time:\s*([0-9.]+) seconds\. "
        r"CPU system time:\s*([0-9.]+) seconds\. "
        r"Elapsed time:\s*([0-9.]+) seconds"
    )

    def __init__(self, txt: str):
        self.txt = txt

    def lines(self):
        return self.txt.splitlines()

    def warnings(self) -> list[str]:
        return [line for line in self.lines() if "WARNING:" in line]

    def errors(self) -> list[str]:
        return [line for line in self.lines() if "ERROR:" in line]

    def infos(self) -> list[str]:
        return [line for line in self.lines() if "INFO:" in line]

    def runtimes(self) -> list[RuntimeInfo]:
        results = []
        for m in self.RE_RUNTIME.finditer(self.txt):
            phase = m.group(1).strip()
            cpu_user = float(m.group(2))
            cpu_sys = float(m.group(3))
            elapsed = float(m.group(4))

            results.append(
                RuntimeInfo(
                    phase=phase,
                    cpu_user=cpu_user,
                    cpu_sys=cpu_sys,
                    elapsed=elapsed,
                )
            )
        return results
