# Take home

In order to run, build the docker image as follows: 

```
docker build . -t [YOUR TAG NAME]
```

To run: 
```
doocker run -p 3000:3000 [YOUR TAG NAME]
```

Make an http request to `0.0.0.0:3000` as: 
```
{"clinical_note": "[YOUR CLINICAL NOTE HERE]"}
```

Decisions: 
* Used Llama 3, needed an LLM that could tak prompts to specify a task and output nature.
    * Output nature is a json blob which can be parsed and sent back to the user.
* Used FastAPI since I am not familiar with VLLM, fastapi is slick and low overhead, making the api layer creation fairly easy.
