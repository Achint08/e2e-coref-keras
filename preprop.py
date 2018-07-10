import re
import numpy as np
import random
import collections

BEGIN_DOCUMENT_REGEX = re.compile(r"#begin document \(((..).*)\); part (\d+)")

GENRE = [ 'bc', 'bn', 'nw', 'mz', 'wb', 'tc', 'pt']

def finalize_clusters(clusters):
    merged_clusters = []
    for c1 in clusters.values():
      existing = None
      for m in c1:
        for c2 in merged_clusters:
          if m in c2:
            existing = c2
            break
        if existing is not None:
          break
      if existing is not None:
        existing.update(c1)
      else:
        merged_clusters.append(set(c1))
    merged_clusters = [list(c) for c in merged_clusters]
    return merged_clusters

def normalize_word(word):
  if word == "/." or word == "/?":
    return word[1:]
  else:
    return word

def get_genre(genre):
  return "{}".format(genre)

def readfile(filename):
    '''
    read file
    return format :
    [['doc_key','text','speaker']['coreference_cluster_start', 'coreference_cluster_end']]
    '''
    f = open(filename)
    sentences = []
    sentence = []
    begin_document_match = ''
    genre = ''
    clusters = collections.defaultdict(list)
    stacks = collections.defaultdict(list)
    word_index = 0
    for line in f:
        begin_document_match = re.match(BEGIN_DOCUMENT_REGEX, line)
        if begin_document_match:
            genre = get_genre(begin_document_match.group(2))
        elif line.startswith("#end document"):
            merged_clusters = finalize_clusters(clusters)
            sentences.append([sentence, merged_clusters])
            word_index = 0;
            sentence = []
            cluster = []
        else:
            splits = line.split()
            if len(splits) >= 12:
                word = normalize_word(splits[3])
                word_index = len(sentence)
                speaker = splits[9]
                coref = splits[-1]
                if coref != '-':
                    for segment in coref.split("|"):
                        if segment[0] == "(":
                            if segment[-1] == ")":
                                cluster_id = int(segment[1:-1])
                                clusters[cluster_id].append((word_index, word_index))
                            else:
                                cluster_id = int(segment[1:])
                                stacks[cluster_id].append(word_index)
                        else:
                            cluster_id = int(segment[:-1])
                            start = stacks[cluster_id].pop()
                            clusters[cluster_id].append((start, word_index))
                sentence.append([GENRE.index(genre), word, speaker])
    return sentences