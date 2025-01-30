import evaluate

meteor = evaluate.load('meteor')
predictions = ["It is a guide to action which ensures that the military always obeys the commands of the party"]
reference = ["It is a guide to action which ensures that the military always obeys the commands of the party"]
results = meteor.compute(predictions=predictions, references=reference)
print(round(results['meteor'], 2))
