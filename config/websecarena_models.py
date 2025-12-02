from agentlab.llm.chat_api import SelfHostedModelArgs


WEBSECARENA_LLAMA = SelfHostedModelArgs(
    model_name="meta-llama/Llama-3.1-8B-Instruct",
    model_url="meta-llama/Llama-3.1-8B-Instruct",
    max_total_tokens=16_384,
    max_input_tokens=16_384 - 512,
    max_new_tokens=512,
    backend="huggingface",
    # provider="novita"
)

WEBSECARENA_QWEN = SelfHostedModelArgs(
    model_name="Qwen/Qwen2.5-7B-Instruct",
    model_url="Qwen/Qwen2.5-7B-Instruct",
    max_total_tokens=16_384,
    max_input_tokens=16_384 - 512,
    max_new_tokens=512,
    backend="huggingface",
)

WEBSECARENA_OPENAI = SelfHostedModelArgs(
    model_name="openai/gpt-oss-20b",
    model_url="openai/gpt-oss-20b",
    max_total_tokens=16_384,
    max_input_tokens=16_384 - 512,
    max_new_tokens=512,
    backend="huggingface",
    # provider="novita"
)

WEBSECARENA_MISTRALAI = SelfHostedModelArgs(
    model_name="mistralai/Mistral-7B-Instruct-v0.2",
    model_url="mistralai/Mistral-7B-Instruct-v0.2",
    max_total_tokens=16_384,
    max_input_tokens=16_384 - 512,
    max_new_tokens=512,
    backend="huggingface",
)

WEBSECARENA_DEEPSEEK = SelfHostedModelArgs(
    model_name="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    model_url="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    max_total_tokens=16_384,
    max_input_tokens=16_384 - 512,
    max_new_tokens=512,
    backend="huggingface",
)