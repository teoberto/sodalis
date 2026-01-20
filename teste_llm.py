from llm import generate_response

user_prompt = "Olá! Só de boa?"
system_prompt = "Você é uma puépera que teve um filho há menos um dia, está cansada e ansiosa para casa. Você está grossa e impaciente.."

response = generate_response(user_prompt, system_prompt)
print("Response:", response)