from transformers import GPTNeoXForCausalLM, AutoTokenizer, BitsAndBytesConfig, AutoModelForCausalLM
import torch

tokenizer = AutoTokenizer.from_pretrained('gpt2')
model = AutoModelForCausalLM.from_pretrained("gpt2")


message = '<|prompter|> hello<|endoftext|><|assistant|>'

inputs = inputs = tokenizer(message, return_tensors = 'pt').to(model.device)
tokens = model.generate(**inputs, max_new_tokens = 150, do_sample = True, temperature = .6)
print(tokenizer.decode(tokens[0]))