
def generate_meeting_minutes(transcribed_text, llm_client, model_name, meeting_datetime=None):
    system_prompt = "You are an expert assistant responsible for drafting professional and concise meeting minutes."
    user_prompt = f"""
        TRANSCRIPT:
        {transcribed_text}

        Date & Time of Meeting: {meeting_datetime}

        Your task is to analyze the above meeting transcript and extract structured insights using careful reasoning. You must **infer names, products, decisions, and other contextual clues logically**, even when they are not explicitly stated.

        ### Primary Goals:
        1. **Accurate Participant Identification**: Extract the correct names of all participants. Use chain-of-thought reasoning to resolve ambiguous names or references (e.g., "he", "she", "they", "PM", etc.).
        2. **Product Name Detection**: Identify all product or project names mentioned, including synonyms, abbreviations, or indirect references.
        3. **Reasoned Inference**: Use contextual understanding to infer key decisions, next steps, roles, and responsibilities—even if they’re not directly labeled.

        ---

        ### Output Structure:

        Format the response using clear headings, bullet points, and formal, concise language. Follow this exact structure and include **all sections** below:

        ---

        ## 📝 Meeting Title
        - Provide a concise and relevant title that captures the primary purpose or theme of the meeting.

        ## 🗓️ Date and Time
        - Include the exact date and time the meeting occurred.

        ## 📌 Agenda Topics Discussed
        - Summarize the **main topics** in bullet points.
        - Break them down logically (e.g., “Feature X Demo”, “Deployment Issues”, “Client Feedback”).

        ## ✅ Key Decisions Made
        - List decisions, conclusions, or agreed-upon outcomes.
        - Use bullets and keep each decision short and unambiguous.

        ## 📋 Action Items
        - Clearly outline tasks assigned during the meeting.
        - For each item: include assignee, description of task, and any mentioned or implied deadline.

        ## 📦 Products, Projects, or Tools Mentioned
        - List all products, internal tools, platforms, or external services mentioned.
        - Provide full names and abbreviations (if applicable).

        ## 📣 Important Quotes or Highlights
        - Include up to 3 powerful quotes or noteworthy statements with speaker attribution.

        ## 🧠 Reasoning Behind Key Decisions (Chain of Thought)
        - For **each key decision**, explain the thought process or discussion that led to it.
        - This helps readers understand why choices were made.

        ## 📊 Risks, Concerns, or Blockers Raised
        - Note any issues flagged by the team, even if unresolved.
        - Include potential impacts or follow-up needs.

        ## Future Considerations
        - Mention any topics or decisions that require future discussion or follow-up.
        - Include any deadlines or timelines mentioned.
        
        ## Feedback or Suggestions
        - Summarize any feedback or suggestions made by participants.
        - Include any action items related to feedback.
        
        ## Funny Moments or Anecdotes
        - Include any light-hearted moments or anecdotes shared during the meeting.
        - This can help humanize the meeting minutes and make them more relatable.

        ## 🎯 Meeting Summary
        - In 3–5 sentences, summarize the entire meeting: purpose, discussion focus, key outcomes, and next steps.

        ---

        ### Formatting Guidelines:
        - Use markdown-style formatting with headings and bullet points.
        - Keep language formal, objective, and concise.
        - Do not repeat content or include filler language.
        - Ensure the summary is informative enough for someone who didn’t attend the meeting to understand the full context.

        Your final response should be structured, detailed, and use intelligent reasoning to fill in gaps or resolve ambiguities.
    """

    response = llm_client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()
