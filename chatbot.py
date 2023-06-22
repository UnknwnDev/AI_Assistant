from transformers import AutoTokenizer, AutoModelWithLMHead
import torch
from dataclasses import dataclass
from skills import factory
from ai import AI


tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-medium')
model = AutoModelWithLMHead.from_pretrained('microsoft/DialoGPT-medium')

class ChatBot:
	def __init__(self):
		self.chat_history_ids = None
		self.bot_input_ids = None


	def chat(self, message, ai:AI):
		for step in range(1):
			# encode the new user input, add the eos_token and return a tensor in Pytorch
			new_user_input_ids = tokenizer.encode(message + tokenizer.eos_token, return_tensors='pt')
			# print(new_user_input_ids)

			# append the new user input tokens to the chat history
			self.bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

			# generated a response while limiting the total chat history to 1000 tokens, 
			self.chat_history_ids = model.generate(
					self.bot_input_ids, max_length=2048,
					pad_token_id=tokenizer.eos_token_id,  
					no_repeat_ngram_size=3,       
					do_sample=True, 
					top_k=100, 
					top_p=0.7,
					temperature = 0.9
			)
			
			# pretty print last ouput tokens from bot
			sentence = tokenizer.decode(self.chat_history_ids[:, self.bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
			print("="*50)
			print(f"Chatbot Heard {message}")
			ai.say(sentence)
			print(f"AI: {sentence}")
			print("="*50)
			