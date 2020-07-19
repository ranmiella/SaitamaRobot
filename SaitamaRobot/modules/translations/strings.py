from SaitamaRobot.modules.sql.translation import prev_locale
from SaitamaRobot.modules.translations.English import EnglishStrings
from SaitamaRobot.modules.translations.Russian import RussianStrings
from SaitamaRobot.modules.translations.Ukraine import UkrainianStrings
from SaitamaRobot.modules.translations.Spanish import SpanishStrings
from SaitamaRobot.modules.translations.Turkish import TurkishStrings
from SaitamaRobot.modules.translations.Indonesian import IndonesianStrings
from SaitamaRobot.modules.translations.Italian import ItalianStrings

def tld(chat_id, t, show_none=True):
    LANGUAGE = prev_locale(chat_id)
    print(chat_id, t)
    if LANGUAGE:
        LOCALE = LANGUAGE.locale_name
        if LOCALE in ('ru') and t in RussianStrings:
           return RussianStrings[t]
        elif LOCALE in ('ua') and t in UkrainianStrings:
            return UkrainianStrings[t]
        elif LOCALE in ('es') and t in SpanishStrings:
            return SpanishStrings[t]
        elif LOCALE in ('tr') and t in TurkishStrings:
            return TurkishStrings[t]
        elif LOCALE in ('id') and t in IndonesianStrings:
            return IndonesianStrings[t]
        elif LOCALE in ('it') and t in ItalianStrings:
            return IndonesianStrings[t]
        else:
            if t in EnglishStrings:
                return EnglishStrings[t]
            else:
                return t
    elif show_none:
        if t in EnglishStrings:
            return EnglishStrings[t]
        else:
            return t



def tld_help(chat_id, t):
    LANGUAGE = prev_locale(chat_id)
    print("tld_help ", chat_id, t)
    if LANGUAGE:
        LOCALE = LANGUAGE.locale_name

        t = t + "_help"

        print("Test2", t)

        if LOCALE in ('ru') and t in RussianStrings:
            return RussianStrings[t]
        elif LOCALE in ('ua') and t in UkrainianStrings:
            return UkrainianStrings[t]
        elif LOCALE in ('es') and t in SpanishStrings:
            return SpanishStrings[t]
        elif LOCALE in ('tr') and t in TurkishStrings:
            return TurkishStrings[t]
        elif LOCALE in ('id') and t in IndonesianStrings:
            return IndonesianStrings[t]
        elif LOCALE in ('it') and t in ItalianStrings:
            return IndonesianStrings[t]
        else:
            return False
    else:
        return False
