from googletrans import Translator

def translate(text):
    translator=Translator()
    translation=translator.translate(text,src='en',dest='sl')
    return(translation.text)

if __name__=='__main__':
    translate("Hello")