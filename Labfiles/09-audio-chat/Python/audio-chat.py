import os

# Add references
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.inference.models import SystemMessage, UserMessage, TextContentItem

def main(): 

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')
        
    try: 
    
        # Get configuration settings 
        load_dotenv()
        project_connection = os.getenv("PROJECT_ENDPOINT")
        model_deployment =  os.getenv("MODEL_DEPLOYMENT")
        
        # Initialize the project client
        project_client = AIProjectClient(
            credential=DefaultAzureCredential(
                exclude_environment_credential=True,
                exclude_managed_identity_credential=True
            ),
            endpoint=project_connection,
        )

        ## Get a chat client
        chat_client = project_client.inference.get_chat_completions_client()

        # Initialize prompts
        system_message = "You are an AI assistant for a produce supplier company."
        prompt = ""

        # Loop until the user types 'quit'
        while True:
            prompt = input("\nAsk a question about the audio\n(or type 'quit' to exit)\n")
            if prompt.lower() == "quit":
                break
            elif len(prompt) == 0:
                    print("Please enter a question.\n")
            else:
                print("Getting a response ...\n")


                # Get a response to audio input
                file_path = "https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Labfiles/09-audio-chat/data/avocados.mp3"
                response = chat_client.complete(
                    model=model_deployment,
                    messages=[
                        SystemMessage(system_message),
                        UserMessage(
                            [
                                TextContentItem(text=prompt),
                                {
                                    "type": "audio_url",
                                    "audio_url": {"url": file_path}
                                }
                            ]
                        )
                    ]
                )
                print(response.choices[0].message.content)

    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()
