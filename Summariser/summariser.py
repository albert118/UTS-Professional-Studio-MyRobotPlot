import re
from heapq import nlargest

import spacy
from spacy.tokenizer import Tokenizer


class Summariser():
    def __init__(self, intro_text: str):
        self.pretrained_model = 'en_core_web_sm'
        self.intro_text = intro_text
        
        # Set up
        self.LoadModel()
        self.GetNlp().tokenizer = self.Custom_Delimiter_Pipeline()

        # Build
        self.LoadText()
    
    def LoadModel(self):
        self._nlp = spacy.load(self.pretrained_model)

    def LoadText(self):
        self._intro_doc = self._nlp(self.intro_text)

    def PrintTokensFromDoc(self):
        print([token.text for token in self._intro_doc])

    def GetSentencesFromDoc(self) -> list:
        return [s for s in self._intro_doc.sents]

    def Custom_Delimiter_Pipeline(self):
        prefix_re = spacy.util.compile_prefix_regex(self.GetNlp().Defaults.prefixes)
        suffix_re = spacy.util.compile_suffix_regex(self.GetNlp().Defaults.suffixes)
        infix_re = re.compile(r'''[-~]''')

        # Adds support to use `-` as the delimiter for tokenization
        return Tokenizer(self.GetNlp().vocab, prefix_search=prefix_re.search,
                      suffix_search=suffix_re.search,
                      infix_finditer=infix_re.finditer,
                      token_match=None
                      )

    def GetWordFrequencies(self):
        self.word_frequencies = dict()
        
        for word in self._intro_doc:
            if word.text not in self.word_frequencies.keys():
                self.word_frequencies[word.text] = 1
            else:
                self.word_frequencies[word.text] += 1
    
    def NormaliseWordFrequencies(self):
        max_frequency = max(self.word_frequencies.values())
        for word in self.word_frequencies.keys():
            self.word_frequencies[word] = self.word_frequencies[word] / max_frequency

    def GetSentenceScores(self):
        self.sentence_scores = dict()

        for sent in self.GetSentencesFromDoc():
            for word in sent:
                if word.text.lower() in self.word_frequencies.keys():
                    if sent not in self.sentence_scores.keys():                            
                        self.sentence_scores[sent] = self.word_frequencies[word.text.lower()]
                    else:
                     self.sentence_scores[sent] += self.word_frequencies[word.text.lower()]

    def GetNlp(self):
        return self._nlp

    def GetSummary(self, consoleLog=False):
        relevancy_score = 0.3
        
        self.GetWordFrequencies()
        self.NormaliseWordFrequencies()
        sentences = self.GetSentencesFromDoc()
        self.GetSentenceScores()

        select_length = int(len(sentences)*relevancy_score)
        summary = nlargest(select_length, self.sentence_scores, key=self.sentence_scores.get)

        if consoleLog:
            print(summary)
        
        return summary


def RunDemo():
    introduction_text="""The human coronavirus was first diagnosed in 1965 by Tyrrell and Bynoe from the respiratory tract sample of an adult with a common cold cultured on human embryonic trachea.1 Naming the virus is based on its crown-like appearance on its surface.2 Coronaviruses (CoVs) are a large family of viruses belonging to the Nidovirales order, which includes Coronaviridae, Arteriviridae, and Roniviridae families.3 Coronavirus contains an RNA genome and belongs to the Coronaviridae family.4 This virus is further subdivided into four groups, ie, the α, β, γ, and δ coronaviruses.5 α- and β-coronavirus can infect mammals, while γ- and δ- coronavirus tend to infect birds.6 Coronavirus in humans causes a range of disorders, from mild respiratory tract infections, such as the common cold to lethal infections, such as the severe acute respiratory syndrome (SARS), Middle East respiratory syndrome (MERS) and Coronavirus disease 2019 (COVID-19). The coronavirus first appeared in the form of severe acute respiratory syndrome coronavirus (SARS-CoV) in Guangdong province, China, in 20027 followed by Middle East respiratory syndrome coronavirus (MERS-CoV) isolated from the sputum of a 60-year-old man who presented symptoms of acute pneumonia and subsequent renal failure in Saudi Arabia in 2012.8 In December 2019, a β-coronavirus was discovered in Wuhan, China. The World Health Organization (WHO) has named the new disease as Coronavirus disease 2019 (COVID-19), and Coronavirus Study Group (CSG) of the International Committee has named it as SARS-CoV-2.9,10 Based on the results of sequencing and evolutionary analysis of the viral genome, bats appear to be responsible for transmitting the virus to humans"""
    sentances = Summariser(introduction_text)
    sentances.PrintTokensFromDoc()
    showSummaryFlag = input("Display summary (Y)?").upper().trim() == 'Y'
    sentances.GetSummary(showSummaryFlag)

