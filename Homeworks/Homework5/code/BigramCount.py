import mrjob
from mrjob.job import MRJob
from mrjob.step import MRStep
import re
from itertools import islice, izip
import itertools

WORD_RE = re.compile(r"[\w']+")

class BigramCount(MRJob):

  def steps(self):
    return [
            MRStep(mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_top)
        ]

  def mapper(self, _, line):
    words = WORD_RE.findall(line)
    firstword = ""
    secondword = ""

    for i in izip(words, islice(words, 1, None)):
      firstword = str(i[0])
      secondword = str(i[1])
      yield (firstword, secondword), 1

  def combiner(self, bigram, counts):
    yield (sorted(bigram), sum(counts))

  def reducer(self, bigram, counts):
    yield None,(bigram, sum(counts))

  def reducer_top(self, _, bigramCount):
    for i in sorted(bigramCount, key=lambda x:x[1], reverse=True)[:10]:
      yield i


if __name__ == '__main__':
  BigramCount.run()