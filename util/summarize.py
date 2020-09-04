from transformers import BartTokenizer, BartForConditionalGeneration
import torch
import time

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}")

# Load Model
pretrained = "sshleifer/distilbart-xsum-12-6"
model = BartForConditionalGeneration.from_pretrained(pretrained)
tokenizer = BartTokenizer.from_pretrained(pretrained)

# Switch to cuda, eval mode, and FP16 for faster inference
if device == "cuda":
    model = model.half()
model.to(device)
model.eval()


class Summarize:

    def __init__(self, original_text, max_len=500, num_beams=10):
        """
        Extract convert text to sound
        """
        self._original_text = original_text
        self._max_len = max_len
        self._num_beams = num_beams

    def summarize_text(self):

        if self._original_text is None or self._original_text == "":
            return "", "Did not run"

        t0 = time.time()

        inputs = tokenizer.batch_encode_plus(
            [self._original_text], max_length=1024, return_tensors="pt"
        )
        inputs = inputs.to(device)

        # Generate Summary
        summary_ids = model.generate(
            inputs["input_ids"],
            num_beams=self._num_beams,
            max_length=self._max_len,
            early_stopping=True,
        )
        out = [
            tokenizer.decode(
                g, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )
            for g in summary_ids
        ]

        t1 = time.time()
        time_taken = f"Summarized on {device} in {t1-t0:.2f}s"

        return out[0], time_taken


if __name__ == '__main__':

    from text_toolkit.url2text.url2text import Url2Text

    url = "https://www.cdc.gov/healthypets/diseases/cat-scratch.html"
    print(url)

    extractText = Url2Text(url)
    title, text = extractText.extract_text_from_html()

    print(title)
    #print(sentences)
    print(text)

    #print(sentences[0])

    ts, _ = Summarize(original_text=text)

    print(ts.summarize_text())
