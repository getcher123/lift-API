import spacy
import re

class TextProcessor:
    def __init__(self):
#       self.nlp = spacy.load('ru_core_news_sm')
        self.linking_words = ['состоит в том что', 'в том что', 'заключается в том что', 'в том что', 'во-первых', 'во-вторых', 'в-третьих', 'в связи с этим', 'в этой связи', 'дело в том что', 'хороший вопрос', 'соглашусь', 'согласен', 'вами что',
                         'в результате', 'в итоге', 'следовательно', 'следовало', 'по сравнению с', 'в отличие от', 'главное', 'с моей стороны', 'могу вас уверить', 'в вашем случае',
                         'как следует', 'в соответствии с', 'вместе с тем', 'как раз', 'тем не менее', 'это позволяет', 'не стоит беспокоиться', 'нечего беспокоиться', 
                         'это позволит', 'на мой взгляд', 'по моему мнению', 'я считаю', 'я вам говорю', 'судя по всему',  'в данной ситуации', 'поверьте',  'могу вас уверить что', 'решайте сами']

    def remove_linking_words(self, text):
        for word in self.linking_words:
            text = text.replace(word, '')
        return text

    def normalize(self, text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def remove_stop_words(self, text):
        text = self.remove_linking_words(self.normalize(text))
        doc = self.nlp(text)
        words = []
        for token in doc:
             if not token.ent_type_ == 'PER' \
             and not token.is_stop \
             and token.is_alpha \
             and not token.pos_ == 'ADP' \
             or token.text in ['не', 'сколько', 'кто', 'что', 'где', 'когда', 'почему', 'зачем', 'как', 'какой', 'какое', 'какая', 'какое', 'какого', 'какие', 'каких']  :
                words.append(token.text)

        return " ".join(words)