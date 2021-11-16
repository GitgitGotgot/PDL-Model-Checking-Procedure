import numpy as np

class Kripke:
    def __init__(self, Adj_M, State_V):
        self.Adj_M = Adj_M
        self.State_V = State_V


class TFIDF:
    def __init__(self, Query, index):
        """
        Query: Query object
        index: Inverted index of all the documents (datatype a dict of dicts with integers)
        """
        self.queries = Query.queries
        self.nr_docs = self.nr_docs(index)
        self.docl_dict = self.docl_dict(index)
        self.rankings = self.ranking(index)
        self.final_df = self.rankdict_to_df(self.rankings, Query)

    def nr_docs(self, index):
        """ returns the number of documents in the index """
        all_docs = set()
        for key in index:
            all_docs.add(index[key].values())

        return len(list(all_docs))

    def docl_dict(self, index):
        """ returns a dictionary with as key document names from the index and as value the length of this document """
        doclength = defaultdict(int)
        for key in index:
            for docname in index[key]:
                doclength[docname] += index[key][docname]

        return doclength

    def ranking(self, index):
        rank = []
        for i, q in enumerate(self.queries):
            clear_output(wait=True)
            print("calculating TFIDF:", int(i/len(self.queries) * 100), '%')
#             scores = defaultdict(int)
            score = dict()
            documents = set()

            for word in q:
                if word not in index: continue
                N = self.nr_docs
                df = sum(index[word].values())
                for docname in index[word]:
                    tf = index[word][docname]
                    idf = np.log10((1 + N) / (1 + df))

                    if tf != 0:
                        score[docname] = tf * idf

            rank.append(sorted(score.items(), key=lambda x: x[1], reverse=1)[:1000])

        clear_output(wait=True)
        return [rank]



    def rankdict_to_df(self, rank_score, Query):
        data = []
        for query in rank_score:
            for i, docname in enumerate(query):
                docId = Query.query_ids[i]
                for j, result in enumerate(docname):
                    name, score = result
                    data.append([docId, 'Q0', name, j + 1, score, '12602426'])

        return pd.DataFrame(data)
