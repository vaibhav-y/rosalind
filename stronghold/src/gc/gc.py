"""
    http://rosalind.info/problems/gc/

    Find the DNA string with the most GC content, given FASTA format strings

    Given: At most 10 DNA strings in FASTA format (of length at most 1 kbp each).

    Return: The ID of the string having the highest GC-content, followed by
            the GC-content of that string. Rosalind allows for a default error
            of 0.001 in all decimal answers unless otherwise stated;
"""
import re


TOLERANCE = 0.001
FASTA_HEADERS = re.compile(">(.+)")
FASTA_DNA_SEQ = re.compile("([ACGT\n]+)")


def parse_fasta(string):
    """
    Accepts a FASTA string and returns a dictionary (header -> sequence)
    """
    lines = string.split('\n')
    headers = []
    sequences = []
    for line in lines:
        is_header = FASTA_HEADERS.match(line)
        is_sequence = FASTA_DNA_SEQ.match(line)
        if is_header:
            headers.append(is_header.group())
            sequences.append('*')
        elif is_sequence:
            sequences.append(is_sequence.group())
    
    # The first step here creates a blank list element at the head of list
    # so zip only works with n - 1 elems and a blank. So we filter list
    sequences = ''.join(sequences).split('*')
    sequences = [s for s in sequences if s]
    return dict(zip(headers, sequences))

def find_key_for_max_value(dictionary):
    """
    Returns key in a dict with maximum value mapped to it
    """
    k = dictionary.keys()
    v = dictionary.values()
    return k[v.index(max(v))]
    
def gc_content(string):
    """
    Returns gc content of a DNA string as a percentage
    """
    string = string.lower()
    return 100.0 * (string.count('g') + string.count('c')) / len(string)
    
def gc(string):
    parsed      = parse_fasta(string)
    gcs         = map(gc_content, parsed.values())
    gc_dict     = dict(zip(parsed.keys(), gcs))
    max_gc_key  = find_key_for_max_value(gc_dict)
    return [max_gc_key, gc_dict[max_gc_key]]


if __name__ == "__main__":
    import os
    import sys
    
    if len(sys.argv) < 2:
        print "Usage: python %s <filename>" % sys.argv[0]
    else:
        fname = sys.argv[1]
        data = open(fname, 'rU').read()
        id_, val = gc(data)
        print id_
        print val