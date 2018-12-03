import mrjob
from mrjob.job import MRJob
from mrjob.step import MRStep
import re
from itertools import islice, izip
import itertools

WORD_RE = re.compile(r"[\w']+")

class MonogramCount(MRJob):
  def steps(self):
    return [
            MRStep(mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_top)
        ]

  def mapper(self, _, line):
    words = WORD_RE.findall(line)

    for word in words:
      yield word, 1

  def combiner(self, monogram, counts):
    yield (monogram, sum(counts))

  def reducer(self, monogram, counts):
    yield None,(monogram, sum(counts))

  def reducer_top(self, _, monogramCount):
    for i in sorted(monogramCount, key=lambda x:x[1], reverse=True)[:10]:
      yield i


if __name__ == '__main__':
  MonogramCount.run()