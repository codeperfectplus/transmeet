
def generate_meeting_minutes(transcribed_text, llm_client, model_name, meeting_datetime=None):
    system_prompt = "You are an expert assistant responsible for drafting professional and concise meeting minutes."
    user_prompt = f"""
        TRANSCRIPT:
        {transcribed_text}

        Date & Time of Meeting: {meeting_datetime}

        Your task is to extract, organize, and format the following information clearly and concisely:

        1. **Meeting Title** – Provide a title that accurately reflects the main theme or purpose of the meeting.
        2. **Date and Time** – Include the exact date and time when the meeting took place.
        3. **Participants** – List all attendees, specifying speakers by name when mentioned.
        4. **Agenda Topics Discussed** – Summarize the key topics or items discussed during the meeting, ensuring each point is clearly outlined.
        5. **Key Decisions Made** – Identify any decisions, agreements, or conclusions that were reached.
        6. **Action Items** – Clearly outline the action items assigned during the meeting, including who is responsible and any deadlines.
        7. **Important Quotes or Highlights** – Include any noteworthy or impactful statements made during the meeting that are important for understanding the context or outcomes.
        8. **Meeting Summary** – Provide a brief summary of the meeting, highlighting the overall discussion and outcomes in a few sentences.

        **Formatting Guidelines**:
        - Use bullet points and headings to structure the content for easy readability.
        - Maintain a formal and objective tone throughout the minutes.
        - Avoid unnecessary repetition or filler phrases.
        - Ensure that the minutes are succinct and informative, offering clarity to anyone reading who wasn't present in the meeting.

        **Structure**:
        Start by listing the **Meeting Title** followed by the sections below in the given order. Each section should be clearly labeled and easy to locate.

        **Sections**:
        - Meeting Title
        - Date and Time
        - Participants
        - Agenda Topics Discussed
        - Key Decisions Made
        - Action Items
        - Important Quotes or Highlights
        - Meeting Summary

        Ensure that each section is concise yet comprehensive, capturing the essence of the meeting.
    """

    response = llm_client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()
