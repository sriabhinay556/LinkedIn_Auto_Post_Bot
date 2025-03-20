from openai import OpenAI
from tiktoken import encoding_for_model  # tiktoken to estimate token count

def calculate_cost(num_tokens, rate_per_1k):
    """
    Calculate cost based on the number of tokens and rate per 1K tokens.
    """
    return (num_tokens / 1000) * rate_per_1k

def get_token_count(text, model):
    """
    Estimate the number of tokens for the given text using tiktoken.
    """
    enc = encoding_for_model(model)  # Get the token encoding for the model
    return len(enc.encode(text))

def generate_parser_logic(model, html_content, user_question, url, schema_instructions):
    """
    Generate parser logic for the HTML content using OpenAI and return token usage and cost.
    
    Args:
        model (str): The GPT model to use.
        html_content (str): The HTML content to parse.
        user_question (str): The user's question.
        url (str): The URL of the searched page.
        schema_instructions (str): Instructions for the schema.

    Returns:
        str: The generated parser logic in Python code.
    """
    prompt = f"""
    You are a website scraper script creator and you have just scraped the following content from a website. I will provide the scrapped HTML which is also reduced in size in the form of a string as HTML_DATA (it only has the body of the HTML). 

    Write the code in python for extracting the information requested by the user question.\n
    
    Do not dump the entire HTML in the output python code. Only include the necessary data which is required for the user question. \n 
    
    The context is provided to you which is a search URL, you can know the context of the query by looking at the search query and parameters in it.\n

    The output should be just in python code without any comment and should implement the main. \n
    
    Returned python code should be able to run without any error. No comments are required in the code. Do not wrap the output in comments or markdown like ```python. \n

    Return type should be a str and Please return the ouput string wrapped in triple quotes.\n
    
    Do not use any imports in the output python code, like json or any other imports. You can use print function to print the output or any other function which doesnt require any imports.\n

    USER QUESTION: {user_question}
    CONTEXT: {url}
    SCHEMA INSTRUCTIONS: {schema_instructions} 
    HTML_TITLE: {html_content.get("title")}
    LINKS_DATA_IN_HTML: {html_content.get("link_urls_data")}
    HTML_DATA: {html_content.get("reduced_html")}
    """

    # write the prompt to a file
    with open("prompt.txt", "w") as file:
        file.write(prompt)

    # Calculate input token count
    input_tokens = get_token_count(prompt, model)
    response_status=""

    # Ensure input tokens do not exceed the limit
    if input_tokens > 4000:
        response_status="Token limit exceeded than 4000"
        raise ValueError(f"Input token count exceeds the 4000-token limit: {input_tokens} tokens.")

    print(f"Input tokens: {input_tokens}")
    client = OpenAI()
    print("GPT working on the prompt.....")
    
    # Call the OpenAI API to generate the parser logic
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates Python code for web scraping."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000 - input_tokens,  # Ensure the output does not exceed the total limit
        n=1,
        stop=None,
        temperature=0.5,
    )
    print("GPT finished working on the prompt.....")

    parser_logic = response.choices[0].message.content
    #print("from html_parser.py this is the response type: ", type(parser_logic))
    #print("from html_parser.py this is the parser_logic: ", parser_logic)
     
    # Calculate output token count
    output_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens

    # Estimate cost based on OpenAI GPT-3.5 pricing
    input_cost = calculate_cost(input_tokens, 0.003)  # $0.003 per 1K input tokens
    output_cost = calculate_cost(output_tokens, 0.006)  # $0.006 per 1K output tokens
    total_cost = input_cost + output_cost

    # Display results
    print(f"Output tokens: {output_tokens}")
    print(f"Total tokens used: {total_tokens}")
    print(f"Estimated input cost: ${input_cost:.6f}")
    print(f"Estimated output cost: ${output_cost:.6f}")
    print(f"Estimated total cost: ${total_cost:.6f}")

    # If the output python code has ```python in the beginning or ``` in the end, remove it

# get the first line of the parser_logic
    first_line = parser_logic.split('\n')[0]
    last_line = parser_logic.split('\n')[-1]
    #print('first_line: ', first_line, 'last_line: ', last_line)
    new_str =""
    if first_line == "'''" and last_line == "'''":
        #print("inside html_parser.py")
        #Split the string into lines and copy everything from the second line onward
        lines = parser_logic.splitlines()

        # Join lines starting from the second line (index 2)
        new_str = "\n".join(lines[1:])

        lines = new_str.splitlines()

        new_str = "\n".join(lines[:-1])
        
        
        return new_str, response_status

    elif first_line == "```python" and last_line != "```":
        lines = parser_logic.splitlines()

        # Join lines starting from the second line (index 2)
        new_str = "\n".join(lines[1:])

        lines = new_str.splitlines()

        new_str = "\n".join(lines[:-1])
        
        
        return new_str, response_status
    # Return parser logic
    return parser_logic, response_status

# Example usage:
# result = generate_parser_logic('gpt-3.5-turbo', html_content, user_question, url, schema_instructions)
# print(result['parser_logic'])
