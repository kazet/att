#!/usr/bin/python

import os
import sys
import nltk
import argparse
from att.log import LogDebug, LogFileContentsDebug
from att.pickle import SaveToFile
from att.corpus import CorpusFactory
from att.aligner import AlignerFactory
from att.dictionary import DictionaryFactory
from att.global_context import global_context

def main():
  parser = argparse.ArgumentParser(description='Align a corpus.')
  parser.add_argument('--training_corpus',
                      help="The corpus our aligner will be trained on.",
                      required=True)
  parser.add_argument('--aligner',
                      help="The aligner configuration location.",
                      required=True)
  parser.add_argument('--training_set_size',
                      help="The number of documents that will be taken from"
                           " the corpus to train the aligner.",
                      default=1000,
                      type=int)
  parser.add_argument('--output',
                      help="The file trained aligner should be written to.",
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
  LogFileContentsDebug("[train.py: aligner]", args.aligner)
  LogFileContentsDebug("[train.py: training corpus]", args.training_corpus)

  current_directory = os.path.dirname(__file__)
  nltk.data.path.append(os.path.join(current_directory, "venv/nltk_data"))
  LogDebug("[train.py] loading corpus...")
  training_corpus = CorpusFactory.MakeFromFile(args.training_corpus)
  LogDebug("[train.py] loading aligner...")
  aligner = AlignerFactory.MakeFromFile(args.aligner)
  LogDebug("[train.py] loading dictionary...")
  dictionary = DictionaryFactory.MakeFromFile(args.dictionary)
  LogDebug("[train.py] training corpus...")
  try:
    aligner.Train(training_corpus, args.training_set_size, dictionary)
  except MemoryError, unused_exception:
    print ("MemoryError: try decreasing"
           " --training_set_size to %d" % (args.training_set_size / 2))

  SaveToFile(aligner, args.output)

if __name__ == "__main__":
    main()
