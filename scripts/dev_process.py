import subprocess

from rich.console import Console  # type: ignore

console = Console()


def _run_functional_tests():
    console.rule("[bold blue]Executing tests via nox")
    with console.status("[bold green] Functional Test execution in progress..."):
        cmd = ["nox", "-s", "functional_tests"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode:
            console.print(
                "[bold red] :broken_heart: Functional Tests have failed. "
                "Please investigate"
            )
            console.print(result.stdout)
            console.print(result.stderr)
            exit(result.returncode)
        else:
            console.print(
                "[bold green] :green_heart: Functional Tests have passed. "
                "Moving on..."
            )


def run_tests():
    _run_functional_tests()
