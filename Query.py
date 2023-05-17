def generate_ngrams(sentence):
    words = sentence.split()
    n = len(words)
    ngram_map = {}

    for i in range(n, 0, -1):
        ngrams = []
        for j in range(0, n - i + 1):
            ngram = ' '.join(words[j:j + i])
            ngrams.append(ngram)

        ngram_map[i] = ngrams

    return ngram_map