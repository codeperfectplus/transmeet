# cython: language_level=3
from datetime import datetime

from transmeet.utils.json_parser import extract_json_from_text


def generate_meeting_minutes(
    transcribed_text, llm_client, model_name, meeting_datetime=None
):
    system_prompt = "You are an expert assistant responsible for drafting professional and concise meeting minutes."

    user_prompt = f"""
        Meeting Transcription: 

        {transcribed_text}

        Date & Time of Meeting: {meeting_datetime}

        Your task is to analyze the above meeting transcript and extract structured, visually rich insights using careful reasoning. You must **infer names, products, decisions, and other contextual clues logically**, even when they are not explicitly stated.

        ---

        ## 🧠 Primary Goals:
        1. **Accurate Participant Identification**  
        - Extract all participants mentioned or inferred.
        - Use chain-of-thought reasoning to resolve references like "he", "PM", "the intern", etc.

        2. **Product & Project Identification**  
        - Detect product names, abbreviations, internal tools, or code names.
        - Include inferred or indirectly mentioned tools/platforms.

        3. **Smart Inference & Contextual Understanding**  
        - Extract structured insights like roles, decisions, blockers, and tasks, even when they are implicit.

        ---

        ## 📘 Output Format

        Use rich markdown with **Tailwind-friendly structure**: proper heading hierarchy, `tables`, `lists`, `inline code`, `blockquotes`, and **clear roles and assignments**.

        Follow **this exact structure** and formatting guidance:

        ---
        ## 📝 Meeting Minutes

        - **Meeting Title**: *Title derived from the transcript or inferred context*
        - **Date & Time**: *Date and time of the meeting*
        - **Participants**: Abc, Xyz, etc. (list all participants)
        - **Meeting Type**: *Type of meeting (e.g., Standup, Retrospective, etc.)*
        - **Meeting Notes**: *Any additional notes or context*
        
        ## 📌 Agenda Topics Discussed
        - Bullet list of primary topics.
        - Break them into logical segments using `**bold**` emphasis if needed.

        ## ✅ Key Decisions Made
        - List clear decisions using bullets.
        - Use `✔️` for accepted points, `❌` for rejected ideas if context allows.

        ## 📋 Action Items

        | Task | Assignee | Deadline | Notes |
        |------|----------|----------|-------|
        | Description of task | Name or Role | Date or "TBD" | Any relevant info |

        ## 📦 Products, Projects, or Tools Mentioned

        - `ProductName` – *Brief description if needed*
        - `ToolAbbr` – *What it's used for*

        ## 📣 Important Quotes or Highlights

        > “Actual quote from participant”  
        > — **Name or Role**

        Up to 3 such quotes that are impactful, funny, or controversial.

        ## 🧠 Reasoning Behind Key Decisions (Chain of Thought)

        For each decision made, explain:

        - **Decision:** What was decided?
        - **Reasoning:** What logic, discussion, or concerns led to this?

        Repeat this format for each major decision.

        ## 📊 Risks, Concerns, or Blockers Raised

        - **Risk 1:** Description and possible impact.
        - **Concern 2:** Who raised it, and what needs resolution.

        ## 🔮 Future Considerations

        - Topics or tasks requiring follow-up.
        - Mention responsible parties and potential timelines.

        ## 💬 Feedback or Suggestions

        - Summarize participant feedback.
        - Include who said it and any follow-up steps.

        ## 😂 Funny Moments or Anecdotes(Add only if exists) otherwise don't add this section

        - A moment or quote that lightened the mood.
        - Optional emojis or reactions allowed (`😅`, `🎉`, etc.).

        ## 🎯 Meeting Summary

        > A final paragraph (3–5 sentences) summarizing:
        > - The purpose of the meeting.
        > - Key topics discussed.
        > - Major outcomes. 
        > - Next steps.

        ---

        ### ✅ Markdown & Formatting Guidelines

        - Use markdown headings (`##`, `###`, etc.) consistently.
        - Use bullet lists, bold text (`**bold**`), `inline code`, and blockquotes.
        - Use tables for clarity where needed (e.g., action items).
        - Avoid repetition or vague summaries.
        - Ensure the output is visually structured and ready for Tailwind rendering.
        """

    response = llm_client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content.strip()


def segment_conversation_by_speaker(transcribed_text, llm_client, model_name):
    system_prompt = """You are an assistant tasked with segmenting a conversation by speaker.
    Identify the speakers based on context and transitions in the dialogue. Label each speaker with a unique identifier (e.g., Speaker 1, Speaker 2, Speaker 3, etc.) 
    and clearly divide the conversation between them. Make sure the segmentation respects the flow of the conversation and clearly marks speaker changes."""

    user_prompt = f"""
        You are given a raw transcript of a multi-speaker conversation with no speaker labels or punctuation-based cues.

        Your task is to:
        1. Segment the transcript by identifying changes in speaker based on context, tone, and content.
        2. Clearly label each part using generic identifiers like Speaker 1, Speaker 2, etc.
        3. Maintain the natural flow of conversation.
        4. If a speaker talks multiple times, reuse their label (do not assign a new number each time).
        5. Do not add any additional commentary or explanations, just the segmented dialogue.
        6. Ensure the output is formatted as a dialogue with clear speaker labels.
        7. Identify the leading speaker based on the context of the conversation and label them as Speaker 1.

        Format your output as follows:

        Speaker 1: [First speaker's dialogue]  
        Speaker 2: [Next speaker's dialogue]  
        Speaker 1: [Speaker 1 again if they speak next]  
        ...

        Here is the transcript text:  
        {transcribed_text}

    """

    response = llm_client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content.strip()


def create_podcast_dialogue(transcribed_text, llm_client, model_name):

    system_prompt = """
        You are a podcast scriptwriter skilled in converting corporate meeting transcripts into
        engaging, two-person podcast conversations. Your tone is friendly, intelligent, and conversational,
        designed for a general audience interested in technology, leadership, and innovation.
        """

    user_prompt = f"""
    Transcript:

        {transcribed_text}

        You are converting this transcript into a podcast script featuring two hosts: **Jerry** and **Christina**.
        Convert the transcript into a lively, engaging dialogue that flows naturally between the two hosts.

        ### 🎙️ Host Personas
        - **Jerry**: Gender: male: is the main host who leads the conversation, asks questions, and introduces topics.s
        - **Christina**: Gender: female: is the co-host who adds depth by providing insights, commentary, and relatable anecdotes.

        - The tone should be friendly, engaging, and easy to follow—like a natural back-and-forth conversation.

        ### 🧠 Podcast Script Rules
        - Alternate between **Jerry** and **Christina** in a realistic and logical manner.
        - Include relevant insights, facts, and engaging discussion points from the transcript.
        - Use **only dialogue**, no narration, no stage directions, and no unnecessary filler.
        - Avoid any content that breaks immersion (e.g., "As per the transcript..." or system instructions).
        - Mention each other's names naturally in the conversation if appropriate.

        ### 📌 Output Format (Strictly Follow)
        ```
        ## Podcast Title

        *A concise, catchy title summarizing the main theme of the transcript.*

        ## Podcast Script

        Jerry: [First line of engaging dialogue]
        Christina: [Reply with insightful or curious tone]
        Jerry: [Continue the flow]
        Christina: [Add more depth or ask questions]
        ...continue alternating until transcript content is fully covered.

        ```

        Generate a well-structured podcast script following the format above.
    """

    response = llm_client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content.strip()


def transform_transcript_to_mind_map(transcribed_text, llm_client, model_name):
    # System prompt to instruct the LLM to organize the transcript into a hierarchical mind map
    system_prompt = """
    You are a highly skilled assistant who specializes in transforming long, unstructured text (such as meeting transcriptions) 
    into a well-organized mind map structure. Your task is to extract the main topics and subtopics, organize them hierarchically, 
    and return the result in JSON format. The output should reflect the main themes, subpoints, and their relationships.
    """

    # User prompt that includes the transcript text and specific instructions
    user_prompt = """
            Given the following transcript, generate a hierarchical mind map in JSON format.

        The map should include:
        - Main topics as parent keys
        - Subtopics and related points as child nodes
        - Each topic/subtopic should be as specific and detailed as possible, while maintaining logical relationships.

        TRANSCRIPT: {transcribed_text}

        > **🧠 Prompt: Generate Hierarchical Mind Map from Transcript**
        >
        > Given the following transcript, generate a **mind map** as a valid **JSON object**.
        >
        > ### ✅ Requirements:
        >
        > 1. **Extract the central theme** or **main topic** of the transcript and use it as the value for the `"Root Topic"` key.
        >
        > 2. Create **logical, high-level topics** directly under the root.
        >
        > 3. Under each topic:
        >
        >    * Identify **subtopics** as nested keys.
        >    * Each subtopic should have an **array of detailed, logically related points**.
        >
        > 4. Your output **must strictly follow this structure**:
        >
        > ```json
        > {
        >   "Root Topic": "Main subject derived from transcript",
        >   "Topic 1": {
        >     "Subtopic 1": ["Point 1", "Point 2"],
        >     "Subtopic 2": ["Point 1"]
        >   },
        >   "Topic 2": {
        >     "Subtopic 1": ["Point 1", "Point 2"],
        >     "Subtopic 2": ["Point 1"]
        >   }
        > }
        > ```
        >
        > ### ⚠️ Rules:
        >
        > * Do **not** use placeholder labels like `"Topic 1"` or `"Subtopic 1"` in the actual output — instead, use the **real names/content** from the transcript.
        > * Ensure the hierarchy flows from **general → specific**.
        > * Avoid redundancy and keep points **concise yet informative**.
        > * Output **only valid JSON** with proper quotation and formatting.

        """
    user_prompt = user_prompt.replace("{transcribed_text}", transcribed_text)

    # Requesting LLM to generate the mind map in JSON format
    response = llm_client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    # Parsing and returning the mind map output
    mind_map = response.choices[0].message.content.strip()

    # Optionally convert the result into a dictionary (JSON)
    mind_map_json = extract_json_from_text(mind_map)

    return mind_map_json
