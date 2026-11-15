# Introduction to RAG  
*Retrieval‑Augmented Generation*

---

## Learning Objectives
After this lesson you will be able to:

1. Say what **RAG** means.  
2. Explain why RAG is useful.  
3. List the main steps of a RAG system.  
4. Follow a simple example that uses RAG to answer a question.  
5. Recognise common limits of RAG.

---

## 1. What is RAG?

**RAG** stands for **Retrieval‑Augmented Generation**.  
It is a way to make a language model (a computer that writes text) smarter by first **retrieving** (searching) relevant information and then **generating** (writing) an answer that uses that information.

- **Retrieval** – finding pieces of text that may contain the answer.  
- **Generation** – the language model creates a natural‑language response.

---

## 2. Why does RAG matter?

- A language model only knows what it saw during training.  
- If the model does not have recent or detailed facts, it may give a wrong answer.  
- By adding a retrieval step, RAG can use up‑to‑date documents (e.g., news, textbooks, recipes).  
- This helps solve problems like:  

  *Answering a school question about the latest Indian space mission.*  
  *Giving a correct list of ingredients for a local dish.*  

---

## 3. How RAG works – step‑by‑step

1. **User asks a question** – e.g., “What are the main ingredients of a masala dosa?”  
2. **Query is turned into a vector** – the question is converted into numbers (called an *embedding*) that capture its meaning.  
3. **Search the document store** – the system compares the query vector with vectors of many documents (recipes, articles). The most similar ones are selected.  
4. **Pass retrieved text to the language model** – the model receives both the original question and the retrieved snippets.  
5. **Model generates the answer** – it writes a response that uses the information from the snippets.  
6. **Answer is returned to the user**.

---

## 4. Practical example – “Masala Dosa ingredients”

We will walk through the steps with a simple Python‑like pseudo code.  
Assume we have a small collection of recipe texts stored in a list called `docs`.

```python
# 1. User question
question = "What are the main ingredients of a masala dosa?"

# 2. Convert question to vector (embedding)
q_vec = embed(question)          # embed() is a function that creates a numeric vector

# 3. Find similar documents
#   compare q_vec with each document vector and keep top 2
retrieved = search_similar(q_vec, docs, top_k=2)

# 4. Build prompt for the language model
prompt = f"Question: {question}\n"
prompt += "Relevant info:\n"
for d in retrieved:
    prompt += d + "\n"

# 5. Generate answer
answer = generate_text(prompt)   # generate_text() calls the language model

# 6. Show answer
print(answer)
```

### Explanation of each line

1. **question** – the text the user typed.  
2. **embed()** – turns the question into numbers that capture its meaning.  
3. **search_similar()** – looks through all stored recipes and returns the two that match best.  
4. **prompt** – a single text that contains the question and the retrieved recipe snippets.  
5. **generate_text()** – the language model reads the prompt and writes a reply.  
6. **print()** – shows the final answer, e.g.:

```
The main ingredients of a masala dosa are:
- Rice (usually parboiled)
- Urad dal (black gram)
- Fenugreek seeds (optional)
- Potatoes, onions, mustard seeds, curry leaves for the masala filling.
```

---

## 5. Glossary

| Term | Simple meaning |
|------|----------------|
| **Retrieval** | Finding relevant text from a large collection. |
| **Generation** | Writing a new answer using a language model. |
| **Language model** | A computer program that can produce human‑like text. |
| **Embedding** | A list of numbers that represents the meaning of a word or sentence. |
| **Prompt** | The text we give to the language model to tell it what to do. |
| **Document store** | A place where many pieces of text (documents) are saved. |
| **Vector similarity** | A way to measure how close two embeddings are. |
| **Top‑k** | The number of most similar documents we keep (e.g., top 2). |

---

## 6. Common misunderstandings & limitations

1. **RAG always gives the correct answer.**  
   - The answer is only as good as the retrieved documents. Wrong or outdated docs lead to wrong answers.

2. **The model creates new facts.**  
   - The model can only combine information it has seen. It cannot invent verified data.

3. **All languages work the same.**  
   - Retrieval works best when the documents are in the same language as the question. English‑only collections may miss Hindi or regional sources.

4. **Speed is not an issue.**  
   - Searching a huge document store can be slow. Efficient indexing (e.g., using FAISS) is needed for large systems.

5. **Privacy is automatic.**  
   - If user data is stored in the document store, it must be protected according to law (e.g., India’s data‑privacy rules).

---

## 7. Quick recap

- **RAG = Retrieval + Generation.**  
- Retrieval finds useful text; generation writes a fluent answer.  
- Steps: ask → embed → search → build prompt → generate → answer.  
- Example: answering a recipe question by pulling two recipe snippets and letting the model write the final list.  
- Remember the limits: quality of sources, language match, speed, and privacy.

---

## 8. Knowledge‑check questions

1. **What does the “R” in RAG stand for?**  
   *Answer: Retrieval – searching for relevant documents.*

2. **Why do we convert a question into an embedding?**  
   *Answer: To compare its meaning with the meanings of stored documents.*

3. **If the retrieved documents are outdated, what happens to the final answer?**  
   *Answer: The answer may contain outdated or wrong information.*

4. **Name one thing that a language model cannot do on its own in a RAG system.**  
   *Answer: It cannot fetch up‑to‑date facts; it needs the retrieval step.*

5. **What is a “prompt” in the context of RAG?**  
   *Answer: The combined text (question + retrieved snippets) that we give to the language model to generate an answer.*

---