import re

def load_vocab(filename):
    eng2ps = {}
    ps2eng = {}
    with open(filename, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 3:
                ps_word, freq, eng_word = parts
                eng2ps[eng_word.lower()] = ps_word
                ps2eng[ps_word.lower()] = eng_word
    return eng2ps, ps2eng

def translate(text, vocab):
    # split words while keeping punctuation as separate tokens
    words = re.findall(r"\b\w+'\w+|\b\w+\b|[^\w\s]", text, flags=re.UNICODE)
    translated = []
    for word in words:
        lw = word.lower()
        ps_word = vocab.get(lw, word)
        if word[0].isupper() and ps_word[0].islower():
            ps_word = ps_word.capitalize()
        translated.append(ps_word)
    return ' '.join(translated)

import tkinter as tk
from tkinter import scrolledtext

def main_gui():
    eng2ps, ps2eng = load_vocab("ps.txt")
    mode = {'dir': 'eng2ps'}  # use mutable dict to allow updates in nested func

    root = tk.Tk()
    root.title("People Speak Translator")
    root.geometry("500x440")

    input_label = tk.Label(root, text="Enter English text:")
    input_label.pack(anchor='w', padx=10, pady=(10,0))
    input_text = scrolledtext.ScrolledText(root, height=6, wrap=tk.WORD)
    input_text.pack(fill=tk.BOTH, expand=False, padx=10, pady=(0,10))

    def do_translate():
        text = input_text.get("1.0", tk.END).strip()
        if mode['dir'] == 'eng2ps':
            vocab = eng2ps
        else:
            vocab = ps2eng
        result = translate(text, vocab)
        output_text.config(state='normal')
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
        output_text.config(state='disabled')

    def do_swap():
        if mode['dir'] == 'eng2ps':
            mode['dir'] = 'ps2eng'
            input_label.config(text="Enter People Speak text:")
            output_label.config(text="English:")
            translate_button.config(text="Translate to English")
        else:
            mode['dir'] = 'eng2ps'
            input_label.config(text="Enter English text:")
            output_label.config(text="People Speak:")
            translate_button.config(text="Translate to People Speak")
        # swap contents too
        orig = input_text.get("1.0", tk.END)
        output = output_text.get("1.0", tk.END)
        input_text.delete("1.0", tk.END)
        input_text.insert(tk.END, output.strip())
        output_text.config(state='normal')
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, orig.strip())
        output_text.config(state='disabled')

    swap_button = tk.Button(root, text="Swap translation direction", command=do_swap)
    swap_button.pack(pady=(0,5))
    translate_button = tk.Button(root, text="Translate to People Speak", command=do_translate)
    translate_button.pack(pady=4)

    output_label = tk.Label(root, text="People Speak:")
    output_label.pack(anchor='w', padx=10, pady=(10,0))
    output_text = scrolledtext.ScrolledText(root, height=6, wrap=tk.WORD, state='disabled')
    output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))

    root.mainloop()

if __name__ == "__main__":
    main_gui()
