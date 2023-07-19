import openai

with open('hidden.txt') as file:                            #we connect to openai API
    openai.api_key = file.read()

def get_api_response(prompt: str) -> str | None:
    text: str | None = None

    try:
        response: dict = openai.Completion.create(          #ChatGPT model for our chatbot
            model = 'gpt-3.5-turbo',
            prompt = prompt,
            temperature = 0.9,
            max_tokens = 150,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0.6,
            stop = [' Human:', ' AI:']
        )
        
        choices: dict = response.get('choices')[0]          #as a response ChatGPT returns a json object with some additional info
        text = choices.get('text')                          #and we need to extract only the response sentence

    except Exception as e:
        print('ERROR:', e)

    return text

def update_list(message: str, pl: list[str]):               #we create a chat history
    pl.append(message)

def create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt

def get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
        pos: int = bot_response.find('\nAI: ')
        bot_response = bot_response[pos + 5:]
    else:
        bot_response = 'Something wrong..........'

    return bot_response\
    
def main():
    prompt_list: list[str] = ['You will pretend to be a rapper that ends every response with "yo"',
                              '\nHuman: What time is it?',
                              '\nAI: It is 12:00, yo']

    while True:
        user_input = input('You: ')
        response = get_bot_response(user_input, prompt_list)
        print(f'Bot: {response}')

if __name__ == '__main__':
    main()