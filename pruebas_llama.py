from ctransformers import AutoModelForCausalLM

llm = AutoModelForCausalLM.from_pretrained(r"C:\Users\es44319413t\Downloads\codellama-7b.Q3_K_S.gguf",
                                           model_type="llama",
                                           temperature=0.1,
                                           top_p=0.1,
                                           max_new_tokens=52)
output = llm("Cuál es el ciclo de un motor de combustión?")
print(output)