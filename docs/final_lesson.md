# Introduction to RAG  
*(Retrieval‑Augmented Generation)*  

---

## Learning Objectives  

By the end of this lesson you will be able to:  

1. Say what **RAG** means.  
2. Explain why RAG is useful.  
3. Describe the basic steps of a RAG system.  
4. Follow a simple, real‑life example of RAG in action.  
5. Recognise key terms and avoid common mistakes.

---

## 1. What is RAG?  

**RAG** stands for **Retrieval‑Augmented Generation**.  
It is a way for a computer to answer questions **by first looking up** (retrieving) information from a large collection of texts, and then **writing** (generating) a response using that information.  

Think of a student who first opens a textbook to find the relevant page, reads it, and then writes an answer in his own words. RAG does the same, but the “student” is an AI model.

---

## 2. Why does RAG matter?  

- **Up‑to‑date answers** – The AI can use the latest facts stored in a document set, instead of relying only on what it learned during training.  
- **More accurate answers** – By checking a source, the AI reduces the chance of making things up (called *hallucination*).  
- **Handles many topics** – The AI can answer questions about anything that exists in the document collection, even if it never saw that topic before.

**Problem it solves:**  
A plain language model may say “I don’t know” or give wrong information. RAG adds a “search step” so the answer is grounded in real text.

---

## 3. How RAG works – Step‑by‑step  

| Step | What happens | Simple picture |
|------|--------------|----------------|
| **1. User asks a question** | The learner types a query, e.g., “How to make masala chai?” | 🗣️ |
| **2. Retrieval** | The system searches a **knowledge base** (a set of documents) for pieces that match the query. | 🔍 |
| **3. Ranking** | The found pieces are ordered by relevance; the top few are kept. | 📊 |
| **4. Generation** | A **language model** (the AI that writes text) receives the retrieved pieces and the original question, then creates a final answer. | ✍️ |
| **5. Output** | The answer is shown to the user. | 📄 |

*Note:* Steps 2‑4 happen automatically and very fast.

---

## 4. Practical Example – “How to make masala chai?”  

Assume we have a small knowledge base that contains three PDFs:  

1. **Recipe‑book.pdf** – many Indian drink recipes.  
2. **Health‑tips.pdf** – benefits of tea.  
3. **Shop‑list.pdf** – common grocery items.

### Step‑by‑step walk‑through  

1. **User query** – You type: *“How to make masala chai?”*  

2. **Retrieval** –  
   * The system looks for the words *masala* and *chai* in all PDFs.  
   * It finds a paragraph in **Recipe‑book.pdf** that lists spices, water, milk, and tea leaves.  

3. **Ranking** –  
   * The paragraph from the recipe book is most relevant, so it is selected.  
   * A short note from **Health‑tips.pdf** about ginger’s benefits is also kept (it adds useful info).  

4. **Generation** –  
   * The language model receives three pieces of text: the recipe paragraph, the health note, and the original question.  
   * It writes a clear answer:  

   > “To make masala chai, boil 1 cup of water with ½ tsp each of cardamom, cinnamon, cloves, and a small piece of ginger. Add 1 tsp black tea leaves and let it simmer for 2 minutes. Then add 1 cup milk and 2 tsp sugar (optional). Bring to a boil once more, strain, and serve hot. Ginger helps digestion, so the chai is also good for your stomach.”  

5. **Output** – The answer appears on your screen.  

You now have a complete, sourced answer that combines the recipe and a health tip.

---

## 5. Glossary  

| Term | Simple definition |
|------|-------------------|
| **Retrieval** | Searching a collection of texts to find pieces that match a query. |
| **Generation** | The AI writing new sentences based on the retrieved pieces. |
| **Language model** | A computer program that can produce human‑like text (e.g., ChatGPT). |
| **Knowledge base** | The set of documents, PDFs, web pages, or databases the system can search. |
| **Prompt** | The text (question or instruction) you give to the AI. |
| **Hallucination** | When an AI makes up information that is not true. |
| **Ranking** | Ordering the retrieved pieces so the most useful ones come first. |
| **Chunk** | A small piece of a larger document, often a paragraph or a few sentences. |

---

## 6. Common Misunderstandings & Limitations  

| Misunderstanding | Reality |
|------------------|---------|
| *RAG always gives the correct answer.* | RAG improves accuracy, but if the knowledge base has wrong or outdated info, the answer will inherit those errors. |
| *The AI “reads” the whole internet each time.* | Retrieval only looks at the documents you have given it. It does not browse the live web unless you connect it to a web search tool. |
| *RAG replaces the need for a language model.* | The generation step still needs a language model; retrieval only supplies data. |
| *All retrieved text is shown to the user.* | Usually the user only sees the final generated answer, not the raw chunks. |
| *RAG works instantly for huge collections.* | Searching very large collections can be slower; efficient indexing is required. |

---

## 7. Quick Recap  

- **RAG = Retrieval‑Augmented Generation**.  
- It first **searches** for relevant text, then **writes** an answer using that text.  
- The method gives more up‑to‑date and reliable answers.  
- Steps: ask → retrieve → rank → generate → show.  
- Example: finding a chai recipe from a PDF and turning it into a clear answer.  

---

## 8. Knowledge‑Check Questions  

1. **What does the “R” in RAG stand for?**  
   *Answer:* Retrieval – searching for relevant information.  

2. **Why is a language model still needed after retrieval?**  
   *Answer:* To combine the retrieved pieces and write a fluent, natural answer.  

3. **If the knowledge base contains an old recipe, will RAG automatically update it?**  
   *Answer:* No. RAG can only use what is in the knowledge base; outdated data will stay outdated unless the base is refreshed.  

4. **Name one common problem that RAG helps reduce.**  
   *Answer:* Hallucination – the AI making up false information.  

5. **In the chai example, which two documents were used?**  
   *Answer:* *Recipe‑book.pdf* (the main recipe) and *Health‑tips.pdf* (the ginger benefit note).  

--- 

*You have now completed the beginner lesson on Introduction to RAG. Keep practicing by thinking of everyday questions and imagining how a retrieval step could help an AI answer them more accurately.*