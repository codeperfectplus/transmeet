
def generate_meeting_minutes(transcribed_text, llm_client, model_name, meeting_datetime=None):
    system_prompt = "You are an expert assistant responsible for drafting professional and concise meeting minutes."
    user_prompt = f"""
        TRANSCRIPT:
        {transcribed_text}

        Date & Time of Meeting: {meeting_datetime}

        Your task is to extract and organize the following information clearly and accurately:

        1. **Meeting Title** – Provide a suitable title that reflects the overall theme or purpose of the meeting.
        2. **Date and Time** – Include the exact date and time of the meeting.
        3. **Participants** – List all participants and identify speakers by name if possible.
        4. **Agenda Topics Discussed** – Summarize the main discussion points or topics covered.
        5. **Key Decisions Made** – Highlight important decisions, agreements, or outcomes reached during the meeting.
        6. **Action Items** – List action items clearly
        7. **Important Quotes or Highlights** – Include any standout comments or quotes that are relevant or insightful.
        8. **Meeting Summary** – End with a brief summary paragraph covering the essence of the meeting.

        **Formatting Requirements**:
        - Use bullet points and headings for readability.
        - Keep the language formal and objective.
        - Avoid repetition and filler phrases.
        - Ensure the minutes are easy to read for someone who did not attend the meeting.

        Start your output with the **Meeting Title**, followed by each section listed above in the given order.
    """
    response = llm_client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()
