# Line Chatbot with OpenAI API
The project is a Line bot application integrated with the OpenAI API. It is designed to accompany my girlfriend while I am serving in the mandatory military service in Taiwan (R.O.C).
- The project involves fine-tuning a GPT-3.5-Turbo model to simulate my chatting style.
## Environment
### Setting up an Anaconda Environment in Ubuntu 20.04
- Create a conda env
    ```
    conda create -n bot python==3.8
    conda activate bot
    pip install -r requirements
    ```
- Set the env variable, the api key need to obtain from Linebot and OpenAI official website
    ```
    export LINE_CHANNEL_ACCESS_TOKEN={LINE_CHANNEL_ACCESS_TOKEN}
    export LINE_CHANNEL_SECRET={LINE_CHANNEL_SECRET}
    export OPENAI_API_KEY={OPENAI_API_KEY}
    ```
- Test `app.py` is working w/o errors.
    ```
    python app.py
    ```
### Setting up Nginx and TLS certification
- Install nginx
    ```
    sudo apt update
    sudo apt install nginx openssl
    ```
- Install certbot for TLS (https)
    ```
    sudo apt install certbot python3-certbot-nginx
    ```
- Set the `location` below `# Default server configuration as follows:
    ```
    server_name {your domain name}
    location / {
            proxy_pass http://127.0.0.1:8082;
            proxy_set_header Host $host;
        }
    ```
- Set the server ip to your domain (Google Domains, etc.)
- `sudo certbot -d {your domain name}`
- Modify the nginx configuration
    ```
    sudo vim /etc/nginx/site-enabled/default
    ```

- Reload nginx: `sudo nginx -t && sudo nginx -s reload`

## Fine-tune an OpenAI Model
- Create training file `mydata.jsonl` which follow the format described from [example-format](https://platform.openai.com/docs/guides/fine-tuning/example-format)
- Run `data_formatting.py` which is provided by OpenAI to valid the training file
- The result looks like as follows:
    ```bash
    No errors found                                                 
    Num examples missing system message: 0                                                                                                                                                         
    Num examples missing user message: 0                                                                                                                                                           

    #### Distribution of num_messages_per_example:
    min / max: 3, 5
    mean / median: 3.3035714285714284, 3.0
    p5 / p95: 3.0, 5.0

    #### Distribution of num_total_tokens_per_example:
    min / max: 181, 280
    mean / median: 216.23214285714286, 214.0
    p5 / p95: 190.0, 248.5

    #### Distribution of num_assistant_tokens_per_example:
    min / max: 4, 75
    mean / median: 23.714285714285715, 21.0
    p5 / p95: 9.0, 44.5

    0 examples may be over the 4096 token limit, they will be truncated during fine-tuning
    Dataset has ~12109 tokens that will be charged for during training
    By default, you'll train for 3 epochs on this dataset
    By default, you'll be charged for ~36327 tokens
    See pricing page to estimate total costs
    ```
- RUN `finetune.py`
## Specify the Model on `app.py`
- We can use the `gpt-3.5-turbo` which is provided by OpenAI official as default or ours fine-tuned model.
    ```python
    # L: 15
    model = 'gpt-3.5-turbo'
    ```
## Execute the LineBot client
- RUN `app.py`