import logging
import re

LOG_LVL = logging.NOTSET
logging.basicConfig(level=LOG_LVL)
_logger = logging.getLogger(__name__)


class StringCleaner:
    def __init__(self, dirtyString: str):
        self.akaChar= '`'
        self.data = dirtyString

    def Clean_DoubleQuotes_WithinSingleQuotes(self):
        """
        for examples such as: '" #1 Jack Jones _the-(best1234567890)_"'
        replaces with " #1 Jack Jones _the-(best1234567890)_ "
        """

        nestedQuotesWithText = r"'\"(.+)+\"'"
        self.data = re.sub(nestedQuotesWithText, r'"\1"', self.data)
        
        return self

    def Clean_Single_Apostrophes(self): 
        """
        simply converting all ' to " - ignoring examples such as: "harry's"
        """

        placeHolder = "GRAMMATICAL_TICK"
        ignoreGrammatricalApostrpohes = r"(?<=\w)'(?=\w)"
        # note the non capturing groups to improve perf.
        getSingleQuotedString = r"(?:')([^']+)*(?:')"
        # also there's a fun edge-case where a value may be:
        # "my already correct thing with a single apostrophe' inside"
        # we need to ignore this!
        # A single regexp with a 'NOT' is incredibly slow, we take the palceholder approach again!
        getAlreadyQuotedStringToIgnore = r'(?:")([^"]+)*(?:")'

        self.data = re.sub(ignoreGrammatricalApostrpohes, placeHolder, self.data)
        self.data = re.sub(getSingleQuotedString, r'"\1"', self.data)
        self.data = re.sub(placeHolder, "'", self.data)

        return self

    def Clean_None_Types(self):
        findNones = "None"
        self.data = re.sub(findNones, '"None"', self.data)
        return self

    def Clean_Aka_Quotes_Escapes(self):
        """
        Captures an aka quoted name such as 'C3P-0' or "C3P-0" and replaces it with `C3P-0`
        the re-quote is configured in the __init__ with akaChar
        """

        # the ' scenario
        trailingEsc = r"""'(?= [a-zA-Z0-9-]+",)"""
        leadingEsc = r"""'(?=[a-zA-Z0-9-]+'[^:,])"""
        # then the " scenario
        doubleQuoteAka = r'\s(?:")([\w\s\.\-#\\/]+)(?:")\s'
        
        # the order is important here because I bloody hate this much regex
        self.data = re.sub(leadingEsc, self.akaChar, self.data)
        self.data = re.sub(trailingEsc, self.akaChar, self.data)
        self.data = re.sub(doubleQuoteAka, fr' {self.akaChar}\1{self.akaChar} ', self.data)
        
        return self

    def Clean_Start_And_End_Of_String(self):
        # just to be fun, dirty json can be wrapped in extra quotes " " that throw the deserializer! YAY
        rg = '^"|"$'
        self.data = re.sub(rg, '', self.data.strip())

        return self

    def GetData(self): return self.data


def DeepClean(dirtyLaundry: str) -> str:
    try:
        return (
            StringCleaner(dirtyLaundry)
                .Clean_DoubleQuotes_WithinSingleQuotes()
                .Clean_Aka_Quotes_Escapes()
                .Clean_None_Types()
                .Clean_Single_Apostrophes()
                .Clean_Start_And_End_Of_String()
                .GetData()
        )
    except Exception as e:
        _logger.error(f"error when cleaning data '{e}'")
        raise

