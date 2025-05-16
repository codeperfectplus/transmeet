from datetime import datetime

from transmeet.utils.json_parser import extract_json_from_text


def generate_meeting_minutes(
    transcribed_text, llm_client, model_name, meeting_datetime=None
):
    system_prompt = "You are an expert assistant responsible for drafting professional and concise meeting minutes."

    user_prompt = f"""
    TRANSCRIPT:

        {transcribed_text}

        Date & Time of Meeting: {meeting_datetime}

        Your task is to analyze the above meeting transcript and extract structured, visually rich insights using careful reasoning. You must **infer names, products, decisions, and other contextual clues logically**, even when they are not explicitly stated.

        ---

        ## 🧠 Primary Goals:
        1. **Accurate Participant Identification**  
        - Extract all participants mentioned or inferred.
        - Use chain-of-thought reasoning to resolve references like "he", "PM", "the intern", etc.

        1. **Product & Project Identification**  
        - Detect product names, abbreviations, internal tools, or code names.
        - Include inferred or indirectly mentioned tools/platforms.

        1. **Smart Inference & Contextual Understanding**  
        - Extract structured insights like roles, decisions, blockers, and tasks, even when they are implicit.

        ---

        ## 📘 Output Format

        Use rich markdown with **Tailwind-friendly structure**: proper heading hierarchy, `tables`, `lists`, `inline code`, `blockquotes`, and **clear roles and assignments**.

        Follow **this exact structure** and formatting guidance:

        ---

        ## 📝 Meeting Title
        - *A concise, meaningful title capturing the central focus of the meeting.*

        ## 🗓️ Date and Time
        - **{meeting_datetime}**

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

        ## 😂 Funny Moments or Anecdotes

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
    TRANSCRIPT TEXT: {transcribed_text}
    Please segment the following conversation by speaker, identifying the shifts in speaker and labeling each section accordingly.
    Ensure you handle multiple speakers and clearly mark the transitions.
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

        You are converting this transcript into a podcast script featuring two hosts: **Alex** and **Jamie**.

        ### 🎙️ Host Personas
        - **Alex** is the main host who leads the conversation, asks questions, and introduces topics.
        - **Jamie** is the co-host who adds depth by providing insights, commentary, and relatable anecdotes.
        - The tone should be friendly, engaging, and easy to follow—like a natural back-and-forth conversation.

        ### 🧠 Podcast Script Rules
        - Alternate between **Alex** and **Jamie** in a realistic and logical manner.
        - Include relevant insights, facts, and engaging discussion points from the transcript.
        - Use **only dialogue**, no narration, no stage directions, and no unnecessary filler.
        - Avoid any content that breaks immersion (e.g., "As per the transcript..." or system instructions).

        ### 📌 Output Format (Strictly Follow)
        ```

        ## Podcast Title

        *A concise, catchy title summarizing the main theme of the transcript.*

        ## Podcast Script

        Alex: [First line of engaging dialogue]
        Jamie: [Reply with insightful or curious tone]
        Alex: [Continue the flow]
        Jamie: [Add more depth or ask questions]
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

        The output should be structured in JSON like:

        {   
            "Root Topic": root_topic,
            "Topic 1": {
                "Subtopic 1": ["Point 1", "Point 2"],
                "Subtopic 2": ["Point 1"]
            },
            "Topic 2": {
                "Subtopic 1": ["Point 1", "Point 2"],
                "Subtopic 2": ["Point 1"]
            }
            ... so on
        }
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

    print(mind_map)

    # Optionally convert the result into a dictionary (JSON)
    mind_map_json = extract_json_from_text(mind_map)

    return mind_map_json
