from textblob import TextBlob

str = "whaat ixs yoor nami"

new_doc = TextBlob(str)
result = new_doc.correct()
print(result)