#!/usr/bin/python

import os
import sys
import nltk
import argparse
from att.log import LogDebug
from att.pickle import LoadFromFile
from att.corpus import CorpusFactory
from att.dictionary import DictionaryFactory
from att.global_context import global_context

def main():
  parser = argparse.ArgumentParser(description='Align a corpus.')
  parser.add_argument('--trained_aligner',
                      help="Trained aligner (written by train.py) to load.",
                      required=True)
  parser.add_argument('--corpus',
                      help="The corpus our aligner will be tested on.",
                      required=True)
  parser.add_argument('--dictionary',
                      help="The location of the aligner dictionary.",
                      required=True)
  parser.add_argument('--verbose', '-v',
                      action='count',
                      default=0,
                      help="Determines verbosity level (none, -v, -vv or"
                           " -vvv). none: prints errors/warnings (default),"
                           " -v - prints basic information, -vv: prints debug"
                           " data, -vvv: prints everything.")

  args = parser.parse_args(sys.argv[1:])
  global_context.SetArgs(args)

  current_directory = os.path.dirname(__file__)
  nltk.data.path.append(os.path.join(current_directory, "venv/nltk_data"))

  LogDebug("[test_aligner.py] loading corpus...")
  corpus = CorpusFactory.MakeFromFile(args.corpus)
  LogDebug("[test_aligner.py] loading aligner...")
  aligner = LoadFromFile(args.trained_aligner)
  LogDebug("[test_aligner.py] loading dictionary...")
  dictionary = DictionaryFactory.MakeFromFile(args.dictionary)
  LogDebug("[test_aligner.py] testing aligner...")
  print aligner.Evaluate(corpus, dictionary)

if __name__ == "__main__":
    main()
