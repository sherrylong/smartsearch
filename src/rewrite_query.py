from openai import OpenAI
client = OpenAI()

def rewrite_query(query):

  prompt = """
  You are a recommendation agent for a database of scholarships, grants, and funds. You are finding a grant that matches your client's needs. 
  Identify any components that may be relevant to a grant search, such as field/topic, purpose/goal or eligibility (sponsors, grant size, etc.).
  Provide as a list of keywords separated by spaces. Limit to 10 keywords and avoid repetition.

  Example:
  Query: Find doctoral grants for research on renewable jet fuel
  Output: renewable fuel clean energy sustainability environment transportation aviation science research doctoral graduate

  Your client has the following query: """

  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "user", "content": prompt + query}
    ]
  )

  print(completion.choices[0].message.content)
  return completion.choices[0].message.content

# print(rewrite_query("Are there specific scholarships for students from low-income families studying engineering?"))