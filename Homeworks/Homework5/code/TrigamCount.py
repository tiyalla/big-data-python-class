import mrjob
from mrjob.job import MRJob
from mrjob.step import MRStep
import re
from itertools import islice, izip
import itertools

WORD_RE = re.compile(r"[\w']+")

class TrigramCount(MRJob):
  def steps(self):
    return [
            MRStep(mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_top)
        ]

  def mapper(self, _, line):
    words = WORD_RE.findall(line)
    trigramList = []

    for i, word in enumerate(words):
      if i < len(words) - 2:
        trigramList = [words[i], words[i+1], words[i+2]]
        yield trigramList, 1


  def combiner(self, trigram, counts):
    yield (trigram, sum(counts))

  def reducer(self, trigram, counts):
    yield None,(trigram, sum(counts))

  def reducer_top(self, _, trigramCount):
    for i in sorted(trigramCount, key=lambda x:x[1], reverse=True)[:10]:
      yield i


if __name__ == '__main__':
  TrigramCount.run()