"""
faq_data.py
25 curated FAQs on Generative AI & Large Language Models
"""

FAQS = [
    (
        "What is a large language model or LLM?",
        "A Large Language Model (LLM) is a deep learning model trained on massive text corpora "
        "to understand and generate human-like language. Examples include GPT-4, Claude, Gemini, "
        "and LLaMA. They use the Transformer architecture and are trained with next-token prediction."
    ),
    (
        "What is generative AI?",
        "Generative AI refers to AI systems that can create new content — text, images, audio, "
        "code, or video — rather than just classifying or analysing existing data. LLMs, diffusion "
        "models (Stable Diffusion, DALL·E), and music generators all fall under generative AI."
    ),
    (
        "What is the transformer architecture?",
        "The Transformer is a neural network architecture introduced in the paper 'Attention Is All "
        "You Need' (2017). It replaces recurrence with self-attention, enabling parallel processing "
        "of sequences. It consists of encoder and decoder stacks, each with multi-head attention "
        "layers and feed-forward networks."
    ),
    (
        "How does attention mechanism work?",
        "Attention allows the model to weigh how relevant each token in the input is to every other "
        "token. In self-attention, each token computes a Query, Key, and Value vector. The dot "
        "product of Q and K gives attention scores, which are softmaxed and used to weight the V "
        "vectors. Multi-head attention runs this in parallel across multiple subspaces."
    ),
    (
        "What is hallucination in AI or LLM hallucination?",
        "Hallucination refers to when an LLM generates text that is factually incorrect, made-up, "
        "or nonsensical, yet sounds confident and plausible. This happens because the model "
        "optimises for fluent, coherent text rather than factual accuracy. Techniques like RAG, "
        "RLHF, and grounding help reduce hallucinations."
    ),
    (
        "What is RAG or retrieval augmented generation?",
        "Retrieval-Augmented Generation (RAG) is a technique where the LLM retrieves relevant "
        "documents from an external knowledge base at inference time before generating a response. "
        "This grounds the model's output in verified facts, reducing hallucination and keeping "
        "knowledge up-to-date without retraining."
    ),
    (
        "What is fine-tuning an LLM?",
        "Fine-tuning is the process of further training a pre-trained LLM on a smaller, task-specific "
        "dataset to adapt it for a particular use case (e.g., customer support, medical Q&A). "
        "Techniques include full fine-tuning, LoRA (Low-Rank Adaptation), QLoRA, and instruction "
        "fine-tuning."
    ),
    (
        "What is prompt engineering?",
        "Prompt engineering is the practice of crafting input prompts to guide an LLM towards "
        "desired outputs. Techniques include zero-shot prompting, few-shot prompting (giving "
        "examples), chain-of-thought (asking the model to reason step by step), and ReAct "
        "(combining reasoning with action)."
    ),
    (
        "What is RLHF or reinforcement learning from human feedback?",
        "RLHF is a training technique where human raters rank model outputs, and those preferences "
        "train a reward model. The LLM is then fine-tuned using reinforcement learning (typically "
        "PPO) to maximise the reward. This aligns the model's outputs with human preferences and "
        "safety guidelines. Used by ChatGPT and Claude."
    ),
    (
        "What are embeddings in NLP or AI?",
        "Embeddings are dense vector representations of tokens, words, or sentences in a "
        "high-dimensional space. Semantically similar items are placed close together. LLMs use "
        "embeddings internally; they are also used externally for semantic search, clustering, "
        "and RAG pipelines. Popular embedding models include OpenAI's text-embedding-ada-002 "
        "and Sentence-BERT."
    ),
    (
        "What is the difference between GPT and BERT?",
        "GPT (Generative Pre-trained Transformer) is a decoder-only model trained with causal "
        "language modelling — it predicts the next token, making it ideal for text generation. "
        "BERT (Bidirectional Encoder Representations from Transformers) is an encoder-only model "
        "trained with masked language modelling, making it ideal for classification and "
        "understanding tasks."
    ),
    (
        "What is tokenisation in LLMs?",
        "Tokenisation splits text into smaller units called tokens before feeding it into an LLM. "
        "Tokens can be words, subwords, or characters. Most modern LLMs use Byte-Pair Encoding "
        "(BPE) or SentencePiece. GPT-4 uses ~100K tokens in its vocabulary. Tokenisation affects "
        "context window usage and cost."
    ),
    (
        "What is a context window or context length?",
        "The context window is the maximum number of tokens an LLM can process in a single "
        "inference call (input + output combined). GPT-4 supports up to 128K tokens; Claude 3 "
        "supports up to 200K. Longer context windows allow models to handle entire books, long "
        "codebases, or extended conversations."
    ),
    (
        "What is temperature in LLM generation?",
        "Temperature is a sampling parameter that controls the randomness of an LLM's output. "
        "A temperature of 0 makes the model deterministic (always picks the highest probability "
        "token). Higher temperatures (e.g. 0.8–1.0) increase diversity and creativity but may "
        "reduce coherence. Top-p (nucleus) sampling is a related technique."
    ),
    (
        "What is a vector database and how is it used in AI?",
        "A vector database stores and indexes high-dimensional embedding vectors, enabling fast "
        "approximate nearest-neighbour (ANN) search. It is a core component in RAG pipelines — "
        "documents are embedded and stored; at query time, the question embedding is compared "
        "against stored vectors to retrieve the most relevant chunks. Examples: Pinecone, Weaviate, "
        "Chroma, FAISS."
    ),
    (
        "What is zero-shot and few-shot learning?",
        "Zero-shot learning means asking the model to perform a task without any examples — "
        "relying purely on its pre-trained knowledge. Few-shot learning includes a small number "
        "of input-output examples in the prompt to guide the model. Few-shot typically improves "
        "accuracy on specialised tasks without any weight updates."
    ),
    (
        "What are AI agents or LLM agents?",
        "LLM agents are systems where the language model acts as a reasoning engine that can "
        "plan and take actions — calling tools (APIs, web search, code execution), reading/writing "
        "files, and iterating until a goal is reached. Frameworks include LangChain, AutoGPT, "
        "CrewAI, and Anthropic's Claude with tool use."
    ),
    (
        "What is LoRA or low-rank adaptation?",
        "LoRA (Low-Rank Adaptation) is a parameter-efficient fine-tuning method. Instead of "
        "updating all billions of model weights, it injects small trainable rank-decomposition "
        "matrices into each layer. This drastically reduces memory and compute requirements "
        "while achieving performance comparable to full fine-tuning. QLoRA adds 4-bit "
        "quantisation on top."
    ),
    (
        "What is the difference between open source and closed source LLMs?",
        "Closed-source LLMs (GPT-4, Claude, Gemini) are proprietary — you access them via API "
        "and cannot see or modify weights. Open-source LLMs (LLaMA 3, Mistral, Falcon, Gemma) "
        "release weights publicly, allowing local deployment, fine-tuning, and research. "
        "Open-source models have rapidly closed the quality gap with proprietary ones."
    ),
    (
        "What is multimodal AI?",
        "Multimodal AI models can process and generate multiple types of data — text, images, "
        "audio, and video — in a single model. Examples include GPT-4o, Claude 3 (text + vision), "
        "and Gemini Ultra. Multimodal models use separate encoders for each modality whose "
        "representations are fused before the language decoder."
    ),
    (
        "What is the difference between inference and training in LLMs?",
        "Training is the process of learning weights from data using gradient descent — it is "
        "computationally intensive and done once (or periodically). Inference is using the trained "
        "model to generate responses — it is much cheaper and happens in real time for each user "
        "query. Most LLM deployments focus on optimising inference cost and latency."
    ),
    (
        "What is quantisation in LLMs?",
        "Quantisation reduces the numerical precision of model weights from 32-bit or 16-bit "
        "floating point down to 8-bit integers or lower (GGUF 4-bit). This shrinks model size "
        "and speeds up inference with minimal quality loss. Tools like llama.cpp and bitsandbytes "
        "enable running quantised LLMs on consumer hardware."
    ),
    (
        "What is chain of thought prompting?",
        "Chain-of-Thought (CoT) prompting asks the LLM to reason step by step before giving a "
        "final answer. This significantly improves performance on multi-step reasoning tasks "
        "(maths, logic, code). Zero-shot CoT adds 'Let's think step by step' to the prompt; "
        "few-shot CoT provides worked examples."
    ),
    (
        "What is system prompt or system message in LLMs?",
        "A system prompt is a special instruction given to an LLM before the conversation begins "
        "that sets its behaviour, persona, tone, and constraints. It is invisible to the end user "
        "but shapes all subsequent responses. Operators use system prompts to customise LLM "
        "products (e.g., 'You are a helpful customer service assistant for Acme Corp.')."
    ),
    (
        "What is constitutional AI or CAI?",
        "Constitutional AI (CAI) is Anthropic's technique for training helpful, harmless, and "
        "honest models. Instead of relying solely on human labels, a set of principles (the "
        "'constitution') guides a model to critique and revise its own outputs. This scales "
        "alignment supervision and is used to train the Claude model family."
    ),
]
