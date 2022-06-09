"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from CompilationEngine import CompilationEngine
from JackTokenizer import JackTokenizer



def xml_line_writer(token_type: str, token: str) -> str:
    token_type = JackTokenizer.tokens_in_xml[token_type]
    return '<' + token_type + '> ' + token + ' </' + token_type + '>\n'


def analyze_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Analyzes a single file.

    Args:
        input_file (typing.TextIO): the file to analyze.
        output_file (typing.TextIO): writes all output to this file.
    """
    """
    We propose implementing the project in two stages. First, write and test
    the JackTokenizer module. Next, write and test the CompilationEngine
    module, which implements the parser described in the chapter.

    Stage I: JackTokenizer 
    Tokenizing, a basic service of any syntax analyzer, is the act of
    breaking a given textual input into a stream of tokens. And while it is
    at it, the tokenizer can also classify the tokens into lexical
    categories. With that in mind, your first task it to implement, and test,
    the JackTokenizer module. Specifically, you have to develop (i) a
    Tokenizer implementation, and (ii) a test program that goes through a
    given input file (.jack file).
    
    Tokenizer Testing:
    Test your tokenizer on the Square Dance and the TestArray programs.
    - Apply your tokenizer test to each Xxx.jack source file of the relevant
    test.
    - Given an Xxx.jack source file, have your tokenizer give the output file
    the name XxxT.xml, and then iterate on every token of the source file
    like so: 
    - Each token should be printed in a separate line, along with its
    classification: symbol, keyword, identifier, integer constant or string
    constant.
    - Use the supplied TextComparer utility to compare the generated output
    to the supplied .xml compare files.
    - Since the output files generated by your tokenizer test will have the
    same names and extensions as those of the supplied compare files, we
    suggest putting them in separate directories.
    
    Stage II: Parser (CompilationEngine) 
    In the context of this project, parsing is defined narrowly as the act of
    going over the tokenized input and rendering its grammatical structure
    using some agreed-upon format. The specific parser that we implement here
    is based on the Jack grammar, and is designed to emit XML output. Both
    the grammar and the agreed-upon XML tags are described in chapter 10. 
    The Jack parser is implemented by the CompilationEngine module. Your task
    is to implement this API: write each one of the specified methods, and
    make sure that it emits the correct XML output. For the benefit of
    unit-testing, we recommend to begin by first writing a compilation engine
    that handles any given Jack code except for expressions; next, extend the
    compilation engine to handle expressions as well. The test programs
    supplied are designed to support this staged testing strategy.
    
    Parser Testing:
    - Apply your syntax analyzer to the supplied test programs, then use the
    supplied TextComparer utility to compare the generated output to the
    supplied .xml compare files.
    - Since the output files generated by your syntax analyzer will have the
    same names and extensions as those of the supplied compare files, we
    suggest putting them in separate directories.
    - Note that the indentation of the XML output is only for readability.
    Web browsers and the supplied TextComparer ignore white space.
    
    Experimenting with the test programs: 
    if you want, you can compile the supplied SquareDance and TestArray
    programs using the supplied ("built-in") JackCompiler, then use the
    supplied VM emulator to run the compiled code. This activity is
    irrelevant to the current project. However, it serves to show that the
    test programs are not just plain text; they also have semantics, or
    meaning, something that the syntax analyzer does not care about.
    """

    tokenizer = JackTokenizer(input_file)
    tokenizer.tokenize()
    comp = CompilationEngine(tokenizer, output_file)
    comp.compile_class()

if "__main__" == __name__:
    # Parses the input path and calls analyze_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: JackAnalyzer <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".jack":
            continue
        output_path = filename + ".xml"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            analyze_file(input_file, output_file)
