import argparse
import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv('OPENAI_API_KEY'),
)

def convert_code(language, file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        code = file.read()

    chat_completion = client.chat.completions.create(
      messages=[
        {
          "role": "system",
          "content": "You are a code converter.  You will receive messages with the target language on the first line followed by a chunk of code.  You should repsond with the translated code without any markdown block or explanations.  If a hash bang #! is appropriate. add one"
        },
        {
          "role": "user",
          "content": f"{language}\n\n{code}",
        }
      ],
      model="gpt-3.5-turbo",
    )

    # Get the generated code without markup
    generated_code = chat_completion.choices[0].message.content.strip()

    # Write the generated code to a new file
    file_name = os.path.basename(file_path)
    new_file_path = f"{os.path.splitext(file_name)[0]}.new"
    with open(new_file_path, 'w') as new_file:
        new_file.write(generated_code)

    print(f"Conversion completed. Generated code written to {new_file_path}")

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Convert code using OpenAI Codex')
    parser.add_argument('language', help='Target programming language')
    parser.add_argument('file_path', help='Path to the file to be converted')
    args = parser.parse_args()

    # Perform conversion
    convert_code(args.language, args.file_path)

