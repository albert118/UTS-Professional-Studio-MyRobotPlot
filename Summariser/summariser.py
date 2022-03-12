import spacy


class Summariser():
    def __init__(self, intro_text: str):
        self.pretrained_model = 'en_core_web_sm'
        self.intro_text = intro_text
        
        # Set up
        self.LoadModel()
        self.LoadText()
    
    def LoadModel(self):
        self._nlp = spacy.load(self.pretrained_model)

    def LoadText(self):
        self._intro_doc = self._nlp(introduction_text)

    def GetTokensFromDoc(self):
        print([token.text for token in self._intro_doc])




introduction_text = ('This is some sample text about the thing with the place and thing. This is some sample text about the thing with the place and thing')
s = Summariser(introduction_text)
s.GetTokensFromDoc()