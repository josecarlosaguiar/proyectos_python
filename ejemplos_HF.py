from transformers import pipeline

classificator = pipeline("token-classification", model="dslim/bert-base-NER")
result = classificator("La mejor manera de nadar mariposa es hacer primero el delfín. Luego hacer ejercicios de técnica específica")

print(result)