from flask import Flask, render_template, request, redirect
import random
import csv

app = Flask(__name__)

class VocabularyApp:
    def __init__(self):
        self.vocab = {}
        self.filename = 'vocab.csv'  # CSV file to store the vocabulary
        self.load_vocab()

    def load_vocab(self):
        try:
            with open(self.filename, 'r') as file:
                reader = csv.reader(file)
                self.vocab = {row[0]: row[1] for row in reader}
        except FileNotFoundError:
            # If the file doesn't exist, create an empty dictionary
            self.vocab = {}

    def save_vocab(self):
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for word, meaning in self.vocab.items():
                writer.writerow([word, meaning])

    def add_word(self, word, meaning):
        self.vocab[word] = meaning
        self.save_vocab()

app_instance = VocabularyApp()

@app.route('/')
def home():
    return render_template('index.html', words=app_instance.vocab.values())

@app.route('/add', methods=['POST'])
def add_word():
    word = request.form['word']
    meaning = request.form['meaning']
    app_instance.add_word(word, meaning)
    return redirect('/')

@app.route('/quiz', methods=['GET', 'POST'])
def start_quiz():
    if not app_instance.vocab:
        return "No words available for quiz. Please add words first."

    if request.method == 'POST':
        words = random.sample(list(app_instance.vocab.keys()), 3)
        score = 0
        total = len(words)

        for word in words:
            meaning = app_instance.vocab[word]
            user_input = request.form.get(word, '')
            if user_input.lower() == meaning.lower():
                score += 1

        return f"Quiz complete! You scored {score}/{total}."

    words = list(app_instance.vocab.keys())
    random.shuffle(words)
    return render_template('quiz.html', words=words[:3])


if __name__ == '__main__':
    app.run(debug=True)
