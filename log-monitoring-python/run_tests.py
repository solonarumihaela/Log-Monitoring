import unittest
from pathlib import Path

class ReportResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        title = test.shortDescription() or test.id().split('.')[-1]
        self.stream.writeln(f"[OK]       {title}")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        title = test.shortDescription() or test.id().split('.')[-1]
        self.stream.writeln(f"[NOT OK]   {title}")

    def addError(self, test, err):
        super().addError(test, err)
        title = test.shortDescription() or test.id().split('.')[-1]
        self.stream.writeln(f"[NOT OK]   {title}")

class ReportRunner(unittest.TextTestRunner):
    resultclass = ReportResult

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover("tests")
    out_file = Path("test_results.log").open("w", encoding="utf-8")
    runner = ReportRunner(verbosity=2, stream=out_file)
    runner.run(suite)
    out_file.close()