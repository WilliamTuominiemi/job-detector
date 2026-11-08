from google import genai

def collect_to_list_with_ai(all_jobs_list):
    if len(all_jobs_list) > 0:    
        all_jobs = ''.join(all_jobs_list)

        client = genai.Client()
        prompt = f"""Create a bullet point list of these job openings. 
            It should be a single line per job.
            A line should contain job title, company and location (in that order). 
            These parameters should be separated with the character |.
            If you can't find a parameter, fill the spot with character -.
            It shouldn't have any markdown formatting. 
            Jobs: {all_jobs}"""
        interaction = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=prompt
        )

        return interaction.output_text

    return ""
