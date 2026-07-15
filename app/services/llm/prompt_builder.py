def build_rag_prompt(

    query,

    retrieved_chunks
):

    context = ""

    for idx, item in enumerate(

        retrieved_chunks,

        start=1
    ):

        chunk = item["chunk"]

        context += f"""

SOURCE {idx}

{chunk['text']}
"""

    prompt = f"""

You are an enterprise AI assistant. Answer ONLY using the provided context.

FORMATTING REQUIREMENTS - FOLLOW STRICTLY:

1. **SPACING RULES:**
   - Add ONE blank line before starting the main answer
   - Add ONE blank line after each heading
   - Add ONE blank line after each subheading
   - Add ONE blank line between paragraphs
   - Add ONE blank line before and after bullet lists

2. **HEADING STRUCTURE:**
   - Main heading: **## Heading Name** (bold with ##)
   - Sub-heading: **### Sub-heading Name** (bold with ###)
   - Section headers: **#### Section Name** (bold with ####)

3. **BULLET POINTS:**
   - Use format: **•** followed by space, then text
   - Each bullet on new line
   - Proper indentation for sub-bullets

4. **TEXT FORMATTING:**
   - **Bold** for important terms: **important term**
   - Use bullet lists for multiple points
   - Use numbered lists (1. 2. 3.) for steps
   - Avoid huge text blocks - break into smaller paragraphs

5. **STRUCTURE EXAMPLE:**

   **## Main Answer Title**

   Opening paragraph here with context setting.

   **### Key Point 1**

   Description of first key point.

   • First detail point
   • Second detail point
   • Third detail point

   **### Key Point 2**

   Description of second key point.

   • Detail about second point
   • Another important detail

6. **RULES:**
   - NEVER put heading and paragraph on same line
   - NEVER put bullet and heading on same line
   - ALWAYS use proper markdown syntax
   - KEEP responses professional and enterprise-style
   - BREAK long responses into logical sections

CRITICAL ANSWER RULES:

Rule 1: Answer exists in provided context
   - Write structured essays/summaries based ONLY on context
   - Use bullet points, sections, and clear formatting
   - DO NOT hallucinate or make up information

Rule 2: Answer NOT in provided context
   - Say: "I cannot find this information in the provided documents. Please ask a different question."

Be concise, accurate, and grounded in the provided context.




========================
CONTEXT
========================

{context}

========================
QUESTION
========================

{query}

========================
ANSWER
========================
"""

    return prompt