#!/usr/bin/python
import argparse
import os
import re
import sys


class StringHunter(object):
    def __init__(self):
        self.OutputFile = "out.txt"
        self.Extensions = ('.cs', '.cshtml', '.aspx', '.js')
        self.Ignore = "\\\(.sonar|bin|Scripts)"

        self.MatchedFiles = 0
        self.MatchedLines = 0
        self.Output = []


    def _verifyArgs(self, args, out):
        if not os.path.exists(args.rootDirectory):
            out.write("'{0}' does not exists. Check path and try again. Make sure to enclose path in quotes.".format(args.rootDirectory))
            return False
        elif not os.path.isdir(args.rootDirectory):
            out.write("'{0}' is not a directory. Check path and try again.".format(args.rootDirectory))
            return False
        return True


    def _searchForStrings(self, stringLiterals, lineNumber, line):
        literals = re.findall('"[^"]*"', line)

        for literal in literals:
            literal = literal.strip()

            if re.search("\w", literal) and re.search(" ", literal):
                stringLiterals.append(str(lineNumber) + "\t" + literal)
                self.MatchedLines += 1


    def _searchAgainInXML(self, stringLiterals, lineNumber, line):
        parsedLine = re.sub("<[^>]*>", " ", line)
        parsedLine = re.sub("&nbsp;", " ", parsedLine).strip()

        if re.search("\w", parsedLine):
            stringLiterals.append(str(lineNumber) + "\t" + parsedLine)
            self.MatchedLines += 1


    def _parseFile(self, filename, path):
        with open(path, 'rb') as f:
            stringLiterals = []
            lineNumber = 0

            for line in f.readlines():
                lineNumber += 1

                self._searchForStrings(stringLiterals, lineNumber, line)
                if filename.endswith('.aspx'):
                    self._searchAgainInXML(stringLiterals, lineNumber, line)

        return stringLiterals


    def _populateOutput(self, path, stringLiterals):
        if stringLiterals:
            self.Output.append(path + "\n\n")
    
            for line in stringLiterals:
                self.Output.append(line + "\n")
    
            self.Output.append("___________________________________________\n\n")


    def _writeOutputFile(self):
        if self.Output:
            with open(self.OutputFile, 'wb') as f:
                for line in self.Output:
                    f.write(line)


    def hunt(self, args, out=sys.stdout):
        if not self._verifyArgs(args, out):
            return False
        else:
            for root, _dirnames, filenames in os.walk(args.rootDirectory):
                for filename in filenames:
                    if filename.endswith(self.Extensions):
                        path = os.path.join(root, filename)

                        if not re.search(self.Ignore, path):
                            self.MatchedFiles += 1
                            stringLiterals = self._parseFile(filename, path)
                            self._populateOutput(path, stringLiterals)

            self._writeOutputFile()
            return self.MatchedFiles, self.MatchedLines


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Hunts for string literals in code files and outputs them for review.")
    parser.add_argument("rootDirectory", help="Root directory to start the hunt (enclosed in quotes)")
    sys.exit(StringHunter().hunt(parser.parse_args()))
